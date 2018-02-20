import binascii
import codecs


def read_file_object(f):  # for testing
    with open(f, 'rb') as f:
        for chunk in iter(lambda: f.read(16), b''):
            print(binascii.hexlify(chunk))


def carve(f, start, end):
    read_bytes = []
    with open(f, 'rb+') as f:
        f.seek(start * 16)
        for x in range((end - start) + 1):
            read_bytes.append(binascii.hexlify(f.read(16)))
    return read_bytes


def find_jfif(f, max_length=None):
    with open(f, 'rb+') as f:
        chunk = f.read()
        last_byte = len(chunk)
        f.seek(0)

        unfiltered_sequence_pairs = []
        filtered_sequence_pairs = []
        location_soi = 0
        locations_eoi = []

        # TODO: Determine what sequence pairs are considered SOI and EOI.
        for x in range(last_byte):
            byte = f.read(1)
            decoded_byte = codecs.decode(binascii.hexlify(byte), 'ascii')
            if decoded_byte == "ff" or decoded_byte == "d8":  # SOI
                location_soi = x
            if decoded_byte == "ff" or decoded_byte == "d9":  # EOI
                locations_eoi.append(x)
        for y in range(len(locations_eoi)):
            if location_soi < locations_eoi[y]:
                unfiltered_sequence_pairs.append([location_soi, y])

        for x in range(len(unfiltered_sequence_pairs)):
            pair = unfiltered_sequence_pairs[x]
            if (pair[1] - pair[0]) <= max_length:
                filtered_sequence_pairs.append(pair)

    return filtered_sequence_pairs


def main():
    #  read_file_object("test/search.jpg")

    #  read_bytes = carve("test/search.jpg", 0, 3)
    #  print(read_bytes)

    sequence_pairs = find_jfif("test/test.dat", 2)
    # sequence_pairs = find_jfif("test/search.jpg", 2)
    print(sequence_pairs)


if __name__ == "__main__":
    main()
