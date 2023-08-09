# BugBear's Slave

This is a open source discord bot that uses [rokstats.online](https://rokstats.online/) API to get all the stats.
For the moment it uses only on message commands to work.

## Required 

1. Python3
2. `.env` file containing:
	```
	APPLICATION_ID=XXX
	GUILD_ID=XXX
	DISCORD_TOKEN=XXX
	...
	```
3. `service_account.json` file to work with gspread package. 
4. Following packages:
	- gspread:
	- python-dotenv;
	- discord.py;
	- requests;
	- StringProgressBar

## Installing

1. Create an application and the bot following the official Discord documentation [here](https://discord.com/developers/docs/intro);
2. Add the bot to your server (suggested to test it in a Test Server before using it);
3. Change the `.env` file values according to the Discord documentation;
4. Change the values in the `sheets.py` file to connect the bot to the spreadsheet you want;
5. Start using it.

## Important notes

Write `stats <player ID>`  to get the following response: 

![Screenshot 2023-07-08 120559](https://github.com/TheMaxi7/RoK-discord-bots/assets/102146744/d5e15db0-5449-4de7-8041-72c975adaaad)

If you want to show different informations then you will need to modify the `slave.py` file.

## Features

This bot is completely different from all the others because it uses APIs to get players data. It is still in beta and the API service + stats tracking is fully offered by @ibugbear.

## Contact and Support

For any bugs or any suggestions feel free to join my [test discord server](https://discord.gg/EH7QhwxqkW), add me on discord (@TheMaxi7) or simply open an issue.
For any questions regarding the stats tracking or APIs reach out to @ibugbear on Discord. 

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/Altaro97/Discord-Bots/blob/main/LICENSE) file for details



