# CS4010 Project

This is the repo for our project in CS4010.

Our problem statement is ...

# Table of Contents

- [Setup Guide](#setup-guide)
- [Tools and Technologies](#tools-and-technologies)

# Setup Guide

## Prerequistes

You need to have this installed.

- Git
- Docker
- Docker Compose
- Docker desktop (Optional, if you want a GUI)
- MongoDB Compass
- Python packages:
    - ZipFile
    - PySpark

## Setup

Clone this repository. Do this with: `git clone git@github.com:hevos93/CS4010.git`

Navigate to the cloned git folder using a shell on Linux or by using Powershell on Windows. When you are in the project folder, there is a compressed file called "container-data.zip". This needs to be decompressed, do this with: 

- `python3 decompress.py`


Then you need to start the containers by utilizing Docker Compose.

- `docker compose up -d`

After the images has been downloaded and started, it is possible to check the status of the containers using:

- `docker ps -a`

Or by entering docker desktop and looking at the running containers using the GUI.


## Push changes

When you are going to push your changes, remember to compress the container-data folder with:

- `python3 compress.py`

# Tools and Technologies

- Python
- MongoDB
- Spark
