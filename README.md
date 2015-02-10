
Python AES files encryption.
Simple script for files encryption/decryption using PyCrypto toolkit.
PyCrypto must be installed.

EXAMPLE:
  ./cnox.py -e -f filename.txt    encrypt single file
  ./cnox.py -e -p /path/dirname   encrypt files in dirname recursively
  ./cnox.py -d -p /path/dirname   decrypt files in dirname recursively
  
  You will be prompted to enter encryption key(twice when encrypt).
  
OPTIONAL ARGUMENTS:
  -e, --encrypt   encrypt file
  -d, --decrypt   decrypt file
  -f, --file      file to encrypt/decrypt
  -p, --path      path and directory name for batch encrypion
