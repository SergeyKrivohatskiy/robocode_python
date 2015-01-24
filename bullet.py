#!/usr/bin/env python
__author__ = 'Sergey Krivohatskiy'
import cocos
from constants import consts
import pyglet


class Bullet(cocos.sprite.Sprite):
    def __init__(self, position, power, rotation, owner):
        super(Bullet, self).__init__(pyglet.resource.image(consts["bullet"]["image"]), (0, 0))
        self.position = position
        self.velocity = consts["bullet"]["max_velocity"] - consts["bullet"]["velocity_power_coefficient"] * power
        self.rotation = rotation
        self.owner = owner