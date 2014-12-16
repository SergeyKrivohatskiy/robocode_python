#!/usr/bin/env python
__author__ = 'Sergey Krivohatskiy'
from robot import Robot
import cocos
import robot_commands


class NoRobotsException(BaseException):
    pass


class GameController(cocos.scene.Scene):
    # robots_list is a list of Robot class subclasses
    def __init__(self, robots_list):
        super(GameController, self).__init__()
        robots_list = filter(lambda x: issubclass(x, Robot), robots_list)
        if len(robots_list) == 0:
            raise NoRobotsException()
        self.time = 0
        self.bullets = []
        self.robots = map(lambda robot_class: robot_class(self, (0, 0)), robots_list)
        for robot in self.robots:
            self.add(robot)
        for bullet in self.bullets:
            self.add(bullet)
        self.schedule(self.update)

    def update(self, dt):
        # dt is ignored for a while
        commands = self.get_robots_commands()
        self.time += 1
        bullet_events = self.move_bullets(commands)
        robot_move_events = self.move_robots(commands)
        self.process_events(bullet_events, robot_move_events)

    def get_robots_commands(self):
        all_commands = [(robot, robot.get_next_command()) for robot in self.robots]
        return all_commands

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
        for t in move_commands:
            t[0].position = (t[0].position[0] + t[1].distance, t[0].position[1])
        return events

    def process_events(self, bullet_events, robot_move_events):
        pass