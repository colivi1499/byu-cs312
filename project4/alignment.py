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
    dp_dict = populate_dict(seq1, seq2, match_award, indel_penalty, sub_penalty, banded_width)

    return extract_alignments_dict(seq1, seq2, dp_dict, gap)

def extract_alignments_dict(a: str, b: str, dp_dict: list[list[tuple[float, int]]], gap: str):
    row: int = len(a)
    col: int = len(b)
    alignment_a = []
    alignment_b = []
    cost: float = dp_dict[row][col][0] 
    
    direction = dp_dict[row][col][1]
    while direction != const.HEAD:
        if direction == const.LEFT:
            alignment_a.append(gap)
            alignment_b.append(b[col - 1])
            col -= 1
        elif direction == const.UP:
            alignment_a.append(a[row - 1])
            alignment_b.append(gap)
            row -= 1
        elif direction == const.DIAGONAL:
            alignment_a.append(a[row - 1])
            alignment_b.append(b[col - 1])
            row -= 1
            col -= 1
        direction = dp_dict[row][col][1]

    str_align_a = reverse_str(''.join(alignment_a))
    str_align_b = reverse_str(''.join(alignment_b))
    return (cost, str_align_a, str_align_b)

def populate_dict(a: str, b: str, match_award: float, indel_cost: float,
                sub_cost: float, banded_width: int):
    if (banded_width == -1):
        banded_width = len(b)
    dp_dict = initialize_dict(a)
    for row in range(len(a) + 1):
        left: int = max(row - banded_width, 0)
        right: int = min(row + banded_width, len(b))
        for col in range(left, right + 1):
            if row != 0 or col!= 0:
                cost, direction = get_cost_and_direction(a, b, row, col, dp_dict, match_award, indel_cost, sub_cost)
                dp_dict[row][col] = (cost, direction)
    return dp_dict

def get_cost_and_direction(a: str, b: str, row: int, col: int, 
                dp_dict: dict[int,dict[int,tuple[float,int]]], match_award: float,
                indel_cost: float, sub_cost: float) -> tuple[float, int]:
    if col - 1 in dp_dict[row]:
        left_cost: float = dp_dict[row][col - 1][0] + indel_cost
    else:
        left_cost: float = float('inf')
    
    if (row - 1 in dp_dict) and (col in dp_dict[row - 1]):
        up_cost: float = dp_dict[row - 1][col][0] + indel_cost
    else:
        up_cost: float = float('inf')

    if (row - 1 in dp_dict) and (col - 1 in dp_dict[row - 1]):
        match: bool = a[row - 1] == b[col - 1]
        diag_cost: float = dp_dict[row - 1][col - 1][0]
        diag_cost += match_award if match else sub_cost
    else:
        diag_cost: float = float('inf')

    min_cost: float = min(diag_cost, left_cost, up_cost)
    if min_cost == diag_cost:
        return (diag_cost, const.DIAGONAL)
    elif min_cost == left_cost:
        return (left_cost, const.LEFT)
    else:
        return (up_cost, const.UP)

def initialize_dict(a: str):
    dp_dict: dict[int,dict[int,tuple[float,int]]] = {}
    for i in range(len(a) + 1):
        dp_dict[i] = {}
    
    dp_dict[0][0] = (0, 0)
    return dp_dict

def reverse_str(s: str) -> str:
    return s[::-1]