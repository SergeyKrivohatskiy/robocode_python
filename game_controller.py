#!/usr/bin/env python
from utils import get_segment_rect_intersection, check_if_point_in_rect, check_if_square_is_out_of_window, \
    get_segments_intersection, get_rand_positions

__author__ = 'Sergey Krivohatskiy'
import cocos
import time
import math
from robot import HitByBullet, Fire, TurnGun, TurnBody, TurnRadar, DoNothing, Move, ScannedRobot
from bullet import Bullet
from itertools import combinations, chain
import constants


class GameController(cocos.layer.Layer):
    tic_time = 0.04

    # robots_list is a list of Robot class subclasses
    def __init__(self, robots_list):
        super(GameController, self).__init__()
        self.w = constants.window_width
        self.h = constants.window_height
        positions = get_rand_positions(self.w, self.h, len(robots_list), 2 * constants.robot_half_width)
        self.robots = [robot_class(self, positions[i]) for i, robot_class in enumerate(robots_list)]
        self.bullets = []
        self.status_labels = {}
        for robot in self.robots:
            self.add(robot, z=1)
            self.status_labels[robot] = cocos.text.Label("")
            self.add(self.status_labels[robot], z=3)
        self.time = 0
        self.robot_events = {}
        self.command_handlers = {TurnGun: self.turn_gun_handler,
                                 TurnRadar: self.turn_radar_handler,
                                 TurnBody: self.turn_body_handler,
                                 DoNothing: self.do_nothing_handler,
                                 Move: self.move_handler}
        self.do(cocos.actions.Repeat(self.update))

    @cocos.actions.CallFuncS
    def update(self):
        start = time.time()

        self.prepare_commands()
        self.time += 1
        self.process_bullets()
        self.process_robot_commands()
        self.move_robots()
        self.make_scan()
        self.process_events()
        self.robot_events = {}
        for robot in self.robots:
            label = self.status_labels[robot]
            label.position = (robot.position[0], robot.position[1] - constants.robot_half_width - 10)
            label.element.document.text = "Energy %.0f, Score %.0f" % (robot.energy, robot.points)

        to_sleep = GameController.tic_time + start - time.time()
        time.sleep(to_sleep if to_sleep > 0 else 0)

    def prepare_commands(self):
        for robot in self.robots:
            robot.prepare_command()
            assert robot.has_command()

    def check_bullets_intersection(self, bullet_steps):
        removed = [False for _ in bullet_steps]
        for i, j in combinations(range(0, len(bullet_steps)), 2):
            u1u2 = get_segments_intersection(bullet_steps[i][1], bullet_steps[j][1])
            if u1u2 is not None:
                removed[i] = removed[j] = True
        new_bullet_steps = []
        for i, bullet_step in enumerate(bullet_steps):
            if removed[i]:
                self.remove_bullet(bullet_step[0])
            else:
                new_bullet_steps.append(bullet_step)
        return new_bullet_steps

    def remove_bullet(self, bullet):
        self.bullets.remove(bullet)
        self.remove(bullet)

    def check_bullets_robots_intersection(self, bullet_steps):
        new_bullet_steps = []
        for bullet, bullet_move_segment in bullet_steps:
            removed = False
            for robot in self.robots:
                if bullet.owner == robot:
                    # cant do suicide
                    continue
                robot_rect = (robot.position, constants.robot_half_width, constants.robot_half_width)
                u1 = get_segment_rect_intersection(bullet_move_segment, robot_rect)
                if u1 is None:
                    continue
                removed = True
                self.robot_events[robot] = HitByBullet(robot, bullet)
                robot.energy -= bullet.robot_damage
                bullet.owner.energy += bullet.energy_and_points_boost
                bullet.owner.points += bullet.energy_and_points_boost
                break
            if removed:
                self.remove_bullet(bullet)
            else:
                new_bullet_steps.append((bullet, bullet_move_segment))
        return new_bullet_steps

    def check_bullets_out_of_window(self, bullet_steps):
        new_bullet_steps = []
        for bullet, bullet_move_segment in bullet_steps:
            if check_if_square_is_out_of_window(bullet_move_segment[1], 0):
                self.remove_bullet(bullet)
            else:
                new_bullet_steps.append((bullet, bullet_move_segment))
        return new_bullet_steps

    def process_bullets(self):
        for robot in self.robots:
            if robot.gun.heat > 0:
                robot.gun.heat = max(0, robot.gun.heat - constants.robot_gun_cooling)
            if not robot.has_command():
                continue
            command = robot.pop_command()
            if not isinstance(command, Fire):
                robot.push_command(command)
                continue
            new_bullet = Bullet(robot.position, command.power, robot.get_gun_heading(), robot)
            self.add(new_bullet, z=2)
            self.bullets.append(new_bullet)

        bullet_steps = [
            (bullet, bullet.get_move_segment()) for bullet
            in
            self.bullets]
        bullet_steps = self.check_bullets_intersection(bullet_steps)
        bullet_steps = self.check_bullets_robots_intersection(bullet_steps)
        bullet_steps = self.check_bullets_out_of_window(bullet_steps)
        for bullet, bullet_move_segment in bullet_steps:
            bullet.position = bullet_move_segment[1]

    def do_nothing_handler(self, _, __):
        pass

    def turn_gun_handler(self, command, robot):
        deg = self.get_rotation_deg(command, constants.robot_max_gun_turn, robot)
        robot.gun.rotation = (deg + robot.gun.rotation) % 360

    def turn_body_handler(self, command, robot):
        max_turn = constants.robot_max_idle_body_turn - constants.robot_velocity_body_turn_coefficient * abs(
            robot.velocity)
        deg = self.get_rotation_deg(command, max_turn if max_turn > 0 else 0, robot)
        robot.rotation = (deg + robot.rotation) % 360

    def turn_radar_handler(self, command, robot):
        deg = self.get_rotation_deg(command, constants.robot_max_radar_turn, robot)
        robot.gun.radar.rotation = (deg + robot.gun.radar.rotation) % 360

    def move_handler(self, command, robot):
        # TODO acceleration
        s = command.distance
        max_velocity = constants.robot_max_velocity
        if abs(s) > max_velocity:
            s = math.copysign(max_velocity, s)
        command.distance -= s
        if command.distance != 0:
            robot.push_command(command)
        robot.velocity = s

    def get_segment_border_intersection(self, segment):
        half_window_width = constants.window_width / 2
        half_window_height = constants.window_height / 2
        # Minkowski addition
        half_width = half_window_width - constants.robot_half_width
        half_height = half_window_height - constants.robot_half_width
        center = (half_window_width, half_window_height)
        window_rect = (center, half_width, half_height)
        u1 = None
        if check_if_point_in_rect(segment[1], window_rect) != check_if_point_in_rect(segment[0], window_rect):
            u1 = get_segment_rect_intersection(segment, window_rect)
        return u1

    def process_robot_commands(self):
        for robot in self.robots:
            robot.acceleration = robot.velocity = 0
            if not robot.has_command():
                continue
            command = robot.pop_command()
            self.command_handlers[type(command)](command, robot)

    def move_robots(self):
        for robot in self.robots:
            if abs(robot.velocity) > constants.robot_max_velocity:
                robot.velocity = math.copysign(constants.robot_max_velocity, robot.velocity)
            if robot.velocity == 0:
                continue
            robot_move_segment = robot.get_move_segment()
            # first intersect with borders
            border_intersections = [(self.get_segment_border_intersection(robot_move_segment), None)]

            def rect(second_robot):
                return second_robot.position, 2 * constants.robot_half_width, 2 * constants.robot_half_width

            robot_intersections = [(get_segment_rect_intersection(robot_move_segment, rect(second_robot)), second_robot)
                                   for second_robot in self.robots if second_robot != robot]
            all_intersections = [x for x in chain(border_intersections, robot_intersections) if x[0] is not None]
            if all_intersections:
                u1, where_min = min(all_intersections)
            else:
                robot.position = robot_move_segment[1]
                continue

            u1 = u1 * 9 / 10
            dx = u1 * (robot_move_segment[1][0] - robot_move_segment[1][0])
            dy = u1 * (robot_move_segment[1][1] - robot_move_segment[1][1])
            new_x = robot_move_segment[0][0] + (dx if dx > 1 else 0)
            new_y = robot_move_segment[0][1] + (dy if dy > 1 else 0)
            robot.position = (new_x, new_y)
            if where_min is None:
                robot.energy -= min(0, abs(robot.velocity) * 0.5 - 1)
                # TODO event
            else:
                robot.energy -= 0.6
                where_min.energy -= 0.6
                # TODO events

    def make_scan(self):
        for robot in self.robots:
            radar_segment = robot.get_radar_segment()

            def rect(second_robot):
                return second_robot.position, constants.robot_half_width, constants.robot_half_width

            robot_intersections = [(get_segment_rect_intersection(radar_segment, rect(second_robot)), second_robot) for
                                   second_robot in self.robots if second_robot != robot]
            all_intersections = [x for x in robot_intersections if x[0] is not None]
            if all_intersections:
                u1, where_min = min(all_intersections)
                self.robot_events[robot] = ScannedRobot(robot, where_min)

    def process_events(self):
        for robot in self.robot_events:
            robot.set_event(self.robot_events[robot])

    @staticmethod
    def get_rotation_deg(command, max_turn, robot):
        deg = command.deg
        if abs(deg) > max_turn:
            deg = math.copysign(max_turn, deg)
        command.deg -= deg
        if command.deg != 0:
            robot.push_command(command)
        return deg