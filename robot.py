#!/usr/bin/env python
__author__ = 'Sergey Krivohatskiy'
import threading
import pyglet
import cocos
from constants import consts
import cocos.euclid as eu
import cocos.collision_model as cm
from gun import Gun


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
