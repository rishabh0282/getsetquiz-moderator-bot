import json
import os
import platform
import random
import sys

import aiohttp
import discord
import yaml
from discord.ext import commands

if not os.path.isfile("config.yaml"):
    sys.exit("'config.yaml' not found! Please add it and try again.")
else:
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)


class general(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="info", aliases=["botinfo"])
    async def info(self, context):
        """
        Get some useful (or not) information about the bot.
        """
        embed = discord.Embed(
            description="GetSetQuiz's Moderator Bot for handling quizzes",
            color=config["success"]
        )
        embed.set_author(
            name="Bot Information"
        )
        embed.add_field(
            name="Creators:",
            value="Vertigo#1313 and rumdev#5981",
            inline=True
        )
        embed.add_field(
            name="Currently using Python Version:",
            value=f"{platform.python_version()}",
            inline=True
        )
        embed.add_field(
            name="Bot usage prefix:",
            value=f"{config['bot_prefix']}",
            inline=False
        )
        embed.set_footer(
            text=f"This info was requested by {context.message.author}"
        )
        await context.send(embed=embed)

    @commands.command(name="serverinfo")
    async def serverinfo(self, context):
        """
        Get some useful (or not) information about the server.
        """
        server = context.message.guild
        roles = [x.name for x in server.roles]
        role_length = len(roles)
        if role_length > 50:
            roles = roles[:50]
            roles.append(f">>>> Displaying[50/{len(roles)}] Roles")
        roles = ", ".join(roles)
        channels = len(server.channels)
        time = str(server.created_at)
        time = time.split(" ")
        time = time[0]

        embed = discord.Embed(
            title="**Server Name:**",
            description=f"{server}",
            color=config["success"]
        )
        embed.set_thumbnail(
            url=server.icon_url
        )
        embed.add_field(
            name="Owner",
            value=f"{server.owner}\n{server.owner.id}"
        )
        embed.add_field(
            name="Server ID",
            value=server.id
        )
        embed.add_field(
            name="Member Count",
            value=server.member_count
        )
        embed.add_field(
            name="Text/Voice Channels",
            value=f"{channels}"
        )
        embed.add_field(
            name=f"Roles ({role_length})",
            value=roles
        )
        embed.set_footer(
            text=f"Created at: {time}"
        )
        await context.send(embed=embed)

    @commands.command(name="ping")
    async def ping(self, context):
        """
        Check if the bot is alive.
        """
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=config["success"]
        )
        await context.send(embed=embed)

    @commands.command(name="invite")
    async def invite(self, context):
        """
        Get the invite link of the bot to be able to invite it.
        """
        embed = discord.Embed(
            description=f"Invite me by clicking [here](https://discordapp.com/oauth2/authorize?&client_id={config['application_id']}&scope=bot&permissions=470150263).",
            color=config['main_color']
        )
        try:
            # To know what permissions to give to your bot, please see here: https://discordapi.com/permissions.html and remember to not give Administrator permissions.
            await context.author.send(embed=embed)
            await context.send("I sent you a private message!")
        except discord.Forbidden:
            await context.send(embed=embed)

    @commands.command(name="server", aliases=["support", "supportserver"])
    async def server(self, context):
        """
        Get the invite link of the discord server of the bot for some support.
        """
        embed = discord.Embed(
            description=f"Join the support server for the bot by clicking [here](https://discord.gg/HzJ3Gfr).",
            color=config['main_color']
        )
        try:
            await context.author.send(embed=embed)
            await context.send("I sent you a private message!")
        except discord.Forbidden:
            await context.send(embed=embed)

    @commands.command(name="poll")
    async def poll(self, context, *, title):
        """
        Create a poll where members can vote.
        """
        embed = discord.Embed(
            title="A new poll has been created!",
            description=f"{title}",
            color=config["success"]
        )
        embed.set_footer(
            text=f"Poll created by: {context.message.author} • React to vote!"
        )
        embed_message = await context.send(embed=embed)
        await embed_message.add_reaction("👍")
        await embed_message.add_reaction("👎")
        await embed_message.add_reaction("🤷")

    @commands.command(name="8ball")
    async def eight_ball(self, context, *, question):
        """
        Ask any question to the bot.
        """
        answers = ['It is certain.', 'It is decidedly so.', 'You may rely on it.', 'Without a doubt.',
                   'Yes - definitely.', 'As I see, yes.', 'Most likely.', 'Outlook good.', 'Yes.',
                   'Signs point to yes.', 'Reply hazy, try again.', 'Ask again later.', 'Better not tell you now.',
                   'Cannot predict now.', 'Concentrate and ask again later.', 'Don\'t count on it.', 'My reply is no.',
                   'My sources say no.', 'Outlook not so good.', 'Very doubtful.']
        embed = discord.Embed(
            title="**My Answer:**",
            description=f"{answers[random.randint(0, len(answers))]}",
            color=config["success"]
        )
        embed.set_footer(
            text=f"The question was: {question}"
        )
        await context.send(embed=embed)

    @commands.command(name="bitcoin")
    async def bitcoin(self, context):
        """
        Get the current price of bitcoin.
        """
        url = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
        # Async HTTP request
        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)
            embed = discord.Embed(
                title=":information_source: Info",
                description=f"Bitcoin price is: ${response['bpi']['USD']['rate']}",
                color=config["success"]
            )
            await context.send(embed=embed)


def setup(bot):
    bot.add_cog(general(bot))
