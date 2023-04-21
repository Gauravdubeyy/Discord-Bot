import discord
from discord import member
from discord import client
from discord.ext import commands
import asyncio
from random import randint
import os
import json
import sys
import datetime
import aiohttp


bot = commands.Bot(command_prefix="!", help_command=None)
#your own prefix


@bot.event
async def on_ready():
  print("Bot is running!")
  await bot.change_presence(activity=discord.Game("Playing Pokemon"))


@bot.command()
async def ping(ctx):
    embed=discord.Embed(title="Bot Ping", description=f"Pong! {round(bot.latency * 1000)}ms", color=0xFF5733)
    embed.set_footer(text=f'Requested by:\n{str(ctx.author)}',icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


@bot.command()
async def hello(ctx):
  await ctx.send("hi")

#kick command using discord.py

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member, *, reason=None):
  await user.kick(reason=reason)
  await ctx.send(f"{user} have been kicked sucessfully")

# <----- kick commmand end ------>

#Ban command using discord.py

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, *, reason=None):
  await user.ban(reason=reason)
  await ctx.send(f"{user} have been bannned sucessfully")

# <----- ban commmand end ------>

#Unban command using discord.py

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = member.split('#')

  for ban_entry in banned_users:
    user = ban_entry.user
  
  if (user.name, user.discriminator) == (member_name, member_discriminator):
    await ctx.guild.unban(user)
    await ctx.send(f"{user} have been unbanned sucessfully")
    return

# <----- unban commmand end ------>

#Say Command 
@bot.command()
async def say(ctx, *, arg):
    embed=discord.Embed(description=f"{arg}\n", color=0xFF5733)
    await ctx.send(embed=embed)

#Say command end ------------------>

#Random command 
@bot.command()
async def random(ctx):
  await ctx.send(randint(1,100))

with open('users.json', "ab+") as ab:
  ab.close()
  f = open('users.json', 'r+')
  f.readline()
  if os.stat("users.json").st_size == 0:
    f.write("{}")
    f.close()
  else:
    pass

with open('users.json', 'r') as f:
  users = json.load(f)
  
#Random command end -------------->

#Avatar Command
@bot.command()
async def avatar(ctx, *,  avamember : discord.Member=None):
    em=discord.Embed(title = "Here is your avatar", color=0xFF5733)
    em.set_image(url=avamember.avatar_url)
    em.set_footer(text=f'Requested by:\n{str(ctx.author)}',icon_url=ctx.author.avatar_url)
    await ctx.send(embed=em)

#Clean Command
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clean(ctx, limit: int):
        await ctx.channel.purge(limit=limit)
        await ctx.send('Cleared by {}'.format(ctx.author.mention))
        await ctx.message.delete()

@clean.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that!")

#Mute Command
@bot.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    embed = discord.Embed(title="muted", description=f"{member.mention} was muted ", colour=discord.Colour.orange())
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f" you have been muted from: {guild.name} reason: {reason}")

@bot.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
   mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

   await member.remove_roles(mutedRole)
   await member.send(f" you have unmutedd from: - {ctx.guild.name}")
   embed = discord.Embed(title="unmute", description=f" unmuted-{member.mention}",colour=discord.Colour.orange())
   await ctx.send(embed=embed)


@bot.command()
async def calculate(ctx):
    def check(m):
        return len(m.content) >= 1 and m.author != bot.user

    await ctx.send("Number 1: ")
    number_1 = await bot.wait_for("message", check=check)
    await ctx.send("For addition send + , for multiplication send * , for subtraction send - , for divide use /")
    operator = await bot.wait_for("message", check=check)
    await ctx.send("Number 2: ")
    number_2 = await bot.wait_for("message", check=check)
    try:
        number_1 = float(number_1.content)
        operator = operator.content
        number_2 = float(number_2.content)
    except:
        await ctx.send("invalid input")
        return
    output = None
    if operator == "+":
        output = number_1 + number_2
    elif operator == "-":
        output = number_1 - number_2
    elif operator == "/":
        output = number_1 / number_2
    elif operator == "*":
        output = number_1 * number_2
    else:
        await ctx.send("invalid input")
        return
    await ctx.send("Answer: " + str(output))



def restart_bot(): 
  os.execv(sys.executable, ['python'] + sys.argv)


@bot.command(name= 'restart')
@commands.has_permissions(administrator=True)
async def restart(ctx):
  await ctx.send("Restarting bot...")
  restart_bot()


@bot.command()
async def emoji(ctx, emoji: discord.Emoji):
    await ctx.send(emoji.url)

@bot.command()
async def help(ctx):
    embed=discord.Embed(title="Bot Help Page!", color=0xFF5733)
    embed.add_field(name="Moderation", value="ban\n kick\n mute\n unmute\n unban\n clean", inline=False)
    embed.add_field(name="Fun/Utility", value="calculate\n say\n emoji\n avatar\n random\n ping", inline=False)
    embed.set_thumbnail(url="https://i.postimg.cc/qMSqcx4g/Server-image.jpg")
    embed.set_footer(text=f'Requested by:\n{str(ctx.author)}',icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

#Random Dog

@bot.command()
async def dog(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/dog')
      dogjson = await request.json()
      # This time we'll get the fact request as well!
      request2 = await session.get('https://some-random-api.ml/facts/dog')
      factjson = await request2.json()

   embed = discord.Embed(title="Doggo!", color=discord.Color.purple())
   embed.set_image(url=dogjson['link'])
   embed.set_footer(text=factjson['fact'])
   await ctx.send(embed=embed)

@bot.command()
async def cat(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/cat')
      dogjson = await request.json()
      # This time we'll get the fact request as well!
      request2 = await session.get('https://some-random-api.ml/facts/cat')
      factjson = await request2.json()

   embed = discord.Embed(title="Meow!", color=discord.Color.purple())
   embed.set_image(url=dogjson['link'])
   embed.set_footer(text=factjson['fact'])
   await ctx.send(embed=embed)


bot.run("")