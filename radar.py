#!/usr/bin/env python
__author__ = 'Sergey Krivohatskiy'
import cocos
from constants import consts
import pyglet


class Radar(cocos.sprite.Sprite):
    def __init__(self):
        self.robot_consts = consts["robot"]
        super(Radar, self).__init__(pyglet.resource.image(self.robot_consts["resources"]["radar"]), (0, 0))
        self.rotation = 0