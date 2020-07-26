import sys


# Define constants
class Backtrack:
    DIAGONAL = 1
    HORIZONTAL = 2
    VERTICAL = 3


def diagonal_score(x, y, match_cost, mismatch_cost):
    return match_cost if x == y else mismatch_cost


# Backtrack from bottom right corner to top left
def backtrack(back, nr, nc, read, reference, sim, max_pos):
    read_alignment = []
    reference_alignment = []
    r, c = max_pos

    while sim[r][c] != 0:
        if back[r][c] == Backtrack.DIAGONAL:
            read_alignment.insert(0, read[r])
            reference_alignment.insert(0, reference[c])
            r = r - 1
            c = c - 1
        elif back[r][c] == Backtrack.HORIZONTAL:
            read_alignment.insert(0, "-")
            reference_alignment.insert(0, reference[c])
            c = c - 1
        else:
            read_alignment.insert(0, read[r])
            reference_alignment.insert(0, "-")
            r = r - 1

    return reference_alignment, read_alignment


def similarity(
    sim, back, nr, nc, read, reference, match_cost, mismatch_cost, gap_cost
):
    # Fill first row and column
    for c in range(nc):
        back[0][c] = Backtrack.HORIZONTAL
    for r in range(nr):
        back[r][0] = Backtrack.VERTICAL

    # Perform algorithm and save information for backtrack
    max_score = 0
    max_pos = (0, 0)
    for r in range(1, nr):
        for c in range(1, nc):
            # Save diagonal score to use it later
            score = sim[r - 1][c - 1] + diagonal_score(
                reference[c], read[r], match_cost, mismatch_cost
            )

            sim[r][c] = max(
                0, sim[r - 1][c] + gap_cost, sim[r][c - 1] + gap_cost, score,
            )

            # Update max and corresponding position
            if sim[r][c] > max_score:
                max_score = sim[r][c]
                max_pos = (r, c)

            # Update backtrack data structure
            if sim[r][c] == score:
                back[r][c] = Backtrack.DIAGONAL
            elif sim[r][c] == sim[r][c - 1] + gap_cost:
                back[r][c] = Backtrack.HORIZONTAL
            else:
                back[r][c] = Backtrack.VERTICAL

    return max, max_pos


def local_alignment(reference, read, match_cost, mismatch_cost, gap_cost):
    # Add space at the beginning to align with matrix rows/columns
    # and make indexing easier
    reference = " " + reference
    read = " " + read
    nc, nr = len(reference), len(read)

    # Initialize empty matrix (different from global alignment)
    # and backtrack data structure
    sim = [[0] * nc for r in range(nr)]
    back = [[0] * nc for r in range(nr)]

    # Update similarity matrix
    max, max_pos = similarity(
        sim, back, nr, nc, read, reference, match_cost, mismatch_cost, gap_cost
    )
    print(f"\nGlobal alignment score: {sim[nr - 1][nc - 1]}")
    print("\n".join(["".join(["{:4}".format(c) for c in r]) for r in sim]))

    # Perform backtrack
    read_alignment, reference_alignment = backtrack(
        back, nr, nc, read, reference, sim, max_pos
    )
    print(
        f"\nFinal alignment:\n{''.join(read_alignment)}\n"
        f"{''.join(reference_alignment)}"
    )


def main():
    if len(sys.argv) != 6:
        raise RuntimeError(
            f"Expected 6 command line arguments, got {len(sys.argv)}"
        )

    # Parse command line arguments
    reference = sys.argv[1]
    read = sys.argv[2]
    match_cost = int(sys.argv[3])
    mismatch_cost = int(sys.argv[4])
    gap_cost = int(sys.argv[5])

    # Perform local alignment
    local_alignment(reference, read, match_cost, mismatch_cost, gap_cost)


if __name__ == "__main__":
    main()
