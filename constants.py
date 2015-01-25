#!/usr/bin/env python
__author__ = 'Sergey Krivohatskiy'

consts = {
    "window": {
        "width": 800,
        "height": 600,
        "vsync": True,
        "resizable": True
    },
    "background_color" : {
        "r": 23,
        "g": 32,
        "b": 23
    },
    "world": {
        "intersection_delta": 0
    },
    "robot": {
        "resources": {
            "body": 'robot.png',
            "gun": 'gun.png',
            "radar": 'radar.png'
        },
        "initial_gun_heat": 3,
        "max_gun_turn": 20,
        "max_radar_turn": 45,
        "max_idle_body_turn": 10,
        "velocity_body_turn_coefficient": 0.75,
        "max_velocity": 8,
        "max_acceleration": 1,
        "max_brake_acceleration": 2,
        "initial_energy": 100,
        "half_width": 50,
        "gun_cooling": 0.1,
        "radar_scan_length": 1200
    },
    "bullet": {
        "image": 'bullet.png',
        "max_velocity": 20,
        "velocity_power_coefficient": 3,
        "half_width": 5
    }
}