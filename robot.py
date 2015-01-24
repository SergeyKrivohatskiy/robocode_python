#!/usr/bin/env python
__author__ = 'Sergey Krivohatskiy'
import threading
import pyglet
import cocos
from constants import consts
import cocos.euclid as eu
from gun import Gun


class DoNothing(object):
    pass


class Fire(object):
    pass


class TurnGun(object):
    def __init__(self, deg):
        self.deg = deg


class TurnBody(object):
    def __init__(self, deg):
        self.deg = deg


class TurnRadar(object):
    def __init__(self, deg):
        self.deg = deg


class Robot(cocos.sprite.Sprite):

    def __init__(self, game_controller, position):
        self.robot_consts = consts["robot"]
        super(Robot, self).__init__(pyglet.resource.image(self.robot_consts["resources"]["body"]), position)
        self.controller = game_controller
        self.position = position
        self.velocity = eu.Vector2(0, 0)
        self.acceleration = eu.Vector2(0, 0)
        self.gun = Gun()
        self.add(self.gun)
        self.rotation = 0

        self.new_command_event = threading.Event()
        self.get_command_event = threading.Event()
        self.new_command_event.clear()
        self.get_command_event.clear()
        self.commands = []
        self.run_thread = threading.Thread(target=self.run)
        self.run_thread.start()
        self.new_command_event.wait()
        self.new_command_event.clear()

    def run(self):
        pass

    def prepare_command(self):
        if len(self.commands) != 0:
            print(self.commands)
            return
        self.get_command_event.set()
        self.new_command_event.wait()
        self.new_command_event.clear()
        print(self.commands)

    def has_command(self):
        return len(self.commands) != 0

    def pop_command(self):
        return self.commands.pop()

    def push_command(self, command):
        self.commands.append(command)

    def on_command(self):
        self.new_command_event.set()
        self.get_command_event.wait()
        self.get_command_event.clear()

    def do_nothing(self):
        self.push_command(DoNothing())
        self.on_command()

    def turn_gun_right(self, deg):
        self.push_command(TurnGun(deg))
        self.on_command()

    def turn_gun_left(self, deg):
        self.push_command(TurnGun(-deg))
        self.on_command()

    def turn_radar_right(self, deg):
        self.push_command(TurnRadar(deg))
        self.on_command()

    def turn_radar_left(self, deg):
        self.push_command(TurnRadar(-deg))
        self.on_command()

    def turn_right(self, deg):
        self.push_command(TurnBody(deg))
        self.on_command()

    def turn_left(self, deg):
        self.push_command(TurnBody(-deg))
        self.on_command()

    def turn_right(self, deg):
        self.push_command(TurnBody(deg))
        self.on_command()

    def turn_left(self, deg):
        self.push_command(TurnBody(-deg))
        self.on_command()