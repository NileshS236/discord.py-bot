from random import randint, choice
from typing import Optional
from aiohttp import request

import praw, random

from discord import Member, Embed, Attachment
from discord.ext.commands import Cog, command, BadArgument
from discord.ext.commands.errors import MissingRequiredArgument, CommandInvokeError, MemberNotFound

reddit = praw.Reddit(client_id="i10kksuKFBQjQg",
                     client_secret="CD1BPDYGJ15-Kc1SqcDuEOzq1Nv-Wg",
                     username="AdKey6705",
                     password="devnilu2306",
                     user_agent="boNo_101"
                    )
class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="hello", aliases=["hi", "hey", "sup", "hola", "howdy"])
    async def say_hello(self, ctx):
        await ctx.send(f"{choice(('Hello ', 'Hey there, ', 'Hey ', 'Sup! ', 'Howdy, ', 'Hola, ', 'Namaste, '))} {ctx.author.mention}!")

    @command(name="roll", aliases=["dice"])
    async def roll_dice(self, ctx, die_string: str):
        try:
            dice, value = (int(term) for term in die_string.split("-"))
            if dice <= 25:
                rolls = [randint(1, value) for i in range(dice)]
                await ctx.send(" + ".join(str(r) for r in rolls) + f" = {sum(rolls)}")
            else:
                await ctx.send("Hold on your dice, buddy. That's too much.")
        except ValueError:
            await ctx.send("That's not a valid input. *count*-*max*")
               

    @command(name="slap", aliases=["hit"])
    async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = "for no reason"):
        await ctx.send(f"{ctx.author.mention} slapped {member.mention} {reason}")

    @slap_member.error
    async def slap_member_error(self, ctx, exc):
        if isinstance(exc, MissingRequiredArgument):
            await ctx.send("Next time mention someone to slap!")
        elif isinstance(exc, CommandInvokeError):
            await ctx.send(f"{ctx.author.mention} slapped {member.mention if member else ctx.author.mention} {reason}")
        elif isinstance(exc, MemberNotFound):
            await ctx.send(f"Now that member is hard to find.")

    @command(name="toss", aliases=["flip"])
    async def toss_coin(self, ctx):
        await ctx.send("It's " + choice(("Heads.", "Tails.", "uh...\ncoin's lost.")))

    @command(name="echo", aliases=["say"])
    async def echo_message(self, ctx, *, message: Optional[str] = "I can't guess what you want me to say."):
        await ctx.message.delete()
        await ctx.send(message)

    @command(name="fact")
    async def animal_fact(self, ctx, animal: str):
        NAMES = ("dog", "cat", "panda", "fox", "bird", "koala", "red_panda", "racoon", "kangaroo")

        if animal and (animal := animal.lower()) in NAMES:
            FACT_URL = f"https://some-random-api.ml/animal/{animal}" if animal != "bird"\
            else "https://some-random-api.ml/animal/birb"
            
            async with request('GET', FACT_URL) as response:
                if response.status == 200:
                    try:
                        data = await response.json()
                        embed = Embed(title=f"{animal.title()} fact", description=data['fact'], colour=choice((0xFF00FF, 0xFF0000, 0x0000FF, 0x00FF00, 0xFFFF00, 0x00FFFF)))
                        embed.set_image(url=data['image'])
                        embed.set_footer(text="Image may not relate to the fact.")
                        await ctx.send(embed=embed)
                    except Exception as e:
                        print(e)
                else:
                    await ctx.send(f"Seems like a bad API.")
        elif not animal.lower() in NAMES:
            await ctx.send("Well, that creature's outta my reach! Why not choose something from - \n`" + "` `".join(name for name in NAMES) + "`")

    @command(name="quote")
    async def send_quote(self, ctx):
        URL = "https://some-random-api.ml/animu/quote"

        async with request('GET', URL) as response:
            if response.status == 200:
                quote = await response.json()
                embed = Embed(title="Quote", description=quote['sentence'], colour=choice((0xFF00FF, 0xFF0000, 0x0000FF, 0x00FF00, 0xFFFF00, 0x00FFFF)))
                embed.set_footer(text=f"-{quote['characther']} from {quote['anime']}")
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"Seems like a bad API.")

    @command(name="wink")
    async def wink(self, ctx):
        URL = "https://some-random-api.ml/animu/wink"
        async with request('GET', URL) as response:
            if response.status == 200:
                wink_link = await response.json()
                embed = Embed(colour=choice((0xFF00FF, 0xFF0000, 0x0000FF, 0x00FF00, 0xFFFF00, 0x00FFFF)))
                embed.set_image(url=wink_link['link'])
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"Seems like a bad API.")

    @command(name="pat")
    async def pat(self, ctx):
        URL = "https://some-random-api.ml/animu/pat"
        async with request('GET', URL) as response:
            if response.status == 200:
                pat_link = await response.json()
                embed = Embed(colour=choice((0xFF00FF, 0xFF0000, 0x0000FF, 0x00FF00, 0xFFFF00, 0x00FFFF)))
                embed.set_image(url=pat_link['link'])
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"Seems like a bad API.")

    @command(name="hug")
    async def hug(self, ctx):
        URL = "https://some-random-api.ml/animu/hug"
        async with request('GET', URL) as response:
            if response.status == 200:
                hug_link = await response.json()
                embed = Embed(colour=choice((0xFF00FF, 0xFF0000, 0x0000FF, 0x00FF00, 0xFFFF00, 0x00FFFF)))
                embed.set_image(url=hug_link['link'])
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"Seems like a bad API.")

    @command(name="face-palm")
    async def face_palm(self, ctx):
        URL = "https://some-random-api.ml/animu/face-palm"
        async with request('GET', URL) as response:
            if response.status == 200:
                face_palm_link = await response.json()
                embed = Embed(colour=choice((0xFF00FF, 0xFF0000, 0x0000FF, 0x00FF00, 0xFFFF00, 0x00FFFF)))
                embed.set_image(url=face_palm_link['link'])
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"Seems like a bad API.")

    @command(name="wasted")
    async def wasted(self, ctx, member: Optional[Member]):
        URL = f"https://some-random-api.ml/canvas/wasted?avatar={member.avatar_url_as(format='png')}" if member\
            else f"https://some-random-api.ml/canvas/wasted?avatar={ctx.author.avatar_url_as(format='png')}"
        # async with request('GET', URL) as response
        # print(URL)
        embed = Embed(colour=choice((0xFF00FF, 0xFF0000, 0x0000FF, 0x00FF00, 0xFFFF00, 0x00FFFF)))
        embed.set_image(url = URL)
        try:
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)

    @command(name="gay")
    async def gay(self, ctx, member: Optional[Member]):
        URL = f"https://some-random-api.ml/canvas/gay?avatar={member.avatar_url_as(format='png')}" if member\
            else f"https://some-random-api.ml/canvas/gay?avatar={ctx.author.avatar_url_as(format='png')}"
        # async with request('GET', URL) as response
        embed = Embed(colour=choice((0xFF00FF, 0xFF0000, 0x0000FF, 0x00FF00, 0xFFFF00, 0x00FFFF)))
        embed.set_image(url = URL)
        try:
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)

    @command(name="glass")
    async def glass(self, ctx, member: Optional[Member]):
        URL = f"https://some-random-api.ml/canvas/glass?avatar={member.avatar_url_as(format='png')}" if member\
            else f"https://some-random-api.ml/canvas/glass?avatar={ctx.author.avatar_url_as(format='png')}"
        # async with request('GET', URL) as response
        embed = Embed(colour=choice((0xFF00FF, 0xFF0000, 0x0000FF, 0x00FF00, 0xFFFF00, 0x00FFFF)))
        embed.set_image(url = URL)
        try:
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)

    @command(name="jail")
    async def jail(self, ctx, member: Optional[Member]):
        URL = f"https://some-random-api.ml/canvas/jail?avatar={member.avatar_url_as(format='png')}" if member\
            else f"https://some-random-api.ml/canvas/jail?avatar={ctx.author.avatar_url_as(format='png')}"
        # async with request('GET', URL) as response
        embed = Embed(colour=choice((0xFF00FF, 0xFF0000, 0x0000FF, 0x00FF00, 0xFFFF00, 0x00FFFF)))
        embed.set_image(url = URL)
        try:
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)

    @command(name="license")
    async def give_license(self, ctx, member: Optional[Member]):
        URL = f"https://some-random-api.ml/canvas/horny?avatar={member.avatar_url_as(format='png')}" if member\
            else f"https://some-random-api.ml/canvas/horny?avatar={ctx.author.avatar_url_as(format='png')}"
        # async with request('GET', URL) as response
        embed = Embed(colour=choice((0xFF00FF, 0xFF0000, 0x0000FF, 0x00FF00, 0xFFFF00, 0x00FFFF)))
        embed.set_image(url = URL)
        try:
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)

    @command(name="nsfw", aliases=["rule34"])
    async def nsfw(self, ctx):
        await ctx.message.delete()
        if not ctx.channel.is_nsfw():
            embed = Embed(
                title=":x: Channel Is Not NSFW",
                color=choice((0xFF00FF, 0xFF0000, 0x0000FF, 0x00FF00, 0xFFFF00, 0x00FFFF))
            )
            embed.set_image(url="https://media2.giphy.com/media/W5C9c8nqoaDJWh34i6/giphy.gif")
        else:
            async with ctx.channel.typing():
                memes_submissions = reddit.subreddit("rule34").hot()
                post_to_pick = random.randint(1, 100)
                for i in range(0, post_to_pick):
                    submission = memes_submissions.__next__()
                embed = Embed(
                    title=submission.title,
                     color=choice((0xFF00FF, 0xFF0000, 0x0000FF, 0x00FF00, 0xFFFF00, 0x00FFFF))
                )
                embed.set_image(url=submission.url)
        await ctx.send(embed=embed)

    @command(name="meme")
    async def meme(self, ctx):
        async with ctx.channel.typing():
            memes_submissions = reddit.subreddit("meme").hot()
            post_to_pick = random.randint(1, 100)
            for i in range(0, post_to_pick):
                submission = memes_submissions.__next__()
            embed = Embed(
                title=submission.title,
                    color=choice((0xFF00FF, 0xFF0000, 0x0000FF, 0x00FF00, 0xFFFF00, 0x00FFFF))
            )
            embed.set_image(url=submission.url)
        await ctx.send(embed=embed)

    @command(name="filter")
    async def give_filter(self, ctx, filter_type: str, member: Optional[Member]):
        FILTERS = ("greyscale", "invert", "brightness", "threshold", "sepia", "red", "green", "blue", "blurple", "pixelate", "blur")
        if filter_type and filter_type in FILTERS:
            URL = f"https://some-random-api.ml/canvas/{filter_type}/?avatar={member.avatar_url_as(format='png')}" if member\
            else f"https://some-random-api.ml/canvas/{filter_type}/?avatar={ctx.author.avatar_url_as(format='png')}"
            embed = Embed(colour=choice((0xFF00FF, 0xFF0000, 0x0000FF, 0x00FF00, 0xFFFF00, 0x00FFFF)))
            embed.set_image(url = URL)
            try:
                await ctx.send(embed=embed)
            except Exception as e:
                print(e)
        # elif not filter_type:
        #     await ctx.send("How about mentioning a filter type, ay.")
        elif not filter_type in FILTERS:
            await ctx.send("Maybe you would like to choose something from - \n`" + "` `".join(filter_avl for filter_avl in FILTERS) + "`")

    @command(name="lyrics")
    async def give_lyrics(self, ctx, *, song_info: str):
        URL = f"https://some-random-api.ml/lyrics?title={song_info}"
        async with request('GET', URL) as response:
            if response.status == 200:
                song_data = await response.json()
                embed = Embed(title=song_data['title'], url=f"{song_data['links']['genius']}", description=f"```{song_data['lyrics'][:2042]}```")
                embed.set_author(name=song_data['author'])
                if song_data['thumbnail']['genius']:
                    embed.set_thumbnail(url=song_data['thumbnail']['genius'])
                await ctx.send(embed=embed)
            else:
                await ctx.send("Seems like I don't have that song.")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")
            print("cog ready")

def setup(bot):
    bot.add_cog(Fun(bot))
