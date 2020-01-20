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
from homeassistant.components.device_tracker import (PLATFORM_SCHEMA, SOURCE_TYPE_GPS)
from homeassistant.helpers.event import track_time_interval

_LOGGER = logging.getLogger(__name__)

CONF_USER = 'user'
CONF_ID = 'myid'
CONF_NAME = 'name'

ATTR_SPEED = 'speed'
ATTR_LAST_UPDATE = 'last_update'

DEFAULT_NAME = 'GPS_Sensor'

MIN_TIME_BETWEEN_SCANS = timedelta(seconds=120)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_USER): cv.string,
    vol.Required(CONF_ID): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
})



def setup_scanner(hass, config, see, discovery_info=None):

    user = config.get(CONF_USER)
    name = config.get(CONF_NAME)
    myid = config.get(CONF_ID)

    scanner = CarGPS(hass, name, user, myid, see)
    return scanner._success
  
class CarGPS:

    def __init__(self, hass, name, user, myid, see) -> None:
        self._name = name
        self._user = user
        self._myid = myid
        self.see = see

        self._success = False

        try:
            self.getInfoFrom()
            track_time_interval(hass, self.getInfoFrom, MIN_TIME_BETWEEN_SCANS)
            self._success =  True
        except:
            _LOGGER.error("Coudnt get car_location coordinates")
            self._success = False



    def getInfoFrom(self, now=None):
        try:
            today = int(datetime.now().strftime("%s")) * 1000
            response = requests.get('https://livegpstracks.com/viewer_coos_s.php', params={'username': self._user, 'ctp': 'one', 'code': self._myid, 'tgst': 'site', 'tgsv': 12, 'tkv11': today})
            data = response.json()
            lat = float(data[0]["lat"])
            lon = float(data[0]["lng"])
            speed = float(data[0]["speed"])
            last_time_rcv = data[0]["d"] + ' ' + data[0]["t"]

            attrs = {
                ATTR_SPEED: speed,
                ATTR_LAST_UPDATE: last_time_rcv
            }
            self.see(
                dev_id=self._name,
                gps=(lat, lon),
                source_type=SOURCE_TYPE_GPS,
                attributes=attrs,
            )
        except:
            _LOGGER.error('coudnt get parameters')
