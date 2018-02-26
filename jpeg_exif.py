import binascii
import codecs
import struct

import tags

FORMAT = {1: 1,  # "unsigned byte"
          2: 1,  # "ascii string"
          3: 2,  # "unsigned short"
          4: 4,  # "unsigned long"
          5: 8,  # "unsigned rational"
          6: 1,  # "signed byte"
          7: 1,  # "undefined"
          }


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
    last_byte = len(read_bytes)
    read_byte_list = []
    f.seek(0)
    exif_marker_index = 0

    for x in range(last_byte):
        read_byte_list.append(codecs.decode(binascii.hexlify(f.read(1)), 'ascii'))

    for x in range(len(read_byte_list)):
        if read_byte_list[x] == "ff":
            if read_byte_list[x + 1] == "e1":
                exif_marker_index = x
                break

    parsed_data = {}

    exif_bytes = read_bytes[exif_marker_index:]
    endian = exif_bytes[10:12]  # endian marker
    exif_tag = exif_bytes[4:10]  # EXIF tag

    if exif_tag != b'Exif\x00\x00':
        raise Exception("ExifParseError")

    if endian == b'MM':
        ifd_start = struct.unpack('>I', exif_bytes[14:18])[0]
        bom_bytes = exif_bytes[10:]

        while ifd_start != 0:
            number_entries = struct.unpack('>H', bom_bytes[ifd_start:ifd_start + 2])[0]
            for x in range(number_entries):
                offset_ifd_start = ifd_start + (x * 12)
                tag_number = bom_bytes[offset_ifd_start + 2:offset_ifd_start + 4]
                retrieved_tag = tags.TAGS.get(int.from_bytes(tag_number, byteorder='big'))

                if retrieved_tag is None:
                    continue

                format_code = struct.unpack('>H', bom_bytes[offset_ifd_start + 4:offset_ifd_start + 6])[0]  # Unpack format code from IFD
                format_code_size = FORMAT.get(format_code)  # get number of bytes for each component

                number_of_components = struct.unpack('>I', bom_bytes[offset_ifd_start + 6:offset_ifd_start + 10])[0]  # of components
                data_size = format_code_size * number_of_components  # date type byte size * number of components

                if data_size > 4:  # last 4 bytes gives data offset
                    data_location = struct.unpack('>I', bom_bytes[offset_ifd_start + 10:offset_ifd_start + 14])[0]
                    data = bom_bytes[data_location:data_location + data_size]
                    if format_code_size == 8:  # meaning its a rational number
                        decoded_data_numerator = struct.unpack('>I', data[0:4])[0]
                        decoded_data_denominator = struct.unpack('>I', data[4:8])[0]
                        decoded_data = str(decoded_data_numerator) + "/" + str(decoded_data_denominator)
                    else:
                        decoded_data = data[0:-1].decode()
                else:  # last 4 bytes contains data
                    data = bom_bytes[offset_ifd_start + 10:offset_ifd_start + 14]
                    if format_code_size == 2:  # short number
                        decoded_data = struct.unpack('>H', data[0:2])[0]
                    else:
                        decoded_data = struct.unpack('>I', data)[0]

                if parsed_data.get(retrieved_tag) is not None:
                    parsed_data[retrieved_tag].append(decoded_data)  # add data to dictionary
                else:
                    parsed_data[retrieved_tag] = [decoded_data]  # add data to dictionary

            ifd_start = struct.unpack('>I', bom_bytes[offset_ifd_start + 14:offset_ifd_start + 18])[0]  # Next 4 bytes offset of next IFD

    elif endian == b'II':
        ifd_start = struct.unpack('<I', exif_bytes[14:18])[0]
        bom_bytes = exif_bytes[10:]

        while ifd_start != 0:
            number_entries = struct.unpack('<H', bom_bytes[ifd_start:ifd_start + 2])[0]
            for x in range(number_entries):
                offset_ifd_start = ifd_start + (x * 12)
                tag_number = bom_bytes[offset_ifd_start + 2:offset_ifd_start + 4]
                retrieved_tag = tags.TAGS.get(int.from_bytes(tag_number, byteorder='little'))

                if retrieved_tag is None:
                    continue

                format_code = struct.unpack('<H', bom_bytes[offset_ifd_start + 4:offset_ifd_start + 6])[0]  # Unpack format code from IFD
                format_code_size = FORMAT.get(format_code)  # get number of bytes for each component

                number_of_components = struct.unpack('<I', bom_bytes[offset_ifd_start + 6:offset_ifd_start + 10])[0]  # of components
                data_size = format_code_size * number_of_components  # date type byte size * number of components

                if data_size > 4:  # last 4 bytes gives data offset
                    data_location = struct.unpack('<I', bom_bytes[offset_ifd_start + 10:offset_ifd_start + 14])[0]
                    data = bom_bytes[data_location:data_location + data_size]
                    if format_code_size == 8:  # meaning its a rational number
                        decoded_data_numerator = struct.unpack('<I', data[0:4])[0]
                        decoded_data_denominator = struct.unpack('<I', data[4:8])[0]
                        decoded_data = str(decoded_data_numerator) + "/" + str(decoded_data_denominator)
                    else:
                        decoded_data = data[0:-1].decode()
                else:  # last 4 bytes contains data
                    data = bom_bytes[offset_ifd_start + 10:offset_ifd_start + 14]
                    if format_code_size == 2:  # short number
                        decoded_data = struct.unpack('<H', data[0:2])[0]
                    else:
                        decoded_data = struct.unpack('<I', data)[0]

                if parsed_data.get(retrieved_tag) is not None:
                    parsed_data[retrieved_tag].append(decoded_data)  # add data to dictionary
                else:
                    parsed_data[retrieved_tag] = [decoded_data]  # add data to dictionary

            ifd_start = struct.unpack('<I', bom_bytes[offset_ifd_start + 14:offset_ifd_start + 18])[0]  # Next 4 bytes offset of next IFD

    return parsed_data


def main():
    # print(parse_exif(open("FullSizeRender.jpg", 'rb')))
    # print()
    print(parse_exif(open("gore-superman.jpg", 'rb')))
    # print(parse_exif(open("leaves.jpg", 'rb')))


if __name__ == "__main__":
    main()
