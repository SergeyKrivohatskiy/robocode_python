#!/usr/bin/env python
__author__ = 'Sergey Krivohatskiy'

window_width = 800
window_height = 600
window_vsync = True
window_resizable = True

background_color_r = 23
background_color_g = 23
background_color_b = 23

bullet_image = 'bullet.png'
bullet_max_velocity = 20
bullet_velocity_power_coefficient = 3
bullet_half_width = 5

robot_body_image = 'robot.png'
robot_gun_image = 'gun.png'
robot_radar_image = 'radar.png'
robot_initial_gun_heat = 3
robot_max_gun_turn = 20
robot_max_radar_turn = 45
robot_max_idle_body_turn = 10
robot_velocity_body_turn_coefficient = 0.75
robot_max_velocity = 8
robot_max_acceleration = 1
robot_max_brake_acceleration = 2
robot_initial_energy = 100
robot_half_width = 50
robot_gun_cooling = 0.1
robot_radar_scan_length = 1200