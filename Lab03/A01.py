import sys


def snp_filer(fin):
    # equivalent to: grep ",<\*>" sorted.vcf

    with open(fin, "r") as fp_in:
        for line in fp_in:
            line = line.strip()
            if line:
                if ",<*>" in line:
                    print(line)


def indel_filer(fin):
    # equivalent to: grep INDEL sorted.vcf

    with open(fin, "r") as fp_in:
        for line in fp_in:
            line = line.strip()
            if line:
                if "INDEL" in line:
                    print(line)


def main():
    if len(sys.argv) != 2:
        raise RuntimeError(
            f"Expected 2 command line arguments, got {len(sys.argv)}"
        )

    # Get input VCF file name
    fin = sys.argv[1]

    # Filter for Single Nucleotides Polymorphism
    print(f"{'*'*80} SNP {'*'*80}")
    snp_filer(fin)

    # Filter by insertions / deletions
    print(f"\n{'*'*80} INDEL {'*'*80}")
    indel_filer(fin)


if __name__ == "__main__":
    main()
