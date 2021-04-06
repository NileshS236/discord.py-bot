from typing import Optional
from googletrans import LANGUAGES, Translator

from discord import Embed
from discord.ext.commands import Cog, command


class Translate(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="translate", aliases=["-t"])
    async def translate_sentence(
        self, ctx, *, sentence: str, lang: Optional[str] = "en"
    ):
        await ctx.message.delete()
        if "_$" in sentence:
            sentence_list = sentence.split("_$")
            sentence = sentence_list[0]
            temp_lang = sentence_list[1]
            # print(lang)
            for l in LANGUAGES:
                if temp_lang == l:
                    lang = temp_lang
                    # print(lang)
                    translator = Translator()
                    t = translator.translate(sentence, dest=lang)
                    # print(t.text)
                    embed = Embed(
                        description=t.origin
                        + "("
                        + t.src
                        + ")\n->\n"
                        + t.text
                        + " ("
                        + t.dest
                        + ")",
                        colour=ctx.author.colour,
                    )
                    await ctx.send(embed=embed)
                    break
            else:
                embed = Embed(
                    title=f"Language code '{temp_lang}' you chose does'nt exist.",
                    description="```"
                    + "\n".join(f"{l} - {LANGUAGES[l]}" for l in LANGUAGES)
                    + "```",
                    colour=ctx.author.colour,
                )
                await ctx.send(embed=embed)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("translate")


def setup(bot):
    bot.add_cog(Translate(bot))