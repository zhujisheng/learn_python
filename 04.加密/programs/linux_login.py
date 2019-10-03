'''
本程序使用Linux操作系统自身的用户信息，验证用户输入的用户名和密码是否正确。
本程序仅能在Linux下运行。
'''

import spwd
import crypt
import getpass
from hmac import compare_digest

username = input('输入用户名: ')
cryptedpasswd = spwd.getspnam(username)[1]

if cryptedpasswd == 'x' or cryptedpasswd == '*':
    print("This user has no password!")
    exit()

cleartext = getpass.getpass('输入密码: ')
r = crypt.crypt(cleartext, salt=cryptedpasswd)

if compare_digest(r, cryptedpasswd):
    print("The username and password is OK!")
else:
    print("The password is wrong!")
