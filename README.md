# Python SDK/API library for Cisco MDS Switches.

![Python](https://img.shields.io/badge/python-v3.6+-blue.svg)
[![](https://img.shields.io/pypi/v/mdssdk.svg)](https://pypi.python.org/pypi/mdssdk)
[![Documentation Status](https://readthedocs.org/projects/mdssdk/badge/?version=latest)](http://mdssdk.readthedocs.io/en/latest/?badge=latest)

This library will be useful for automating day to day tasks or developing new tools which involve Cisco MDS switches

* Python version: 3.6 and above
* Supports both NXAPI and SSH
* Limited support for N9K and FI 
* Apache License, Version 2.0 (the "License")

## Installation Steps

### From pip:

Installs the last released version,

```
    pip install mdssdk
```

### From github:
   
1) Download the zip file from the github

       wget https://github.com/Cisco-SAN/mdssdk/archive/master.zip

2) Unzip the file

       unzip master.zip 

3) Execute `source install.sh`

       cd mdssdk-master/
       source install.sh
       or
       source ./install.sh
       or 
       . ./install.sh

4) Once successfully done issue `pip list` and you should see mdssdk package installed

        >>> pip list
        Package    Version   
        ---------- ----------
        .
        . 
        mdssdk     1.3.1       <---
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
| 9.2(1) and below | v1.3.1 |
| 8.5(1) and below | v1.2.0 |
| 8.4(2b) and below | v1.1.0 |
| 8.4(2a) and below | v1.0.1 |

