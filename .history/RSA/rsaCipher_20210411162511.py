


 import sys



DEFAULT_BLOCK_SIZE = 128 # 128 bytes

BYTE_SIZE = 256 # One byte has 256 different values.



def main():



 filename = 'encrypted_file.txt' # the file to write to/read from
 mode = 'encrypt' # set to 'encrypt' or 'decrypt'



if mode == 'encrypt':

       message = '''"Journalists belong in the gutter because that is where the ruling classes throw their guilty secrets." -Gerald Priestland "The Founding Fathers gave the free press the protection it must have to bare the secrets of government and inform the people." -Hugo Black'''

        pubKeyFilename = 'al_sweigart_pubkey.txt'

       print('Encrypting and writing to %s...' % (filename))

      encryptedText = encryptAndWriteToFile(filename, pubKeyFilename, message)

 23.

 24.         print('Encrypted text:')

 25.         print(encryptedText)

 26.

 27.     elif mode == 'decrypt':

 28.         privKeyFilename = 'al_sweigart_privkey.txt'

 29.         print('Reading from %s and decrypting...' % (filename))

 30.         decryptedText = readFromFileAndDecrypt(filename, privKeyFilename)

 31.

 32.         print('Decrypted text:')

 33.         print(decryptedText)

 34.

 35.

 36. def getBlocksFromText(message, blockSize=DEFAULT_BLOCK_SIZE):

 37.     # Converts a string message to a list of block integers. Each integer

 38.     # represents 128 (or whatever blockSize is set to) string characters.

 39.

 40.     messageBytes = message.encode('ascii') # convert the string to bytes

 41.

 42.     blockInts = []

 43.     for blockStart in range(0, len(messageBytes), blockSize):

 44.         # Calculate the block integer for this block of text

 45.         blockInt = 0

 46.         for i in range(blockStart, min(blockStart + blockSize, len(messageBytes))):

 47.             blockInt += messageBytes[i] * (BYTE_SIZE ** (i % blockSize))

 48.         blockInts.append(blockInt)

 49.     return blockInts

 50.

 51.

 52. def getTextFromBlocks(blockInts, messageLength, blockSize=DEFAULT_BLOCK_SIZE):

 53.     # Converts a list of block integers to the original message string.

 54.     # The original message length is needed to properly convert the last

 55.     # block integer.

 56.     message = []

 57.     for blockInt in blockInts:

 58.         blockMessage = []

 59.         for i in range(blockSize - 1, -1, -1):

 60.             if len(message) + i < messageLength:

 61.                 # Decode the message string for the 128 (or whatever

 62.                 # blockSize is set to) characters from this block integer.

 63.                 asciiNumber = blockInt // (BYTE_SIZE ** i)

 64.                 blockInt = blockInt % (BYTE_SIZE ** i)

 65.                 blockMessage.insert(0, chr(asciiNumber))

 66.         message.extend(blockMessage)

 67.     return ''.join(message)

 68.

 69.

 70. def encryptMessage(message, key, blockSize=DEFAULT_BLOCK_SIZE):

 71.     # Converts the message string into a list of block integers, and then

 72.     # encrypts each block integer. Pass the PUBLIC key to encrypt.

 73.     encryptedBlocks = []

 74.     n, e = key

 75.

 76.     for block in getBlocksFromText(message, blockSize):

 77.         # ciphertext = plaintext ^ e mod n

 78.         encryptedBlocks.append(pow(block, e, n))

 79.     return encryptedBlocks

 80.

 81.

 82. def decryptMessage(encryptedBlocks, messageLength, key, blockSize=DEFAULT_BLOCK_SIZE):

 83.     # Decrypts a list of encrypted block ints into the original message

 84.     # string. The original message length is required to properly decrypt

 85.     # the last block. Be sure to pass the PRIVATE key to decrypt.

 86.     decryptedBlocks = []

 87.     n, d = key

 88.     for block in encryptedBlocks:

 89.         # plaintext = ciphertext ^ d mod n

 90.         decryptedBlocks.append(pow(block, d, n))

 91.     return getTextFromBlocks(decryptedBlocks, messageLength, blockSize)

 92.

 93.

 94. def readKeyFile(keyFilename):

 95.     # Given the filename of a file that contains a public or private key,

 96.     # return the key as a (n,e) or (n,d) tuple value.

 97.     fo = open(keyFilename)

 98.     content = fo.read()

 99.     fo.close()

100.     keySize, n, EorD = content.split(',')

101.     return (int(keySize), int(n), int(EorD))

102.

103.

104. def encryptAndWriteToFile(messageFilename, keyFilename, message, blockSize=DEFAULT_BLOCK_SIZE):

105.     # Using a key from a key file, encrypt the message and save it to a

106.     # file. Returns the encrypted message string.

107.     keySize, n, e = readKeyFile(keyFilename)

108.

109.     # Check that key size is greater than block size.

110.     if keySize < blockSize * 8: # * 8 to convert bytes to bits

111.         sys.exit('ERROR: Block size is %s bits and key size is %s bits. The RSA cipher requires the block size to be equal to or less than the key size. Either increase the block size or use different keys.' % (blockSize * 8, keySize))

112.    

113.

114.     # Encrypt the message

115.     encryptedBlocks = encryptMessage(message, (n, e), blockSize)

116.

117.     # Convert the large int values to one string value.

118.     for i in range(len(encryptedBlocks)):

119.         encryptedBlocks[i] = str(encryptedBlocks[i])

120.     encryptedContent = ','.join(encryptedBlocks)

121.

122.     # Write out the encrypted string to the output file.

123.     encryptedContent = '%s_%s_%s' % (len(message), blockSize, encryptedContent)

124.     fo = open(messageFilename, 'w')

125.     fo.write(encryptedContent)

126.     fo.close()

127.     # Also return the encrypted string.

128.     return encryptedContent

129.

130.

131. def readFromFileAndDecrypt(messageFilename, keyFilename):

132.     # Using a key from a key file, read an encrypted message from a file

133.     # and then decrypt it. Returns the decrypted message string.

134.     keySize, n, d = readKeyFile(keyFilename)



    # Read in the message length and the encrypted message from the file.

    fo = open(messageFilename)

    content = fo.read()

    messageLength, blockSize, encryptedMessage = content.split('_')

    messageLength = int(messageLength)

    blockSize = int(blockSize)



  # Check that key size is greater than block size.

   if keySize < blockSize * 8: # * 8 to convert bytes to bits

     sys.exit('ERROR: Block size is %s bits and key size is %s bits. The RSA cipher requires the block size to be equal to or less than the key size. Did you specify the correct key file and encrypted file?' % (blockSize * 8, keySize))



   # Convert the encrypted message into large int values.

  encryptedBlocks = []

   for block in encryptedMessage.split(','):

     encryptedBlocks.append(int(block))



 # Decrypt the large int values.

 return decryptMessage(encryptedBlocks, messageLength, (n, d), blockSize)



# If rsaCipher.py is run (instead of imported as a module) call

 # the main() function.

if __name__ == '__main__':

    main()