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
        self.rot_speed = 0

    def update(self):
        x, y = self.position[0], self.position[1]
        self.rotation += self.rot_speed
        a = math.radians(self.rotation)
        sin, cos = math.sin(a), math.cos(a)

        self.speed += self.vel
        if abs(self.speed) > self.max_speed:
            self.speed = math.copysign(self.max_speed, self.speed)

        dx, dy = (cos * self.speed), (-sin * self.speed)
        x += dx
        y += dy
        # simple cutting if out of the border
        if y < 0:
            y = 0
        if x < 0:
            x = 0
        w, h = cocos.director.director.get_window_size()
        if y > h:
            y = h
        if x > w:
            x = w
        self.position = (x, y)
