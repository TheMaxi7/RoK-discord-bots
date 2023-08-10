# HoH Slave

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
4. Packages included in `requirements.txt`

## Installing

1. Create an application and the bot following the official Discord documentation [here](https://discord.com/developers/docs/intro);
2. Add the bot to your server (suggested to test it in a Test Server before using it in the real server);
3. Change the `.env` file values according to the Discord documentation;
4. Change the values in the `utils.py` file to connect the bot to the spreadsheet you want;
5. Start using it.

## Important notes

Attach a screenshot of your Hall of Heroes to get the following response: 

If the user attaches the picture and in the same message writes `Register <player ID>` the deads will be registered in a google spreadsheet.

## Features

Since this bot uses a trained model it can extract text from different size images without any problem. Keep in mind it is not perfect and it can be improved. 

## Contact and Support

For any bugs or any suggestions feel free to join my [test discord server](https://discord.gg/EH7QhwxqkW), add me on discord (@TheMaxi7) or simply open an issue.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/Altaro97/Discord-Bots/blob/main/LICENSE) file for details
