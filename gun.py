#!/usr/bin/env python
__author__ = 'Sergey Krivohatskiy'
import cocos
from constants import consts
import pyglet
from radar import Radar


class Gun(cocos.sprite.Sprite):
    def __init__(self):
        self.robot_consts = consts["robot"]
        super(Gun, self).__init__(pyglet.resource.image(self.robot_consts["resources"]["gun"]), (0, 0))
        self.heat = self.robot_consts["initial_gun_heat"]
        self.radar = Radar()
        self.add(self.radar)
        self.rotation = 0