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
4. All the packages included in `requirements.txt`

## Installing

1. Create an application and the bot following the official Discord documentation [here](https://discord.com/developers/docs/intro);
2. Add the bot to your server (suggested to test it in a Test Server before using it);
3. Change the `.env` file values according to the Discord documentation;
4. Change the values in the `sheets.py` file to connect the bot to the spreadsheet you want (how to create your `service_account.json` file [here](https://docs.gspread.org/en/v5.9.0/oauth2.html));
5. Start using it.

## Important notes

Given the `/stats` command + the ingame player ID, gives the following output: 

![Screenshot 2023-08-27 133759](https://github.com/TheMaxi7/RoK-discord-bots/assets/102146744/b7921f06-e91e-42f1-8e85-41507c186faa)


With a spreadsheet organized with the following columns: 

![Sheet](https://user-images.githubusercontent.com/102146744/216849022-f586aced-15f6-4c60-85f4-941790f08d88.png)

If you want to show different informations then you will need to modify the `StatsTracker.py` file.

`/top` prints following message: 

![Screenshot 2023-02-17 220011](https://user-images.githubusercontent.com/102146744/219792492-e71a3332-ab52-49fe-93da-c6620081c1ea.png)


## Features

- `/stats` command, given player ID prints KvK stats of that specific player. Also binds discord ID to that rok ID;
- `stats` message prints KvK stats of the ID curently binded to your discord ID;
- `stats <governor ID>` message is like the `/stats` command. Users can simply write a message to get both their stats and their ID registered for future uses;
- `/top` command, given ranks, prints cumulated kingdom stats;
- `/help` command, displays list of all possible commands

## Contact and Support

If you want to reach out to me for any kind of problem/request feel free to add me on discord (@themaxi7).

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/Altaro97/Discord-Bots/blob/main/LICENSE) file for details



