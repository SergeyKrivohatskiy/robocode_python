#!/usr/bin/env python
__author__ = 'Sergey Krivohatskiy'
import cocos
import math


class GameObject(cocos.sprite.Sprite):
    def __init__(self, img, position):
        super(GameObject, self).__init__(img)
        self.position = position
        self.vel = 0;
        self.rotation = 0;

    def update(self, dt):
        x, y = self.position[0], self.position[1]
        a = math.radians(self.rotation)
        sin, cos = math.sin(a), math.cos(a)
        dx, dy = (cos * self.vel * dt), (-sin * self.vel * dt)
        self.position = (x + dx, y + dy)