#!/usr/bin/env python
__author__ = 'Sergey Krivohatskiy'


class Command(object):
    pass


class DoNothing(Command):
    pass


class Fire(Command):
    def __init__(self, power):
        self.power = power


class Move(Command):
    def __init__(self, distance):
        self.distance = distance


class Turn(Command):
    def __init__(self, what, deg):
        self.what = what
        self.deg = deg