#          
# Filename: domoticz http.py
# Version : 0.1
# Author  : Lisa Esselink
# Purpose : Controller Domoticz MQTT & HTTP
# Usage   : Send and receive messages from Domoticz using both MQTT and HTTP
#
# Copyright (c) 2017 - Lisa Esselink. All rights reserved.  
# Licensend under the Creative Commons Attribution-NonCommercial 4.0 International License.
# See LICENSE file in the project root for full license information.  
#

import ujson, urequests, uasyncio.queues as queues
from upyeasy import protocol as uprotocol, core
from asyn import Event

#
# CUSTOM PROTOCOL GLOBALS
#

name     = "Domoticz HTTP"
protocol = "HTTP"
template = "domoticz_http.html"

#
#
#

class domoticz_http_protocol:
    processcnt          = 1

    def __init__(self) :
        self._log   = core._log
        self._log.debug("Protocol: domoticz http contruction")
        self._lock  = Event()
        # release lock, ready for next loop
        self._lock.clear()

    def init(self, protocol):        
        self._log.debug("Protocol "+name+": Init")
        self._client_id  = protocol['client_id']
        self._server     = protocol['hostname']
        self._port       = protocol['port']
        self._user       = protocol['user']
        self._password   = protocol['password']
        self._queue      = queues.Queue(maxsize=100)
        return self._queue
        
    def connect(self):
        self._log.debug("Protocol "+name+": connect")
        
    def disconnect(self):
        self._log.debug("Protocol "+name+": disconnect")

    def check(self):
        self._log.debug("Protocol "+name+": check")
        
    def status(self):
        self._log.debug("Protocol "+name+": status")

    def receive(self):
        self._log.debug("Protocol "+name+": recieve")
        
    def send(self,devicedata):    
        self._log.debug("Protocol "+name+": send "+devicedata["stype"])
        # Assemble server url
        message = None
        # case
        while True:

            # case SENSOR_TYPE_SINGLE
            if devicedata["stype"] == core.SENSOR_TYPE_SINGLE:
                self._log.debug("Protocol "+name+": SENSOR_TYPE_SINGLE")
                # Get plugin values
                try:
                    devicedata['value1'] = self._queue.get_nowait()
                except Exception:
                    self._log.debug("Protocol "+name+" SENSOR_TYPE_TEMP_HUM exception: Queue Emtpy!")
                    break
                
                # Assemble http message
                message = "/json.htm?type=command&param=udevice&idx="+str(devicedata["serverid"])+"&nvalue=0&svalue="+str(devicedata["value1"])+";0"
                break

            # case SENSOR_TYPE_LONG
            if devicedata["stype"] == core.SENSOR_TYPE_LONG:
                self._log.debug("Protocol "+name+": SENSOR_TYPE_LONG")
                break

            # case SENSOR_TYPE_DUAL
            if devicedata["stype"] == core.SENSOR_TYPE_DUAL:
                self._log.debug("Protocol "+name+": SENSOR_TYPE_DUAL")
                break

            # case SENSOR_TYPE_TEMP_HUM
            if devicedata["stype"] == core.SENSOR_TYPE_TEMP_HUM:
                self._log.debug("Protocol "+name+": SENSOR_TYPE_TEMP_HUM")
                # Get plugin values
                try:
                    devicedata['value1'] = self._queue.get_nowait()
                    devicedata['value2'] = self._queue.get_nowait()
                except Exception:
                    self._log.debug("Protocol "+name+" SENSOR_TYPE_TEMP_HUM exception: Queue Emtpy!")
                    break
                # Assemble http message
                message = "/json.htm?type=command&param=udevice&idx="+str(devicedata["serverid"])+"&nvalue=0&svalue="+str(devicedata["value1"])+str(devicedata["value2"])+";0"
                break

            # case SENSOR_TYPE_TEMP_BARO
            if devicedata["stype"] == core.SENSOR_TYPE_TEMP_BARO:
                self._log.debug("Protocol "+name+": SENSOR_TYPE_TEMP_BARO")
                break

            # case SENSOR_TYPE_TEMP_HUM_BARO
            if devicedata["stype"] == core.SENSOR_TYPE_TEMP_HUM_BARO:
                self._log.debug("Protocol "+name+": SENSOR_TYPE_TEMP_HUM_BARO")
                # Get plugin values
                try:
                    devicedata['value1'] = self._queue.get_nowait()
                    devicedata['value2'] = self._queue.get_nowait()
                    devicedata['value3'] = self._queue.get_nowait()
                except Exception:
                    self._log.debug("Protocol "+name+" SENSOR_TYPE_TEMP_HUM_BARO exception: Queue Emtpy!")
                    break
                # Assemble http message
                message = "/json.htm?type=command&param=udevice&idx="+str(devicedata["serverid"])+"&nvalue=0&svalue="+str(devicedata["value1"])+str(devicedata["value2"])+";0;"+str(devicedata["value3"])+";0"
                break

            # case SENSOR_TYPE_SWITCH
            if devicedata["stype"] == core.SENSOR_TYPE_SWITCH:
                self._log.debug("Protocol "+name+": SENSOR_TYPE_SWITCH")
                # Get plugin values
                try:
                    devicedata['value1'] = self._queue.get_nowait()
                except Exception:
                    self._log.debug("Protocol "+name+" SENSOR_TYPE_SWITCH exception: Queue Emtpy!")
                    break

                # Switches can have many values, domoticz only two: on or off
                switch_on  = ['closed','press','double','long', 'on']
                switch_off = ['open','release', 'off']    
                
                if devicedata["value1"].lower() in switch_on: 
                    devicedata["value1"] = 'On'
                elif devicedata["value1"].lower() in switch_off: 
                    devicedata["value1"] = 'Off'
                else: 
                    self._log.debug("Protocol "+name+" SENSOR_TYPE_SWITCH error: Value1 break!")
                    print(devicedata["value1"])
                    break

                # Assemble http message
                message = "/json.htm?type=command&param=switchlight&idx="+str(devicedata["serverid"])+"&switchcmd="+devicedata["value1"]
                break

            # case SENSOR_TYPE_DIMMER
            if devicedata["stype"] == core.SENSOR_TYPE_DIMMER:
                self._log.debug("Protocol "+name+": SENSOR_TYPE_DIMMER")
                break

            # case SENSOR_TYPE_WIND
            if devicedata["stype"] == core.SENSOR_TYPE_WIND:
                self._log.debug("Protocol "+name+": SENSOR_TYPE_WIND")
                break

            # else UNKNOWN
            self._log.debug("Protocol "+name+": Unknown sensor type!")
            break

        if message != None: 
            self._log.debug("Protocol "+name+" message: "+"http://"+self._server+":"+str(self._port)+message)
            # Send data
            try:
                response = urequests.get("http://"+self._server+":"+str(self._port)+message)
                self._log.debug("Protocol "+name+" response: "+response.text)
                response.close()
            except OSError as e:
                self._log.debug("Protocol "+name+" Exception: "+repr(e))
            #self._log.debug("Protocol "+name+" response: "+resp.read().decode("utf-8"))
           
    def process(self):
        # processing todo for protocol
        self._log.debug("Protocol "+name)
        devicedata = {}
        try:
            while self._queue.get_nowait() != core.QUEUE_MESSAGE_START:
                pass
            devicedata['stype'] = self._queue.get_nowait()
            devicedata['serverid'] = self._queue.get_nowait()
        except Exception as e:
            self._log.debug("Protocol "+name+" proces Exception: "+repr(e))
        self.send(devicedata)

        # release lock, ready for next processing
        self._lock.clear()
