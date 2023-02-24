import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('GUILD_ID')
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True  # Add this line
bot = commands.Bot(command_prefix="/", intents=intents)
objDiscordGuildID = discord.Object(id=int(GUILD))
accepted_players=[]

async def send_signup(channel:None, match_time:str, match_day:str, day_number:str, month:str, accepted:list):
    accepted_users = []
    denied_users = []
    count = 0
    reacted_users = {}
    await channel.send("@Verified\nReact to be added to respective column\n")
    embed = discord.Embed(color=0xa30000, title="TLG Ark of Osiris", description="@Verified\n"+match_time+" "+match_day+" "+ day_number+" "+month)
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/1015409348022898720/1058154316449447986/2359_battle_pfp_14.png?width=810&height=810")
    embed.add_field(name=f"✅ ACCEPTED {count}/30", value="\u200b", inline=True)
    embed.add_field(name="❌ DECLINED", value="\u200b", inline=True)
    message = await channel.send(embed=embed)
    await message.add_reaction("✅")
    await message.add_reaction("❌")

    def check(reaction, user):
        if user == bot.user or reaction.message.id != message.id:
            return False
        if user.id in reacted_users and reacted_users[user.id] == reaction.emoji:
            return False
        return True

    while True:
        reaction, user = await bot.wait_for('reaction_add', check=check)
        if user.id in reacted_users:

            prev_reaction = reacted_users[user.id]
            if prev_reaction != reaction.emoji:
                if prev_reaction == "✅":
                    accepted_users.remove(user.name)
                    accepted.remove(user.name)
                    count -=1
                elif prev_reaction == "❌":
                    denied_users.remove(user.name)

            await message.remove_reaction(prev_reaction, user)


        reacted_users[user.id] = reaction.emoji

        if reaction.emoji == "✅":
            accepted_users.append(user.name)
            accepted.append(user.name)
            count +=1
        elif reaction.emoji == "❌":
            denied_users.append(user.name)

        embed.set_field_at(0, name=f"✅ ACCEPTED {count}/30", value=", ".join(accepted_users), inline=True)
        embed.set_field_at(1, name="❌ DECLINED", value=", ".join(denied_users), inline=True)

        await message.edit(embed=embed)

async def send_accepted_players(accepted:list,channel=None):
    #embed = discord.Embed(color=0xa30000, title="TLG Ark of Osiris", description="Following players make sure to be in TLG before Thursday reset for registration:")
    #embed.add_field(name=" ", value=" ", inline=True)
    await channel.send("@verified")
    await channel.send("Following players make sure to be in TLG before Thursday reset for registration:\n\n")
    for x in accepted:
        #embed.set_field_at(0, name=" ", value=", ".join(x), inline=True)
        await channel.send(f"➢ {x}\n") #channel.send(embed=embed)

@bot.event
async def on_message(msg = discord.Message):
    content = msg.content
    channel=msg.channel
    if msg.content.startswith('Ark'):
        event_details=msg.content.split(" ")
        match_time = event_details[1]
        match_day = event_details[2]
        day_number = event_details[3]
        month = event_details[4]
        await send_signup(channel, match_time, match_day, day_number, month,accepted_players)
    elif content == "close signup":
        await send_accepted_players(accepted_players,channel=channel)
        await bot.close()
     
async def main():
    await bot.start(TOKEN, reconnect=True)

asyncio.run(main())




