# HoH Slave

This is a discord bot designed to assist kingdom leaderships in keeping track of their kingdom dead troops. The bot uses image processing and text recognition to extract information from screenshots of Hall of Heroes and then presents the information in a formatted embed within a Discord channel. In addition can write the stats extracted in a google spreadsheet.

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
5. Download and install Tesseract OCR on your machine and add it to Environment variables

## Installing

1. Create an application and the bot following the official Discord documentation [here](https://discord.com/developers/docs/intro);
2. Add the bot to your server (suggested to test it in a Test Server before using it in the real server);
3. Change the `.env` file values according to the Discord documentation;
4. Change the values in the `util.py` file to connect the bot to the spreadsheet you want (how to create your `service_account.json` file [here](https://docs.gspread.org/en/v5.9.0/oauth2.html));
5. Edit `best.pt` path in `extractor.py`;
6. Edit path to tesseract.exe in `util.py`;
7. Start using it.

## Important notes

Attach a screenshot of your Hall of Heroes to get the following response: 

![Screenshot 2023-08-27 115647](https://github.com/TheMaxi7/RoK-discord-bots/assets/102146744/1e3bd5a4-2d13-4d2b-824c-4ef4ed4e3583)


If the user attaches the picture and in the same message writes `Register <player ID>` the deads will be registered in a google spreadsheet.

## Disclaimer

Since this bot uses a trained model it can extract text from different size images but keep in mind it is not perfect and it can be improved. 

## Contact and Support

For any bugs or any suggestions feel free to join my [test discord server](https://discord.gg/EH7QhwxqkW), add me on discord (@TheMaxi7) or simply open an issue.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/Altaro97/Discord-Bots/blob/main/LICENSE) file for details
