'''
Nicole Torres
CS2302 LAB 4B
OBJECTIVE: To practice hash tables
Last Modified: 11/11/18
'''

import math

class HNode:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next

class Hashtable():
    def __init__(self, initial_size, hash_object):
        self.table = [None] * initial_size  # this is the array where the "linked lists" will be stored
        self.hash_object = hash_object  # will be used for hashing the elements
        self.size = 0  # keep track on number of elements
        self.chain_lengths = {}  # will be used to key = index, value = len(table[index]) pairs

    def insert(self, word):
        self.size += 1
        index = self.hash_object.hash(word)  # mathematically manipulate the object to provide me a unique index

        # two possibilities, either something there in the table or not,
        # but it doesn't matter, our new node will point to whatever was there before
        self.table[index] = HNode(word, self.table[index])
        if index in self.chain_lengths:
            self.chain_lengths[index] += 1
        else:
            self.chain_lengths[index] = 1

    def search(self, word):
        index = self.hash_object.hash(word)

        if self.table[index] is None:
            return False
        else:
            tmp = self.table[index]
            while tmp is not None:
                if tmp.data == word:
                    return True
                else:
                    tmp = tmp.next
            return False

    def get_load_factor(self):
        return self.size / len(self.table)

    def get_average_comparisons(self):
        sum = 0
        for key in self.chain_lengths:
            sum += self.chain_lengths[key]
        avg_chain_length = sum / len(self.chain_lengths)
        return avg_chain_length / 2  # why 2? Because on average, we will search for words towards
        # the middle of the list and not the extremes, so

class Hashfunction:
    def __init__(self, base, hashtable_size):
        self.base = base
        self.hashtable_size = hashtable_size

    def hash(self, word):
        """
        This function will take a word and
        return a unique number between 0 and hashtable_size.
        :param word: string - the word to be hashed
        :return: int - index in the range [0, hashtable_size]
        """
        shift = ord('a')  # a = 97 right now
        index = 0
        for i in range(len(word)):
            cval = ord(word[i]) - shift  # this will make is so that a = 0, b = 1, etc.
            index += cval * math.pow(self.base, i)  # treating the word as a self.base number, i.e.
            # 316 = 6*10^0 + 1*10^1 + 3*10^2 for a base 10 number
        index = abs(index)
        return int(index) % self.hashtable_size


# Lab Functions

def print_anagrams(word, prefix=""):
    if len(word) <= 1:
        str = prefix + word
        if english_words.search(str):
            print(prefix + word)

    else:
        for i in range(len(word)):
            cur = word[i: i + 1]
            before = word[: i]  # letters before cur
            after = word[i + 1:]  # letters after cur
            if cur not in before:  # Check if permutations of cur have not been generated.
                print_anagrams(before + after, prefix + cur)

def count_anagrams(word, prefix=""):
    if len(word) <= 1:
        str = prefix + word
        if english_words.search(str):
            return 1
        else:
            return 0

    else:
        count = 0
        for i in range(len(word)):
            cur = word[i: i + 1]
            before = word[0: i]  # letters before cur
            after = word[i + 1:]  # letters after cur
            if cur not in before:  # Check if permutations of cur have not been generated.
                count += count_anagrams(before + after, prefix + cur)
        return count

def anagrams_from_file(filename):
    f = open(filename)
    maxCount = 0
    maxWord = ""
    for line in f:
        count = count_anagrams(line[0:-1])  # -1 index means last one
        print(line[0:-1], count)
        if count > maxCount:
            maxCount = count
            maxWord = line[0:-1]
    print("The word with the most anagrams stored in %s was %s with %d anagrams" % (filename, maxWord, maxCount))

def buildTable(filename, init_size, hash_object):
    """
    This method will build the vocabulary using the data structure of the user's choice
    If the user does not select one, a python set is used for the vocabulary
    :param response:
    :return:
    """
    f = open(filename)
    english_words = Hashtable(init_size, hash_object)  # TODO
    for line in f:
        english_words.insert(line[:-1].lower())
    return english_words

if __name__ == '__main__':
    english_words = None
    while True:
        try:
            filename = input("Enter the name of the file to use for the vocabulary: ")
            size_resp = input("Enter the size of the table you'd like to use: ")
            base_resp = input("Enter an int you'd like to use for the base: ")

            hash_object = Hashfunction(int(base_resp), int(size_resp))
            english_words = buildTable(filename, int(size_resp), hash_object)
            if english_words is not None:
                print("Avg num comparisons:", english_words.get_average_comparisons())
                print("Load factor:", english_words.get_load_factor())
                break
        except:
            print("Invalid file!")

    while True:
        response = input("\nEnter a word to test your program or just hit <return> to read words from file:\n")
        if response == '':
            break
        else:
            print_anagrams(response.lower())
            print("Number of anagrams is ", count_anagrams(response.lower()))
    while True:
        try:
            response = input("Enter the name of the file with words: ")
            anagrams_from_file(response)
            break
        except:
            print("Invalid file!")
