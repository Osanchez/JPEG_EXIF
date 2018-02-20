import binascii
import codecs


def carve(f, start, end):
    f.seek(start)
    return f.read((end + 1) - start)


def find_jfif(f, max_length=None):
    with open(f, 'rb') as f:
        chunk = f.read()
        last_byte = len(chunk)
        f.seek(0)

        unfiltered_sequence_pairs = []
        filtered_sequence_pairs = []
        locations_soi = []
        locations_eoi = []

        for x in range(last_byte):
            decoded_byte = codecs.decode(binascii.hexlify(f.read(1)), 'ascii')
            if decoded_byte == "ff":  # SOI (ff d8)
                next_decoded__byte = codecs.decode(binascii.hexlify(f.read(1)), 'ascii')
                if next_decoded__byte == "d8":
                    locations_soi.append(x)

        f.seek(0)

        for x in range(last_byte):
            decoded_byte = codecs.decode(binascii.hexlify(f.read(1)), 'ascii')
            if decoded_byte == "ff":  # EOI (ff d9)
                next_decoded__byte = codecs.decode(binascii.hexlify(f.read(1)), 'ascii')
                if next_decoded__byte == "d9":
                    locations_eoi.append(x)
        f.close()

        print("SOI: " + str(locations_soi))
        print("EOI: " + str(locations_eoi))

    for x in range(len(locations_soi)):
        for y in range(len(locations_eoi)):
            if locations_soi[x] < locations_eoi[y]:
                unfiltered_sequence_pairs.append([locations_soi[x], locations_eoi[y]])

    for x in range(len(unfiltered_sequence_pairs)):
        pair = unfiltered_sequence_pairs[x]
        if (pair[1] - pair[0]) <= max_length:
            filtered_sequence_pairs.append(pair)
    return filtered_sequence_pairs


def parse_exif(f):
    pass
    # do it!

    # ...

    # Don't hardcode the answer! Return your computed dictionary.


def main():
    #  read_bytes = carve("test/search.jpg", 0, 3)
    #  print(read_bytes)

    print("My Test File.")
    sequence_pairs = find_jfif("test/test.dat", 2)
    print(sequence_pairs)

    print()

    print("Image from course website.")
    sequence_pairs = find_jfif("test/search.JFIF", 185484)
    print(sequence_pairs)

    print()

    read_bytes = carve("test/search.JFIF", 0, 4)
    print(read_bytes)


if __name__ == "__main__":
    main()
