#!/usr/bin/env python
__author__ = 'Sergey Krivohatskiy'
import cocos


class GameObject(cocos.sprite.Sprite):
    def __init__(self, img, position):
        super(GameObject, self).__init__(img)
        self.position = position
        self.vel = 0;
        self.deg = 0;

    def update(self, dt):
        pass