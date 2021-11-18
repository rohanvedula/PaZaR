def is_phrase(word):
    for i, char in enumerate(word):
        if (char == ',') or (char == '.') or (char == ':'):
            if str.isalpha(word[i-1]) or str.isalpha(word[i+1]):
                return True
            else:
                return False
        # elif (char == '—'):
        #     return True

def to_latex_code(phrase_list):
    paragraph = ""
    for phrase in phrase_list:
        for word in phrase:
            if (not str.isalpha(word) and not is_phrase(word)) or ("\\" in word): #any(char.isdigit() for char in word):
                paragraph += "$" + word + "$ "
            else:
                paragraph += word + " "
    return paragraph