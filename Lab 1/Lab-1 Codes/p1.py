import re

def read_file(file_name):
    with open (file_name, 'r') as file:
        text = file.read()
    return text

def write_file(file_name, text):
    with open(file_name, 'w') as file:
        file.write(text)

def clean_text(text):
    # Remove unnecessary chars
    cleaned_text = re.sub(r'[^a-zA-Z]', '', text)
    return cleaned_text

def match_length(text, key):
    while len(key) < len(text):
        key += key

    while len(key) > len(text):
        key = key[:-1]
    
    # print(text)
    # print(key)
    return key

def vigenere_encrypt(plaintext, key):

    ciphertext = ''
    key_len = len(key)
    
    for i, char in enumerate(plaintext):
        # Determine Shift
        shift = ord(key[i % key_len]) - ord('a')
        
        # Encrypt 
        if char.isupper():
            ciphertext += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        else:
            ciphertext += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))   

    return ciphertext


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


def main():
    raw_text = read_file('input.txt')

    key = read_file('key.txt')


    plaintext = clean_text(raw_text)
    write_file('plaintext.txt', plaintext)
    # print(text)

    encrypted_text = vigenere_encrypt(plaintext, key)

    write_file('output.txt', encrypted_text)

    again = read_file('output.txt')
    
    # print(text)
    # print(encrypted_text)
    decrypted_text = vigenere_decrypt(again, key)
    write_file('decrypted_text.txt', decrypted_text)
    # print(decrypted_text)

if __name__ == "__main__":
    main()