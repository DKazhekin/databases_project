# AsyncTGBots
## Task: Develop database scheme and several interfaces for interaction with it
## Solution: Database consists of all the necessary tables which reflects data about e-commerce shop. Client, courier and owner bots provide intraction using all the resources of the database.
## Install/Run: 
* Git clone the repository
* Create your own ```.env``` secret file and define such variables: ```CLIENT_BOT_TOKEN=...``` ```OWNER_BOT_TOKEN=...``` ```COURIER_BOT_TOKEN=...``` ```PASSWORD=... - Password for Postgresql Database```
* Run ```docker-compose up``` command
