"""The car_location component."""

import time
import requests
import json
import math
from aiohttp import ClientSession
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
        await car_gps.getInfoFrom()
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

    async def async_update(self, now, **kwargs) -> None:
        await self.getInfoFrom()

    async def getInfoFrom(self):
        today = int(datetime.now().strftime("%s")) * 1000
        url = 'https://livegpstracks.com/viewer_coos_s.php?username=' + str(self._user) + '&ctp=one&code=' + str(self._myid) + '&tgst=site&tgsv=12&tkv11=' + str(today)
        async with ClientSession() as session:
            async with session.get(url) as response:
                response = await response.read()
                data=json.loads(response.decode('utf8'))
                time_gps=data[0]["d"] + ' ' + data[0]["t"]
                if datetime.now().timestamp() - datetime.strptime(time_gps, '%Y-%m-%d %H:%M:%S').timestamp() < 90 : #фильтр от старых данных
                    self._lat = float(data[0]["lat"])
                    self._lon = float(data[0]["lng"])
                    self._speed = float(data[0]["speed"])
                    self._last_upd = data[0]["d"] + ' ' + data[0]["t"]
                    async_dispatcher_send(self.hass, DOMAIN)
