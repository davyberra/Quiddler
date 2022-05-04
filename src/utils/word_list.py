"""
Gets the word list from scrabble_word_list.txt.
"""


def get_word_list():

    with open('D:/Python Games/Quiddler_Arcade/src/utils/scrabble_word_list.txt') as word_file:
        word_list = []
        for line in word_file:
            new_line = line.rstrip()
            word_list.append(new_line)

    return word_list
