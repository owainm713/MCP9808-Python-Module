# MCP9808-Python-Module
Python 3.x  module for use with MCP9808 digital temperature sensor. 

This requires the smbus module for the i2c connection. I used the adafruit MCP9808
break out board connected to a Raspberry Pi 3 for development of this module.

Connections to the MCP9808 from the Pi are as follows

- Pi SCL to MCP SCL
- Pi SDA to MCP SDA
- Pi 3.3V to MCP Vdd
- Pi Gnd to MCP Gnd
- MCP Alert - requires pull up resistor
- MCP A0 - MCP A2  N/C - used to set i2c address

With the above A0-A2 connections the i2c address is 0x18

For testing of the Alert/Interrupt capabilities I used a
1k ohm pull up resister between Alert & Vdd and placed a 
LED between Alert & Gnd.

Current functions include:
- read_temperature()
- set_t_critical(temperature)
- set_t_upper(temperature)
- set_t_lower(temperature)
- set_resolution(res = 0.0625)
- set_hysteresis(hys = 0)
- set_shutdown(mode=True)
- set_critical_lock(critLock = True)
- set_window_lock(winLock = True)
- set_alerts(control = True, select = "all", polarity = "low", mode = "comparator")
- get_alerts()
- clear_interrupt()

For information on how the sensor works check out the datasheet, It has good explanations for
the sensor hysteresis, how the different alerts work, comparator vs interrupt, Tupper vs Tcritcal
etc.

Note: 
If you set either the critical lock which makes Tcritcal unchangable, or the window lock which
makes Tupper and Tlower unchangable, those items can not be unlocked without a power on reset,
which I found required grounding the Vdd pin (after removing the 3.3V source of course).
