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

Installs the latest version.

```
    pip install mdssdk
    export NET_TEXTFSM=$HOME/mdssdk-templates/
```

### From github:

```
   git clone https://github.com/Cisco-SAN/mdssdk.git
   cd mdssdk
   python setup.py install
   pip install -r requirements.txt
   export NET_TEXTFSM=$HOME/mdssdk-templates/
```

> ### Note:
> * `mdssdk` requires `NET_TEXTFSM` environment variable to be set
> * This variable points to the directory where the textfsm templates are copied to
> * To set the env please execute the below command after installing `mdssdk`
>> `export NET_TEXTFSM=$HOME/mdssdk-templates/`
> * It is recommended that you add this env permanently into your `.bashrc` or `.cshrc` file

## Uninstallation Steps

To uninstall mdssdk,

       pip uninstall mdssdk

## Documentation

* http://mdssdk.readthedocs.io


