import binascii
import codecs


def carve(f, start, end):
    f.seek(start)
    return f.read((end + 1) - start)


# TODO: fix counting issues
def find_jfif(f, max_length=None):
    chunk = f.read()
    last_byte = len(chunk)

    if max_length is None:
        max_length = last_byte

    f.seek(0)

    unfiltered_sequence_pairs = []
    filtered_sequence_pairs = []

    locations_soi = []
    locations_eoi = []

    soi_index = -1
    eoi_index = -1

    for x in range(last_byte):
        decoded_byte = codecs.decode(binascii.hexlify(f.read(1)), 'ascii')
        if decoded_byte == "ff":
            next_decoded_byte = codecs.decode(binascii.hexlify(f.read(1)), 'ascii')
            if next_decoded_byte == "d8":  # SOI (ff d8)
                soi_index += 1
                locations_soi.append(soi_index)
            else:
                soi_index += 1
        else:
            soi_index += 1

    f.seek(0)

    for x in range(last_byte):
        decoded_byte = codecs.decode(binascii.hexlify(f.read(1)), 'ascii')
        if decoded_byte == "ff":
            next_decoded_byte = codecs.decode(binascii.hexlify(f.read(1)), 'ascii')
            if next_decoded_byte == "d9":  # SOI (ff d8)
                eoi_index += 1
                locations_eoi.append(eoi_index)
            else:
                eoi_index += 1
        else:
            eoi_index += 1

    print(locations_soi)
    print(locations_eoi)

    for x in range(len(locations_soi)):
        for y in range(len(locations_eoi)):
            if locations_soi[x] < locations_eoi[y]:
                unfiltered_sequence_pairs.append((locations_soi[x], locations_eoi[y]))

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
    # sequence_pairs = find_jfif(open("Designs.doc", 'rb'), 154)
    sequence_pairs = find_jfif(open("test/test.dat", 'rb'), 2)
    print(sequence_pairs)


if __name__ == "__main__":
    main()
