import os, subprocess
import sys
from base64 import b64encode
import crypt
from passlib.hash import pbkdf2_sha256


def create_user(username):
    with open('shadow', 'r') as fp:  # Opening shadow file in read mode
        arr = []
        for line in fp:  # Enumerating through all the entries in shadow file
            temp = line.split(':')
            if temp[0] == username:  # checking whether entered username exist or not
                print("The user already exist. Try deleting it first.")
                sys.exit()

    passwd = input("Enter Password for the user: " or "password")
    re_passwd = input("Re-enter Password for the user: " or "password")

    # just making sure you know what you are entering in password
    if passwd != re_passwd:
        print("Passwords do not match")
        sys.exit()

    rand1 = os.urandom(6)
    salt = str(b64encode(rand1).decode('utf-8'))  # generating salt, eight characters long

    hash = crypt.crypt(passwd, '$6$' + salt)  # generating hash
    line = username + ':' + hash + ":17710:0:99999:7:::"
    file1 = open("/etc/shadow", "a+")  # Opening shadow file in append+ mode
    file1.write(line + '\n')  # Making hash entry in the shadow file
    try:
        os.mkdir("/home/" + username)  # Making home file for the user
    except:
        print("Directory: /home/" + username + " already exist")
    file2 = open("/etc/passwd", "a+")  # Opening passwd file in append+ mode

    count = 1000

    with open('/etc/passwd', 'r') as f:  # Opening passwd file in read mode
        arr1 = []
        for line in f:
            temp1 = line.split(':')
            # checking number of existing UID
            while (int(temp1[3]) >= count and int(temp1[3]) < 65534):
                count = int(temp1[3]) + 1  # assigning new uid = 1000+number of UIDs +1

    count = str(count)
    str1 = username + ':x:' + count + ':' + count + ':,,,:/home/' + username + ':/bin/bash'
    file2.write(str1 + '\n')  # creating entry in passwd file for new user
    file2.close()
    file1.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # checking whether program is running as a root or not.
    # if os.getuid() != 0:
    #     print("Please, run as root.")
    #     sys.exit()

    uname = input("Enter Username you want to add: " or "username")

    create_user(uname)
