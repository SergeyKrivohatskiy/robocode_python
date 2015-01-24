#!/usr/bin/env python
__author__ = 'Sergey Krivohatskiy'
from robot import Robot
import cocos
import time
import cocos.euclid as eu
import cocos.collision_model as cm
from constants import consts
import random


def get_rand_position(w, h):
    return eu.Vector2(random.randrange(w), random.randrange(h))


class GameController(cocos.layer.Layer):
    tic_time = 0.5
    # robots_list is a list of Robot class subclasses
    def __init__(self, robots_list):
        super(GameController, self).__init__()
        self.w = consts["window"]["width"]
        self.h = consts["window"]["height"]
        self.robots = [robot_class(self, get_rand_position(self.w, self.h)) for robot_class in robots_list]
        for robot in self.robots:
            self.add(robot, z=1)
        self.time = 0
        self.do(cocos.actions.Repeat(self.update))


    @cocos.actions.CallFuncS
    def update(self):
        start = time.time()

        self.time += 1


        # TODO
        print(self.time)

        to_sleep = GameController.tic_time + start - time.time()
        time.sleep(to_sleep if to_sleep > 0 else 0)