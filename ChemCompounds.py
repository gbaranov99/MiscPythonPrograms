from JsonParse import JsonList
import re


class ChemCompoundsClass(JsonList):
    """
    Class that accepts natural language input of chemical compounds and returns their atomic mass
    Must follow the format AtomNumberofatoms
    H2O = 2Hs and 1 O = 18.0152 amu
    Typing "stop" will close the application
    Keeps track of atomic weight using a Json file, extracts using my JsonParse module
    """
    def __init__(self):
        location = "C:/Users/Laptop babyyy/Dropbox/Everything/Programming/PyCharm/"
        file = "Personal/HWAlgorithms/Chem/ElementMass.json"
        super().__init__(location + file)

    def find_mass(self, compound):
        # Splits string inputted by capital characters, symbols and numbers (does not split by lower case)
        split = re.sub(r'(?=[A-Z])|(?=[0-9])|(?=\()|(?=\))', r" ", compound)
        split = split.split()
        print(split)
        try:
            masses = ""
            first_letter = True
            # Loops through each character, and determines how to add it to final string (which is evaluated)
            for index, c in enumerate(split):
                if index == 0:
                    if c.isdigit():
                        if split[index + 1].isdigit():
                            masses += c
                        else:
                            masses += c + "*("
                        continue
                    else:
                        masses += "("
                if c.isdigit():
                    # While loop accounts for numbers at start of string, which are different from other numbers
                    # Different because they must have a *( following
                    # Once full starting number is complete, the while loop will break quickly
                    count = index
                    while count >= 0:
                        count -= 1
                        if not split[count].isdigit():
                            break
                        if count == 0:
                            if split[index + 1].isdigit():
                                masses += c
                            else:
                                masses += c + "*("
                    # If the first number is being processed, does not execute next if statement
                    if count == -1:
                        continue
                    # This if determines if * should be placed, if previous char is a number, it does not add *
                    # Allows for numbers greater than 1 digit
                    if not split[index - 1].isdigit():
                        masses += "*"
                    masses += c
                # Adds the next element with a + before it, if it is not preceded by a (
                elif c.isalpha() and not first_letter and split[index-1] != "(":
                    masses += "+" + self.file_dict[c]
                # Adds next element without a + before it, since it is preceded by (
                elif (c.isalpha() and first_letter) or (c.isalpha() and split[index-1] == "("):
                    masses += self.file_dict[c]
                    first_letter = False
                elif c == "(":
                    masses += "+" + c
                elif c == ")":
                    masses += c
            masses += ")"
            # Shows output
            print(masses)
            print(eval(masses))
        # Error handling for element that does not exist
        except KeyError:
            print("That is not a valid compound")


def chem_compounds_mass():
    element_list = ChemCompoundsClass()
    while True:
        user_input = input("Enter a compound to find the mass of\n")
        if user_input == "stop":
            break
        else:
            element_list.find_mass(user_input)


if __name__ == "__main__":
    chem_compounds_mass()
