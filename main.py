#Pydroid run kivy

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.clipboard import Clipboard


# ============================================================
#                    VITcore TERMINAL
# ============================================================

PASSWORD = "lethus"


# ============================================================
#                    MORSE CODE
# ============================================================

MORSE = {
    "A": ".-",    "B": "-...",  "C": "-.-.",  "D": "-..",
    "E": ".",     "F": "..-.",  "G": "--.",   "H": "....",
    "I": "..",    "J": ".---",  "K": "-.-",   "L": ".-..",
    "M": "--",    "N": "-.",    "O": "---",   "P": ".--.",
    "Q": "--.-",  "R": ".-.",   "S": "...",   "T": "-",
    "U": "..-",   "V": "...-",  "W": ".--",   "X": "-..-",
    "Y": "-.--",  "Z": "--..",

    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----."
}


REVERSE_MORSE = {
    value: key for key, value in MORSE.items()
}


# ============================================================
#                    MORSE -> TCORE
# ============================================================

def morse_letter_to_tcore(letter):

    if not letter:
        return ""

    result = ""
    current_symbol = letter[0]
    count = 0

    for symbol in letter:

        if symbol == current_symbol:
            count += 1

        else:
            result += str(count) + current_symbol + '"'
            current_symbol = symbol
            count = 1

    result += str(count) + current_symbol

    return result


def morse_to_tcore(morse):

    words = morse.split("    ")

    result = []

    for word in words:

        letters = word.split()
        tcore_word = []

        for letter in letters:
            tcore_word.append(
                morse_letter_to_tcore(letter)
            )

        result.append(" ".join(tcore_word))

    return "#".join(result)


# ============================================================
#                    TCORE -> MORSE
# ============================================================

def tcore_letter_to_morse(tcore):

    result = ""
    number = ""

    for character in tcore:

        if character.isdigit():
            number += character

        elif character in ".-":

            if number:
                result += character * int(number)
                number = ""

        elif character == '"':
            pass

    return result


def tcore_to_morse(tcore):

    words = tcore.split("#")

    result = []

    for word in words:

        letters = word.split()
        morse_word = []

        for letter in letters:
            morse_word.append(
                tcore_letter_to_morse(letter)
            )

        result.append(" ".join(morse_word))

    return "    ".join(result)


# ============================================================
#                    ENGLISH -> MORSE
# ============================================================

def english_to_morse(text):

    words = text.upper().split()
    result = []

    for word in words:

        letters = []

        for character in word:

            if character in MORSE:
                letters.append(MORSE[character])

        result.append(" ".join(letters))

    return "    ".join(result)


# ============================================================
#                    MORSE -> ENGLISH
# ============================================================

def morse_to_english(morse):

    words = morse.split("    ")
    result = []

    for word in words:

        letters = word.split()
        english_word = ""

        for letter in letters:

            if letter in REVERSE_MORSE:
                english_word += REVERSE_MORSE[letter]

        result.append(english_word)

    return " ".join(result).lower()


# ============================================================
#                    VITcore APP
# ============================================================

class VITcore(App):

    def build(self):

        self.show_login()

        return self.root


# ============================================================
#                    LOGIN
# ============================================================

    def show_login(self):

        self.root = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=20
        )

        self.root.add_widget(
            Label(
                text="VITcore TERMINAL",
                font_size=30
            )
        )

        self.root.add_widget(
            Label(
                text="[ PRIVATE TRANSLATION SYSTEM ]",
                font_size=16
            )
        )

        self.password = TextInput(
            hint_text="ACCESS PASSWORD",
            password=True,
            multiline=False,
            size_hint_y=None,
            height=50
        )

        button = Button(
            text="AUTHENTICATE",
            size_hint_y=None,
            height=55
        )

        self.status = Label(
            text="",
            font_size=18
        )

        button.bind(
            on_press=self.login
        )

        self.root.add_widget(self.password)
        self.root.add_widget(button)
        self.root.add_widget(self.status)


    def login(self, instance):

        if self.password.text == PASSWORD:

            self.show_menu()

        else:

            self.status.text = "[ ACCESS DENIED ]"


