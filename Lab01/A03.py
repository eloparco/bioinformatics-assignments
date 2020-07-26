import sys


def compare_fasta_files(fin1, fin2):
    reads = {}

    # Read first file and store in map
    with open(fin1, "r") as fp_in:
        for line in fp_in:
            line = line.strip()
            if line.startswith(">"):
                read_id = line
            else:
                reads[line] = read_id

    with open("common.fa", "w") as fp_out, open(fin2, "r") as fp_in:
        for line in fp_in:
            line = line.strip()
            if line.startswith(">"):
                read_id = line
                continue

            # Write common reads to output file
            if line in reads:
                fp_out.write(f"{reads[line]}{read_id}\n")
                fp_out.write(f"{line}\n")


def main():
    if len(sys.argv) != 3:
        raise RuntimeError(
            f"Expected 3 command line arguments, got {len(sys.argv)}"
        )

    # Parse command line arguments
    fin1 = sys.argv[1]
    fin2 = sys.argv[2]

    # Compare FASTA files
    compare_fasta_files(fin1, fin2)


if __name__ == "__main__":
    main()
