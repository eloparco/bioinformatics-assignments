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


def consensus_region(fin):
    # Read alignment file and store it
    sequences, positions = read_alignment_file(fin)

    # All reads have the same length
    size = len(sequences[0])
    prev_is_space = False
    count = 0
    for i in range(max(positions) + size):
        counts = {"A": 0, "T": 0, "C": 0, "G": 0}

        # Update the count for each base considering all the bases
        # in the i-th position (for all the sequences)
        for j in range(len(sequences)):
            if i >= positions[j] and i < positions[j] + size:
                base = sequences[j][i - positions[j]]
                counts[base] += 1

        # Calculate the maximum number of votes
        max_count = max(
            counts["A"], max(counts["T"], max(counts["C"], counts["G"]))
        )

        # Print a newline and update count if no base in current position
        # and previous position was not empty
        if max_count == 0:
            if prev_is_space is not True:
                count += 1
                print("")
            prev_is_space = True
            continue

        # Print the base with the maximum number of votes
        if counts["A"] == max_count:
            print("A", end="")
        elif counts["T"] == max_count:
            print("T", end="")
        elif counts["C"] == max_count:
            print("C", end="")
        elif counts["G"] == max_count:
            print("G", end="")
        prev_is_space = False

    print(f"\n\nNumber of consensus regions: {count + 1}")


def main():
    if len(sys.argv) != 2:
        raise RuntimeError(
            f"Expected 2 command line arguments, got {len(sys.argv)}"
        )

    # Parse command line arguments
    fin = sys.argv[1]

    # Compare FASTA files
    consensus_region(fin)


if __name__ == "__main__":
    main()
