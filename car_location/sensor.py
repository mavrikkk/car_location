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
CONF_SITE = 'haddr'
CONF_NAME = 'name'

ATTR_LAT = 'latitude'
ATTR_LON = 'longitude'
ATTR_SPEED = 'speed'
ATTR_DATE = 'date'

DEFAULT_NAME = 'GPS_Sensor'

SCAN_INTERVAL = timedelta(seconds=120)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_USER): cv.string,
    vol.Required(CONF_ID): cv.string,
    vol.Required(CONF_SITE): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
})



def setup_platform(hass, config, add_devices, discovery_info=None):

    user = config.get(CONF_USER)
    name = config.get(CONF_NAME)
    myid = config.get(CONF_ID)
    haddr = config.get(CONF_SITE)

    add_devices([CarGPS(name, user, myid, haddr)])
    
    
    
class CarGPS(Entity):

    def __init__(self, name, user, myid, haddr):
        self._name = name
        self._user = user
        self._myid = myid
        self._haddr = haddr

        self._lat = 0
        self._lon = 0
        self._speed = 0
        self._need_upd = True
        self._last_time_rcv = ''
        self._last_time_upd = ''



    def getInfoFrom(self):
        try:
            today = int(datetime.now().strftime("%s")) * 1000
            response = requests.get('https://livegpstracks.com/viewer_coos_s.php', params={'username': self._user, 'ctp': 'one', 'code': self._myid, 'tgst': 'site', 'tgs
            data = response.json()
            latA = self._lat
            lonA = self._lon
            latB = float(data[0]["lat"])
            lonB = float(data[0]["lng"])
            self._need_upd = True
            if latA != 0 and lonA != 0 and latB !=0 and lonB != 0:
                dst = self.getDistance(latA, lonA, latB, lonB)
                if dst < 0.1:
                    self._need_upd = False
            self._lat = latB
            self._lon = lonB
            self._speed = float(data[0]["speed"])
            self._last_time_rcv = data[0]["d"] + ' ' + data[0]["t"]
        except:
            _LOGGER.error('coudnt get parameters')
        
    def putInfoTo(self):
        if self._lat != 0 and self._lon != 0 and self._lat != None and self._lon != None:
            try:
                header  = {'Content-Type': 'application/x-www-form-urlencoded'}
                body = 'latitude=' + str(self._lat) + '&longitude=' + str(self._lon) + '&device=' + str(self._name) + '&accuracy=30&battery=100&speed=' + str(self._speed
                response = requests.post(self._haddr, headers=header, data=body)
                self._last_time_upd = time.strftime("%Y.%m.%d %H:%M")
            except:
                _LOGGER.error('coudnt put parameters')

    def getDistance(self, latA, lonA, latB, lonB):
        dst = 0
        try:
            latRadA = math.radians(latA)
            lonRadA = math.radians(lonA)
            latRadB = math.radians(latB)
            lonRadB = math.radians(lonB)
            x = latRadB - latRadA
            y = (lonRadB-lonRadA)*math.cos((latRadB+latRadA)*0.5)
            dst = 6371*math.sqrt(x*x+y*y)
        except:
            _LOGGER.error('couldnt getDistance')
        return dst



    #for HASS
    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._last_time_upd

    def update(self):
        self.getInfoFrom()
        if self._need_upd == True:
            self.putInfoTo()
            
    @property
    def device_state_attributes(self):
        attr = {}
        attr[ATTR_LAT] = self._lat
        attr[ATTR_LON] = self._lon
        attr[ATTR_SPEED] = self._speed
        attr[ATTR_DATE] = self._last_time_rcv
        return attr
        
