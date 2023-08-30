import os
import sys
from passlib.hash import sha512_crypt


def check_root_privileges():
    """Check if the program is running with root privileges."""
    if os.getuid() != 0:
        print("Please run as root.")
        sys.exit()


def get_user_credentials():
    """Get username and password from the user."""
    uname = input("Enter username: ")
    password = input(f"Enter Password for {uname}: ")
    return uname, password


def authenticate_user(uname, password):
    """Authenticate the user."""
    with open('/etc/shadow', 'r') as fp:
        for line in fp:
            temp = line.split(':')
            if temp[0] == uname:
                salt_and_pass = temp[1].split('$')
                salt = salt_and_pass[2]
                # Calculate hash using the retrieved salt and the password
                calculated_hash = sha512_crypt.hash(password, salt_size=8, salt=salt, rounds=5000)
                if calculated_hash == temp[1]:
                    return True
                else:
                    return False
    return False


def main():
    check_root_privileges()
    uname, password = get_user_credentials()

    if authenticate_user(uname, password):
        print("Login successful.")
    else:
        print("Invalid Password or User does not exist.")


if __name__ == '__main__':
    main()
