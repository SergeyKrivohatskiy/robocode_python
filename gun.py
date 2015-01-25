#!/usr/bin/env python
__author__ = 'Sergey Krivohatskiy'
import cocos
import constants
import pyglet
from radar import Radar


class Gun(cocos.sprite.Sprite):
    def __init__(self):
        super(Gun, self).__init__(pyglet.resource.image(constants.robot_gun_image), (0, 0))
        self.heat = constants.robot_initial_gun_heat
        self.radar = Radar()
        self.add(self.radar)
        self.rotation = 0