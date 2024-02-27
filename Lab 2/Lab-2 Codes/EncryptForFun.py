### EncryptForFun.py
### Avi Kak (kak@purdue.edu)
### January 21, 2014, modified January 11, 2016


### Medium strength encryption/decryption for secure message exchange
### for fun.


### Based on differential XORing of bit blocks. Differential XORing
### destroys any repetitive patterns in the messages to be encrypted and
### makes it more difficult to break encryption by statistical
### analysis. Differential XORing needs an Initialization Vector that is
### derived from a pass phrase in the script shown below. The security
### level of this script can be taken to full strength by using 3DES or
### AES for encrypting the bit blocks produced by differential XORing.


# Call syntax:
#   EncryptForFun.py message_file.txt output.txt
# The encrypted output is deposited in the file ‘output.txt’

import sys
from BitVector import *

if len(sys.argv) != 3:
    sys.exit('''Needs two command-line arguments, one for'''
            '''the message file and the other for the '''
            '''encrypted output file''')
    

PassPhrase = "Hopes and dreams of a million years"
BLOCKSIZE = 64
numbytes = BLOCKSIZE // 8

# Reduce the passphrase to a bit array of size BLOCKSIZE:
bv_iv = BitVector(bitlist = [0]*BLOCKSIZE)
for i in range(0,len(PassPhrase) // numbytes):
    textstr = PassPhrase[i*numbytes:(i+1)*numbytes]
    bv_iv ^= BitVector( textstring = textstr )

# Get key from user:
key = None
if sys.version_info[0] == 3:
    key = input("\nEnter key: ")
else:
    key = raw_input("\nEnter key: ")
key = key.strip()

# Reduce the key to a bit array of size BLOCKSIZE:
key_bv = BitVector(bitlist = [0]*BLOCKSIZE)
for i in range(0,len(key) // numbytes):
    keyblock = key[i*numbytes:(i+1)*numbytes]
    key_bv ^= BitVector( textstring = keyblock )
    
print(key_bv)


# Create a bitvector for storing the ciphertext bit array:
msg_encrypted_bv = BitVector( size = 0 )

# Carry out differential XORing of bit blocks and encryption:
previous_block = bv_iv
bv = BitVector( filename = sys.argv[1] )
while (bv.more_to_read):
    bv_read = bv.read_bits_from_file(BLOCKSIZE)

    if len(bv_read) < BLOCKSIZE:
        bv_read += BitVector(size = (BLOCKSIZE - len(bv_read)))

    bv_read ^= key_bv
    bv_read ^= previous_block
    previous_block = bv_read.deep_copy()
    msg_encrypted_bv += bv_read

# Convert the encrypted bitvector into a hex string:
outputhex = msg_encrypted_bv.get_hex_string_from_bitvector()

# Write ciphertext bitvector to the output file:
FILEOUT = open(sys.argv[2], 'w')
FILEOUT.write(outputhex)
FILEOUT.close()