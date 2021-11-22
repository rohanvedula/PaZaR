from pylatex.base_classes.command import Command
from pylatex.document import Document
from pylatex.utils import NoEscape
from pylatex.math import Math
from pylatex.package import Package

# function to create a document when called, takes file name and file path
def create_document(filename: str, filepath: str)->Document:
    # create document object with filepath
    doc = Document(default_filepath=filepath)

    # append title and date
    doc.preamble.append(Command('title', filename))
    doc.preamble.append(Command('date', NoEscape(r'\today')))
    doc.append(NoEscape(r'\maketitle'))

    # append required packages
    doc.packages.append(Package('amssymb'))
    doc.packages.append(Package('amsfonts'))
    doc.packages.append(Package('amsmath'))

    # generate pdf and tex
    doc.generate_pdf()
    doc.generate_tex()

    # return created document
    return doc

# function to append string to already created document
def append_text(doc: Document, text: str) -> Document:
    # create array of strings to be appended
    strings = []

    # set previous index of last 'cut' string
    prev_ind = 0

    # set switch for in math to false
    in_math = False

    # loop through string
    for i, char in enumerate(text):
        # check for inline math character
        if char=='$':
            # if not already in math mode, append text to string array and start search for end of math
            if not in_math:
                strings.append(text[prev_ind:i])
                in_math = True
                prev_ind = i
            else:   # if already in math mode, append equation to string array and get out of math search
                math_string = NoEscape(r"{}".format(text[prev_ind+1:i]))
                strings.append(Math(data=[math_string], inline=True))
                in_math = False
                prev_ind = i+1

    # append final string
    strings.append(text[prev_ind:])

    # append all strings into one line
    for string in strings:
        doc.append(string)

    # generate pdf and tex
    doc.generate_pdf()
    doc.generate_tex()

    # return appended document
    return doc

# function to append display math: INCOMPLETE
def append_display(doc: Document, text: str) -> Document:
    
    strings = []

    prev_ind = 0
    
    in_math = False
    
    for i, char in enumerate(text):
        
        if (char == '$' and text[i + 1] == '$') or (char == '[' or char == ']'):
            # if not already in math mode, append text to string array and start search for end of math
            if not in_math:
                strings.append(text[prev_ind:i])
                in_math = True
                prev_ind = i
            else:   # if already in math mode, append equation to string array and get out of math search
                math_string = NoEscape(r"{}".format(text[prev_ind+1:i]))
                strings.append(Math(data=[math_string], inline=True))
                in_math = False
                prev_ind = i+1

    # append final string
    strings.append(text[prev_ind:])

    # append all strings into one line
    for string in strings:
        doc.append(string)

    # generate pdf and tex
    doc.generate_pdf()
    doc.generate_tex()
    
    return doc