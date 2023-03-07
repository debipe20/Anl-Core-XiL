#!/usr/bin/env python

# Copyright (c) 2019 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

"""Spawn NPCs into the simulation"""

import glob
import os
import sys
import time

import fnmatch
from os.path import expanduser

def find_file(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result      

#this looks for the carla python API .egg file in the directory above the executed directory
try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

#this looks for the carla python API .egg file in ~/carla
try:
    
    carla_egg_name = 'carla-*' + str(sys.version_info.major) + '.' + str(sys.version_info.minor) + '-' + str('win-amd64' if os.name == 'nt' else 'linux-x86_64') + '.egg'
    print("Looking for CARLA egg: " + carla_egg_name)
    carla_egg_locations = find_file(carla_egg_name,expanduser("~") + '/carla')
    print("Found carla egg(s): " + str(carla_egg_locations))

    if len(carla_egg_locations) == 1:
        carla_egg_to_use = carla_egg_locations[0]
    else:
        print("\nFound multiple carla egg files: ")
        for i,egg_found in enumerate(carla_egg_locations):
            print("[" + str(i+1) + "]    " + egg_found)

        egg_selected = input("\nSelect a carla egg file to use: ")

        try:
            egg_selected = int(egg_selected)
        except:
            print("\nInvalid selection, please try again")
            sys.exit()

        if (egg_selected <= len(carla_egg_locations)):
            carla_egg_to_use = carla_egg_locations[egg_selected-1]
        else:
            print("\nInvalid selection, please try again")
            sys.exit()

    sys.path.append(carla_egg_to_use)

    #sys.path.append(glob.glob(expanduser("~") + '/carla/CARLA_0.9.10_TFHRC_Ubuntu_20220301/LinuxNoEditor/PythonAPI/carla/dist/carla-*%d.%d-%s.egg' % (
    #    sys.version_info.major,
    #    sys.version_info.minor,
    #    'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

from carla import VehicleLightState as vls

import argparse
import logging
from numpy import random

def main():
    argparser = argparse.ArgumentParser(
        description=__doc__)
    argparser.add_argument(
        '--host',
        metavar='H',
        default='127.0.0.1',
        help='IP of the host server (default: 127.0.0.1)')
    argparser.add_argument(
        '-p', '--port',
        metavar='P',
        default=2000,
        type=int,
        help='TCP port to listen to (default: 2000)')
    argparser.add_argument(
        '-n', '--number-of-vehicles',
        metavar='N',
        default=10,
        type=int,
        help='number of vehicles (default: 10)')
    argparser.add_argument(
        '-w', '--number-of-walkers',
        metavar='W',
        default=50,
        type=int,
        help='number of walkers (default: 50)')
    argparser.add_argument(
        '--safe',
        action='store_true',
        help='avoid spawning vehicles prone to accidents')
    argparser.add_argument(
        '--filterv',
        metavar='PATTERN',
        default='vehicle.*',
        help='vehicles filter (default: "vehicle.*")')
    argparser.add_argument(
        '--filterw',
        metavar='PATTERN',
        default='walker.pedestrian.*',
        help='pedestrians filter (default: "walker.pedestrian.*")')
    argparser.add_argument(
        '--tm-port',
        metavar='P',
        default=8000,
        type=int,
        help='port to communicate with TM (default: 8000)')
    argparser.add_argument(
        '--sync',
        action='store_true',
        help='Synchronous mode execution')
    argparser.add_argument(
        '--hybrid',
        action='store_true',
        help='Enanble')
    argparser.add_argument(
        '-s', '--seed',
        metavar='S',
        type=int,
        help='Random device seed')
    argparser.add_argument(
        '--car-lights-on',
        action='store_true',
        default=False,
        help='Enanble car lights')
    args = argparser.parse_args()

    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

    vehicles_list = []
    walkers_list = []
    all_id = []
    client = carla.Client(args.host, args.port)
    client.set_timeout(10.0)
    synchronous_master = False
    random.seed(args.seed if args.seed is not None else int(time.time()))

    try:
        print(client.get_available_maps())
        
        #world = client.load_world('Carla_v14_10_1_2021')
        #world = client.get_world()
        

    finally:

        if args.sync and synchronous_master:
            settings = world.get_settings()
            settings.synchronous_mode = False
            settings.fixed_delta_seconds = None
            world.apply_settings(settings)

        print('\nENDING')


        time.sleep(0.5)

if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('\ndone.')
