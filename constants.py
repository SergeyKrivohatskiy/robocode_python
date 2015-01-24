#!/usr/bin/env python
__author__ = 'Sergey Krivohatskiy'

consts = {
    "window": {
        "width": 1200,
        "height": 600,
        "vsync": True,
        "resizable": True
    },
    "background_color" : {
        "r": 255,
        "g": 255,
        "b": 255
    },
    "world": {
    },
    "robot": {
        "width": 50,
        "height": 50,
        "resources": {
            "body": 'robot.png',
            "gun": 'gun.png',
            "radar": 'radar.png'
        },
        "initial_gun_heat": 3
    }
}