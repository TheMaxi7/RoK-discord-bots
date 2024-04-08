import os
import requests
from dotenv import load_dotenv

load_dotenv()

APP = os.getenv("APPLICATION_ID")
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("GUILD_ID")

url = f"https://discord.com/api/v10/applications/{APP}/guilds/{GUILD}/commands"

commands = [
    {
        "name": "stats",
        "description": "Display your KvK stats if you followed markers :D",
        "type": 1,
        "options": [
            {
                "name": "governor_id",
                "description": "The governor ID",
                "required": True,
                "type": 4,
            },
        ],
    },
    {
        "name": "top",
        "description": "Display KvK stats of top X by power",
        "type": 1,
        "options": [
            {
                "name": "rank",
                "description": "How many ranks",
                "required": True,
                "type": 4,
            },
        ],
    },
    {
        "name": "help",
        "description": "Show commands list",
        "type": 1,
    },
]

# To update commands
for command in commands:
    # This creates or updates the slash commands
    headers = {"Authorization": f"Bot {TOKEN}"}
    response = requests.post(url, headers=headers, json=command)
    if response.status_code >= 400:
        print(response.content)
        raise Exception("Request Error!")
    else:
        print("Command updated")
