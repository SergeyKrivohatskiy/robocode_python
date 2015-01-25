#!/usr/bin/env python
__author__ = 'Sergey Krivohatskiy'
import math
import cocos.euclid as eu
import constants
import random


def deg_to_vector(rotation):
    radians_rotation = math.radians(rotation)
    return eu.Vector2(math.cos(radians_rotation), -math.sin(radians_rotation))


def get_rand_positions(w, h, objects_count, object_width):
    object_width += 10
    available_positions = [(i, j) for i in range(0, w // object_width) for j in range(0, h // object_width)]
    positions = []
    for i in range(0, objects_count):
        pos = available_positions[random.randrange(0, len(available_positions))]
        available_positions.remove(pos)
        positions.append((pos[0] * object_width + object_width / 2, pos[1] * object_width + object_width / 2))
    return positions


def check_edge(segment1, segment2, u1u2):
    new_intersection = get_segments_intersection(segment1, segment2)
    if u1u2 is None or (new_intersection is not None and new_intersection[0] < u1u2[0]):
        u1u2 = new_intersection
    return u1u2


def get_segment_rect_intersection(segment, rect):
    rect_center, half_width, half_height = rect
    # square points
    p1 = (rect_center[0] - half_width, rect_center[1] - half_height)
    p2 = (rect_center[0] - half_width, rect_center[1] + half_height)
    p3 = (rect_center[0] + half_width, rect_center[1] + half_height)
    p4 = (rect_center[0] + half_width, rect_center[1] - half_height)

    u1u2 = None
    u1u2 = check_edge(segment, (p1, p2), u1u2)
    u1u2 = check_edge(segment, (p2, p3), u1u2)
    u1u2 = check_edge(segment, (p3, p4), u1u2)
    u1u2 = check_edge(segment, (p4, p1), u1u2)
    return u1u2[0] if u1u2 is not None else None


def get_segments_intersection(segment1, segment2):
    segment1_beg, segment1_end = segment1
    segment2_beg, segment2_end = segment2
    divisor = (segment2_end[1] - segment2_beg[1]) * (segment1_end[0] - segment1_beg[0]) - \
              (segment2_end[0] - segment2_beg[0]) * (segment1_end[1] - segment1_beg[1])
    if divisor == 0:
        # parallel segments
        return None
    u1 = (segment2_end[0] - segment2_beg[0]) * (segment1_beg[1] - segment2_beg[1]) - \
         (segment2_end[1] - segment2_beg[1]) * (segment1_beg[0] - segment2_beg[0])
    u1 /= divisor
    if u1 >= 1 or u1 <= 0:
        # intersection is out of segment 1
        return None
    u2 = (segment1_end[0] - segment1_beg[0]) * (segment1_beg[1] - segment2_beg[1]) - \
         (segment1_end[1] - segment1_beg[1]) * (segment1_beg[0] - segment2_beg[0])
    u2 /= divisor
    if u2 >= 1 or u2 <= 0:
        # intersection is out of segment 2
        return None
    return u1, u2


def check_if_square_is_out_of_window(point, half_width):
    window_width = constants.window_width
    window_height = constants.window_height
    return (window_width - half_width <= point[0]) or (half_width >= point[0]) or \
           (window_height - half_width <= point[1]) or (half_width >= point[1])


def check_if_point_in_rect(point, rect):
    rect_center, half_width, half_height = rect
    return (rect_center[0] - half_width <= point[0]) and (rect_center[0] + half_width >= point[0]) and \
           (rect_center[1] - half_height <= point[1]) and (rect_center[1] + half_height >= point[1])
