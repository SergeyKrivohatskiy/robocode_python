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


def get_rand_position(w, h):
    return eu.Vector2(random.randrange(w), random.randrange(h))


def deg_to_vector(rotation):
    radians_rotation = math.radians(rotation)
    return eu.Vector2(math.cos(radians_rotation), -math.sin(radians_rotation))


class GameController(cocos.layer.Layer):
    tic_time = 0.1
    # robots_list is a list of Robot class subclasses
    def __init__(self, robots_list):
        super(GameController, self).__init__()
        self.w = consts["window"]["width"]
        self.h = consts["window"]["height"]
        self.robots = [robot_class(self, get_rand_position(self.w, self.h)) for robot_class in robots_list]
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

        print(self.time)
        to_sleep = GameController.tic_time + start - time.time()
        time.sleep(to_sleep if to_sleep > 0 else 0)

    def prepare_commands(self):
        for robot in self.robots:
            robot.prepare_command()
            assert robot.has_command()

    def process_bullets(self):
        for robot in self.robots:
            if not robot.has_command():
                continue
            command = robot.pop_command()
            if not isinstance(command, Fire):
                robot.push_command(command)
                continue
            new_bullet = Bullet(robot.position, command.power, robot.get_gun_heading(), robot)
            self.add(new_bullet, z=2)
            self.bullets.append(new_bullet)

        for bullet in self.bullets:
            old_pos = bullet.position
            bullet.position += bullet.velocity * deg_to_vector(bullet.rotation)
            # TODO collisions
            if self.check_if_square_is_out_of_window(bullet.position, consts["bullet"]["half_width"]):
                self.bullets.remove(bullet)
                self.remove(bullet)
            pass

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

    def process_robots(self):
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
                max_vel = consts["robot"]["max_velocity"]
                distance = command.distance
                if abs(distance) > max_vel:
                    distance = math.copysign(max_vel, distance)
                command.distance -= distance
                if command.distance != 0:
                    robot.push_command(command)
                robot.position += distance * deg_to_vector(robot.rotation)
                continue
            # push command back if do not know how to process it
            robot.push_command(command)

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

    @staticmethod
    def check_if_square_is_out_of_window(point, half_width):
        window_width = consts["window"]["width"]
        window_height = consts["window"]["height"]
        return (window_width - half_width <= point[0]) or (half_width >= point[0]) or \
                (window_height - half_width <= point[1]) or (half_width >= point[1])