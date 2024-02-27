def get_dictionary_words(length):
    # path to the dictionary file
    dictionary_file = "/usr/share/dict/words" 

    # Set to store the words
    words = set()

    # Store the words in the set from the dictionary file
    with open(dictionary_file, "r") as file:
        for line in file:
            # Remove leading/trailing whitespace
            word = line.strip()
            
            # Only store the words of length less than or equal to the specified length
            if len(word) <= length:
                # add the word to the set
                words.add(word.lower())

        # Additional words related to this assignment
        words.add("mit")
        words.add("cryptography")
        words.add("cryptographic")
        words.add("Public-key")
        words.add("nist")
    
    return words

#Global Variables

dictionary = get_dictionary_words(10)
final_key = ''

possible_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ,?!-()."
valid_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ,?!-().")

# Holds the 10 ciphertexts
ciphertexts = []


# Read ciphertexts from the file and store them in a list
def read_ciphers():
    with open('Ciphertext_Assignment_3.txt', 'r') as file:
        for line in file:
            ciphertext = list(map(int, line.strip()[1:-1].split(', ')))
            global ciphertexts
            ciphertexts.append(ciphertext)


def decrypt_test(ciphertext, key, threshold):
    # print(ciphertext)
    plaintext = ''
    # print(key)
    prev_cipher_byte = chr(ciphertext[0] ^ ord(key[0]))
    plaintext += prev_cipher_byte
    # print(plaintext)
    for i in range(1, len(key)):
        m = ciphertext[i] ^ ((ord(key[i]) + ciphertext[i - 1]) % 256)
        plaintext += chr(m)

    # print(plaintext)
    words = plaintext.split(" ")
    mx = 0
    mcnt = 0
    for word in words:
        if(word.lower() in dictionary):
            mx += len(word)
            mcnt += 1
    
    if mx > threshold:
        global final_key
        final_key = key
        # print(mcnt)
        # print("len", len(key))
    return mx

def test_encryption():
    print(encrypt("HelloWorld", "qWeRtY1234"))


def encrypt(plaintext, key):
    ciphertext = ''
    prev_cipher_byte = 0
    
    for i in range(len(key)):
        c = ord(plaintext[i]) ^ ((ord(key[i]) + prev_cipher_byte) % 256)
        prev_cipher_byte = c
        ciphertext += chr(c)

    return ciphertext


def decrypt(ciphertext, key):
    plaintext = ''
    prev_cipher_byte = chr(ciphertext[0] ^ ord(key[0]))
    plaintext += prev_cipher_byte


    for i in range(1, len(key)):
        m = ciphertext[i] ^ ((ord(key[i]) + ciphertext[i - 1]) % 256)
        plaintext += chr(m)

    print(plaintext)
    return plaintext


mp = dict()

candidate_pads = []

# Algo:
# First check for all possible valid characters of message bytes m_i
# as c_i = m_i xor ((p_i + c_prev) % 256)
# ((p_i + c_prev) % 256) = c_i xor m_i
# Now predict the pad byte: p_i = c_i xor ((m_i - c_prev) % 256)

# Now check if the pad byte produces valid characters for all other message bytes of same index


# predict the ind-th pad byte
def predict(ind):
    tmp = []
    # print("predict", ind)
    for i in range(len(possible_chars)):
        res = ciphertexts[0][ind] ^ ord(possible_chars[i])

        # Predict pad byte
        pad = (res - ciphertexts[0][ind - 1]) % 256

        cnt = 0
        # Check if the pad byte produces valid characters for message bytes
        for j in range(1, len(ciphertexts)):
            val = (pad + ciphertexts[j][ind - 1]) % 256
            val = ciphertexts[j][ind] ^ val
            if chr(val) in valid_chars:
                cnt += 1
        
        # All other message bytes found from the pad byte are valid, so candidate pad byte found
        if cnt == 9:    
            tmp.append(pad)
            # return
    candidate_pads.append(tmp)


def guess_pad_bytes():
    # To Store possible pad bytes
    tmp = []

    # Check for all possible characters a message can have
    for i in range(len(possible_chars)):
        # Consider as pad byte
        pad = ord(possible_chars[i]) ^ ciphertexts[0][0]

        # Count the number of valid characters found when the pad byte used to encrypt
        cnt = 0
        for j in range(1, len(ciphertexts)):
            x = pad ^ ciphertexts[j][0]
            # print(x)
            if chr(x) in valid_chars:
                # print(chr(x))
                cnt += 1
        
        # All other messages are valid if this is the cadidate pad byte
        if cnt == 9:
            # print("done", chr(pad))
            tmp.append(pad)

    candidate_pads.append(tmp)


    # Predict the other pad bytes. (from 1 to 60)
    for j in range(1, 60):
        predict(j)



max_length = 0

# Recursively generate all possible keys of given length limit
# ind = starting index of key generation
# threshold = how many matches needed for the key to be considered

def recursive_key_gen(key, ind, lim, threshold):
    if ind == lim:
        global max_length

        for i in range(10):
            max_length = max(max_length, decrypt_test(ciphertexts[i], key, threshold))
        # if threshold < 40:
        #     print(threshold, max_length)
        return
    
    # Recursive call
    for i in candidate_pads[ind]:
        recursive_key_gen(key + chr(i), ind + 1, lim, threshold)


