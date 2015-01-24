#!/usr/bin/env python
import math

__author__ = 'Sergey Krivohatskiy'
import cocos
import time
import cocos.euclid as eu
from constants import consts
import random
from robot import *


def get_rand_position(w, h):
    return eu.Vector2(random.randrange(w), random.randrange(h))


class GameController(cocos.layer.Layer):
    tic_time = 1
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
            fire = command
            # TODO execute fire command

        for bullet in self.bullets:
            # TODO process bullets
            pass

    def get_rotation_deg(self, command, max_turn, robot):
        deg = command.deg
        if abs(deg) > max_turn:
            deg = math.copysign(max_turn, deg)
        command.deg -= deg
        if command.deg != 0:
            robot.push_command(command)
        return deg

    def process_robots(self):
        for robot in self.robots:
            if not robot.has_command():
                continue
            command = robot.pop_command()
            if isinstance(command, DoNothing):
                continue
            if isinstance(command, TurnGun):
                deg = self.get_rotation_deg(command, consts["robot"]["max_gun_turn"], robot)
                robot.gun.rotation += deg
                continue
            if isinstance(command, TurnBody):
                max_turn = consts["robot"]["max_idle_body_turn"] - consts["robot"]["velocity_body_turn_coefficient"] *\
                                                                   abs(robot.velocity)
                deg = self.get_rotation_deg(command, max_turn if max_turn > 0 else 0, robot)
                robot.rotation += deg
                continue
            if isinstance(command, TurnRadar):
                deg = self.get_rotation_deg(command, consts["robot"]["max_radar_turn"], robot)
                robot.gun.radar.rotation += deg
                continue
            # TODO process other commands
            robot.push_command(command)

    def make_scan(self):
        pass

    def process_events(self):
        pass