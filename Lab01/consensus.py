import sys


def read_alignment_file(fin):
    sequences = []
    positions = []

    with open(fin, "r") as fp_in:
        for line in fp_in:
            line = line.strip()
            elements = line.split("\t")
            seq = elements[1]
            pos = elements[2]

            sequences.append(seq)
            positions.append(int(pos))

    return sequences, positions


# Assumption in requirements: all reads have the same length
def consensus_region(fin):
    # Read alignment file and store it
    sequences, positions = read_alignment_file(fin)

    size = len(sequences[0])
    num_regions = 0
    region, regions = [], []

    for i in range(max(positions) + size):
        max_count, max_base = 0, ""
        counts = {"A": 0, "T": 0, "C": 0, "G": 0}

        # Update the count for each base considering all the bases
        # in the i-th position (for all the reads)
        for read in range(len(sequences)):
            pos = positions[read]
            if pos <= i < pos + size:
                base = sequences[read][i - pos]
                counts[base] += 1

                if counts[base] > max_count:
                    max_count = counts[base]
                    max_base = base

        if max_base == "":
            # If current region not empty
            if len(region) > 0:
                regions.append(region)
                num_regions += 1
            region = []
        else:
            region.append(max_base)

    if len(region) > 0:
        regions.append(region)
        num_regions += 1

    return num_regions, regions


def main():
    if len(sys.argv) != 2:
        raise RuntimeError(
            f"Expected 2 command line arguments, got {len(sys.argv)}"
        )

    # Parse command line arguments
    fin = sys.argv[1]

    # Compare FASTA files
    num_regions, regions = consensus_region(fin)
    print(f"Number of consensus regions: {num_regions}")
    for region in regions:
        print("".join(region))


if __name__ == "__main__":
    main()
