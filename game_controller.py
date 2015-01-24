#!/usr/bin/env python
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
    tic_time = 0.1
    # robots_list is a list of Robot class subclasses
    def __init__(self, robots_list):
        super(GameController, self).__init__()
        self.w = consts["window"]["width"]
        self.h = consts["window"]["height"]
        self.robots = [robot_class(self, get_rand_position(self.w, self.h)) for robot_class in robots_list]
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

        # TODO process bullets

    def process_robots(self):
        for robot in self.robots:
            if not robot.has_command():
                continue
            command = robot.pop_command()
            if isinstance(command, DoNothing):
                continue
            if isinstance(command, TurnGun):
                robot.gun.rotation += command.deg
                continue
            if isinstance(command, TurnBody):
                robot.rotation += command.deg
                continue
            if isinstance(command, TurnRadar):
                robot.gun.radar.rotation += command.deg
                continue
            # TODO process other commands
            robot.push_command(command)

    def make_scan(self):
        pass

    def process_events(self):
        pass