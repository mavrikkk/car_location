#!/usr/local/bin/python3
# coding: utf-8

import time
import requests
import json
import math

import logging

from datetime import datetime
from datetime import timedelta

import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (CONF_NAME)
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

CONF_USER = 'user'
CONF_ID = 'myid'
CONF_NAME = 'name'

ATTR_SPEED = 'speed'
ATTR_LAT = 'latitude'
ATTR_LON = 'longitude'
DEFAULT_NAME = 'GPS_Sensor'

SCAN_INTERVAL = timedelta(seconds=120)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_USER): cv.string,
    vol.Required(CONF_ID): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
})


def setup_platform(hass, config, add_devices, discovery_info=None):

    user = config.get(CONF_USER)
    name = config.get(CONF_NAME)
    myid = config.get(CONF_ID)

    add_devices([CarGPS(name, user, myid)])
    
class CarGPS(Entity):

    def __init__(self, name, user, myid):
        self._name = name
        self._user = user
        self._myid = myid

        self._lat = 0
        self._lon = 0
        self._speed = 0
        self._last_upd = None

        self.getInfoFrom()



    def getInfoFrom(self, now=None):
        try:
            today = int(datetime.now().strftime("%s")) * 1000
            response = requests.get('https://livegpstracks.com/viewer_coos_s.php', params={'username': self._user, 'ctp': 'one', 'code': self._myid, 'tgst': 'site', 'tgsv': 12, 'tkv11': today})
            data = response.json()
            self._lat = float(data[0]["lat"])
            self._lon = float(data[0]["lng"])
            self._speed = float(data[0]["speed"])
            self._last_upd = data[0]["d"] + ' ' + data[0]["t"]
        except:
            _LOGGER.error('coudnt get parameters')



    #for HASS
    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._last_upd

    def update(self):
        self.getInfoFrom()

    @property
    def device_state_attributes(self):
        attrs = {}
        attrs[ATTR_LAT] = self._lat
        attrs[ATTR_LON] = self._lon
        attrs[ATTR_SPEED] = self._speed
        return attrs
    
