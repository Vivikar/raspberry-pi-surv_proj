# Raspberri Pi Smart Surveillance Camera
Repository containing code and description of Pi project

## Prerequisites

What libraries you'll need to install the software
```
$ sudo apt-get update
$ sudo apt-get upgrade

$ pip install pyTelegramBotAPI
$ pip  install numpy
$ pip install --user imutils
$ sudo apt-get install python-picamera python3-picamera

$ sudo apt-get install mysql-server

```
You'll also need opencv installed on your machine. You can see how to do that [here](https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/)

## Installing
To get this project working you'll need to download and install it on your raspberry pi. Project location sholuld be next:
```
/
├── ...
├── home                      # home directory
│   ├── surv_project          # folder containing main files
|   |   ├──detect_frames
|   │   ├──moovm_det.py 
|   │   ├──bot                #bot.py and conf files
│   |   |   ├──bot.py
│   |   |   ├──conf.json
│   |   |   ├──conf.py
│   |   |   ├──...
│   |   ├──...
└── ...
```
## Usage
After initializing a new conversation with a bot you'll see next menu:
<img align="center" src="https://github.com/Vivikar/raspberry-pi-surv_proj/blob/master/readme_data/main_menu.jpg" width="300">  
Send photo 📷 - send captured frame to user  
Send video 🎥 - opens new menu, where you can choose lenght of viedo to be sent    
<img align="center" src="https://github.com/Vivikar/raspberry-pi-surv_proj/blob/master/readme_data/photo_2018-09-07_17-34-44.jpg" width="300">  
Save images 📁 - saves all images from MySQL table to local directory  
Pi Settings ⚙ - opens new menu with Pi Settings    
<img align="center" src="https://github.com/Vivikar/raspberry-pi-surv_proj/blob/master/readme_data/photo_2018-09-07_17-18-08.jpg" width="300">  

Delete temp files 🗑 - deletes all files from detect_frames folder (deleting temp data of current surveillance)  
Truncate SQL table ✂ - deletes all images from SQL table (deleting data of all surveillances)  

## Examples of work  
<img align="center" src="https://github.com/Vivikar/raspberry-pi-surv_proj/blob/master/readme_data/photo_2018-09-07_17-18-28.jpg" width="300">    
<img align="center" src="https://github.com/Vivikar/raspberry-pi-surv_proj/blob/master/readme_data/photo_2018-09-07_17-17-43.jpg" width="300">    
<img align="center" src="https://github.com/Vivikar/raspberry-pi-surv_proj/blob/master/readme_data/photo_2018-09-07_17-17-57.jpg" width="300">    

Under each sent frame, there is button: "Get full photo". If pressed, the original, uncropped version of that frame is extracted from SQL table and sent to user  

<img align="center" src="https://github.com/Vivikar/raspberry-pi-surv_proj/blob/master/readme_data/photo_2018-09-07_17-18-03.jpg" width="300">    
