from morse import MorseCodeConverter

if __name__ == "__main__":

    translator = MorseCodeConverter()

    print("Welcome to Morse Code Translator")

    while True:
        choice = input("To convert text to morse code, type 'M'\n"
                       "To convert morse code to text, type 'T'\n"
                       "To quit, type 'Q'\n"
                       "Your choice: ").lower()
        if choice == "m":
            source = input("Please enter the text you wish to convert to Morse code:\n")
            output = translator.translate_text_to_morse_code(source)
            print(f"Text: {source}\n"
                  f"Morse Code: {output}\n")
        elif choice == "t":
            source = input("Please enter the Morse code you wish to convert to text:\n")
            output = translator.translate_morse_code_to_text(source)
            print(f"Morse Code: {source}\n"
                  f"Text: {output}\n")
        elif choice == "q":
            break
