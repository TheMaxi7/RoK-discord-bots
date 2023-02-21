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


@bot.hybrid_command(name="ark")
async def user_command(ctx):
    interaction: discord.Interaction = ctx.interaction
    data = interaction.data
    options = data["options"]
    option = options[0]
    value = option["value"]
    text_entered = value.split(" ")
    match_time = text_entered[0]
    match_day = text_entered[1]
    day_number = text_entered[2]
    month = text_entered[3]
    accepted_users = []
    denied_users = []
    in_doubt_users = []
    reacted_users = {}
    embed = discord.Embed(color=0xa30000, title="TLG Ark of Osiris", description=match_time+" "+match_day+" "+ day_number+" "+month)
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/1015409348022898720/1058154316449447986/2359_battle_pfp_14.png?width=810&height=810")
    embed.add_field(name="✅Accepted", value="\u200b", inline=True)
    embed.add_field(name="❌Declined", value="\u200b", inline=True)
    embed.add_field(name="❔In doubt", value="\u200b", inline=True)
    message = await ctx.send(embed=embed)
    await message.add_reaction("✅")
    await message.add_reaction("❌")
    await message.add_reaction("❔")

    def check(reaction, user):
        if user == bot.user or reaction.message.id != message.id:
            return False
        if user.id in reacted_users and reacted_users[user.id] == reaction.emoji:
            return False
        return True

    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=172800, check=check)
        except asyncio.TimeoutError:
            embed= discord.Embed(title = "Registered players", description="Following players make sure to be in TLG before Friday reset to be registered:")
            for x in accepted_users:
                embed.add_field(name=x, value=" ")
            await ctx.send(embed=embed)
            break

  
        if user.id in reacted_users:

            prev_reaction = reacted_users[user.id]
            if prev_reaction != reaction.emoji:
                if prev_reaction == "✅":
                    accepted_users.remove(user.name)
                elif prev_reaction == "❌":
                    denied_users.remove(user.name)
                elif prev_reaction == "❔":
                    in_doubt_users.remove(user.name)
                    

            await message.remove_reaction(prev_reaction, user)


        reacted_users[user.id] = reaction.emoji

        if reaction.emoji == "✅":
            accepted_users.append(user.name)
        elif reaction.emoji == "❌":
            denied_users.append(user.name)
        elif reaction.emoji == "❔":
            in_doubt_users.append(user.name)

        embed.set_field_at(0, name="✅Accepted", value=", ".join(accepted_users), inline=True)
        embed.set_field_at(1, name="❌Declined", value=", ".join(denied_users), inline=True)
        embed.set_field_at(2, name="❔In doubt", value=", ".join(in_doubt_users), inline=True)

        await message.edit(embed=embed)

@bot.event
async def on_message(msg = discord.Message):
    content = msg.content
    if content == "close":
        await bot.close()

     
async def main():
    await bot.start(TOKEN, reconnect=True)

asyncio.run(main())


