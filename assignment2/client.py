from struct import Struct
import sys

packer = [Struct("f?c"), Struct("c9si"), Struct("i?f"), Struct("cf9s")]

if len(sys.argv) > 4:
    for i in range(4):
        filename = sys.argv[i + 1]
        with open(filename, "rb") as file:
            packed_data = file.read(packer[i].size)
            data = packer[i].unpack(packed_data)
            print(data)
else:
    print("Usage: script.py file1 file2 file3 file4")

packer1 = Struct("14s i ?")
print(packer1.pack(b"elso", 54, True))

packer2 = Struct("f ? c")
print(packer2.pack(57.5, False, b'X'))

packer3 = Struct("i 12s f")
print(packer3.pack(45, b"masodik", 64.9))

packer4 = Struct("c i 15s")
print(packer4.pack(b'Z', 76, b"harmadik"))
