import math
def kasiki(ciphertext):
    # print(ciphertext)
    counts = []
    keyIndices = []
    matches = []
    keys = []
    gcfs = []
    keyPred = 0

    # make a list of common patterns of lengths 2-6
    for i in range(2, 9, 1):
        for j in range(len(ciphertext)-i+1):
            pattern = [ciphertext[n] for n in range(j, j+i, 1)]
            keys.append(pattern)
            keyIndices.append(j)
            count = 0

            # save distance between common patterns in "matches"
            for k in range(j, len(ciphertext)-len(pattern), 1):
                if pattern == list(ciphertext[k+1:k+len(pattern)+1]):
                    count += 1
                    matches.append(1+abs(k-j))
                    counts.append(pattern)

    print(len(counts))
    # store the gcds of all pairs of values in matches
    for m in range(len(matches)):
        for n in range(len(matches)-m-1):
            factor = math.gcd(matches[m], matches[m+n+1])
            if matches[m] != matches[m+n+1] and factor != 1:
                gcfs.append(math.gcd(matches[m], matches[m+n+1]))

    # # predicted key length is mode of gcfs
    # try:
    #     keyPred = max(set(gcfs), key=gcfs.count)
    # except:
    #     keyPred = 0

    return keyPred





def find_repeat_distances(text, min_length=3):
    repeats = {}
    for length in range(min_length, len(text) // 2):
        for i in range(len(text) - length):
            substring = text[i:i+length]
            if substring in text[i+length:]:
                distance = text[i+length:].index(substring) + length
                if length not in repeats:
                    repeats[length] = []
                repeats[length].append(distance)
    return repeats

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def find_possible_key_lengths(repeat_distances):
    possible_lengths = []
    for length, distances in repeat_distances.items():
        gcd_values = [abs(distances[i] - distances[j]) for i in range(len(distances)) for j in range(i + 1, len(distances))]
        possible_lengths.extend([length] * len([1 for gcd_value in gcd_values if gcd_value > 1 and gcd_value <= length]))

    return list(set(possible_lengths))

def attack_vigenere_cipher(ciphertext, key_length):
    key = ''
    for i in range(key_length):
        sliced_text = ciphertext[i::key_length]
        most_common_char = max(set(sliced_text), key=sliced_text.count)
        key += chr((ord(most_common_char) - ord('E')) % 26 + ord('A'))  # Assuming English language

    return key







def get_key_length(ciphertext):
    # Perform Kasiski examination to estimate key length
    distances = []
    for i in range(len(ciphertext)):
        for j in range(i + 3, len(ciphertext)):
            if ciphertext[i:i+3] == ciphertext[j:j+3]:
                distances.append(j - i)
    print(len(distances))
    for i in range(0, len(distances)):
        if distances[i] == 7:
            print("got")

    # Find possible key lengths based on common factors of distances
    possible_lengths = []
    for i in range(2, min(30, max(distances)) + 1):
        if all(d % i == 0 for d in distances):
            possible_lengths.append(i)

    return possible_lengths


def vigenere_decrypt(ciphertext, key):
    plaintext = ''
    key_len = len(key)
    
    for i, char in enumerate(ciphertext):
         # Determine the shift 
        shift = ord(key[i % key_len]) - ord('a')
        
        # Decrypt the character 
        if char.isupper():
            plaintext += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
        else:
            plaintext += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
    
    return plaintext


def vigenere_decrypt_without_key(ciphertext, key_length):
    # Attempt to decrypt the ciphertext without the key
    possible_keys = []
    for length in key_length:
        key = ''
        for i in range(length):
            # Frequency analysis to guess the most likely key
            subtext = ciphertext[i::length]
            most_common = max(set(subtext), key=subtext.count)
            shift = (ord(most_common) - ord('e')) % 26  # Assuming 'e' is the most common letter in English
            key += chr((ord('a') + shift) % 26)

        possible_keys.append(key)

    return possible_keys

def main():
    # Read ciphertext from 'output.txt'
    with open('output.txt', 'r') as file:
        ciphertext = file.read()  


    # key_len = kasiki(ciphertext)
    # print("Key len", key_len)

    # Step (a): Predict the key length
    # predicted_key_lengths = get_key_length(ciphertext)
    # print("Predicted Key Lengths:", predicted_key_lengths)

    # # Step (b): Decrypt the ciphertext without the key
    # possible_keys = vigenere_decrypt_without_key(ciphertext, predicted_key_lengths)
    # for key in possible_keys:
    #     decrypted_text = vigenere_decrypt(ciphertext, key)
    #     print("\nKey:", key)
    #     print("Decrypted Text:", decrypted_text)
    print(gcd(4,6))
        
    repeat_distances = find_repeat_distances(ciphertext)
    possible_key_lengths = find_possible_key_lengths(repeat_distances)

    print("Possible key lengths:", possible_key_lengths)

    for key_length in possible_key_lengths:
        key = attack_vigenere_cipher(ciphertext, key_length)
        print(f"Key with length {key_length}: {key}")

if __name__ == "__main__":
    main()