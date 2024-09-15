# Simple CLI encryption tool written in python that can encrypt and decrypt files. 

# Installation:  

git clone https://github.com/hmMythreya/nCrypt  

cd nCrypt  

pip install -r requirements.txt  

# To run:  

python3 nCrypt.py

# Usage:  

python3 nCrypt.py by default enters into interactive mode, follow the instructions shown on screen.

In order to use this tool without interactive mode, you need to pass in command line arguments

python3 nCrypt.py \[--help | -h] prints the help page

The tool takes in 4 arguments:

  --mode : Encryption mode or Decryption mode

  --input : path to input file
  
  --output : path to output file (WARNING: WILL OVERWRITE OUTPUT FILE COMPLETELY, BE CAREFUL)
  
  --key : enter the key to be used for encryption/decryption
