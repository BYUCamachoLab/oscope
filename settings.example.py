"""Settings for the experiment.

This file contains the settings that are used in the experiment.
All variables are imported into main.

Make sure this file is named "settings.py" so it will be imported.
By default it should be named "settings.example.py" so as to not overwrite
existing settings when updating.

"""
#Laser Sweep
lambda_start    = 1550
lambda_stop     = 1630
duration        = 15
trigger_step    = 0.01
power_dBm       = 12
#Data Collection
sample_rate     = 1e09
buffer          = 2 #Additional time around duration to prevent timeout.

#Save Data
#The first argument passed will be used as the file name.
filename_prefix = ""
filename_suffix = "data_now"
data_directory  = "measurements/"
append_date     = True #Appends date to the beginning of the directory.
save_raw_data   = True #Save raw data collected from devices.

#Oscilloscope
scope_IP        = "10.32.112.140" #Oscilloscope IP Address
take_screenshot = True
active_channels = [1,2,3] #Channels to activate and use.
trigger_channel = 1 #Channel for trigger signal.
trigger_level   = 1 #Voltage threshold for postitive slope edge trigger.
channel_setting = {
    #Additional settings to pass to each channel if used.
    1: {"range": 10}, 
    2: {"range": 0.85, "position": -2},
    3: {"range": 0.24, "position": -4.2},
    4: {"range": 0.5}
}