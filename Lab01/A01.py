import sys
from random import choices

READ_ID_ = ">read_id_"
SEQ_LEN = 50


def fasta_random_generator(
    a_prob, t_prob, c_prob, g_prob, read_num, fout="A01.fa"
):
    # Build list for bases and weights
    bases = ["A", "T", "C", "G"]
    weights = [a_prob, t_prob, c_prob, g_prob]

    with open(fout, "w") as fp:
        for i in range(read_num):
            # Write line description
            fp.write(f"{READ_ID_}{i}\n")

            # Write sequence data
            sequence = choices(population=bases, weights=weights, k=SEQ_LEN)
            fp.write(f"{''.join(sequence)}\n")


def main():
    if len(sys.argv) != 6:
        raise RuntimeError(
            f"Expected 6 command line arguments, got {len(sys.argv)}"
        )

    # Parse command line arguments
    read_num = int(sys.argv[1])
    a_prob = int(sys.argv[2])
    t_prob = int(sys.argv[3])
    c_prob = int(sys.argv[4])
    g_prob = int(sys.argv[5])

    # Generate FASTA file
    fasta_random_generator(a_prob, t_prob, c_prob, g_prob, read_num)


if __name__ == "__main__":
    main()
