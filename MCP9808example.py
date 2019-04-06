#!/usr/bin/env python3
"""MCP9808example, example program on use of the MCP9808 python
module

created April 4, 2019
last modified April 4, 2019"""

"""
Copyright 2019 Owain Martin

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import MCP9808
import time

TempSensor = MCP9808.MCP9808(0x18)

TempSensor.set_resolution(0.0625)
print(TempSensor.single_access_read(0x08))

TempSensor.set_hysteresis(1.5)
print(hex(TempSensor.single_word_read(0x01)))

TempSensor.set_t_upper(21)
TempSensor.set_t_critical(26)
TempSensor.set_t_lower(-9.25)

print(TempSensor.twos_complement_conversion(TempSensor.single_word_read(0x02)))
print(TempSensor.twos_complement_conversion(TempSensor.single_word_read(0x03)))
print(TempSensor.twos_complement_conversion(TempSensor.single_word_read(0x04)))

TempSensor.set_alerts(control = True, select = "all", polarity = "high", mode = "comparator")
print(hex(TempSensor.single_word_read(0x01)))

while True:
    print(TempSensor.read_temperature())
    print(TempSensor.get_alerts())
    time.sleep(1)



