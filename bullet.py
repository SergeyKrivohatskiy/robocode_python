#!/usr/bin/env python
__author__ = 'Sergey Krivohatskiy'
import cocos
import constants
import pyglet
from utils import deg_to_vector


class Bullet(cocos.sprite.Sprite):
    def __init__(self, position, power, rotation, owner):
        super(Bullet, self).__init__(pyglet.resource.image(constants.bullet_image), (0, 0))
        self.position = position
        self.velocity = constants.bullet_max_velocity - constants.bullet_velocity_power_coefficient * power
        self.rotation = rotation
        self.owner = owner
        self.robot_damage = 4 * power + ((2 * (power - 1)) if power > 1 else 0)
        self.energy_and_points_boost = 3 * power

    def get_move_segment(self):
        return self.position, self.position + self.velocity * deg_to_vector(self.rotation)