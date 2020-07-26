import sys


def gtf_filter(fin, fout="data/reduced.gtf"):
    with open(fin, "r") as fp_in, open(fout, "w") as fp_out:
        for line in fp_in:
            # Select chromosomes 10 and 18, gene_biotype
            # equals to "protein_coding" and feature equals to "gene"
            if (
                line.startswith("10") or line.startswith("18")
            ) and "protein_coding" in line:
                feature = line.split("\t")[2]
                if feature == "gene":
                    fp_out.write(line)


def raw_read_count(sam_file, gtf_file="data/reduced.gtf"):
    # BETTER to store in memory the GTF file
    # because it is usually shorter than the SAM file

    positions = {10: {}, 18: {}}
    count = {10: {}, 18: {}}
    with open(gtf_file, "r") as fp_in:
        for line in fp_in:
            cols = line.split("\t")
            start = int(cols[3])
            end = int(cols[4])
            chr = int(cols[0])
            name = cols[8].split(";")[2].split(" ")[2].replace('"', "")

            positions[chr][name] = (start, end)
            count[chr][name] = 0

    with open(sam_file, "r") as fp_in:
        # No need to remove initial 4 lines since they
        # have already been dropped previously using samtools
        for line in fp_in:
            cols = line.split("\t")
            chr = int(cols[2])
            pos = int(cols[3])

            # Perform linear search
            for name in positions[chr]:
                start, end = positions[chr][name]
                if pos >= start and pos <= end:
                    count[chr][name] += 1
                    break

    print("Read counts for chromosome 10:")
    for key in count[10]:
        print(f"{key}: {count[10][key]}")

    print("Read counts for chromosome 18:")
    for key in count[18]:
        print(f"{key}: {count[18][key]}")


def main():
    if len(sys.argv) != 3:
        raise RuntimeError(
            f"Expected 3 command line arguments, got {len(sys.argv)}"
        )

    # Get input GTF and SAM file names
    fin_gtf = sys.argv[1]
    fin_sam = sys.argv[2]

    # Filter by chromosome number, feature, gene_biotype
    gtf_filter(fin_gtf)

    # Calculate and print raw read counts
    raw_read_count(fin_sam)


if __name__ == "__main__":
    main()
