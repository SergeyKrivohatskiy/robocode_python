#!/usr/bin/env python
__author__ = 'Sergey Krivohatskiy'
import threading
import pyglet
import cocos
from constants import consts
from gun import Gun


class DoNothing(object):
    pass


class Fire(object):
    def __init__(self, power):
        self.power = power


class Turn(object):
    def __init__(self, deg):
        self.deg = deg


class TurnGun(Turn):
    def __repr__(self):
        return 'Turn gun %d deg' % self.deg


class TurnBody(Turn):
    def __repr__(self):
        return 'Turn body %d deg' % self.deg


class TurnRadar(Turn):
    def __repr__(self):
        return 'Turn radar %d deg' % self.deg


class Move(object):
    def __init__(self, distance):
        self.distance = distance

    def __repr__(self):
        return 'Move %d distance' % self.distance


class ScannedRobot(object):
    pass


class HitByBullet(object):
    def __init__(self, robot, bullet):
        self.bearing = (180 + bullet.rotation) - robot.rotation

    def get_bearing(self):
        return self.bearing


class Robot(cocos.sprite.Sprite):

    def __init__(self, game_controller, position):
        self.robot_consts = consts["robot"]
        super(Robot, self).__init__(pyglet.resource.image(self.robot_consts["resources"]["body"]), position)
        self.controller = game_controller
        self.position = position
        self.velocity = 0
        self.acceleration = 0
        self.gun = Gun()
        self.add(self.gun)
        self.rotation = 0
        self.energy = self.robot_consts["initial_energy"]
        self.points = 0
        self.event = None
        self.processing_event = False
        self.removed_commands = []

        self.new_command_event = threading.Event()
        self.get_command_event = threading.Event()
        self.new_command_event.clear()
        self.get_command_event.clear()
        self.commands = []
        self.run_thread = threading.Thread(target=self.run)
        self.run_thread.setDaemon(True)
        self.run_thread.start()
        self.new_command_event.wait()
        self.new_command_event.clear()

    def run(self):
        pass

    def prepare_command(self):
        if len(self.commands) != 0:
            return
        self.get_command_event.set()
        self.new_command_event.wait()
        self.new_command_event.clear()

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
        if self.event is not None and not self.processing_event:
            self.processing_event = True
            self.process_event()
            self.event = None
            self.commands = self.removed_commands
            self.removed_commands = []
            if len(self.commands) != 0:
                self.on_command()
            self.processing_event = False

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

    def ahead(self, distance):
        self.push_command(Move(distance))
        self.on_command()

    def back(self, distance):
        self.push_command(Move(-distance))
        self.on_command()

    def set_event(self, event):
        if self.event is not None:
            return
        # remove all commands. So event will be processed next turn
        self.removed_commands = self.commands
        self.commands = []
        self.event = event

    def fire(self, power):
        if self.gun.heat != 0:
            return
        self.energy -= power
        self.gun.heat += (1 + power / 5)
        self.push_command(Fire(power))
        self.on_command()

    def get_heading(self):
        return self.rotation

    def get_gun_heading(self):
        return (self.get_heading() + self.gun.rotation) % 360

    def get_radar_heading(self):
        return (self.get_gun_heading() + self.gun.radar.rotation) % 360

    def process_event(self):
        if isinstance(self.event, ScannedRobot):
            self.on_scanned_robot(self.event)
            return
        if isinstance(self.event, HitByBullet):
            self.on_hit_by_bullet(self.event)
            return

    def on_scanned_robot(self, event):
        pass

    def on_hit_by_bullet(self, event):
        pass