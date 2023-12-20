import discord
import asyncio
import os
import aiohttp
import io

from dotenv import load_dotenv
from discord.ext import commands
from PIL import Image
from extractor import extract_deads
from util import Spreadsheet

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('GUILD_ID')
THUMBNAIL_URL = "https://media.discordapp.net/attachments/1186979000694870059/1186980301264666664/HallOfHeroes_thumbnail.webp?ex=6595388c&is=6582c38c&hm=101a32f909f7b47bd983c4ae99204e99ac142bc07b658ae47ed6094239703c7a&=&format=webp&width=1600&height=900"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)
objDiscordGuildID = discord.Object(id=int(GUILD))

bot.remove_command("help")
sheet = Spreadsheet()

async def send_embed(t4_deads, t5_deads, description, channel=None, author=None, author_id=None, player_id=None):
    """
    Send an embedded message with dead troop information.

    Args:
        t4_deads (int): Total T4 dead troops.
        t5_deads (int): Total T5 dead troops.
        description (str): Description of the dead troops.
        channel (discord.TextChannel, optional): Channel to send the message to. Defaults to None.
        author (discord.User, optional): Author of the message. Defaults to None.
        author_id (int, optional): Author's ID. Defaults to None.
        player_id (int, optional): Governor's player ID. Defaults to None.
    """
    if t4_deads is not None and t5_deads is not None and description is not None:
        
        if player_id:
            description += f"\nConfirmed registration to Governor ID: {player_id}"
            sheet.register_stats(t4_deads, t5_deads, player_id)
        user = await bot.fetch_user(author_id)
        if user.avatar:
            userpfp = user.avatar
        else:
            userpfp = "https://media.discordapp.net/attachments/1186979000694870059/1186979049822756958/2ead53f5d9c64c6987ff27141023b96b.jpg?ex=65953762&is=6582c262&hm=21b8fafa1e7689f7ad5df76f4dc9d775c67741ba84319758d388d5eff0990408&=&format=webp&width=512&height=512"


        embed = discord.Embed(color=0xf90101)
        embed.title = ":crossed_swords: Hall of Heroes :crossed_swords:"
        embed.set_author(name="TheMaxi7", url="https://github.com/TheMaxi7",
                             icon_url="https://avatars.githubusercontent.com/u/102146744?v=4")
        embed.set_thumbnail(url=f"{THUMBNAIL_URL}")
        embed.description = description
        embed.add_field(name="<:t4:1145292870086041640> TOT T4 DEADS", value=t4_deads, inline=True)
        embed.add_field(name="<:t5:1145292909680283778> TOT T5 DEADS", value=t5_deads, inline=True)     
        embed.set_footer(text=f"Requested by @{author.name}",
                             icon_url=f"{userpfp}")
        
        if channel is None:
            raise ValueError("Channel is not specified.")
        
        await channel.send(embed=embed)
        
    else:
        if channel is None:
            raise ValueError("Channel is not specified.")
        
        await channel.send(f"Sorry {author.mention}, could not get any data from this pic. Pls resend with better quality.")

@bot.event
async def on_message(message):
    """
    Event handler for received messages.

    Args:
        message (discord.Message): Received message.
    """
    player_id = None
    if message.author == bot.user:
        return  

    content = message.content.split()
    if len(content) == 2:
        request = content[0].lower()
        player_id = content[1]
        if request == "register":
            try:
                player_id = int(player_id)
            except ValueError as e:
                print(e)
                return  

    if message.attachments:
        for attachment in message.attachments:
            if attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                await message.channel.send(f"Processing {message.author.mention}'s image...")
                image_bytes = await attachment.read()
                image = Image.open(io.BytesIO(image_bytes))
                t4_deads, t5_deads, description = extract_deads(image)
                await send_embed(t4_deads, t5_deads, description, message.channel, message.author, message.author.id, player_id)
            else:
                await message.channel.send(f"I can only process images, try again.")

async def main():
    await bot.start(TOKEN, reconnect=True)

asyncio.run(main())