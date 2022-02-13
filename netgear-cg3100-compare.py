import os, sys, platform
from urllib import request
import requests

gateway_ip_endpoint   = 'MSO:0n0Adm1Ni$tRaT0r@192.168.99.1'
binary_010_editor     = 'C:/Program Files/010 Editor/010Editor.exe'

file_befor = 'GatewaySettings_bef.bin'
file_after = 'GatewaySettings_aft.bin'

from subprocess import call

def print_log(str):
    print('    ' + str)

def open_compare_tool(file_a, file_b):
    binary = binary_010_editor
    if platform.uname().release.endswith("WSL2"):
        binary = binary_010_editor.replace('C:/', '/mnt/c/')

    call([binary, f'-compare:{file_a}::{file_b}::\\b\\e\\t', '-safe', '-template:netgear-cg3100-config-decoder.bt', '-nowarnings'])

def get_config_file(file):
    try:
        res = requests.get(f'http://{gateway_ip_endpoint}/GatewaySettings.bin')
    except Exception as e:
        print("[e] misc request error: ", e)
        return False

    if file:
        with open(file, "wb") as f:
            f.write(res.content)

    return res.content

def compare():
    print('\n--\n')

    print_log('[i] (1) downloading «before» file')
    get_config_file(file_befor)

    print_log('[>] waiting for after; press Enter when ready...'); input()

    print_log('[i] (2) downloading «after» file')
    get_config_file(file_after)

    print_log('[!] decoding both files:')
    call(["python", "./netgear-cg3100-config-decoder.py", file_befor])
    call(["python", "./netgear-cg3100-config-decoder.py", file_after])

    print_log('[>] launching comparison tool...')
    open_compare_tool('{file_befor}.dec', '{file_after}.dec')

if __name__ == "__main__":
    try:
        while(True):
            compare()
            
    except KeyboardInterrupt:
        print('\n'); print_log('[!] exiting loop...\n')
        pass