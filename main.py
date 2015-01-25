#!/usr/bin/env python
__author__ = 'Sergey Krivohatskiy'
import game_controller
from constants import consts
import example_robot
from robot import Robot
import cocos


def load_robots():
    """
    load Robot subclasses list from somewhere
    :return: Robot subclasses list
    """
    return [example_robot.ExampleRobot] * 5


class NoRobotsException(BaseException):
    pass


def main():
    try:
        robots_list = load_robots()
        robots_list = list(filter(lambda x: issubclass(x, Robot), robots_list))
        if len(robots_list) == 0:
            raise NoRobotsException()
        cocos.director.director.init(**consts["window"])
        game_layer = game_controller.GameController(robots_list)
        scene = cocos.scene.Scene()
        background_color = consts["background_color"]
        scene.add(cocos.layer.ColorLayer(background_color["r"], background_color["g"], background_color["b"], 255), z=-1)
        scene.add(game_layer)
        cocos.director.director.run(scene)
    except NoRobotsException as e:
        print('There is no robots in robots_list')
        return -1
    except BaseException as e:
        print('Unexpected exception: ' + str(e))
        return -2


if __name__ == '__main__':
    exit(main())