import os
import sys
import re
from passlib.hash import sha512_crypt

# Constants for file paths
SHADOW_FILE = '/etc/shadow'
PASSWD_FILE = '/etc/passwd'

def get_valid_salt():
    while True:
        user_input = input("Enter an 8-character salt (lowercase letters and digits): ")

        if re.match(r"^[a-z0-9]{8}$", user_input):
            return user_input
        else:
            print("Invalid salt. Please enter exactly 8 lowercase letters or digits.")
            retry = input("Do you want to retry? (yes/no): ")
            if retry.lower() != "yes":
                sys.exit("Exiting.")

def user_exists(username):
    with open(SHADOW_FILE, 'r') as fp:
        for line in fp:
            if line.startswith(username + ":"):
                return True
    return False

def update_shadow_file(username, password_hash):
    # Making hash entry in the shadow file
    shadow_line = f"{username}:{password_hash}:17710:0:99999:7:::"
    with open(SHADOW_FILE, 'a+') as shadow_file:
        shadow_file.write(shadow_line + '\n')

def create_home_directory(username):
    try:
        os.mkdir("/home/" + username)
    except FileExistsError:
        print("Directory: /home/" + username + " already exists")

def update_passwd_file(username):
    # Making user entry in the passwd file
    
    # Count is the default user ID number in our system
    count = 1000

    with open(PASSWD_FILE, 'r') as f:
        for line in f:
            temp1 = line.split(':')
            while int(temp1[3]) >= count and int(temp1[3]) < 65534:
                count = int(temp1[3]) + 1
    count = str(count)

    passwd_line = f"{username}:x:{count}:{count}:,,,:/home/{username}:/bin/bash"

    with open(PASSWD_FILE, 'a+') as passwd_file:
        passwd_file.write(passwd_line + '\n')

def get_input(prompt, default=None):
    if default is not None:
        prompt += f" (or press Enter for {default}) : "
    response = input(prompt)
    if not response:
        return default
    return response

def create_user(username):
    if user_exists(username):
        print("The user already exists. Try deleting it first.")
        sys.exit()

    password = get_input("Enter Password for the user", "password")
    re_password = get_input("Re-enter Password for the user", "password")

    # Just making sure you know what you are entering in password
    if password != re_password:
        print("Passwords do not match")
        sys.exit()

    salt = get_valid_salt()
    password_hash = sha512_crypt.hash(password, salt_size=8, salt=salt, rounds=5000)

    update_passwd_file(username)
    update_shadow_file(username, password_hash)
    create_home_directory(username)


if __name__ == '__main__':
    # Checking whether the program is running as a root or not.
    if os.getuid() != 0:
        print("Please, run as root.")
        sys.exit()

    uname = get_input("Enter Username you want to add", "username")
    create_user(uname)

