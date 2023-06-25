

import asyncio
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from sheets import KvkStats, DiscordDB, TopX


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('GUILD_ID')
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents, help_command=None)
objDiscordGuildID = discord.Object(id=int(GUILD))
kvk_stats = KvkStats()
discord_db = DiscordDB()
topx = TopX()
bot.remove_command("help")
#This function gets data from sheets and embeds message in chat
async def send_id_stats(gov_id: int, interaction: discord.Interaction=None, channel=None):
    field_keys = ["Rank", "Kills Required", "Deads Required", "T4 Kills", "T5 Kills", "Deads"]
    footer_keys = ["Kills percentage", "Deads percentage"]  
    player_stats = kvk_stats.get_player_stats(gov_id)
    if player_stats:
        embed = discord.Embed(color=0xff6bfa) #Band color
        embed.title = f"KvK Personal stats"   #Message Title
        description = f""  #Message description
        if gov_id == 26143013:
            embed.set_image(url="https://cdn.discordapp.com/attachments/1076154233197445201/1098997553837645864/BAG32_COTTO.jpg")
        elif gov_id == 62432900:
            embed.set_image(url="https://cdn.discordapp.com/attachments/1076154233197445201/1098998640988659774/Screenshot_2023-04-21_174757.png")  # Personalized images for kd mascottes
        elif gov_id == 42365158:
            embed.set_image(url="https://cdn.discordapp.com/attachments/1076154233197445201/1098999395837546526/clown_face.png")
        keysInFooter = [] #dummy footer fields
        for header, content in player_stats.items():
            if header in field_keys:
                embed.add_field(name=header, value=content if content != "" else "No data", inline=True)
            elif header not in footer_keys:
                description += f"{header}: {content if content != '' else '0'}\n"    
            else:
                keysInFooter.append(f"{header}: {content if content != '' else '0'}")
        embed.description = description
        embed.set_footer(text=" | ".join(keysInFooter))
        if interaction:
            await interaction.response.send_message(embed=embed)
        elif channel:
            await channel.send(embed=embed)
    else:
        if interaction:
            await interaction.response.send_message(
                "Bro, this ID does not exist",
                ephemeral=True
            )
        elif channel:
            await channel.send("Bro, this ID does not exist", ephemeral=True)

async def send_top_x_stats(value:int, interaction:discord.Interaction=None, channel=None):
    top_x_stats = topx.top_x(value)
    title = f"KvK stats of Top "+ str(value) +" by power"
    fields = ["Total T4 Kills", "Total T5 Kills", "Total Deads"]
    if top_x_stats:
        embed = discord.Embed(color=0xa30000)
        embed.title= title
        embed.description = f"- Stay strapped or get clapped -"
        embed.add_field(name=fields[0], value=f"{top_x_stats[0]:,}" if top_x_stats[0] != "" else "No data", inline=True)
        embed.add_field(name=fields[1], value=f"{top_x_stats[1]:,}" if top_x_stats[1] != "" else "No data", inline=True)
        embed.add_field(name=fields[2], value=f"{top_x_stats[2]:,}" if top_x_stats[2] != "" else "No data", inline=True)
        embed.set_image(url="https://cdn.discordapp.com/attachments/917952363808059444/1075874094429524068/cropped-Kingdom-of-Alberta-2-1.png")
        if interaction:
            await interaction.response.send_message(embed=embed)
        elif channel:
            await channel.send(embed=embed)
    else:
        if interaction:
            await interaction.response.send_message("You need to enter a number greater than 0", ephemeral=True)
        elif channel:
            await channel.send("You need to enter a number greater than 0", ephemeral=True)

@bot.hybrid_command(name="stats")
async def stats(ctx):
    interaction: discord.Interaction = ctx.interaction
    author_id = interaction.user.id
    data = interaction.data
    options = data["options"]
    option = options[0]
    value = option["value"]
    player_id = None
    try:
        player_id = int(value)
    except Exception as e:
        print(e)
    if player_id :
        await send_id_stats(player_id,interaction)
        await discord_db.save_dc_id(author_id,player_id)

@bot.hybrid_command(name="top")
async def top(ctx):
    interaction: discord.Interaction = ctx.interaction
    data = interaction.data
    options = data["options"]
    option = options[0]
    value = option["value"]
    ranks = None
    try:
        ranks = int(value)
    except Exception as e:
        print (e)
    if ranks:
        if ranks > 450:
            await interaction.response.send_message("We track only top 300 players by power. Enter a value less than 300", ephemeral=True)
        else:
            await send_top_x_stats(value, interaction)
            
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
               await send_id_stats(gov_id= id_from_db, channel=channel)
            else:
                await channel.send(content = "Your ID has not been registered yet. Write 'stats <your id>' to save your ID before using 'stats'. (Example: stats 12345678)")
    elif len(content) == 2:
        request = content[0].lower()
        id = content[1]
        if request == "stats" and id:
            try:
                player_id = int(id)
            except Exception as e:
                print(e)
            if kvk_stats.get_player_stats(player_id):
                await send_id_stats(gov_id= player_id, channel=channel)
                await discord_db.save_dc_id(author_id, player_id)
            else:
                await channel.send("Bro, this ID does not exist")

@bot.hybrid_command(name="help")
async def help(ctx):
    embed = discord.Embed(title="Commands list", description=" ")
    embed.add_field(name="`/stats`", value="Shows KvK stats of the ID you enter. Also saves it for future uses")
    embed.add_field(name="`stats`", value="Shows KvK stats of the ID saved in the database for your Discord ID")
    embed.add_field(name="`/top`", value="Shows cumulated KvK stats of top X of the kingdom")
    embed.set_image(url="https://cdn.discordapp.com/attachments/1076154233197445201/1076154255108485140/7biumd.jpg")
    await ctx.send(embed=embed)

async def main():
    await bot.start(TOKEN, reconnect=True)

asyncio.run(main())
