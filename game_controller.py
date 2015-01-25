#!/usr/bin/env python
import math

__author__ = 'Sergey Krivohatskiy'
import cocos
from constants import consts
import time
import cocos.euclid as eu
import random
from robot import *
from bullet import *

class GameController(cocos.layer.Layer):
    tic_time = 0.02

    # robots_list is a list of Robot class subclasses
    def __init__(self, robots_list):
        super(GameController, self).__init__()
        self.w = consts["window"]["width"]
        self.h = consts["window"]["height"]
        positions = get_rand_positions(self.w, self.h, len(robots_list), 2 * consts["robot"]["half_width"])
        self.robots = [robots_list[i](self, positions[i]) for i in range(0, len(robots_list))]
        self.bullets = []
        for robot in self.robots:
            self.add(robot, z=1)
        self.time = 0
        self.do(cocos.actions.Repeat(self.update))

    @cocos.actions.CallFuncS
    def update(self):
        start = time.time()

        self.prepare_commands()
        self.time += 1
        self.process_bullets()
        self.process_robots()
        self.make_scan()
        self.process_events()

        to_sleep = GameController.tic_time + start - time.time()
        time.sleep(to_sleep if to_sleep > 0 else 0)

    def prepare_commands(self):
        for robot in self.robots:
            robot.prepare_command()
            assert robot.has_command()

    def check_bullets_intersection(self, bullet_old_pos_new_pos):
        removed = [False for _ in bullet_old_pos_new_pos]
        for i in range(0, len(bullet_old_pos_new_pos)):
            bullet_step1 = bullet_old_pos_new_pos[i]
            for j in range(i + 1, len(bullet_old_pos_new_pos)):
                bullet_step2 = bullet_old_pos_new_pos[j]
                u1u2 = get_segments_intersection(bullet_step1[1], bullet_step1[2], bullet_step2[1], bullet_step2[2])
                if u1u2 is not None:
                    removed[i] = removed[j] = True
        new_bullet_old_pos_new_pos = []
        for i in range(0, len(bullet_old_pos_new_pos)):
            if removed[i]:
                self.remove_bullet(bullet_old_pos_new_pos[i][0])
            else:
                new_bullet_old_pos_new_pos.append(bullet_old_pos_new_pos[i])
        return new_bullet_old_pos_new_pos

    def remove_bullet(self, bullet):
        self.bullets.remove(bullet)
        self.remove(bullet)

    def check_bullets_robots_intersection(self, bullet_old_pos_new_pos):
        new_bullet_old_pos_new_pos = []
        for bullet, old_pos, new_pos in bullet_old_pos_new_pos:
            removed = False
            for robot in self.robots:
                if bullet.owner == robot:
                    # cant do suicide
                    continue
                u1 = get_segment_rect_intersection(old_pos, new_pos, robot.position, consts["robot"]["half_width"],
                                                   consts["robot"]["half_width"])
                if u1 is None:
                    continue
                removed = True
                # TODO event
                robot.energy -= bullet.robot_damage
                bullet.owner.energy += bullet.energy_and_points_boost
                bullet.owner.points += bullet.energy_and_points_boost
                break
            if removed:
                self.remove_bullet(bullet)
            else:
                new_bullet_old_pos_new_pos.append((bullet, old_pos, new_pos))
        return new_bullet_old_pos_new_pos

    def check_bullets_out_of_window(self, bullet_old_pos_new_pos):
        new_bullet_old_pos_new_pos = []
        for bullet, old_pos, new_pos in bullet_old_pos_new_pos:
            if check_if_square_is_out_of_window(new_pos, 0):
                self.remove_bullet(bullet)
            else:
                new_bullet_old_pos_new_pos.append((bullet, old_pos, new_pos))
        return new_bullet_old_pos_new_pos

    def process_bullets(self):
        for robot in self.robots:
            if robot.gun.heat > 0:
                robot.gun.heat = max(0, robot.gun.heat - consts["robot"]["gun_cooling"])
            if not robot.has_command():
                continue
            command = robot.pop_command()
            if not isinstance(command, Fire):
                robot.push_command(command)
                continue
            new_bullet = Bullet(robot.position, command.power, robot.get_gun_heading(), robot)
            self.add(new_bullet, z=2)
            self.bullets.append(new_bullet)

        bullet_old_pos_new_pos = [
            (bullet, bullet.position, bullet.position + bullet.velocity * deg_to_vector(bullet.rotation)) for bullet in
            self.bullets]
        bullet_old_pos_new_pos = self.check_bullets_intersection(bullet_old_pos_new_pos)
        bullet_old_pos_new_pos = self.check_bullets_robots_intersection(bullet_old_pos_new_pos)
        bullet_old_pos_new_pos = self.check_bullets_out_of_window(bullet_old_pos_new_pos)
        for bullet, _, new_pos in bullet_old_pos_new_pos:
            bullet.position = new_pos

    def process_turn_command(self, command, robot):
        if isinstance(command, TurnGun):
            deg = self.get_rotation_deg(command, consts["robot"]["max_gun_turn"], robot)
            robot.gun.rotation = (deg + robot.gun.rotation) % 360
            return
        if isinstance(command, TurnBody):
            max_turn = consts["robot"]["max_idle_body_turn"] - consts["robot"]["velocity_body_turn_coefficient"] * \
                                                               abs(robot.velocity)
            deg = self.get_rotation_deg(command, max_turn if max_turn > 0 else 0, robot)
            robot.rotation = (deg + robot.rotation) % 360
            return
        if isinstance(command, TurnRadar):
            deg = self.get_rotation_deg(command, consts["robot"]["max_radar_turn"], robot)
            robot.gun.radar.rotation = (deg + robot.gun.radar.rotation) % 360
            return

    def process_move(self, command, robot):
        # TODO acceleration
        s = command.distance
        max_velocity = consts["robot"]["max_velocity"]
        if abs(s) > max_velocity:
            s = math.copysign(max_velocity, s)
        command.distance -= s
        if command.distance != 0:
            robot.push_command(command)
        robot.velocity = s


    def process_robots(self):
        # process commands
        for robot in self.robots:
            if not robot.has_command():
                continue
            command = robot.pop_command()
            if isinstance(command, DoNothing):
                continue
            if isinstance(command, Turn):
                self.process_turn_command(command, robot)
                continue
            if isinstance(command, Move):
                self.process_move(command, robot)
            else:
                robot.acceleration = -robot.velocity


        # move robots
        for robot in self.robots:
            robot.velocity += robot.acceleration
            if abs(robot.velocity) > consts["robot"]["max_velocity"]:
                robot.velocity = math.copysign(consts["robot"]["max_velocity"], robot.velocity)
            if robot.velocity == 0:
                continue
            old_pos = robot.position
            new_pos = robot.position + robot.velocity * deg_to_vector(robot.rotation)
            # first intersect with borders
            half_window_width = consts["window"]["width"] / 2
            half_window_height = consts["window"]["height"] / 2
            # Minkowski addition
            half_width = half_window_width - consts["robot"]["half_width"]
            half_height = half_window_height - consts["robot"]["half_width"]
            center = (half_window_width, half_window_height)
            u1 = None
            if check_if_point_in_rect(old_pos, center, half_width, half_height) != check_if_point_in_rect(new_pos,
                                                                                                          center,
                                                                                                          half_width,
                                                                                                          half_height):
                u1 = get_segment_rect_intersection(old_pos, new_pos, center,
                                                   half_width, half_height)
            where_min = None
            for second_robot in self.robots:
                if second_robot == robot:
                    continue
                new_u1 = get_segment_rect_intersection(old_pos, new_pos, second_robot.position,
                                                       2 * consts["robot"]["half_width"],
                                                       2 * consts["robot"]["half_width"])
                if u1 is None or (new_u1 is not None and new_u1 < u1):
                    u1 = new_u1
                    where_min = second_robot

            if u1 is None:
                robot.position = new_pos
                continue

            # u1 is a time of the first intersection (from 0 to 1)
            u1 = u1 * 9 / 10
            dx = u1 * (new_pos[0] - old_pos[0])
            dy = u1 * (new_pos[1] - old_pos[1])
            new_pos[0] = old_pos[0] + (dx if dx > 1 else 0)
            new_pos[1] = old_pos[1] + (dy if dy > 1 else 0)
            robot.position = new_pos
            if where_min is None:
                robot.energy -= min(0, abs(robot.velocity) * 0.5 - 1)
                # TODO event
            else:
                robot.energy -= 0.6
                where_min.energy -= 0.6
                # TODO events
            robot.acceleration = robot.velocity = 0


    def make_scan(self):
        pass

    def process_events(self):
        pass

    @staticmethod
    def get_rotation_deg(command, max_turn, robot):
        deg = command.deg
        if abs(deg) > max_turn:
            deg = math.copysign(max_turn, deg)
        command.deg -= deg
        if command.deg != 0:
            robot.push_command(command)
        return deg





