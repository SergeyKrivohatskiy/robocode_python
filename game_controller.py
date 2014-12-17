#!/usr/bin/env python
__author__ = 'Sergey Krivohatskiy'
from robot import Robot
import cocos
import robot_commands
import time


class NoRobotsException(BaseException):
    pass


class GameController(cocos.scene.Scene):
    tic_time = 0.1
    # robots_list is a list of Robot class subclasses
    def __init__(self, robots_list):
        super(GameController, self).__init__()
        robots_list = filter(lambda x: issubclass(x, Robot), robots_list)
        if len(robots_list) == 0:
            raise NoRobotsException()
        self.time = 0
        self.bullets = []
        self.robots = map(lambda robot_class: robot_class(self, (200, 200)), robots_list)
        for robot in self.robots:
            self.add(robot)
        for bullet in self.bullets:
            self.add(bullet)
        self.do(cocos.actions.Repeat(self.update))


    @cocos.actions.CallFuncS
    def update(self):
        # dt is ignored for a while
        start = time.time()

        self.time += 1
        for robot in self.robots:
            robot.update()

        for robot in self.robots:
            robot.exec_next_command()

        time.sleep(GameController.tic_time + start - time.time())

    def move_bullets(self, commands):
        fire_commands = filter(lambda t: isinstance(t[1], robot_commands.Fire), commands)
        for fire_command in fire_commands:
            pass

        events = []
        for bullet in self.bullets:
            pass
        return events

    def move_robots(self, commands):
        events = []
        turn_commands = filter(lambda t: isinstance(t[1], robot_commands.Turn), commands)
        move_commands = filter(lambda t: isinstance(t[1], robot_commands.Move), commands)
        return events

    def process_events(self, bullet_events, robot_move_events):
        pass