# ============================================================
#                    MAIN MENU
# ============================================================

    def show_menu(self):

        self.root.clear_widgets()

        self.root.add_widget(
            Label(
                text="VITcore TERMINAL",
                font_size=30,
                size_hint_y=None,
                height=70
            )
        )

        choices = [
            ("[1] ENGLISH  -> MORSE", self.english_morse),
            ("[2] MORSE    -> TCORE", self.morse_tcore),
            ("[3] TCORE    -> ENGLISH", self.tcore_english),
            ("[4] TCORE    -> MORSE", self.tcore_morse),
            ("[5] MORSE    -> ENGLISH", self.morse_english),
            ("[6] WHAT'S VITCORE?", self.whats_vitcore)
        ]

        for text, function in choices:

            button = Button(
                text=text,
                size_hint_y=None,
                height=55
            )

            button.bind(
                on_press=function
            )

            self.root.add_widget(button)

        terminate = Button(
            text="[0] TERMINATE SESSION",
            size_hint_y=None,
            height=55
        )

        terminate.bind(
            on_press=self.terminate
        )

        self.root.add_widget(terminate)


# ============================================================
#                    1. ENGLISH -> MORSE
# ============================================================

    def english_morse(self, instance):

        self.root.clear_widgets()

        self.root.add_widget(
            Label(
                text="ENGLISH -> MORSE",
                font_size=28
            )
        )

        self.input_box = TextInput(
            hint_text="ENTER ENGLISH",
            multiline=True
        )

        self.root.add_widget(self.input_box)

        translate = Button(
            text="TRANSLATE",
            size_hint_y=None,
            height=55
        )

        translate.bind(
            on_press=self.translate_english
        )

        self.root.add_widget(translate)

        back = Button(
            text="[7] RETURN TO MAIN TERMINAL",
            size_hint_y=None,
            height=55
        )

        back.bind(
            on_press=lambda x: self.show_menu()
        )

        self.root.add_widget(back)


    def translate_english(self, instance):

        result = english_to_morse(
            self.input_box.text
        )

        self.show_result(
            "MORSE:",
            result,
            "COPY MORSE"
        )


# ============================================================
#                    2. MORSE -> TCORE
# ============================================================

    def morse_tcore(self, instance):

        self.root.clear_widgets()

        self.root.add_widget(
            Label(
                text="MORSE -> TCORE",
                font_size=28
            )
        )

        self.input_box = TextInput(
            hint_text="ENTER MORSE",
            multiline=True
        )

        self.root.add_widget(self.input_box)

        translate = Button(
            text="TRANSLATE",
            size_hint_y=None,
            height=55
        )

        translate.bind(
            on_press=self.translate_morse_tcore
        )

        self.root.add_widget(translate)

        back = Button(
            text="[7] RETURN TO MAIN TERMINAL",
            size_hint_y=None,
            height=55
        )

        back.bind(
            on_press=lambda x: self.show_menu()
        )

        self.root.add_widget(back)


    def translate_morse_tcore(self, instance):

        result = morse_to_tcore(
            self.input_box.text
        )

        self.show_result(
            "TCORE:",
            result,
            "COPY TCORE"
        )


# ============================================================
#                    3. TCORE -> ENGLISH
# ============================================================

    def tcore_english(self, instance):

        self.root.clear_widgets()

        self.root.add_widget(
            Label(
                text="TCORE -> ENGLISH",
                font_size=28
            )
        )

        self.input_box = TextInput(
            hint_text="ENTER TCORE",
            multiline=True
        )

        self.root.add_widget(self.input_box)

        translate = Button(
            text="TRANSLATE",
            size_hint_y=None,
            height=55
        )

        translate.bind(
            on_press=self.translate_tcore_english
        )

        self.root.add_widget(translate)

        back = Button(
            text="[7] RETURN TO MAIN TERMINAL",
            size_hint_y=None,
            height=55
        )

        back.bind(
            on_press=lambda x: self.show_menu()
        )

        self.root.add_widget(back)


    def translate_tcore_english(self, instance):

        morse = tcore_to_morse(
            self.input_box.text
        )

        result = morse_to_english(morse)

        self.show_result(
            "ENGLISH:",
            result,
            "COPY ENGLISH"
        )


