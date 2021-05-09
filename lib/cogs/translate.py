from typing import Optional
from googletrans import LANGUAGES, Translator

from discord import Embed
from discord.ext.commands import Cog, command


class Translate(Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_code_valid(self, tmp):
        for l in LANGUAGES:
            if tmp == l:
                return tmp
                break
        else:
            return False

    def get_description():
        return (
            "It translates! Flags you wanna try -\n`--src`  `--dest`  `--hide`\n\nLANGUAGE CODES:\n```"
            + "\n".join(
                f"{LANGUAGES[l]} ==>> {l}" for i, l in enumerate(LANGUAGES) if i < 2000
            )
            + "```"
        )

    def get_dest(self, sentence):
        sentence_list = sentence.split("--dest")
        temp_dest = sentence_list[1].split()[0]
        return self.is_code_valid(temp_dest)

    def get_src(self, sentence):
        sentence_list = sentence.split("--src")
        temp_dest = sentence_list[1].split()[0]
        return self.is_code_valid(temp_dest)

    def get_clean_sentence(self, sentence):
        sen_arr = []
        sen_arr = sentence.split()

        if "--dest" in sen_arr:
            i = sen_arr.index("--dest")
            sen_arr.remove("--dest")
            sen_arr.remove(sen_arr[i])
        if "--src" in sen_arr:
            i = sen_arr.index("--src")
            sen_arr.remove("--src")
            sen_arr.remove(sen_arr[i])
        if "--hide" in sen_arr:
            i = sen_arr.index("--hide")
            sen_arr.remove("--hide")
        return " ".join(sen_arr)

    @command(
        name="translate",
        aliases=["$t"],
        description=get_description(),
    )
    async def translate_sentence(self, ctx, *, sentence: str):
        try:
            dest = ""
            src = ""
            output = ""
            t = None
            og_sentence = self.get_clean_sentence(sentence)
            # print(og_sentence)

            if "--dest" in sentence:
                dest = self.get_dest(sentence)

            if "--src" in sentence:
                src = self.get_src(sentence)

            translator = Translator()
            if src:
                t = translator.translate(
                    og_sentence,
                    src=src,
                    dest=f"{'en' if not dest else dest}",
                )
            else:
                t = translator.translate(
                    og_sentence,
                    dest=f"{'en' if not dest else dest}",
                )

            if "--hide" in sentence:
                output = t.text
            else:
                output = (
                    t.origin
                    + "("
                    + LANGUAGES[t.src]
                    + ")\n->\n"
                    + t.text
                    + " ("
                    + LANGUAGES[t.dest]
                    + ")"
                )
            await ctx.message.delete()
            embed = Embed(
                description=output,
                colour=ctx.author.colour,
            )
            await ctx.send(embed=embed)
        except:
            await ctx.send(
                embed=Embed(
                    description="Check your command once again.",
                    colour=ctx.author.colour,
                )
            )

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("translate")


def setup(bot):
    bot.add_cog(Translate(bot))