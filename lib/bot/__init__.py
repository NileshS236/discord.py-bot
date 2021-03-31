from asyncio import sleep
from datetime import datetime
from glob import glob
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import Intents, Embed, File
from discord.ext.commands import Bot as BotBase, CommandNotFound

from ..db import db

PREFIX = ':'
OWNER_IDS = [751832971664818287]
COGS = [path.split("\\")[-1][:-3] for path in glob("D:/Nilesh/WEBD/PYTHON/discord.py-bot/lib/cogs/*.py")]

class Ready(object):
	def __init__(self):
		for cog in COGS:
			setattr(self, cog, False)

	def ready_up(self, cog):
		setattr(self, cog, True)
		print(f" {cog} cog ready")

	def all_ready(self):
		return all([getattr(self, cog) for cog in COGS])

class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.cogs_ready = Ready()
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)

        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS, intents=Intents.all())

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"{cog} cog loaded")
        print("setup completed")

    def run(self, version):
        self.VERSION = version

        print("running setup...")
        self.setup()

        with open("./lib/bot/token.0", 'r', encoding='utf-8') as tf:
            self.TOKEN = tf.read()

        print("Bot Running...")
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self):
        print("Bot Connected.")

    async def on_disconnect(self):
        print("Bot Disconnected.")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong.")
            
        await self.stdout.send("An error occured.")
        raise

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            pass
        elif hasattr(exc, 'original'):
            raise exc.original
        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(824242087683817512)
            self.stdout = self.get_channel(824242087683817515)
            self.scheduler.start()


            # embed = Embed(title="Now Online!", description="I'm on.", timestamp=datetime.utcnow(), colour=0xFF00FF)
            # embed.add_field(name="Name", value="Value",inline=True)
            # embed.set_footer(text="This is a footer!")
            # embed.set_author(name="Nilesh", icon_url=self.guild.icon_url)
            # embed.set_thumbnail(url=self.guild.icon_url)
            # embed.set_image(url=self.guild.icon_url)

            # await channel.send(embed=embed)
            # await channel.send(file=File("./data/images/394230.jpg"))
            while not self.cogs_ready.all_ready():
                await sleep(0.5)    

            await self.stdout.send("Now Online!")

            self.ready = True
            print("Bot Ready.")

        elif self.ready:
            print("Bot Reconnected.")

    async def on_message(self, message):
        pass

bot = Bot()