def get_rand_positions(w, h, count, width):
    width += 10
    available_positions = [(i, j) for i in range(0, w // width) for j in range(0, h // width)]
    positions = []
    for i in range(0, count):
        pos = available_positions[random.randrange(0, len(available_positions))]
        available_positions.remove(pos)
        positions.append((pos[0] * width + width / 2, pos[1] * width + width / 2))
    return positions


def deg_to_vector(rotation):
    radians_rotation = math.radians(rotation)
    return eu.Vector2(math.cos(radians_rotation), -math.sin(radians_rotation))


def check_edge(p1, p2, segment_beg, segment_end, u1u2):
    new_intersection = get_segments_intersection(segment_beg, segment_end, p1, p2)
    if u1u2 is None or (new_intersection is not None and new_intersection[0] < u1u2[0]):
        u1u2 = new_intersection
    return u1u2


def get_segment_rect_intersection(segment_beg, segment_end, square_center,
                                  half_width, half_height):
    # square points
    p1 = (square_center[0] - half_width, square_center[1] - half_height)
    p2 = (square_center[0] - half_width, square_center[1] + half_height)
    p3 = (square_center[0] + half_width, square_center[1] + half_height)
    p4 = (square_center[0] + half_width, square_center[1] - half_height)

    u1u2 = None
    u1u2 = check_edge(p1, p2, segment_beg, segment_end, u1u2)
    u1u2 = check_edge(p2, p3, segment_beg, segment_end, u1u2)
    u1u2 = check_edge(p3, p4, segment_beg, segment_end, u1u2)
    u1u2 = check_edge(p4, p1, segment_beg, segment_end, u1u2)
    return u1u2[0] if u1u2 is not None else None


def get_segments_intersection(segment1_beg, segment1_end, segment2_beg, segment2_end):
    divisor = (segment2_end[1] - segment2_beg[1]) * (segment1_end[0] - segment1_beg[0]) - \
              (segment2_end[0] - segment2_beg[0]) * (segment1_end[1] - segment1_beg[1])
    if divisor == 0:
        # parallel segments
        return None
    u1 = (segment2_end[0] - segment2_beg[0]) * (segment1_beg[1] - segment2_beg[1]) - \
         (segment2_end[1] - segment2_beg[1]) * (segment1_beg[0] - segment2_beg[0])
    u1 /= divisor
    intersection_delta = consts["world"]["intersection_delta"]
    if u1 >= 1 - intersection_delta or u1 <= intersection_delta:
        # intersection is out of segment 1
        return None
    u2 = (segment1_end[0] - segment1_beg[0]) * (segment1_beg[1] - segment2_beg[1]) - \
         (segment1_end[1] - segment1_beg[1]) * (segment1_beg[0] - segment2_beg[0])
    u2 /= divisor
    if u2 >= 1 - intersection_delta or u2 <= intersection_delta:
        # intersection is out of segment 2
        return None
    return u1, u2


def check_if_square_is_out_of_window(point, half_width):
    window_width = consts["window"]["width"]
    window_height = consts["window"]["height"]
    return (window_width - half_width <= point[0]) or (half_width >= point[0]) or \
           (window_height - half_width <= point[1]) or (half_width >= point[1])


def check_if_point_in_rect(point, square_center, half_width, half_height):
    return (square_center[0] - half_width <= point[0]) and (square_center[0] + half_width >= point[0]) and \
           (square_center[1] - half_height <= point[1]) and (square_center[1] + half_height >= point[1])
