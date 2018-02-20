# SOI ff or d8
# EOI ff or d9


def createTestFile():
    with open("test/test.dat", "rb+") as f:
        f.write(b'\xff')
        f.write(b'\xff')
        f.write(b'B')
        f.write(b'\xff')
        f.write(b'B')
        f.write(b'B')
        f.write(b'\xff')
        f.write(b'\xff')
        f.write(b'\xff')
        f.write(b'\xff')
        f.write(b'\xff')
    print("Wrote byte to file.")


def main():
    createTestFile()


if __name__ == "__main__":
    main()
