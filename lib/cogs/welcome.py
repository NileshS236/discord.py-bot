from discord.ext.commands import Cog, command

from ..db import db


class Welcome(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("welcome")

    @Cog.listener()
    async def on_guild_join(self, guild):
        cli = self.bot
        ctx = cli.get_context

        db.execute("INSERT INTO guilds (GuildID) VALUES (?)", guild.id)
        db.commit()

        await guild.create_text_channel("📯announcements-and-suggestions")
        general = find(
            lambda x: x.name == "📯announcements-and-suggestions", guild.text_channels
        )

        if general and general.permissions_for(guild.me).send_messages:
            await general.send(
                f"Hey **{guild.name}**, this is *`{self.bot.user.display_name}`*. Type `-help` to know some commands to start with."
            )

    @Cog.listener()
    async def on_member_join(self, member):
        pass

    @Cog.listener()
    async def on_member_remove(self, member):
        pass


def setup(bot):
    bot.add_cog(Welcome(bot))