import asyncio
import discord
import os
import requests
from datetime import date
from dotenv import load_dotenv
from discord.ext import commands
from sheets import DiscordDB, Requirements
from StringProgressBar import progressBar

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('GUILD_ID')
ROKSTATS_API = os.getenv('ROKSTATS_APY')

intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix="/", intents=intents)
objDiscordGuildID = discord.Object(id=int(GUILD))

discord_db = DiscordDB()
requirements = Requirements()
bot.remove_command("help")

TODAY_DATE = today = date.today()
START_DATE = "2023-07-23"
SNAPSHOT_DATE = "2023-06-28"

async def find_status(kills_percentage, deads_percentage):
    if kills_percentage >= 100 and deads_percentage >= 100:
        return "MGE Competitor"
    elif kills_percentage > 50 and deads_percentage > 100:
        return "Safe"
    elif deads_percentage > 50 and kills_percentage > 100:
        return "Safe"
    elif kills_percentage > 50 and deads_percentage < 100:
        return "Warning"
    elif deads_percentage > 50 and kills_percentage < 100:
        return "Warning"
    elif kills_percentage <= 100 and deads_percentage <= 100:
        return "Probation"
    else:
        return "Unknown"

async def check_id(gov_id: int):
    url = f"https://rokstats.online/api/governor/{gov_id}/summary?apiKey={ROKSTATS_API}&startDate={START_DATE}&endDate={TODAY_DATE}&initialSnapshotDate={SNAPSHOT_DATE}"
    response = requests.get(url)
    data = response.json()
    return data if data else False

async def send_id_stats(response, author_id, interaction: discord.Interaction=None, channel=None):
 
    last_scan = response['SnapshotTime']
    date_only = last_scan.split('T')[0]
    gov_id = response['GovernorId']
    name = response['Name']
    alliance = response['Alliance']
    kp = response["KillPoints"]["Total"]
    totdeads = response["Dead"]
    power = response['Power']
    initial_snapshot_data = response['initialSnapshot']
    power_initial_snapshot = initial_snapshot_data.get('Power')
    CurrentT4 = response["killPointsDiff"]["T4"]
    CurrentT5 = response["killPointsDiff"]["T5"]
    CurrentDeads = response["deadDiff"]
    CurrentKills = int(CurrentT4) + int(CurrentT5)
    kill_req, deads_req = requirements.find_requirements(power_initial_snapshot)

    kills_percentage = CurrentKills * 100 // int(kill_req)
    deads_percentage = CurrentDeads * 100 // int(deads_req)
    player_status = await find_status(kills_percentage, deads_percentage)

    total = 100
    size = 15
    killsbar = progressBar.filledBar(total, kills_percentage, size)
    deadsbar = progressBar.filledBar(total, int(deads_percentage), size)
    
    if response:
        embed = discord.Embed(color=0x00ffe5)
        embed.title = f"KvK Personal stats"
        embed.set_thumbnail(url=f"https://rokstats.online/img/governors/{gov_id}.jpg")
        description = f"Governor: {name if name else '0'}\nPower snapshot: {power_initial_snapshot if power_initial_snapshot else '0'}\nCurrent power: {power if power else '0'}\nGovernor ID: {gov_id if gov_id else '0'}\nAlliance: {alliance if alliance else '0'}\nAccount KP: {kp if kp else '0'}\nAccount deads: {totdeads if totdeads else '0'}\nAccount status: {player_status if player_status else '0'}\n"

        embed.description = description

        embed.add_field(name="KILLS REQUIRED", value=kill_req, inline=True)
        embed.add_field(name="DEADS REQUIRED", value=deads_req, inline=True)

        embed.add_field(name="CURRENT KILLS", value=f"{CurrentKills}\n{killsbar[0]}   {int(killsbar[1])}%", inline=False)
        embed.add_field(name="CURRENT DEADS", value=f"{CurrentDeads}\n{deadsbar[0]}   {int(deadsbar[1])}%", inline=False)

        embed.set_footer(text=f"Scan date: {date_only}\n\nData from www.rokstats.online made by @ibugbear\nBot by @themaxi7")

        if interaction:
            await interaction.response.send_message(embed=embed)
        elif channel:
            await channel.send(embed=embed)
    else:
        if interaction:
            await interaction.response.send_message("Bro, this ID does not exist", ephemeral=True)
        elif channel:
            await channel.send("Bro, this ID does not exist", ephemeral=True)


@bot.event
async def on_message(msg: discord.Message):
    author=msg.author
    author_id = author.id
    content = msg.content
    channel = msg.channel

    content = content.split(" ")
    if len(content) == 1:
        request = content[0].lower()
        if request == "stats":
            id_from_db = discord_db.get_id_from_discord(author_id=author_id)
            if id_from_db:
               url=f"https://rokstats.online/api/governor/{id_from_db}/summary?apiKey={ROKSTATS_API}&startDate={START_DATE}&endDate={TODAY_DATE}&initialSnapshotDate={SNAPSHOT_DATE}"
               response = requests.get(url)
               await send_id_stats(response.json(), channel=channel, author_id=int(author_id))
            else:
                await channel.send(content = "Your ID has not been registered yet. Write 'stats <your id>' to save your ID before using 'stats'. (Example: Stats 12345678)")
    elif len(content) == 2:
        request = content[0].lower()
        id = content[1]
        if request == "stats" and id:
            try:
                player_id = int(id)
            except Exception as e:
                print(e)
            response = await check_id(player_id)
            if response is not False:
                await send_id_stats(response, channel=channel, author_id=int(author_id))
                await discord_db.save_dc_id(author_id, player_id)
            else:
                await channel.send("Bro, this ID does not exist")


async def main():
    await bot.start(TOKEN, reconnect=True)

asyncio.run(main())

