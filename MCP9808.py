#!/usr/bin/env python3
"""MCP9808, python module for the MCP9808 digital temperature
sensor

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

import time, sys, smbus

class MCP9808:

    def __init__(self, i2cAddress):

        self.i2cAddress = i2cAddress
        self.bus =smbus.SMBus(1)

        return

    def single_access_read(self, reg=0x00):
        """single_access_read, function to read a single 8 bit data register
        of the MCP9808 digital temperature sensor"""                  
       
        dataTransfer=self.bus.read_byte_data(self.i2cAddress,reg)
        
        return dataTransfer

    def single_word_read(self, reg=0x00):
        """single_word_read, function to read a single 16 bit data register
        of the MCP9808 digital temperature sensor

        data returned from sensor is LSB first (i.e. in the MSB place of
        dataTransfer).  Function reorders data to read normally"""                  
       
        dataTransfer=self.bus.read_word_data(self.i2cAddress,reg)
        dataTransfer = ((dataTransfer & 0x00FF)<<8) + ((dataTransfer & 0xFF00)>>8)
        
        return dataTransfer

    def single_access_write(self, reg=0x00, regValue = 0):
        """single_access_write, function to write to a single 8 bit data register
        of the MCP9808 digital temperature sensor"""                  
       
        self.bus.write_byte_data(self.i2cAddress,reg, regValue)
        
        return

    def single_word_write(self, reg=0x00, regValue = 0):
        """single_word_write, function to write to a single 16 bit data register
        of the MCP9808 digital temperature sensor

        data returned from sensor is LSB first (i.e. in the MSB place of
        dataTransfer).  Function reorders data to read normally"""                  
       
        regValue = ((regValue & 0x00FF)<<8) + ((regValue & 0xFF00)>>8)
        self.bus.write_word_data(self.i2cAddress, reg, regValue)
        
        return

    def twos_complement_conversion(self, tempData):
        """twos_complement_conversion, function to change the 13 bit value
        split across 2 bytes from 2s complement to normal binary/decimal"""

        signBit= (tempData & 0x1000)>>12
        tempData = tempData & 0xFFF  # strip off sign bit        

        if signBit == 1:  # negative number        
            x = tempData
            x = x^0xFFF
            x = -(x + 1)
        else: # positive number        
            x = tempData

        temperature = x/16

        return temperature

    def conversion_to_twos_complement(self, num2convert):
        """conversion_to_twos_complement, function to change a number
        into twos complement 13 bit number"""        

        if num2convert < 0:
            x = abs(num2convert*16)        
            x = int(x) & 0xFFF
            x = x^0x1FFF
            x = x+1

        else:
            x = int(num2convert*16)
            x = x & 0xFFF

        return x

    def read_temperature(self):
        """read_temperature, function to read the temperature data
        from register 0x05 of the MCP9808 and convert to decimal format"""

        # read data from MCP9808 regisiter
        tempData = self.single_word_read(0x05)

        # reorder data with MSB first then LSB, put this into single_word_read funct
        #tempData = ((tempData & 0x00FF)<<8) + ((tempData & 0xFF00)>>8)

        # take off alert flags from temerature data
        tempData = tempData & 0x1FFF

        temperature = self.twos_complement_conversion(tempData)

        return temperature
       
    def set_t_critical(self, temperature):
        """set_t_critical, function to set the Tcritical value kept in
        register 0x04"""

        temperature = self.conversion_to_twos_complement(temperature)
        self.single_word_write(0x04, temperature)

        return

    def set_t_upper(self, temperature):
        """set_t_upper, function to set the Tupper value kept in
        register 0x02"""

        temperature = self.conversion_to_twos_complement(temperature)
        self.single_word_write(0x02, temperature)

        return

    def set_t_lower(self, temperature):
        """set_t_lower, function to set the Tlower value kept in
        register 0x03"""

        temperature = self.conversion_to_twos_complement(temperature)
        self.single_word_write(0x03, temperature)

        return

    def set_resolution(self, res = 0.0625):
        """set_resolution, function to set the sensor resolution to one of
        four values, 0.5, 0.25, 0.125 or 0.0625 degrees C. This sets bits 0
        & 1 of register 0x08"""        

        if res == 0.5:
            resBits = 0b00
        elif res == 0.25:
            resBits = 0b01
        elif res == 0.125:
            resBits = 0b10
        else:
            resBits = 0b11

        self.single_access_write(0x08, resBits)

        return

    def set_hysteresis(self, hys = 0):
        """set_hysteresis, function to set the sensor hysteresis to one of
        four values, 0, 1.5, 3.0, 6.0 degrees C.  This sets bits 9 & 10 of
        register 0x01"""

        if hys == 1.5:
            hysBits = 0b01
        elif hys == 3.0:
            hysBits = 0b10
        elif hys == 6.0:
            hysBits = 0b11
        else:
            hysBits = 0b00

        configReg = self.single_word_read(0x01)
        configReg = configReg &  0x01FF
        configReg = configReg | (hysBits<<9)

        self.single_word_write(0x01, configReg)

        return

    def set_shutdown(self, mode=True):
        """set_shutdown, function to set the sensor shutdown mode bit, bit 8
        of register 0x01.  True = shutdown/low power mode, False = continuous
        conversion"""

        if mode == False:
            modeBit = 0
        else:
            modeBit = 1

        configReg = self.single_word_read(0x01)
        configReg = configReg &  0x06FF
        configReg = configReg | (modeBit<<8)

        self.single_word_write(0x01, configReg)

        return

    def set_critical_lock(self, critLock = True):
        """set__critical_lock, function to enable the sensor critical lock
        function. This sets bit 7 of register 0x01"""

        # Note: Once critcal lock is set it can only be cleared by a power
        # on reset

        if critLock == False:
            modeBit = 0
        else:
            modeBit = 1

        configReg = self.single_word_read(0x01)
        configReg = configReg &  0x077F
        configReg = configReg | (modeBit<<7)

        self.single_word_write(0x01, configReg)

        return

    def set_window_lock(self, winLock = True):
        """set__window_lock, function to enable the sensor window lock
        function. This sets bit 6 of register 0x01"""

        # Note: Once window lock is set it can only be cleared by a power
        # on reset

        if winLock == False:
            modeBit = 0
        else:
            modeBit = 1

        configReg = self.single_word_read(0x01)
        configReg = configReg &  0x07BF
        configReg = configReg | (modeBit<<6)

        self.single_word_write(0x01, configReg)

        return

    def set_alerts(self, control = True, select = "all", polarity = "low", mode = "comparator"):
        """set_alerts, function to set the alert properties of the sensor including
        control - True/False, select - all/critcal, polarity = high/low, mode = compartor/
        interrupt.  This sets bits 0-3 of register 0x01"""

        if control == False:
            cntBit = 0
        else:
            cntBit = 1

        if select == "crtical":
            selectBit = 1
        else:
            selectBit = 0

        if polarity == "high":
            polBit = 1
        else:
            polBit = 0

        if mode == "interrupt":
            modeBit = 1
        else:
            modeBit = 0

        configReg = self.single_word_read(0x01)
        configReg = configReg &  0x07F0
        configReg = configReg | (cntBit<<3) + (selectBit<<2) + (polBit<<1) + modeBit    

        self.single_word_write(0x01, configReg)

        return

    def get_alerts(self):
        """get_alerts, function to get the sensor alert data including Ta vs
        Tup, Tlow, Tcrit, bits 13-15 in register 0x05 and alert status from
        bit 4 of register 0x01"""

        # get Ta vs Tcritical, Tupper, Tlower status bits from reg 0x05
        # read data from MCP9808 regisiter
        tempData = self.single_word_read(0x05)   

        # take off alert flags from temerature data
        alertData = (tempData & 0xE000)>>13        

        # get alert status (bit 4) from reg 0x01
        alertStatus = self.single_word_read(0x01)
        alertStatus = (alertStatus & 0x0010)>>4           

        return alertData, alertStatus

    def clear_interrupt(self):
        """clear_interrupt, function to set the interrupt clear bit
        to clear the sensor interrupt, when in interrupt mode. Sets bit 5
        of register 0x01"""

        configReg = self.single_word_read(0x01)    
        configReg = configReg | 1<<5        

        self.single_word_write(0x01, configReg)

        return
