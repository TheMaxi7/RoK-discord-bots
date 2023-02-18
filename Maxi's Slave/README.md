# Maxi's Slave

This is a open source discord bot built to help tracking Rise Of Kingdoms KvK data for your kingdom using `/` commands. 
For the moment there is only one command, may add more in future.

## Required 

1. Python3
2. `.env` file containing:
	```
	APPLICATION_ID=XXX
	GUILD_ID=XXX
	DISCORD_TOKEN=XXX
	```
3. `service_account.json` file to work with gspread package. 
4. Following packages:
	- gspread:
	- python-dotenv;
	- discord.py;
	- requests.

## Installing

1. Create an application and the bot following the official Discord documentation [here](https://discord.com/developers/docs/intro);
2. Add the bot to your server (suggested to test it in a Test Server before using it);
3. Change the `.env` file values according to the Discord documentation;
4. Change the values in the `sheets.py` file to connect the bot to the spreadsheet you want;
5. Start using it.

## Important notes

Given the `/stats` command + the ingame player ID, gives the following output: 

![Output](https://user-images.githubusercontent.com/102146744/216848991-9e62e4dc-cf14-4125-b393-639ad551c660.png)

With a spreadsheet organized with the following columns: 

![Sheet](https://user-images.githubusercontent.com/102146744/216849022-f586aced-15f6-4c60-85f4-941790f08d88.png)

If you want to show different informations then you will need to modify the `StatsTracker.py` file.

`/top` prints following message: 

![Screenshot 2023-02-17 220011](https://user-images.githubusercontent.com/102146744/219792492-e71a3332-ab52-49fe-93da-c6620081c1ea.png)


## Features

- `/stats` command, given player ID prints KvK stats of that specific player. Also binds discord ID to that rok ID;
- `stats` message prints KvK stats of the ID curently binded to your discord ID;
- `/top` command, given ranks, prints cumulated stats
- `/help` command, displays list of all possible commands

## Upcoming Features

- Whatever kd needs

## Contact and Support

For any bugs or any suggestions feel free to contact me in Discord (Vulcan Maxi#7453).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details



