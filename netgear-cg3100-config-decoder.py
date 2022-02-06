from ast import arguments
import os, sys

filename="GatewaySettings(4).bin.dec"

if len(sys.argv) > 1:
    filename = sys.argv[1]

text=""
b=None

with open(f"{filename}", "rb") as f:
    b=f.read()
    #for i, byte in enumerate(b):
    #    text += f'{byte:02X}/{i&0xff:02X}/{byte ^ (i & 0xff):02X} '
    #
    #    #if ((i + 1) % 16) == 0:
    #    if (i & 0xF) == 0xF:
    #        text += "--\n"
#print(text)

encode = False
suffix = ".dec"

if filename.endswith(".dec"):
    encode = True
    suffix = ".bin"
    
b_dec = bytearray(b)

with open(f"{filename}{suffix}", "wb") as fout:
    for i, byte in enumerate(b):
        if (i & 1) == 0:
            if encode:
                # swy: swap
                tmp_a = b_dec[i    ]
                tmp_b = b_dec[i + 1]
                b_dec[i    ] = tmp_b
                b_dec[i + 1] = tmp_a

                # swy: add the odd bytes against their file offset
                #      make it wrap around
                b_dec[i] = (b_dec[i] + i) & 0xff
            else:
                # swy: subtract the odd bytes against their file offset
                #      make it wrap around
                b_dec[i] = (b_dec[i] - i) & 0xff

                # swy: swap
                tmp_a = b_dec[i    ]
                tmp_b = b_dec[i + 1]
                b_dec[i    ] = tmp_b
                b_dec[i + 1] = tmp_a

        fout.write(int.to_bytes(b_dec[i], 1, "little"))