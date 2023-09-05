import discord
import asyncio
import os
import io
import json
import numpy as np
from dotenv import load_dotenv
from discord.ext import commands
from PIL import Image
from extractor import extract_info_from_image, PATH_TO_JSON

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('GUILD_ID')
THUMBNAIL_URL = "https://cdn.discordapp.com/attachments/1076154233197445201/1148652776713375785/scholar.png"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)
objDiscordGuildID = discord.Object(id=int(GUILD))
bot.remove_command("help")

async def add_new_question(message):
    """
    Add a new question and answer to the JSON file.

    Args:
        message (discord.Message): The message containing the question and answer.
    """
    if message.author == bot.user:
        return

    if message.content.lower().startswith("add new"):
        content = message.content[len("add new"):].strip() 
        parts = content.split(";")

        if len(parts) == 2:
            question = parts[0].strip()
            answer = parts[1].strip()
            
            try:
                with open(PATH_TO_JSON, 'r') as file:
                    question_answer_pairs = json.load(file)
            except FileNotFoundError:
                question_answer_pairs = [] 

            question_answer_pairs.append({"question": question, "answer": answer})

            with open(PATH_TO_JSON, 'w') as file:
                json.dump(question_answer_pairs, file)

            await message.channel.send(f"Question and answer added successfully.")
        else:
            await message.channel.send("Invalid format. Please use 'add new question;answer'.")

async def send_embed(question, answer, channel=None, author=None, author_id=None):
    """
    Send an embedded message with question and answer information.

    Args:
        question (str): Question extracted from an image.
        answer (str): Answer to the question from the database.
        channel (discord.TextChannel, optional): Channel to send the message to. Defaults to None.
        author (discord.User, optional): Author of the message. Defaults to None.
        author_id (int, optional): Author's ID. Defaults to None.
    """
    if question is not None and answer is not None:
        user = await bot.fetch_user(author_id)
        userpfp = user.avatar if user.avatar else "https://media.discordapp.net/attachments/1076154233197445201/1127610236744773792/discord-black-icon-1.png"

        embed = discord.Embed(color=0xf90101)
        embed.title = ":mortar_board: Peerless Slave :mortar_board:"
        embed.set_author(name="TheMaxi7", url="https://github.com/TheMaxi7", icon_url="https://avatars.githubusercontent.com/u/102146744?v=4")
        embed.set_thumbnail(url=f"{THUMBNAIL_URL}")
        embed.add_field(name=":question: Question:", value=question, inline=False)
        embed.add_field(name=":white_check_mark: Answer:", value=answer, inline=False)
        embed.set_footer(text=f"Requested by @{author.name}", icon_url=f"{userpfp}")

        if channel is None:
            raise ValueError("Channel is not specified.")
        
        await channel.send(embed=embed)    
    else:
        await channel.send(f"Sorry {author.mention}, I don't know the answer to that question.")
        
        if channel is None:
            raise ValueError("Channel is not specified.")
        
        await channel.send(f"Sorry {author.mention}, could not get any data from this pic. Please resend with better quality.")

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
    if message.content.lower().startswith("add new"):
        await add_new_question(message)

    if message.attachments:
        for attachment in message.attachments:
            if attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                await message.channel.send(f"Processing {message.author.mention}'s image...")
                image_bytes = await attachment.read() 
                image = Image.open(io.BytesIO(image_bytes))
                image_np = np.array(image)
                question, answer = extract_info_from_image(image_np)
                if question == "Error" and answer == "Error":
                    await message.channel.send(f"Poor quality image, can not process.")
                    break
                elif question == "Missing" and answer == "Missing":
                    await message.channel.send(f"Sorry, i dont know the answer to this question.")
                    break
                await send_embed(question, answer, message.channel, message.author, message.author.id)
            else:
                await message.channel.send(f"I can only process images, try again.")

async def main():
    await bot.start(TOKEN, reconnect=True)

asyncio.run(main())