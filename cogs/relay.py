from time import sleep
from discord import app_commands
from discord.ext import tasks, commands
from threading import Thread
from helpers.config import logging, read_channels_json, write_channels_json, read_usernames_json, write_usernames_json
from helpers.parser import parser


logger = logging.getLogger(__name__)


class Relay(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.channels = read_channels_json()
        self.usernames = read_usernames_json()
        Thread(target=self.parsing).start()

    @commands.command()
    async def set(self, ctx):
        if ctx.channel.id not in self.channels:
            self.channels.append(ctx.channel.id)
        write_channels_json(self.channels)
        await ctx.send("Channel Set.")
    
    @commands.command()
    async def add(self, ctx, username):
        if username not in self.usernames:
            self.usernames.append(username)
        write_usernames_json(self.usernames)
        await ctx.send("Username Added.")

    def parsing(self):
        scraped_tweet = ""
        last_scraped = None
        
        while True:
            if scraped_tweet != last_scraped:
                for username in self.usernames:
                    scraped_tweet = parser(username)
                    for channel_id in self.channels:
                        channel = self.client.get_channel(channel_id)
                        self.client.loop.create_task(channel.send(scraped_tweet))
                        last_scraped = scraped_tweet
                
            sleep(60.0)  


async def setup(client):
    await client.add_cog(Relay(client))
