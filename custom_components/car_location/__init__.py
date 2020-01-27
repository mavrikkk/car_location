"""The car_location component."""

import time
import requests
import json
import math

import logging

from datetime import datetime
from datetime import timedelta

import voluptuous as vol

from homeassistant.core import callback
from homeassistant.const import (CONF_NAME, CONF_USERNAME, CONF_CLIENT_ID, CONF_SCAN_INTERVAL)
from homeassistant.helpers.discovery import async_load_platform
from homeassistant.helpers.event import async_track_time_interval
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.typing import ConfigType, HomeAssistantType
from homeassistant.helpers.dispatcher import async_dispatcher_send

SCAN_INTERVAL = timedelta(seconds=120)

_LOGGER = logging.getLogger(__name__)

SUPPORTED_DOMAINS = ["sensor"]

DOMAIN = "car_location"

CONFIG_SCHEMA = vol.Schema({DOMAIN: vol.Schema({vol.Required(CONF_CLIENT_ID): cv.string, vol.Required(CONF_USERNAME): cv.string, vol.Optional(CONF_SCAN_INTERVAL, default=SCAN_INTERVAL): cv.time_period,})}, extra=vol.ALLOW_EXTRA,)





async def async_setup(hass: HomeAssistantType, config: ConfigType) -> bool:

    hass.data[DOMAIN] = {}

    kwargs = dict(config[DOMAIN])
    myid = kwargs.get(CONF_CLIENT_ID)
    username = kwargs.get(CONF_USERNAME)
    scan_delta = kwargs.get(CONF_SCAN_INTERVAL)

    car_gps = hass.data[DOMAIN]["car_gps"] = CarGPS(hass, username, myid)
    try:
        await car_gps.update()
    except:
        _LOGGER.warning("Connect to car_location failed")
        return False

    async_track_time_interval(hass, car_gps.async_update, scan_delta)

    for platform in SUPPORTED_DOMAINS:
        hass.async_create_task(async_load_platform(hass, platform, DOMAIN, {}, config))

    return True





class CarGPS:

    def __init__(self, hass, user, myid):
        self.hass = hass
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

    async def update(self):
        self.getInfoFrom()

    async def async_update(self, now, **kwargs) -> None:
        try:
            await self.update()
        except:
            _LOGGER.warning("Update failed")
            return
        async_dispatcher_send(self.hass, DOMAIN)
