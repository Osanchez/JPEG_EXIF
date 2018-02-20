# SOI (ff d8)
# EOI ff or d9


def createTestFile():
    with open("test/test.dat", "rb+") as f:
        f.write(b'\xff')
        f.write(b'\xd9')  # EOI

        f.write(b'\xff')
        f.write(b'\xd8')  # SOI

        f.write(b'B')     # B

        f.write(b'\xff')
        f.write(b'\xd9')  # EOI

        f.write(b'B')     # B

        f.write(b'B')     # B

        f.write(b'\xff')
        f.write(b'\xd9')  # EOI

        f.write(b'\xff')
        f.write(b'\xd8')  # SOI

        f.write(b'\xff')
        f.write(b'\xd9')  # EOI

        f.write(b'\xff')
        f.write(b'\xd8')  # SOI

        f.write(b'\xff')
        f.write(b'\xd8')  # SOI

        f.write(b'\xff')
        f.write(b'\xd9')  # EOI

    print("Wrote byte to file.")


def main():
    createTestFile()


if __name__ == "__main__":
    main()
