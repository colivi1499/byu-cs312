# Uncomment this line to import some functions that can help
# you debug your algorithm
import sys
from cmath import inf
import copy
LARGE_VALUE = sys.float_info.max
from plotting import draw_line, draw_hull, circle_point, show_plot

class Node:

    def __init__(self, point: tuple[float, float], 
                 cc: 'Node' = None, 
                 cl: 'Node' = None):
        self.point = point
        self.cc = cc if cc is not None else self
        self.cl = cl if cl is not None else self




class Hull:

    def __init__(self,left: Node,right: Node = None):
        self.left_most = left
        self.right_most = right if right is not None else left

    def to_list(self) -> list[tuple[float, float]]:
        hull_list: list[tuple[float, float]] = []
        starting_node: Node = self.left_most
        hull_list.append(starting_node.point)
        next_node: Node = starting_node.cc
        while (next_node.point != starting_node.point):
            hull_list.append(next_node.point)
            next_node = next_node.cc
        return hull_list

# O(n) with n being the number of points in both hulls
def merge_hulls(left_hull: Hull, right_hull: Hull) -> Hull:
    upper_left: Node = left_hull.right_most
    upper_right: Node = right_hull.left_most
    slope = get_slope(upper_left,upper_right)
    middle_slope = slope
    changed = True

    while changed:
        changed = False
        slope_increased = True
        while slope_increased:
            slope_increased = False
            new_slope = get_slope(upper_left,upper_right.cl)
            if slope < new_slope:
                slope = new_slope
                upper_right = upper_right.cl
                slope_increased = True
                changed = True

        slope_decreased = True
        while slope_decreased:
            slope_decreased = False
            new_slope = get_slope(upper_left.cc,upper_right)
            if slope > new_slope:
                slope = new_slope
                upper_left = upper_left.cc
                slope_decreased = True
                changed = True

    lower_left = left_hull.right_most
    lower_right = right_hull.left_most
    slope = middle_slope
    changed = True

    while changed:
        changed = False
        slope_decreased = True
        while slope_decreased:
            slope_decreased = False
            new_slope = get_slope(lower_left,lower_right.cc)
            if slope > new_slope:
                slope = new_slope
                lower_right = lower_right.cc
                slope_decreased = True
                changed = True

        slope_increased = True
        while slope_increased:
            slope_increased = False
            new_slope = get_slope(lower_left.cl,lower_right)
            if slope < new_slope:
                slope = new_slope
                lower_left = lower_left.cl
                slope_increased = True
                changed = True

    upper_left.cl = upper_right
    upper_right.cc = upper_left
    lower_left.cc = lower_right
    lower_right.cl = lower_left



    return Hull(left_hull.left_most,right_hull.right_most)

# O(nlog(n))
def compute_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    points.sort()
    hull: Hull = convex_hull(points)
    return hull.to_list()

# O(nlog(n))
def convex_hull(points: list[tuple[float,float]]) -> Hull:
    if (len(points) == 1):
        return Hull(Node(points[0]))
    left,right = split(points)
    left_hull: Hull = convex_hull(left)
    right_hull: Hull = convex_hull(right)
    
    return merge_hulls(left_hull,right_hull)

# Split a list of points by the median x value
def split(points: list[tuple[float,float]]) -> tuple[list[tuple[float,float]], list[tuple[float,float]]]:
    num_points: int = len(points)
    mid_index: int = num_points // 2

    return points[:mid_index],points[mid_index:]

def get_slope(left: Node, right: Node) -> float:
    x1, y1 = left.point
    x2, y2 = right.point
    if x2 == x1:
        return float(inf)
    return (y2 - y1) / (x2 - x1)

