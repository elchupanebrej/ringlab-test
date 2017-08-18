from time import strptime, mktime
from datetime import datetime
import logging

import requests


class RoverCamera(object):
    def __init__(self):
        self.__name = None
        self.__full_name = None
        self.__id = None
        self.__rover_id = None

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def full_name(self):
        return self.__full_name

    @full_name.setter
    def full_name(self, value):
        self.__full_name = value


class Rover(object):
    def __init__(self):
        self.__id = None
        self.__name = None
        self.__landing_date = None
        self.__status = None
        self.__max_sol = None
        self.__max_date = None
        self.__total_photos = None
        self.__cameras = None

    def is_totally_initialized(self):
        return all([self.__getattribute__(attr) is None for attr in (
            'name',
            'landing_date',
            'status',
            'max_sol',
            'max_date',
            'total_photos',
            'cameras',
        )])

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value
        
    @property
    def landing_date(self):
        return self.__landing_date

    @landing_date.setter
    def landing_date(self, value):
        self.__landing_date = value

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value

    @property
    def max_sol(self):
        return self.__max_sol

    @max_sol.setter
    def max_sol(self, value):
        self.__max_sol = value

    @property
    def max_date(self):
        return self.__max_date

    @max_date.setter
    def max_date(self, value):
        self.__max_date = value

    @property
    def total_photos(self):
        return self.__total_photos

    @total_photos.setter
    def total_photos(self, value):
        self.__total_photos = value

    @property
    def cameras(self):
        return self.__cameras

    @cameras.setter
    def cameras(self, value):
        self.__cameras = value

    def build_from_meta(self, meta):
        for attr in ("id", "name", "status", "max_sol",  "total_photos"):
            self.__setattr__(attr, meta[attr])

        for attr in ("landing_date", "launch_date", "max_date"):
            try:
                self.__setattr__(attr,datetime.fromtimestamp(mktime(strptime(meta[attr], '%Y-%m-%d'))))
            except Exception:
                raise

        camera_list = []
        for camera_meta in meta['cameras']:
            camera = RoverCamera()
            camera.name = camera_meta['name']
            camera.full_name = camera_meta['full_name']
            camera_list.append(camera)
        self.cameras = camera_list

        return self


class NASARoverAPI(object):
    def __init__(self, api_key='DEMO_KEY', rover='curiosity'):
        self.api_key = api_key
        self.base_url = 'https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos'.format(rover=rover)
        self.rover = Rover().build_from_meta(self.get_rover_meta())

    def get_rover_meta(self):
        images_meta = self.get_image_metas_by_sol(0, page=1)
        rover_meta = images_meta[0]['rover']
        return rover_meta

    def get_image_metas_by_sol(self, sol, camera=None, page=None):
        try:
            response = requests.get(self.base_url, params={'sol': sol, 'page': page, 'camera': camera, 'api_key': self.api_key})
        except Exception:
            logging.exception('Excepted with: ')
            raise

        if response.ok:
            image_metas = response.json()['photos']
            return image_metas
        else:
            response.raise_for_status()

    def get_image_metas_by_date(self, date, camera=None, page=None):
        try:
            response = requests.get(self.base_url, params={'earth_date': date, 'page': page, 'camera': camera, 'api_key': self.api_key})
        except Exception:
            logging.exception('Excepted with: ')
            raise

        if response.ok:
            image_metas = response.json()['photos']
            return image_metas
        else:
            response.raise_for_status()
