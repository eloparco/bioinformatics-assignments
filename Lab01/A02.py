import sys
import re

LC_NUM = 6


def write_fasta_statistics(fin, fout, th):
    base_counts = {"A": 0, "T": 0, "C": 0, "G": 0}
    lc_counts = 0

    with open(fin, "r") as fp_in, open(fout, "w") as fp_out:
        fp_out.write("GC content:\n")
        gc_count = 0

        # ASSUMPTION: each read spans only one line
        # (not true in general)
        for line in fp_in:
            line = line.strip()
            if line.startswith(">"):
                read_id = line
                continue

            # Count occurrences of each base
            for base in line:
                base_counts[base] += 1

            # Count low complexity sequences
            found = False
            for base in ["A", "T", "C", "G"]:
                lc_seq = base * LC_NUM
                if lc_seq in line:
                    found = True
                    break
            if found:
                lc_counts += 1

            # Calculate GC content
            gc_content = len(re.findall("C|G", line))
            if gc_content > th:
                fp_out.write(f"{read_id}: {gc_content}\n")
                gc_count += 1

        # Write summary on file
        fp_out.write(f"Number of A bases: {base_counts['A']}\n")
        fp_out.write(f"Number of T bases: {base_counts['T']}\n")
        fp_out.write(f"Number of C bases: {base_counts['C']}\n")
        fp_out.write(f"Number of G bases: {base_counts['G']}\n")
        fp_out.write(
            f"Reads with at least one low complexity seq: {lc_counts}\n"
        )
        fp_out.write(f"Reads with high GC content: {gc_count}\n")


def main():
    if len(sys.argv) != 4:
        raise RuntimeError(
            f"Expected 4 command line arguments, got {len(sys.argv)}"
        )

    # Parse command line arguments
    fin = sys.argv[1]
    fout = sys.argv[2]
    GC_THRESHOLD = int(sys.argv[3])

    # Generate FASTA file
    write_fasta_statistics(fin, fout, GC_THRESHOLD)


if __name__ == "__main__":
    main()