# ============================================================
#                    4. TCORE -> MORSE
# ============================================================

    def tcore_morse(self, instance):

        self.root.clear_widgets()

        self.root.add_widget(
            Label(
                text="TCORE -> MORSE",
                font_size=28
            )
        )

        self.input_box = TextInput(
            hint_text="ENTER TCORE",
            multiline=True
        )

        self.root.add_widget(self.input_box)

        translate = Button(
            text="TRANSLATE",
            size_hint_y=None,
            height=55
        )

        translate.bind(
            on_press=self.translate_tcore_morse
        )

        self.root.add_widget(translate)

        back = Button(
            text="[7] RETURN TO MAIN TERMINAL",
            size_hint_y=None,
            height=55
        )

        back.bind(
            on_press=lambda x: self.show_menu()
        )

        self.root.add_widget(back)


    def translate_tcore_morse(self, instance):

        result = tcore_to_morse(
            self.input_box.text
        )

        self.show_result(
            "MORSE:",
            result,
            "COPY MORSE"
        )


# ============================================================
#                    5. MORSE -> ENGLISH
# ============================================================

    def morse_english(self, instance):

        self.root.clear_widgets()

        self.root.add_widget(
            Label(
                text="MORSE -> ENGLISH",
                font_size=28
            )
        )

        self.input_box = TextInput(
            hint_text="ENTER MORSE",
            multiline=True
        )

        self.root.add_widget(self.input_box)

        translate = Button(
            text="TRANSLATE",
            size_hint_y=None,
            height=55
        )

        translate.bind(
            on_press=self.translate_morse_english
        )

        self.root.add_widget(translate)

        back = Button(
            text="[7] RETURN TO MAIN TERMINAL",
            size_hint_y=None,
            height=55
        )

        back.bind(
            on_press=lambda x: self.show_menu()
        )

        self.root.add_widget(back)


    def translate_morse_english(self, instance):

        result = morse_to_english(
            self.input_box.text
        )

        self.show_result(
            "ENGLISH:",
            result,
            "COPY ENGLISH"
        )


# ============================================================
#                    RESULT SCREEN
# ============================================================

    def show_result(self, title, result, copy_text):

        self.root.clear_widgets()

        self.root.add_widget(
            Label(
                text=title,
                font_size=25,
                size_hint_y=None,
                height=60
            )
        )

        self.root.add_widget(
            Label(
                text=result,
                font_size=20
            )
        )

        copy_button = Button(
            text=copy_text,
            size_hint_y=None,
            height=55
        )

        def copy_result(instance):

            Clipboard.copy(result)

            copy_button.text = "✓ COPIED"

        copy_button.bind(
            on_press=copy_result
        )

        self.root.add_widget(copy_button)

        back = Button(
            text="[7] RETURN TO MAIN TERMINAL",
            size_hint_y=None,
            height=55
        )

        back.bind(
            on_press=lambda x: self.show_menu()
        )

        self.root.add_widget(back)


# ============================================================
#                    6. WHAT'S VITCORE?
# ============================================================

    def whats_vitcore(self, instance):

        self.root.clear_widgets()

        text = """WHAT'S VITcore?

VITcore is a private translator terminal.

It can translate between multiple systems:

[1] English -> Morse code
[2] Morse code -> Tcore
[3] Tcore -> English
[4] Tcore -> Morse code
[5] Morse code -> English

------------------------------------------------------------

WHAT IS TCORE?

Tcore is a custom language based on Morse code.

A number tells Tcore how many times
a symbol repeats.

Examples:

3. = ...
2- = --

The " symbol means the Morse symbol
changes while remaining inside the same letter.

A normal space separates Morse letters.
# separates words.

Tcore is therefore a logical layer
built on Morse code.
"""

        self.root.add_widget(
            Label(
                text=text,
                font_size=15
            )
        )

        back = Button(
            text="[7] RETURN TO MAIN TERMINAL",
            size_hint_y=None,
            height=55
        )

        back.bind(
            on_press=lambda x: self.show_menu()
        )

        self.root.add_widget(back)


# ============================================================
#                    TERMINATE
# ============================================================

    def terminate(self, instance):

        self.root.clear_widgets()

        self.root.add_widget(
            Label(
                text="TERMINATING SECURE SESSION...\n\nCONNECTION CLOSED.",
                font_size=20
            )
        )


# ============================================================
#                    START VITcore
# ============================================================

VITcore().run()