def generate_and_test_keys():
    # actual_key = "wKt3UqHiLNrOT1GeGXtNqfqWTA37c6fEtinmavOjzDBbMHpH75h6cGWaDbp1"
    recursive_key_gen('', 0, 15, 12)
    # print(final_key)
    # print("len1", len(final_key))

    global final_key

    recursive_key_gen(final_key, 15, 30, 20)

    recursive_key_gen(final_key, 30, 45, 30)
    # print(final_key)
    # print("len3", len(final_key))

    recursive_key_gen(final_key, 45, 60, 35)
    # print(final_key)
    # print("len4", len(final_key))


# Prints all possible pad bytes
def possible_pad_bytes():
    total_options = 1
    for i in candidate_pads:
        # total_options *= len(i)
        # print(len(i))
        for j in i:
            # total_options += len()
            print(chr(j), end="")
        print()

    print(total_options)

def change_char(s, ind, char):
    str_list = list(s)
    str_list[ind] = char
    return "".join(str_list)

def brute_fix(ind):
    for i in range(len(candidate_pads[ind])):
        global final_key
        better_key = final_key
        better_key = change_char(final_key, ind, chr(candidate_pads[ind][i]))
        # print(final_key, better_key)

        cnt = 0
        for j in range(10):
            cur_match = match_test(ciphertexts[j], final_key)
            again_match = match_test(ciphertexts[j], better_key)
            if again_match > cur_match:
                cnt += 1

            # print(cnt)
            if cnt >= 4 and better_key != None:
                return better_key

    return final_key

def brute_fix2(ind1, ind2):
    for i in range(len(candidate_pads[ind1])):
        for k in range(len(candidate_pads[ind2])):

            global final_key
            better_key = final_key
            better_key = change_char(final_key, ind1, chr(candidate_pads[ind1][i]))
            better_key = change_char(better_key, ind2, chr(candidate_pads[ind2][k]))
            # print(final_key, better_key)

            cnt = 0
            for j in range(10):
                cur_match = match_test(ciphertexts[j], final_key)
                again_match = match_test(ciphertexts[j], better_key)
                if again_match > cur_match:
                    cnt += 1

                # print(cnt)
                if cnt >= 3 and better_key != None:
                    return better_key

    return final_key


def brute_fix3(ind1, ind2, ind3):
    for i in range(len(candidate_pads[ind1])):
        for k in range(len(candidate_pads[ind2])):
            for l in range(len(candidate_pads[ind3])):
                global final_key
                better_key = final_key
                better_key = change_char(better_key, ind1, chr(candidate_pads[ind1][i]))
                better_key = change_char(better_key, ind2, chr(candidate_pads[ind2][k]))
                better_key = change_char(better_key, ind3, chr(candidate_pads[ind3][l]))
                # print(final_key, better_key)

                cnt = 0
                for j in range(10):
                    cur_match = match_test(ciphertexts[j], final_key)
                    again_match = match_test(ciphertexts[j], better_key)
                    if again_match > cur_match:
                        cnt += 1

                    # print(cnt)
                    if cnt >= 3 and better_key != None:
                        return better_key

    return final_key

def match_test(ciphertext, key):
    plaintext = ''
    # print(key)
    prev_cipher_byte = chr(ciphertext[0] ^ ord(key[0]))
    plaintext += prev_cipher_byte
    # print(plaintext)
    for i in range(1, len(key)):
        m = ciphertext[i] ^ ((ord(key[i]) + ciphertext[i - 1]) % 256)
        plaintext += chr(m)

    # print(plaintext)
    words = plaintext.split(" ")
    mcnt = 0
    for word in words:
        if(word.lower() in dictionary):
            mcnt += 1

    return mcnt


def main():
    # To test the encryption technique
    # test_encryption()

    # Read the ciphertexts from the text file
    read_ciphers()

    guess_pad_bytes()
    generate_and_test_keys()
    
    global final_key
    print("Lenght of final key:",len(final_key))

    
    # Apply brute force to fix some keys
    # Uncomment some brute forces if some letters don't match
    # final_key = brute_fix(15)
    # final_key = brute_fix(24)
    # final_key = brute_fix(37)
    final_key = brute_fix(43)
    final_key = brute_fix(49)
    # final_key = brute_fix2(29, 30)
    final_key = brute_fix2(23, 24)
    final_key = brute_fix2(1, 2)
    final_key = brute_fix(1)
    # final_key = brute_fix(29)
    # final_key = brute_fix3(15, 16, 17)
    final_key = brute_fix(15)

    with open ("Decrypted_Messages.txt", "w") as file:
        for i in range(10):
            print(f"{i + 1}-th message: ")
            decrypted_message = decrypt(ciphertexts[i], final_key)
            print()

            # Write in a file
            file.write(f"{i + 1}-th message: \n")
            file.write(decrypted_message + "\n\n")


    print("One time Pad:", final_key)


if __name__ == "__main__":
    main()
