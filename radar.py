#!/usr/bin/env python
__author__ = 'Sergey Krivohatskiy'
import cocos
import pyglet
import constants


class Radar(cocos.sprite.Sprite):
    def __init__(self):
        super(Radar, self).__init__(pyglet.resource.image(constants.robot_radar_image), (0, 0))
        self.rotation = 0