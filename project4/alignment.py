from collections import namedtuple
Constants = namedtuple('Constants', ['HEAD', 'DIAGONAL', 'UP', 'LEFT'])
const = Constants(HEAD=0, LEFT=1, UP=3, DIAGONAL=2)

def align(
        seq1: str,
        seq2: str,
        match_award=-3,
        indel_penalty=5,
        sub_penalty=1,
        banded_width=-1,
        gap='-'
) -> tuple[float, str | None, str | None]:
    """
        Align seq1 against seq2 using Needleman-Wunsch
        Put seq1 on left (j) and seq2 on top (i)
        => matrix[i][j]
        :param seq1: the first sequence to align; should be on the "left" of the matrix
        :param seq2: the second sequence to align; should be on the "top" of the matrix
        :param match_award: how many points to award a match
        :param indel_penalty: how many points to award a gap in either sequence
        :param sub_penalty: how many points to award a substitution
        :param banded_width: banded_width * 2 + 1 is the width of the banded alignment; -1 indicates full alignment
        :param gap: the character to use to represent gaps in the alignment strings
        :return: alignment cost, alignment 1, alignment 2
    """
    if (banded_width == -1):
        return align_no_band(seq1, seq2, match_award, indel_penalty, sub_penalty, gap)
    else:
        return -9000, None, None
    
def align_no_band(
        seq1: str,
        seq2: str,
        match_award=-3,
        indel_penalty=5,
        sub_penalty=1,
        gap='-'
) -> tuple[float, str | None, str | None]:
    dp_table = populate_matrix(seq1, seq2, match_award, indel_penalty, sub_penalty)

    return extract_alignments(seq1, seq2, dp_table, gap)

def populate_matrix(a: str, b: str, match_award: float, indel_cost: float,
                    sub_cost: float) -> list[list[tuple[float, int]]]:
    
    dp_table = initialize_matrix(len(a),len(b),indel_cost)

    for row in range(1, len(dp_table)):
        for col in range(1, len(dp_table[0])):
            match: bool = a[row - 1] == b[col - 1]
            left_cost: float = dp_table[row][col - 1][0] + indel_cost
            up_cost: float = dp_table[row - 1][col][0] + indel_cost
            diag_cost: float = dp_table[row - 1][col - 1][0]
            diag_cost += match_award if match else sub_cost
            min_cost: float = min(diag_cost, left_cost, up_cost)
            if min_cost == diag_cost:
                dp_table[row][col] = (diag_cost, const.DIAGONAL)
            elif min_cost == left_cost:
                dp_table[row][col] = (left_cost, const.LEFT)
            else:
                dp_table[row][col] = (up_cost, const.UP)

    return dp_table

def extract_alignments(a: str, b: str, dp_table: list[list[tuple[float, int]]],
                       gap: str) -> tuple[float, str | None, str | None]:
    row: int = len(a)
    col: int = len(b)
    alignment_a: str = ""
    alignment_b: str = ""
    cost: float = dp_table[row][col][0]
    direction: int = dp_table[row][col][1]
    while direction != const.HEAD:
        if direction == const.LEFT:
            alignment_a += gap
            alignment_b += b[col - 1]
            col -= 1
        elif direction == const.UP:
            alignment_a += a[row - 1]
            alignment_b += gap
            row -= 1
        elif direction == const.DIAGONAL:
            print(row - 1)
            alignment_a += a[row - 1]
            alignment_b += b[col - 1]
            row -= 1
            col -= 1
        direction = dp_table[row][col][1]
    
    return cost, reverse_str(alignment_a), reverse_str(alignment_b)

def initialize_matrix(len_a: int, len_b: int, indel_cost: float) -> list[list[tuple[float, int]]]:
    dp_table = [[None] * (len_b + 1) for _ in range(len_a + 1)]

    dp_table[0] = [(indel_cost * i, const.LEFT) for i in range(len(dp_table[0]))]

    for i in range(len(dp_table)):
        dp_table[i][0] = (indel_cost * i, const.UP)

    dp_table[0][0] = (0,0)

    return dp_table

def reverse_str(s: str) -> str:
    return s[::-1]

a = "ATGCATGC"
b = "ATGGTGC"
print(populate_matrix(a,b,-3,5,1))