#!/usr/bin/env python

import os
import sys
import struct
import random
import getpass
import sys

try:
    from Crypto.Cipher import AES
    from argparse import ArgumentParser
    from argparse import RawTextHelpFormatter
except:
    print """
    Pycrypto and argparse needed.
    argparse: https: //pypi.python.org/pypi/argparse/1.3.0
    pycrypto: https://pypi.python.org/pypi/pycrypto"""


global ver
ver = 0.1

# Encryption
def Encrypt(in_file, key, out_file=None, chunksize=8192):
    if not out_file:
        out_file = in_file + '.nox'

    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_file)

    with open(in_file, 'rb') as infile:
        with open(out_file, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))
    os.remove(in_file)

# Decryption
def Decrypt(in_file, key, out_file=None, chunksize=8192):

    if not out_file:
        out_file = os.path.splitext(in_file)[0]

    with open(in_file, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)

        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_file, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)


def main():
    # Var for the key double checking
    checked = False
    # Cl arguments parser options
    parser = ArgumentParser(description="""

DESCRIPTION:
    Script uses PyCrypto AES, pycrypto must be installed.
    There're two options for cnox: single file encrypt/decrypt and files in 
    defined directory. After encryption source file will be deleted.

EXAMPLE:
    ./cnox.py -e -f filename.txt encrypt single file
    ./cnox.py -e -p /path/dirname encrypt all files in directory
    ./cnox.py -d -p /path/dirname decrypt all files in directory
    
    You will be prompted to enter the encryption key(16 symbols min).
    """, epilog="""
    
    +-+-+-+-+-+-+-+-+-+-+-+-+-+  - https://github.com/nafscript/cnox -
    |C|L|A|V|I|C|U|L|A| |N|O|X|  - Nafscript -
    +-+-+-+-+-+-+-+-+-+-+-+-+-+  - v. %s
    """ % ver, formatter_class=RawTextHelpFormatter)
    
    parser.add_argument('-d', '--decrypt', action='store_true', help='decrypt'
    ' file')
    parser.add_argument('-e', '--encrypt', action='store_true', help='encrypt'
    ' file')
    parser.add_argument('-p', '--path', action='store', help='encrypt files'
    ' in directory recursively')
    parser.add_argument('-f', '--file', action='store', help='single file to'
    ' encrypt or decrypt')
    # In no args case
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
        
    args = parser.parse_args()

    in_key = getpass.getpass('Nox: ')
    # Check the key twice
    if args.encrypt:
        check_key = getpass.getpass('Nox?: ')
        if in_key == check_key:
            checked = True
        else:
            print 'Not match... Try again...'
            exit()
    filename = args.file
    # Single file enc & dec
    if not args.path:
        if args.decrypt:
            Decrypt(in_file=filename, key=in_key)

        elif args.encrypt:
            if checked:
                Encrypt(in_file=filename, key=in_key)
    # In directory recursively
    else:
        path = args.path
        for root, dirs, files in os.walk(path):
            for f in files:
                f = os.path.join(root, f)
                if args.decrypt:
                    Decrypt(in_file=f, key=in_key)
                elif args.encrypt:
                    if checked:
                        Encrypt(in_file=f, key=in_key)


if __name__ == '__main__':
    main()
