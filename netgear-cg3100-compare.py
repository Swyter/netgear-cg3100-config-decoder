import os, sys, platform
from urllib import request
import requests

gateway_ip_endpoint   = 'MSO:0n0Adm1Ni$tRaT0r@192.168.99.1'

file_befor = 'GatewaySettings_a.bin'
file_after = 'GatewaySettings_b.bin'

from subprocess import call

def print_log(str):
    print('    ' + str)

def open_compare_tool(file_a, file_b):
    call(['010Editor.exe', f'-compare:{file_a}::{file_b}::\\b\\e\\t', '-template:netgear-cg3100-config-decoder.bt'])

def get_config_file(file):
    try:
        res = requests.get(f'http://{gateway_ip_endpoint}/GatewaySettings.bin')
    except Exception as e:
        print('[e] misc request error: ', e)
        return False

    if file:
        with open(file, 'wb') as f:
            f.write(res.content)

    return res.content

if __name__ == '__main__':
    try:
        print_log('[i] (1) downloading «before» file')
        get_config_file(file_befor); call(['python', './netgear-cg3100-config-decoder.py', file_befor]); print('\n')

        while(True):
            print('\n--\n')

            print_log('[>] waiting for after; press the enter key when ready...'); input()

            print_log('[i] (2) downloading «after» file')
            get_config_file(file_after); call(['python', './netgear-cg3100-config-decoder.py', file_after]); print('\n')

            print_log('[>] launching comparison tool...')
            open_compare_tool(f'{file_befor}.dec', f'{file_after}.dec')

            print_log('[i] press the enter key...'); input()

            # swy: swap them so that we can chain the comparison with the previous one; A -> B then B -> C
            print_log('[>] swapping comparison order for the next run...')
            tmp = file_befor
            file_befor = file_after
            file_after = tmp
            
    except KeyboardInterrupt:
        print('\n'); print_log('[!] exiting loop...\n')
        pass