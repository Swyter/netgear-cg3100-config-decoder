import sys
import hashlib, struct

filename="GatewaySettings(6).bin"

if len(sys.argv) > 1:
    filename = sys.argv[1]

print(f'[i] opening «{filename}»')

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

if filename.endswith(".dec"):
    print(f'[+] encoding')
    encode = True
    suffix = ".bin"
else:
    print(f'[+] decoding')
    encode = False
    suffix = ".dec"
    
b_dec = bytearray(b)

with open(f"{filename}{suffix}", "wb") as fout:
    for i, byte in enumerate(b):
        if (i & 1) == 0:
            if encode:
                # swy: swap it back
                tmp_a = b_dec[i    ]
                tmp_b = b_dec[i + 1]
                b_dec[i    ] = tmp_b
                b_dec[i + 1] = tmp_a

                # swy: add the odd bytes against their file offset
                #      make it wrap around
                b_dec[i] = (b_dec[i] + i) & 0xff
            else:
                # swy: to decode; subtract the odd bytes against
                #      their file offset and make it wrap around
                b_dec[i] = (b_dec[i] - i) & 0xff

                # swy: swap; wtfbbq, maybe an artifact of the endianness
                #      for the ushort-sized blocks ¯\_(ツ)_/¯
                tmp_a = b_dec[i    ]
                tmp_b = b_dec[i + 1]
                b_dec[i    ] = tmp_b
                b_dec[i + 1] = tmp_a

        fout.write(int.to_bytes(b_dec[i], 1, "little"))

if not encode:
    # swy: big endian uint; at offset 0x4c
    stated_size = struct.unpack(">I", b_dec[0x5c:0x60])[0]
    print(f'[i] stated size: {stated_size:#x}, actual size: {len(b_dec[16:]):#x}')

    # swy: thanks to Joseph Lehner for all the work and this generic salt value; see gwsettings.cc and FORMAT.md in bcm2-utils
    ret = hashlib.md5(b_dec[16:16 + stated_size] + b"2Pslc;u(egmd0-'x")
    print(f'[i] computed MD5 hash: {ret.digest().hex()}')
    print(f'[i] existing MD5 hash: {  b_dec[:16].hex()}', ret.digest() == b_dec[:16] and '(valid)' or '(invalid)')