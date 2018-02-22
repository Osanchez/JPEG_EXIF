import binascii
import codecs
import struct


def carve(f, start, end):
    f.seek(start)
    return f.read((end + 1) - start)


def find_jfif(f, max_length=None):
    chunk = f.read()
    last_byte = len(chunk)

    if max_length is None:
        max_length = last_byte

    f.seek(0)

    byte_list = []

    unfiltered_sequence_pairs = []
    filtered_sequence_pairs = []

    locations_soi = []
    locations_eoi = []

    for x in range(last_byte):
        read_byte = codecs.decode(binascii.hexlify(f.read(1)), 'ascii')
        byte_list.append(read_byte)

    for x in range(len(byte_list)):
        if byte_list[x] == "ff":
            if byte_list[x + 1] == "d8":
                locations_soi.append(x)
            elif byte_list[x + 1] == "d9":
                locations_eoi.append(x + 1)

    for x in range(len(locations_soi)):
        for y in range(len(locations_eoi)):
            if locations_soi[x] < locations_eoi[y]:
                unfiltered_sequence_pairs.append((locations_soi[x], locations_eoi[y]))

    for x in range(len(unfiltered_sequence_pairs)):
        pair = unfiltered_sequence_pairs[x]
        if (pair[1] - pair[0]) < max_length:
            filtered_sequence_pairs.append(pair)
    return filtered_sequence_pairs


def parse_exif(f):
    read_bytes = f.read()

    print(read_bytes[0:2])

def main():
    parse_exif(open("Designs.doc", 'rb'))


if __name__ == "__main__":
    main()
