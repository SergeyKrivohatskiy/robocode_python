#!/usr/bin/env python
__author__ = 'Sergey Krivohatskiy'
import game_controller
from constants import consts
import example_robots
from robot import Robot
import cocos


def load_robots():
    """
    load Robot subclasses list from somewhere
    :return: Robot subclasses list
    """
    return [example_robots.MyFirstRobot, example_robots.Fire] * 2


class NoRobotsException(Exception):
    pass


def main():
    try:
        robots_list = load_robots()
        robots_list = [x for x in robots_list if issubclass(x, Robot)]
        if len(robots_list) == 0:
            raise NoRobotsException()
        cocos.director.director.init(**consts["window"])
        game_layer = game_controller.GameController(robots_list)
        scene = cocos.scene.Scene()
        background_color = consts["background_color"]
        scene.add(cocos.layer.ColorLayer(background_color["r"], background_color["g"], background_color["b"], 255), z=-1)
        scene.add(game_layer)
        cocos.director.director.run(scene)
    except NoRobotsException as _:
        print('There is no robots in robots_list')
        return -2
    except Exception as e:
        print('Unexpected exception: ' + str(e))
        return -3


if __name__ == '__main__':
    exit(main())