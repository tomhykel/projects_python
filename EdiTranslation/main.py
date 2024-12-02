from os import listdir
from os.path import isfile, join
import csv
import datetime as dt
import shutil
import xml.etree.ElementTree as ElementTree

DIR_IN = "./MsgIn/"
DIR_OUT = "./MsgOut/"
DIR_ARCHIVE = "./MsgArchive/"
DIR_ERROR = "./MsgError/"


def move_file(file_name, source, destination):
    """ Moves a file from the source directory to the destination directory
    :param file_name: name of the file to be moved
    :param source: path to the source directory
    :param destination: path to the destination directory
    """
    src = source + file_name
    dst = destination + file_name
    # Use exception handling
    try:
        shutil.move(src=src, dst=dst)
        print(f"File moved from {src} to {dst}")
    except FileNotFoundError:
        print(f"Error: File not found: {src}")
    # Use if else (another option)
    # if isfile(src):
    #     shutil.move(src=src, dst=dst)
    #     print(f"File successfully moved from {src} to {dst}")
    # else:
    #     print(f"Error: File not found: {src}")


def send_error_notification(attachment):
    """ Sends an e-mail in case the received message is invalid
    :param attachment: the erroneous file which will be sent as an attachment
    """
    # No e-mail configured, no e-mail sent (just demo of the e-mail notification function)
    print(f"Notification e-mail sent for message {attachment} (log only; no e-mail configured)")


def read_xml(file_name, source):
    """ Parses the received XML file and moves it to another directory after processing
    :param file_name: name of the file to be processed
    :param source: path to the source directory
    """
    required_data = []
    file = f"{source}{file_name}"

    try:
        tree = ElementTree.parse(file)
        root = tree.getroot()
    except ElementTree.ParseError:
        print(f"Error: Invalid XML message received: {file}")
        move_file(file_name=file_name, source=DIR_IN, destination=DIR_ERROR)
        send_error_notification(attachment=file)

        return required_data

    order_header = {}
    order_items = []

    # Read header
    order_header["order_id"] = root.find(".ORDER_HEADER/ORDER_INFO/ORDER_ID").text
    order_header["order_date"] = root.find(".ORDER_HEADER/ORDER_INFO/ORDER_DATE").text

    for party in root.findall("./ORDER_HEADER/ORDER_INFO/PARTIES/PARTY"):
        if party.find("PARTY_ROLE").text == "buyer":
            order_header["buyer_id"] = party.find("PARTY_ID").text
        elif party.find("PARTY_ROLE").text == "delivery":
            order_header["delivery_id"] = party.find("PARTY_ID").text

    # Read line items
    for item in root.findall("./ORDER_ITEM_LIST/ORDER_ITEM"):
        line_item = {
            "line_nr": item.find("LINE_ITEM_ID").text,
            "product_id": item.find("PRODUCT_ID/SUPPLIER_PID").text,
            "ean": item.find("PRODUCT_ID/INTERNATIONAL_PID").text,
            "quantity": item.find("QUANTITY").text,
            "unit": item.find("ORDER_UNIT").text,
            "delivery_date": item.find("REQUESTED_DELIVERY_DATE").text
        }
        order_items.append(line_item)

    required_data = [(order_header | item) for item in order_items]
    move_file(file_name=file_name, source=DIR_IN, destination=DIR_ARCHIVE)

    return required_data


def write_csv(data, destination):
    """ Creates and writes the CSV file
    :param data: source data used to create the CSV file
    :param destination: path to the destination directory
    """
    fields = ["order_id", "order_date", "buyer_id", "delivery_id",
              "line_nr", "product_id", "ean", "quantity", "unit", "delivery_date"]

    # Create CSV file name
    timestamp = dt.datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"{destination}order_{timestamp}.csv"

    # Write CSV file
    with open(file_name, mode='w', newline='') as csv_file:   # newline='' necessary in Windows (line breaks issue)
        writer = csv.DictWriter(f=csv_file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)

    print(f"CSV file saved as: {file_name}")


if __name__ == "__main__":

    # In real life operation, the task should be scheduled to run every few minutes
    # Options: UNIX/LINUX crontab or Python while True cycle + time.sleep(seconds) or schedule
    # For testing/demonstration purposes, while cycle not implemented, the code below runs only once

    # Create a list of received files
    received_files = [file for file in listdir(DIR_IN) if isfile(join(DIR_IN, file))]

    # Process received files one by one
    for file in received_files:
        print(f"Processing file {file}")

        # Read XML file
        order_data = read_xml(file_name=file, source=DIR_IN)

        # Create CSV file
        if order_data:
            write_csv(data=order_data, destination=DIR_OUT)
