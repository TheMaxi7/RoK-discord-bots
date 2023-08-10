import discord
import asyncio
import os
from dotenv import load_dotenv
from discord.ext import commands
from PIL import Image
import aiohttp
import io
from extractor import extract_deads
from util import Spreadsheet


load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('GUILD_ID')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)
objDiscordGuildID = discord.Object(id=int(GUILD))

bot.remove_command("help")
sheet = Spreadsheet()

async def send_embed(t4_deads, t5_deads, description, channel=None, author=None, author_id=None, player_id=None):
    if t4_deads is not None and t5_deads is not None and description is not None:
        
        if player_id:
            description += f"\nConfirmed registration to Governor ID: {player_id}"
            sheet.register_stats(t4_deads, t5_deads, player_id)
        user = await bot.fetch_user(author_id)
        if user.avatar:
            userpfp = user.avatar
        else:
            userpfp = "https://media.discordapp.net/attachments/1076154233197445201/1127610236744773792/discord-black-icon-1.png"


        embed = discord.Embed(color=0xf90101)
        embed.title = "Hall of Heroes"
        
        embed.set_thumbnail(url=f"{userpfp}")
        embed.description = description
        embed.add_field(name="TOT T4 DEAD", value=t4_deads, inline=True)
        embed.add_field(name="TOT T5 DEAD", value=t5_deads, inline=True)     
        embed.set_footer(text="Bot by @themaxi7") 
        
        if channel is None:
            raise ValueError("Channel is not specified.")
        
        await channel.send(embed=embed)
        
    else:
        if channel is None:
            raise ValueError("Channel is not specified.")
        
        await channel.send(f"Sorry {author.mention}, could not get any data from this pic. Pls resend with better quality.")

@bot.event
async def on_message(message):
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