from asyncio import sleep
from datetime import datetime
from glob import glob
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import dotenv_values

from discord import Intents, Embed, File
from discord.ext.commands import (
    Bot as BotBase,
    CommandNotFound,
    Context,
    BadArgument,
    DisabledCommand,
    when_mentioned_or,
)
from discord.ext.commands.errors import (
    MissingRequiredArgument,
    CommandInvokeError,
    MemberNotFound,
    CommandOnCooldown,
)
from discord.errors import Forbidden, HTTPException

from ..db import db

config = dotenv_values(".env")

PREFIX = "-"
OWNER_IDS = [751832971664818287]
COGS = [path.split("\\")[-1][:-3] for path in glob(config["COGS_PATH"])]
IGNORE_EXCEPTIONS = [
    CommandInvokeError,
    MemberNotFound,
    CommandNotFound,
    BadArgument,
    DisabledCommand,
]


def get_prefix(bot, message):
    prefix = db.field("SELECT Prefix FROM guilds WHERE GuildID = ?", message.guild.id)
    return when_mentioned_or(prefix)(bot, message)


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
        self.ready = False
        self.cogs_ready = Ready()
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)

        super().__init__(
            command_prefix=get_prefix, owner_ids=OWNER_IDS, intents=Intents.all()
        )

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"{cog} cog loaded")
        print("setup completed")

    def run(self, version):
        self.VERSION = version

        print("running setup...")
        self.setup()

        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("Bot Running...")
        super().run(self.TOKEN, reconnect=True)

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)
        if ctx.command is not None and ctx.guild is not None:
            if self.ready:
                await self.invoke(ctx)
            else:
                await ctx.send("I'm not ready.")

    async def rules_reminder(self):
        await self.stdout.send("Remenber to adhere to the rules.")

    async def on_connect(self):
        print("Bot Connected.")

    async def on_disconnect(self):
        # await self.stdout.send("Adios, bitches!")
        print("Bot Disconnected.")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong.")

        await self.stdout.send("An error occured.")
        raise

    async def on_command_error(self, ctx, exc):
        if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
            pass
        elif isinstance(exc, CommandOnCooldown):
            if str(exc.cooldown.type).split(".")[-1] == "user":
                await ctx.send(
                    f"Woah! Spamming isn't cool. Wait {exc.retry_after:,.0f}s before using that command again"
                )
            elif str(exc.cooldown.type).split(".")[-1] == "guild":
                await ctx.send(
                    f"Cooldown there! You can use this command again in {exc.retry_after:,.0f}s."
                )
        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send("I believe you have something more to say!")
        elif hasattr(exc, "original"):
            if isinstance(exc.original, Forbidden):
                await ctx.send("I'm not permitted to do that. So I won't.")
            elif isinstance(exc.original, HTTPException):
                await ctx.send(
                    "I guess, something's not allowing me to send a response. HTTP maybe"
                )
            else:
                raise exc.original
        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(824242087683817512)
            self.stdout = self.get_channel(827868996413423626)
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
        # Ignore messages sent by yourself
        if message.author.bot:
            return

        # A way to blacklist users from the bot by not processing commands
        # if the author is in the blacklisted_users list
        # if message.author.id in bot.blacklisted_users:
        #     return

        # Whenever the bot is tagged, respond with its prefix
        if message.content.startswith(f"<@!{bot.user.id}>") and len(
            message.content
        ) == len(f"<@!{bot.user.id}>"):
            data = await bot.config.get_by_id(message.guild.id)
            if not data or "prefix" not in data:
                prefix = get_prefix
            else:
                prefix = data["prefix"]
            await message.channel.send(f"My prefix here is `{prefix}`", delete_after=15)

        await bot.process_commands(message)


bot = Bot()