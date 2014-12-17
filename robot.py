#!/usr/bin/env python
__author__ = 'Sergey Krivohatskiy'
import threading
import robot_commands
import pyglet
from game_object import GameObject


class Robot(GameObject):
    def __init__(self, game_controller, position):
        super(Robot, self).__init__(pyglet.resource.image('robot.png'), position)
        self.max_speed = 8
        self.controller = game_controller
        self.new_command_event = threading.Event()
        self.get_command_event = threading.Event()
        self.command = None
        self.run_thread = threading.Thread(target=self.run)
        self.run_thread.start()

    def exec_next_command(self):
        self.new_command_event.wait()
        self.new_command_event.clear()
        self.get_command_event.set()

    def get_x(self):
        return self.position[0]

    def get_y(self):
        return self.position[1]

    def run(self):
        pass

    def turn_gun_right(self, deg):
        self.command = robot_commands.Turn('gun', deg)
        self.on_command()

    def fire(self, power):
        self.command = robot_commands.Fire()
        self.on_command()

    def set_vel(self, vel):
        self.vel = vel
        self.on_command()

    def set_rot_speed(self, speed):
        self.rot_speed = speed
        self.on_command()

    def on_command(self):
        self.new_command_event.set()
        self.get_command_event.wait()
        self.get_command_event.clear()

    def do_nothing(self):
        self.on_command()

    def get_battle_field_width(self):
        pass

    def get_battle_field_height(self):
        pass

    def get_energy(self):
        pass