# Maxi's Slave

This is a open source discord bot built to help user registration in Rise of Kingdoms events such as Ark of Osiris game mode.
It creates a list of registered users using reactions.

## Required 

1. Python3
2. `.env` file containing:
	```
	APPLICATION_ID=XXX
	GUILD_ID=XXX
	DISCORD_TOKEN=XXX
	```
3. Following packages:
	- python-dotenv;
	- discord.py;

## Installing

1. Create an application and the bot following the official Discord documentation [here](https://discord.com/developers/docs/intro);
2. Add the bot to your server (suggested to test it in a Test Server before using it);
3. Change the `.env` file values according to the Discord documentation;
4. Change the values in the `ark.py` file to as you want. Free to change emojis, field names etc;
5. Start using it.

## How to use

At this stage, use the `/ark` command and enter time of the match, day of the match, day number of the match and month. Then press enter to start the event.
Now users can react to it, based on which reaction they choose, they will be added to the respective column.
At the end of the timout, the bot will automatically send an embed with the list of registered users.


## Features

- `/ark` command, creates "reaction collector" event for events;
- `close` message to force close;

## Upcoming Features



## Contact and Support

For any bugs or any suggestions feel free to contact me in Discord (Vulcan Maxi#7453).

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/Altaro97/Discord-Bots/blob/main/LICENSE) file for details



