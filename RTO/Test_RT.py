import os
#os.environ['PATH'] = "C:\\Users\\ando600\\Anaconda3\\Lib\\site-packages" + ";" + os.environ['PATH']

import pyvisa as visa
import VISAresourceExtentions
from pathlib import Path
import time

# -----------------------------------------------------------
# Initialization
# -----------------------------------------------------------
rm = visa.ResourceManager()
scope = rm.open_resource('TCPIP::10.32.112.162::INSTR')

# The file VISAresourceExtentions.py must be in the same folder as this file
# It contains PyVISA Visa.Resource extension functions for and 2 new exception types

# try block to catch any InstrumentErrorException()
try:
    scope.write_termination = ''
    # Some instruments require LF at the end of each command. In that case, use:
    # scope.write_termination = '\n'
    scope.ext_clear_status()  # Clear instrument io buffers and status
    print(scope.query('*IDN?'))  # Query the Identification string
    scope.write('*RST;*CLS')  # Reset the instrument, clear the Error queue
    scope.write('SYST:DISP:UPD ON')  # Display update ON - switch OFF after debugging
    scope.ext_error_checking()  # Error Checking after Initialization block

    # -----------------------------------------------------------
    # Basic Settings:
    # -----------------------------------------------------------
    #Timebase & Acquisition Settings
    #scope.write('ACQ:POIN:AUTO RECL')  # Define Horizontal scale by number of points
    #scope.write('ACQ:POIN 4008')  # 4008 X points

    scope.write('ACQ:POIN:AUTO RES')
    scope.write('ACQ:SRAT 20e9')
    scope.write('TIM:REF 0')
    #scope.write('TIM:RANG {}'.format(acquisition_time))  # Set Acquisition time

    #Channel 1 Settings
    scope.write('CHAN1:RANG 22')  # Horizontal range 7V
    scope.write('CHAN1:POS 0')  # Offset 0
    scope.write('CHAN1:COUP DCL')  # Coupling DC 1MOhm
    scope.write('CHAN1:STAT ON')  # Switch Channel 1 ON

    #Channel 2 Settings
    # scope.write('CHAN2:RANG 50')  # Horizontal range 50V
    # scope.write('CHAN2:POS 0')  # Offset 0
    # scope.write('CHAN2:COUP DCL')  # Coupling DC 1MOhm
    # scope.write('CHAN2:STAT ON')  # Switch Channel 2 ON

    scope.ext_error_checking()  # Error Checking

    # scope.write('CURSor1:STATe ON')
    # scope.write('CURSor1:FUNCtion HORizontal')
    # scope.write('CURSor1:SOURce C1W1')
    # #scope.write('CURSor1:SSOurce C1W1')

    # scope.write('CURSor1:TRACKing:STATe ON')
    # scope.ext_error_checking()

    # print(scope.write('CURSor1:YDELta:VAL 0'))
    
    # for i in range(100):
    #     x = scope.write('CURSor1:Y2P 0')
    #     print(x, type(x))
    #     time.sleep(0.2)
    #     i = i+1
    scope.write('TIM:SCAL 1e-9')
    scope.write('MEAS1:SOUR C1W1')
    scope.write('MEAS1 ON')
    scope.write('MEAS1:MAIN MAX')


    scope.query('*OPC?')

    for i in range(500):
        print(scope.query('MEAS1:RES:ACT?'))
        time.sleep(0.05)

    #scope.write('CURSor1:TRACKing:STATe OFF')
    #scope.write('CURSor1:STATe OFF')

    scope.ext_error_checking()


except VISAresourceExtentions.InstrumentErrorException as e:
    # Catching instrument error exception and showing its content
    print('Instrument error(s) occurred:\n' + e.message)