# from typing import Optional

# from discord import Embed
# from discord.utils import get
# from discord.ext.menus import MenuPages, ListPageSource
# from discord.ext.commands import Cog, command


# def syntax(command):
#     cmd_and_aliases = "|".join([str(command), *command.aliases])
#     params = []

#     for key, value in command.params.items():
#         if key not in ("self", "ctx"):
#             params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")

#     params = " ".join(params)

#     return f"```{cmd_and_aliases} {params}```"


# class HelpMenu(ListPageSource):
#     def __init__(self, ctx, data):
#         self.ctx = ctx

#         super().__init__(data, per_page=5)

#     async def write_page(self, menu, fields=[]):
#         offset = (menu.current_page * self.per_page) + 1
#         len_data = len(self.entries)

#         embed = Embed(
#             title="Help",
#             description="Welcome to the boNo help dialog!",
#             colour=self.ctx.author.colour,
#         )
#         embed.set_thumbnail(url=self.ctx.guild.me.avatar_url)
#         embed.set_footer(
#             text=f"{offset:,} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} commands."
#         )

#         for name, value in fields:
#             embed.add_field(name=name, value=value, inline=False)

#         return embed

#     async def format_page(self, menu, entries):
#         fields = []
#         for entry in entries:
#             fields.append((entry.brief or "No Description", syntax(entry)))

#         return await self.write_page(menu, fields)


# class Help(Cog):
#     def __init__(self, bot):
#         self.bot = bot
#         self.bot.remove_command("help")

#     async def cmd_help(self, ctx, command):
#         embed = Embed(
#             title=f"Help with `{command}`",
#             description=syntax(command),
#             colour=ctx.author.colour,
#         )
#         embed.add_field(name="Command Description", value=command.help)
#         await ctx.send(embed=embed)

#     @command(name="help")
#     async def show_help(self, ctx, cmd: Optional[str]):
#         """
#         Helps to know commands better.
#         """
#         if cmd is None:
#             menu = MenuPages(
#                 source=HelpMenu(ctx, list(self.bot.commands)),
#                 clear_reactions_after=True,
#                 delete_message_after=True,
#             )

#             await menu.start(ctx)
#         else:
#             if (command := get(self.bot.commands, name=cmd)) :
#                 await self.cmd_help(ctx, command)
#             else:
#                 await ctx.send(
#                     "I don't follow that command. Perhaps that's an alias or not a command at all."
#                 )

#     @Cog.listener()
#     async def on_ready(self):
#         if not self.bot.ready:
#             self.bot.cogs_ready.ready_up("help")


# def setup(bot):
#     bot.add_cog(Help(bot))


from discord.ext import commands
from discord.ext.commands import Cog
from utils.util import Pag


class Help(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")
        self.cmds_per_page = 6

    def get_command_signature(self, command: commands.Command, ctx: commands.Context):
        aliases = "|".join(command.aliases)
        cmd_invoke = f"[{command.name}|{aliases}]" if command.aliases else command.name

        full_invoke = command.qualified_name.replace(command.name, "")

        signature = f"{ctx.prefix}{full_invoke}{cmd_invoke}"
        return signature

    async def return_filtered_commands(self, walkable, ctx):
        filtered = []

        for c in walkable.walk_commands():
            try:
                if c.hidden:
                    continue

                elif c.parent:
                    continue

                await c.can_run(ctx)
                filtered.append(c)
            except commands.CommandError:
                continue

        return self.return_sorted_commands(filtered)

    def return_sorted_commands(self, commandList):
        return sorted(commandList, key=lambda x: x.name)

    async def setup_help_pag(self, ctx, entity=None, title=None):
        entity = entity or self.bot
        title = title or self.bot.description

        pages = []

        if isinstance(entity, commands.Command):
            filtered_commands = (
                list(set(entity.all_commands.values()))
                if hasattr(entity, "all_commands")
                else []
            )
            filtered_commands.insert(0, entity)

        else:
            filtered_commands = await self.return_filtered_commands(entity, ctx)

        for i in range(0, len(filtered_commands), self.cmds_per_page):
            next_commands = filtered_commands[i : i + self.cmds_per_page]
            commands_entry = ""

            for cmd in next_commands:
                desc = cmd.short_doc or cmd.description
                signature = self.get_command_signature(cmd, ctx)
                subcommand = "Has subcommands" if hasattr(cmd, "all_commands") else ""

                commands_entry += (
                    f"• **__{cmd.name}__**\n```\n{signature}\n```\n{desc}\n"
                    if isinstance(entity, commands.Command)
                    else f"• **__{cmd.name}__**\n{desc}\n    {subcommand}\n"
                )
            pages.append(commands_entry)

        await Pag(title=title, color=0xCE2029, entries=pages, length=1).start(ctx)

    @commands.command(
        name="help", aliases=["h", "commands"], description="The help command. Duh!"
    )
    async def help_command(self, ctx, *, entity=None):
        if not entity:
            await self.setup_help_pag(ctx)

        else:
            cog = self.bot.get_cog(entity)
            if cog:
                await self.setup_help_pag(ctx, cog, f"{cog.qualified_name}'s commands")

            else:
                command = self.bot.get_command(entity)
                if command:
                    await self.setup_help_pag(ctx, command, command.name)

                else:
                    await ctx.send("Entity not found.")

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("help")
            print("cog ready")


def setup(bot):
    bot.add_cog(Help(bot))