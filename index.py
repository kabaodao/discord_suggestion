import discord
from discord.ext import commands
import os
from datetime import datetime, timedelta, timezone
from googletrans import Translator

# JST time
JST = timezone(timedelta(hours=+9), "JST")
dt = datetime.now(JST)
JSTdt = dt.isoformat(" ", "seconds")

# Translator
translator = Translator()

bot = commands.Bot(command_prefix="d.")

@bot.event
async def on_ready():
    print(bot.user.name)

# limit channel
limit_channel = [734362201795723324]

# @bot.event
# async def on_raw_reaction_add(payload, ctx):
#     if ctx.channel.id in limit_channel:
#         if payload.user_id

@bot.command(name="suggestion", aliases=["sug"])
async def suggestion(ctx, *, text=""):
    # get user role
    user_roles = [role.id for role in ctx.message.author.roles]
    # sync role
    sync_role = 560416383704236046
    if ctx.channel.id in limit_channel:
        if sync_role in user_roles:
            if text == "":
                pass
            else:
                # translate
                translatetext = translator.translate(text)
                if translatetext.src == "en":
                    authtext = translator.translate(translatetext.text, dest="ja").text
                else:
                    authtext = translator.translate(translatetext.text).text
                # embed details
                await ctx.message.delete()
                embed = discord.Embed(title=f"{text}", description=f"Translate:\n"
                                                                   f"{authtext}")
                embed.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
                embed.set_footer(text=f"{JSTdt}")
                # send messages
                await ctx.send(ctx.message.author.mention)
                embedmessage = await ctx.send(embed=embed)
                # add reactions
                for n in ['\N{LARGE GREEN CIRCLE}',
                          '\N{CROSS MARK}']:
                    await embedmessage.add_reaction(n)
        else:
            await ctx.send("Please sync your account first.")
    else:
        await ctx.send(f"Please enter in {bot.get_channel(limit_channel[0]).mention}")

# @bot.command(name="leaderboard", aliases=["lea"])
# async def leaderboard(ctx, )

bot.run(os.environ["DISCORD_TOKEN_DEV"])