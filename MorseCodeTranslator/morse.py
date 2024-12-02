import csv

MORSE_CODE = "./morse-code.csv"


class MorseCodeConverter:
    def __init__(self):
        self.morse_code_csv = MORSE_CODE
        self.text_to_morse = {}
        self.morse_to_text = {}
        self._prepare_dictionaries()

    def _prepare_dictionaries(self):
        """Creates dictionaries text_to_morse and morse_to_text"""
        with (open(self.morse_code_csv, mode="r") as csv_file):
            data = csv.reader(csv_file)
            for row in data:
                char, code = row
                self.text_to_morse[char] = code
                self.morse_to_text[code] = char

    def translate_text_to_morse_code(self, text):
        """Converts text to Morse code
        :param text: text to be converted, alphanumeric characters only
        :return: Morse code
        """
        output = ""
        for char in text.upper():
            try:
                if char == " ":
                    output += "/" + " "
                else:
                    output += self.text_to_morse[char] + " "
            except KeyError:
                print(f"'{char}' skipped. Only alphanumeric characters cant be translated.")
                continue
        return output.strip()

    def translate_morse_code_to_text(self, code):
        """Converts Morse code to text
        :param code: Morse code to be converted
        :return: text in upper case letters
        """
        output = ""
        morse_code = code.split()
        for char in morse_code:
            try:
                if char == "/":
                    output += " "
                else:
                    output += self.morse_to_text[char]
            except KeyError:
                print(f"'{char}' skipped.")
                continue
        return output.strip()
