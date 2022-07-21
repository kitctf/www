import struct
import sys


EOCD = "504b0506"


def little_endian_to_int(hexstr: str):
    hexbytes = bytearray.fromhex(hexstr)
    hexbytes.reverse()
    return int(hexbytes.hex(), 16)


path_in = sys.argv[1]
path_out = sys.argv[2]

file_in = open(path_in, "rb")
file_out = open(path_out, "wb")


bytestring = file_in.read().hex()

# gather positions of valid central directory headers
positions = []
start = 0
while (cur := bytestring.find(EOCD, start)) != -1:
    offset_start = cur + 2 * 16
    pos = little_endian_to_int(bytestring[offset_start: offset_start + 2 * 4]) * 2
    positions.append(pos)

    start = cur + 1

# collect valid headers and flag letters
flag_letters = dict()
local_headers = []
central_headers = []
local_size = 0
central_size = 0
for pos in positions:
    central = bytestring[pos: bytestring.find("504b0", pos + 1)]
    local_pos = little_endian_to_int(central[2 * 42: 2 * 46]) * 2
    local = bytestring[local_pos: bytestring.find("504b0", local_pos + 1)]

    central = (
        central[0:60]
        + "00000000"
        + central[68:84]
        + struct.pack("<I", (local_size // 2)).hex()
        + central[92:]
    )

    local_headers.append(local)
    local_size += len(local)
    central_headers.append(central)
    central_size += len(central)

    if local[60:68] == "flag".encode("utf8").hex():
        data = bytes.fromhex(local[68:74]).decode("ascii")
        flag_letters[int(data[0:2])] = data[2]

# build valid zip archive
num = struct.pack("<H", (len(local_headers))).hex()
end = (
    "504b050600000000"
    + num
    + num
    + struct.pack("<I", (central_size // 2)).hex()
    + struct.pack("<I", (local_size // 2)).hex()
    + "00000000"
)
result = "".join(local_headers) + "".join(central_headers) + end

file_out.write(bytes.fromhex(result))

flag = ""
items = list(flag_letters.items())
items.sort()
for (key, value) in items:
    flag += value
print("The flag is: " + flag)
