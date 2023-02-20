import os
from dotenv import load_dotenv
import requests
load_dotenv()
APP = os.getenv("APP_ID")
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("GUILD_ID")

url = f"https://discord.com/api/v10/applications/{APP}/guilds/{GUILD}/commands"

commands = [
    {
        "name": "ark",
        "description": "Create a registration form for Ark Of Osiris",
        "type": 1,
        "options": [
            {
                "name": "time_and_day",
                "description": "Time and day eg: 15:00 Saturday 15 November)",
                "required": True,
                "type": 3, 
            },
        ],
    }
]


                                
                         

for command in commands:
    # This create or update the slash commands
    headers = { "Authorization": f"Bot {TOKEN}" }
    response = requests.post(url, headers=headers, json=command)
    if response.status_code >= 400:
        print(response.content)
        raise Exception("Request Error!")
    else:
        print("command updated")  
