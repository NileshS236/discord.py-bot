from random import randint, choice
from typing import Optional

from discord import Member
from discord import Role
from discord.ext.commands import Cog, command, BadArgument
from discord.ext.commands.errors import MissingRequiredArgument, CommandInvokeError, MemberNotFound

class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="hello", aliases=["hi", "hey", "sup", "hola", "howdy"])
    async def say_hello(self, ctx):
        await ctx.send(f"{choice(('Hello ', 'Hey there, ', 'Hey ', 'Sup! ', 'Howdy, ', 'Hola, ', 'Namaste, '))}{ctx.author.mention}!")

    @command(name="roll")
    async def roll_dice(self, ctx, die_string: Optional[str]):
        if die_string:
            try:
                dice, value = (int(term) for term in die_string.split("-"))
                if dice <= 25:
                    rolls = [randint(1, value) for i in range(dice)]
                    await ctx.send(" + ".join(str(r) for r in rolls) + f" = {sum(rolls)}")
                else:
                    await ctx.send("Hold on your dice, buddy. That's too much.")
            except ValueError:
                await ctx.send("That's not a valid input.")
        else:
            await ctx.send('die string is missing: *count*-*max*')
               

    @command(name="slap", aliases=["hit"])
    async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = "for no reason"):
        await ctx.send(f"{ctx.author.mention} slapped {member.mention} {reason}")

    @slap_member.error
    async def slap_member_error(self, ctx, exc):
        if isinstance(exc, MissingRequiredArgument):
            await ctx.send("Next time mention someone!")
        elif isinstance(exc, CommandInvokeError):
            await ctx.send(f"{ctx.author.mention} slapped {member.mention if member else ctx.author.mention} {reason}")
        elif isinstance(exc, MemberNotFound):
            await ctx.send(f"Now that member is hard to find.")

    @command(name="toss", aliases=["flip"])
    async def toss_coin(self, ctx):
        await ctx.send("It's " + choice(("Heads.", "Tails.", "uh...\ncoin's lost.")))

    @command(name="echo", aliases=["say"])
    async def echo_message(self, ctx, message):
        await ctx.message.delete()
        await ctx.send(message)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")
            print("cog ready")

def setup(bot):
    bot.add_cog(Fun(bot))
