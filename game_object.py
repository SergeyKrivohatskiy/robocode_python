#!/usr/bin/env python
__author__ = 'Sergey Krivohatskiy'
import cocos
import math


class GameObject(cocos.sprite.Sprite):
    def __init__(self, img, position):
        super(GameObject, self).__init__(img)
        self.position = position
        self.vel = 0
        self.speed = 0
        self.rotation = 0

    def update(self):
        x, y = self.position[0], self.position[1]
        a = math.radians(self.rotation)
        sin, cos = math.sin(a), math.cos(a)

        self.speed += self.vel
        if abs(self.speed) > self.max_speed:
            self.speed = math.copysign(self.max_speed, self.speed)

        dx, dy = (cos * self.speed), (-sin * self.speed)
        self.position = (x + dx, y + dy)