# Python SDK/API library for Cisco MDS Switches.

![Python](https://img.shields.io/badge/python-v3.6+-blue.svg)

This library will be useful for automating day to day tasks or developing new tools which involve Cisco MDS switches

* Python version: 3.6 and above
* Supports both NXAPI and SSH 
* Apache License, Version 2.0 (the "License")


## Installation Steps
1) First create a virtual environment with python3

       virtualenv testmdssdk -p python3

2) Activate the virtual env

       cd testmdssdk/
       source bin/activate
       
3) Next download the zip file from the github 

       wget https://github.com/Cisco-SAN/mdssdk/archive/master.zip
       
4) Unzip the file

       unzip master.zip 
           
5) Execute `source install.sh` 
       
       cd mdssdk-master/
       source install.sh
       or
       source ./install.sh
       or 
       . ./install.sh
       
6) Once successfully done issue `pip list` and you should see mdssdk package installed
                           
        >>> pip list
        Package    Version   
        ---------- ----------
        .
        . 
        mdssdk     1.0.1       <---
        .
        .
        
        
## Uninstallation Steps

To uninstall mdssdk,

       pip uninstall mdssdk
       

## Documentation

* http://mdssdk.readthedocs.io

## Support Matrix

|**NXOS Version**|**SDK Version** |
| :------: | :------:  |
| 8.4(2b) and below | 1.0.2 |
| 8.4(2a) and below | 1.0.1 |
