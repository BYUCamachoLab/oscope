from settings import *

# ---------------------------------------------------------------------------- #
# Libraries
# ---------------------------------------------------------------------------- #
import os
from pathlib import Path
#import time
import sys
from datetime import datetime

from TSL550 import TSL550
import serial.tools.list_ports
from laser_control import *

from RTO.controller import RTO as connectScope
from data_processing import WavelengthAnalyzer, VisualizeData

# ---------------------------------------------------------------------------- #
# Check Input
# ---------------------------------------------------------------------------- #
print("Checking inputs.")
#Get command line arguments.
args = sys.argv[1:]
filename = filename_prefix + sys.argv[0] + filename_suffix

#Check laser settings.
laser_sweep_rate = (lambda_stop - lambda_start) / duration
checkSweepRate(laser_sweep_rate)
checkWavelength(lambda_start)
checkWavelength(lambda_stop)

# ---------------------------------------------------------------------------- #
# Initialize Save Directory
# ---------------------------------------------------------------------------- #
today = datetime.now()
datePrefix = "{}_{}_{}_{}_{}_".format(today.year, today.month, today.day, today.hour, today.minute)
prefix = datePrefix if append_date else ""
folderName = prefix + data_directory
folderPath = Path(Path.cwd(), "DATA", folderName)
print("Saving data to {} in current directory.".format(folderName))
if not os.path.exists(folderPath):
    print("Creating {} directory.".format(folderName))
    os.makedirs(folderPath)

# ---------------------------------------------------------------------------- #
# Initialize Devices
# ---------------------------------------------------------------------------- #
print("Initializing devices.")

#Initialize Laser
print("Initializing laser.")
laser = initLaser()
laser.on()
laser.power_dBm(power_dBm)
laser.openShutter()
laser.sweep_set_mode(
    continuous=True,
    twoway=True,
    trigger=False,
    const_freq_step=False
)
print("Enabling laser's trigger output.")
laser.trigger_enable_output()
triggerMode = laser.trigger_set_mode("Step")
triggerStep = laser.trigger_set_step(trigger_step)
print("Setting trigger to: {} and step to {}".format(triggerMode, triggerStep))

#Get number of samples to record. Add buffer just in case.
acquireTime = duration + buffer
numSamples = int((acquireTime) * sample_rate)
print("Set for {:.2E} Samples @ {:.2E} Sa/s.".format(numSamples, sample_rate))

#Oscilloscope Settings
print("Initializing Oscilloscope")
scope = connectScope(scope_IP)
scope.acquisition_settings(
    sample_rate = sample_rate,
    duration = acquireTime + buffer,
    force_realtime = False
)
for channel in active_channels:
    channelMode = "Trigger" if (channel == trigger_channel) else "Data"
    print("Adding Channel {} - {}".format(channel, channelMode))
    scope.add_channel(
        channel_num = channel,
        **channel_setting[channel]
    )
#Add trigger.
print("Adding Edge Trigger @ {} Volt(s).".format(trigger_level))
scope.edge_trigger(
    source_channel = trigger_channel,
    trigger_level = trigger_level
)

# ---------------------------------------------------------------------------- #
# Settings Check / Details
# ---------------------------------------------------------------------------- #
check_values = {
    "Acquire Mode": "ACQ:MODE?",
    "ADC Rate": "ACQ:POIN:ARATe?", #Query only.
    "Sample Rate": "ACQ:SRATe?",
    "Real Sample Rate": "ACQ:SRR?",
    "Max Samples": "ACQ:POIN:MAX?",
}

#for value, command in check_values.items():
#    print("Scope {} is {:.2e}.".format(value, scope.query(command)))

# ---------------------------------------------------------------------------- #
# Collect Data
# ---------------------------------------------------------------------------- #
print('Starting Acquisition')
scope.start_acquisition(
    timeout = duration*3
)

#Sweep Laser
print('Sweeping Laser')
laser.sweep_wavelength(
    start=lambda_start,
    stop=lambda_stop,
    duration=duration,
    number=1
)

#Wait for Measurement Completion
print('Waiting for acquisition to complete.')
scope.wait_for_device()
#Take Screenshot
if take_screenshot:
    scope.take_screenshot(folderPath / "screenshot.png")

#Acquire Data
#HACK: In the future, build a class to hold the data instead.
rawData = [None, None, None, None, None] #Ugly hack to make the numbers line up nicely.
for channel in active_channels:
    rawData[channel] = scope.get_data_ascii(channel)


wavelengthLog = laser.wavelength_logging()
wavelengthLogSize = laser.wavelength_logging_number()

#Optional Save Raw Data
if save_raw_data:
    print("Saving raw data.")
    for channel in active_channels:
        with open(folderPath / "CHAN{}_Raw.txt".format(channel), "w") as out:
            out.write(str(rawData[channel]))
    with open(folderPath / "Wavelength_Log.txt", "w") as out:
        out.write(str(wavelengthLog))

# ---------------------------------------------------------------------------- #
# Process Data
# ---------------------------------------------------------------------------- #
print("Processing Data")
analysis = WavelengthAnalyzer(
    sample_rate = sample_rate,
    wavelength_log = wavelengthLog,
    trigger_data = rawData[trigger_channel]
)

print('=' * 30)
print("Expected number of wavelength points: " + str(int(wavelengthLogSize)))
print("Measured number of wavelength points: " + str(analysis.num_peaks()))
print('=' * 30)

#HACK: In the future, build a class to hold the data instead.
data = [None, None, None, None, None] #Really ugly hack to make index numbers line up.
for channel in active_channels:
    data[channel] = analysis.process_data(rawData[channel])

print("Raw Datasets: {}".format(len(rawData)))
print("Datasets Returned: {}".format((len(data))))

# ---------------------------------------------------------------------------- #
# Generate Visuals & Save Data
# ---------------------------------------------------------------------------- #
for channel in active_channels:
    if (channel != trigger_channel):
        print("Displaying data for channel " + str(channel))
        VisualizeData(folderPath, filename, channel, **(data[channel]))
