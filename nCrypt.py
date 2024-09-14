# Importing modules that we will use. cryptography module is the go-to for encryption. Colorama is a cross-platform python module that will give color output to terminal
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from colorama import init as colorama_init
from colorama import deinit as colorama_deinit
from colorama import reinit as colorama_reinit
from colorama import Fore
from colorama import Style
from base64 import urlsafe_b64encode
from random import choices
from string import ascii_letters
from string import digits
from argparse import ArgumentParser
import sys

# Defining global variables
colorInit = False
colorReset = Style.RESET_ALL

# Defining Custom Exception
class fileErr(Exception):
    pass

# Defining a function that will print colored or non colored text to stdout (terminal). Takes in 2 lists, messageList that contains message
def terminalPrinter(messageList, colorList):
    
    global colorInit
    global colorReset
    
    if(colorInit):
        colorama_reinit()
    else:
        colorama_init()
        colorInit = True
    
    if type(messageList) != list and type(colorList) != list:
        print(f"{colorList}{messageList}{colorReset}",end="")

    else:
        for message,color in zip(messageList, colorList):
            print(f"{color}{message}{colorReset}",end="")

    
    colorama_deinit()

# Defining a function to read the file that the user provides
def readFile(pathToFile):
    try:
        with open(pathToFile, "rb") as file:
            return file.read()
    except:
        raise fileErr

# Defining a function to write to file
def writeFile(content, pathToFile):
    try:
        with open(pathToFile, "wb+") as file:
            file.write(content)
    except:
        raise fileErr

# Function for generating key compatible for Fernet, based on user key
def keyGen(keyIn):
    salt = b"1"
    keyIn = bytes(keyIn, "utf-8")
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=480000,)
    enc = urlsafe_b64encode(kdf.derive(keyIn))
    return Fernet(enc)

# Function for encryption and decryption
def encryptAndDecrypt(call, content):
    if(call == "e"):
        flag = True
        while flag:
            terminalPrinter(["Would you like to generate a ","key ","or use your own? ", "[G]","enerate ","[O]","wn: "],[Fore.WHITE, Fore.GREEN, Fore.WHITE, Fore.RED, Fore.WHITE, Fore.RED, Fore.WHITE])
            choice = input().lower()
            if choice == "g":
                key = "".join(choices(ascii_letters+digits,k=32))
                break
            elif choice == "o":
                key = input("Enter key: ")
                break
            else:
                terminalPrinter(["Please enter a valid choice between ","O ","for entering your own key or ", "G ", "for generating a key\n"],[Fore.WHITE, Fore.RED, Fore.WHITE, Fore.RED, Fore.WHITE])
                continue

        fernet = keyGen(key)
        terminalPrinter(["Key used to encrypt: ",f"{key}\n"],[Fore.WHITE, Fore.GREEN])
        encrypted = fernet.encrypt(content)

        return encrypted

    else:
        terminalPrinter("Enter the key to be used for decryption: ", Fore.WHITE)
        keyIn = input()
        fernet = keyGen(keyIn)
        decrypted = fernet.decrypt(content)

        return decrypted

def main():
    terminalPrinter(["# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #\n# ","Welcome to Mythreya's nCrypt program! ","#\n# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #\n\n"],[Fore.RED,Fore.YELLOW,Fore.RED])
    flag = True
    while flag:
        terminalPrinter(["Please choose what you would like to do: ","[E]","ncrypt ","[D]","ecrypt ","[Q]" , "uit: "], [Fore.WHITE, Fore.RED, Fore.WHITE, Fore.RED, Fore.WHITE, Fore.RED, Fore.WHITE])
        choice = input().lower()
        if choice == "e":
            call = "e"
            flag = False
        elif choice == "d":
            call = "d"
            flag = False
        elif choice == "q":
            terminalPrinter("Thanks for using Mythreya's nCrypt program! Exiting...\n",Fore.RED)
            return False
        else:
            terminalPrinter(["Please enter a valid choice between ","e ","for encrypt and ","d ","for decrypt\n"],[Fore.WHITE, Fore.RED, Fore.WHITE, Fore.RED, Fore.WHITE])
        
    pathToFile = input("Please enter path to input file: ")
    try:
        out = encryptAndDecrypt(call, readFile(pathToFile))
    except fileErr:
        print("Could not open file/File not found. Please make sure the path you have entered is correct, and that you have appropriate read permissions.")
        return True
    except Exception:
        raise Exception
    else:
        if call == "e":
            print("Encrypted successfully! Please enter the path to file you want to write the encrypted data to: ",end="")
        else:
            print("Decrypted with key provided. Please enter the path to file you want to write the decrypted data to: ",end="")
        
        pathToFileTwo = input()
        try:
            writeFile(out,pathToFileTwo)
        except Exception:
            raise Exception
            print("Could not write to file/Path not found. Please make sure the path you have entered is correct, and that you have appropriate write permissions.")
            return True
        else:
            print("Write Successful!")
            return True

if __name__ == "__main__":
    parser = ArgumentParser(
            prog = "python3 nCrypt.py",
            description = "CLI tool to encrypt and decrypt files, written in python",
            epilog = "Thanks for using nCrypt. check https://github.com/hmMythreya/nCrypt")
    
    if(len(sys.argv)==1):
        exitFlag = True
        while exitFlag:
            exitFlag = main()
    else:
        parser.add_argument("--mode", action="store", required=True, metavar="Used to set encrypt mode or decrypt mode. e | enc | encrypt or d | dec | decrypt")
        parser.add_argument("--input", action="store", required=True, metavar="Path to file to be encrypted or decrypted", nargs=1)
        parser.add_argument("--output", action="store", required=True, metavar="Path to destination file for storing encrypted or decrypted data", nargs=1)
        parser.add_argument("--key", action="store", required=True, metavar="Use this to enter your own key. Program will generate it's own and output to stdout if this is not specified", nargs="?")
        


