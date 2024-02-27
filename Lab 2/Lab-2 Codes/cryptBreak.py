from BitVector import *

BLOCKSIZE = 16
numbytes = BLOCKSIZE // 8


# Decrypt using key, passphrase
def decrypt_with_key(encrypted_bv, key_bv, bv_iv):
    msg_decrypted_bv = BitVector(size=0)
    previous_decrypted_block = bv_iv

    for i in range(0, len(encrypted_bv) // BLOCKSIZE):
        # Extract a block of size BLOCKSIZE from the encrypted bit vector
        bv = encrypted_bv[i * BLOCKSIZE:(i + 1) * BLOCKSIZE]

        # Make a deep copy of the current block
        temp = bv.deep_copy()

        # XOR the current block with the previous decrypted block
        bv ^= previous_decrypted_block

        # Update the previous_decrypted_block with the original block (before XORing with the key)
        previous_decrypted_block = temp

        # XOR the current block with the key block
        bv ^= key_bv

        # Append the decrypted block to the decrypted message bit vector
        msg_decrypted_bv += bv

    return msg_decrypted_bv.get_text_from_bitvector()

def main():
    # Read the passphrase from the user or file, wherever it's coming from in your code
    PassPhrase = "Hopes and dreams of a million years"

    # Reduce the passphrase to a bit array of size BLOCKSIZE
    bv_iv = BitVector(bitlist=[0] * BLOCKSIZE)
    for i in range(0, len(PassPhrase) // numbytes):
        textstr = PassPhrase[i * numbytes:(i + 1) * numbytes]
        bv_iv ^= BitVector(textstring=textstr)

    # converting the given hex string to bitvector
    encrypted_bv = BitVector(hexstring="3c2b223a71277173636930742f6c296b33702e2a7d127b086b146c09721821083d092c112645265e7b202574126f147c0b690b3d392d2b342b40")
    # print(encrypted_bv)

    # Iterate through all possible keys and try decryption
    for i in range(2 ** 16):
        # Convert the integer i to a binary string with BLOCKSIZE bits
        binary_key = "{0:b}".format(i).zfill(BLOCKSIZE)
        
        # BitVector from the binary key
        key_bv = BitVector(bitstring=binary_key)

        # Decrypt with the current key
        decrypted_text = decrypt_with_key(encrypted_bv, key_bv, bv_iv)

        # print(decrypted_text)
        if "Douglas Adams" in decrypted_text:
            print("Decryption successful with key:", binary_key)
            print("Decrypted text:", decrypted_text)
            with open('recovered_plaintext.txt', 'w') as file:
                file.write(decrypted_text)

            with open('recovered_key.txt', 'w') as file:
                file.write(binary_key)
            break
    else:
        print("Key not found.")

if __name__ == "__main__":
    main()