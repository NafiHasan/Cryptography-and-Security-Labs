from BitVector import BitVector


def get_dictionary_words(length):
    # path to the dictionary file
    dictionary_file = "/usr/share/dict/words" 

    # List to store the words
    words = []

    # Store the words in the list from dictionary file
    with open(dictionary_file, "r") as file:
        for line in file:
            # Remove leading/trailing whitespace
            word = line.strip()
            
            # Only store the words of length 8
            if len(word) == length:
                # add the word to the list
                words.append(word)
    
    return words


def main():
    # Get the words of length 8 from dictionary
    dict_words = get_dictionary_words(8)

    # Get the hex strings and convert to bit vector
    cipher1 = "e9 3a e9 c5 fc 73 55 d5".replace(" ", "")
    cipher1_bv = BitVector(hexstring = cipher1)

    cipher2 = "f4 3a fe c7 e1 68 4a df".replace(" ", "")

    cipher2_bv = BitVector(hexstring = cipher2)

    # print(len(cipher1_bv))

    cipher1_xor_cipher2 = cipher1_bv ^ cipher2_bv

    words_bv = []

    # print(len(cipher1_xor_cipher2))
    cur = 1
    for word in dict_words:
        words_bv.append(BitVector(textstring = word))
        # if len(BitVector(textstring = word)) != 64:
        #     print("what")

    # print('no')
        
    words_bv_hex_strings = {word1_xor_cipher1_xor_cipher2.getHexStringFromBitVector() for word1_xor_cipher1_xor_cipher2 in words_bv}

    for word1 in dict_words:
        cur += 1
        word1_bv = BitVector(textstring = word1)
        word1_xor_cipher1_xor_cipher2 = cipher1_xor_cipher2 ^ word1_bv
        # print(cur)
        if word1_xor_cipher1_xor_cipher2.getHexStringFromBitVector() in words_bv_hex_strings:
            print("yes", word1, (word1_bv ^ cipher1_xor_cipher2).get_bitvector_in_ascii())
            break
        # word2 = word1_xor_cipher1_xor_cipher2.get_bitvector_in_ascii()

        # print("no - ", word1, word2)
        # for word2 in dict_words:
        #     word2_bv = BitVector(textstring = word2)
        #     print(word1_xor_cipher1_xor_cipher2 , word2_bv)
        #     if word1_xor_cipher1_xor_cipher2 == word2_bv:
        #         print("Yes ", word1, word2)
        #         found = True
        #         break

    print("done")

if __name__ == "__main__":
    main()