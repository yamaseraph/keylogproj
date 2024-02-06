#this program generates a new key 
from cryptography.fernet import Fernet

key = Fernet.generate_key() #generates keys

file = open("encryptionkey.txt", "wb") #writing to file
file.write(key)
file.close()