# AsyncTGBots
## Task: Develop database scheme and several interfaces for interaction with it
## Solution: Database consists of all the necessary tables which reflects data about e-commerce shop. Client, courier and owner bots provide intraction using all the resources of the database.
## Repository structure:
* ```Dockerfile-clbot```. ```Dockerfile-crbot```, ```Dockerfile-owbot```: dockerfiles for creating images for every telegram bot
* ```Dockerfile-psql```: dockerfile for creating postgres image
* ```client_bot.py```, ```courier_bot.py```, ```owner_bot.py```: telegram bots source files
* ```requirements.txt```: all the requirements important to install for proper bots working
* ```ini.sql```: SQL script that runs for the first time to create a database scheme
* ```docker-compose.yaml```: YAML configuration for containers orchestration
## Install/Run: 
* Git clone the repository
* Create your own ```.env``` secret file and define such variables: ```CLIENT_BOT_TOKEN=...``` ```OWNER_BOT_TOKEN=...``` ```COURIER_BOT_TOKEN=...``` ```PASSWORD=... - Password for Postgresql Database```
* Run ```docker-compose up``` command
## Database Scheme
![DBScheme](/assets/ShopDBscheme.png)
