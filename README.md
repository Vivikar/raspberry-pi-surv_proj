# Raspberri Pi Smart Surveillance Camera
Repository containing code and description of Pi project

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What libraries you'll need to install the software
```
$ sudo apt-get update
$ sudo apt-get upgrade

$ pip install pyTelegramBotAPI
$ pip  install numpy
$ pip install --user imutils
$ sudo apt-get install python-picamera python3-picamera

$sudo apt-get update
$sudo apt-get install mysql-server

```
You'll also need opencv installed on your machine. You can see how to do that [here](https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/)

### Installing
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
<img align="right" src="https://github.com/Vivikar/raspberry-pi-surv_proj/blob/master/readme_data/main_menu.jpg" width="100">
## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


