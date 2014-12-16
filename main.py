#!/usr/bin/env python
__author__ = 'Sergey Krivohatskiy'
import game_controller
import traceback
import example_robot
import cocos


def load_robots():
    """
    load Robot subclasses list from somewhere
    :return: Robot subclasses list
    """
    return [example_robot.ExampleRobot]


def main():
    try:
        robots_list = load_robots()
        cocos.director.director.init()
        game_scene = game_controller.GameController(robots_list)
        cocos.director.director.run(game_scene)
    except game_controller.NoRobotsException as e:
        print('There is no robots in robots_list ')
        return -1
    except BaseException as e:
        print(traceback.format_exc())
        print('Unexpected exception: ' + e.message)
        return -2


if __name__ == '__main__':
    exit(main())