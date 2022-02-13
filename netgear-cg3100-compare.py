import os, sys
from urllib import request
import requests

gateway_ip_endpoint = "192.168.99.1"
binary_010_editor   = "C:\Program Files\\010 Editor\\010Editor.exe"

from subprocess import call

def open_compare_tool(file_a, file_b):
    call([binary_010_editor, "-compare:{file_a}::{file_b}}"])

def get_config_file(file = None):
    try:
        res = requests.get(f'http://{gateway_ip_endpoint}/GatewaySettings.bin')
    except Exception as e:
        print("[e] misc request error: ", e)
        return False

    if file:
        with open(file, "wb") as f:
            b=f.write(res.content)

    return res.content

def compare():
    print(f'[i] opening »')

    get_config_file("GatewaySettings_before.bin")

    input("[>] waiting for after...")

    get_config_file("GatewaySettings_after.bin")

    call(["python", "./netgear-cg3100-config-decoder.py", "GatewaySettings_before.bin"])
    call(["python", "./netgear-cg3100-config-decoder.py", "GatewaySettings_after.bin"])

    open_compare_tool("GatewaySettings_before.bin.dec", "GatewaySettings_after.bin.dec")

if __name__ == "__main__":
  compare()