from random import randint, choice
from typing import Optional
from aiohttp import request
from dotenv import dotenv_values
import praw, random

from discord import Member, Embed
from discord.ext.commands import Cog, command, BadArgument, BucketType, cooldown
from discord.ext.commands.errors import (
    CommandInvokeError,
    MemberNotFound,
)

config = dotenv_values(".env")

reddit = praw.Reddit(
    client_id=config["CLIENT_ID"],
    client_secret=config["CLIENT_SECRET"],
    username=config["USERNAME"],
    password=config["PASSWORD"],
    user_agent=config["USER_AGENT"],
)


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="hello", aliases=["hi", "hey", "sup", "hola", "howdy"])
    async def say_hello(self, ctx):
        """
        I love greeting, only if you do first.
        """
        await ctx.send(
            f"{choice(('Hello ', 'Hey there, ', 'Hey ', 'Sup! ', 'Howdy, ', 'Hola, ', 'Namaste, '))} {ctx.author.mention}!"
        )

    @command(name="roll", aliases=["dice"])
    @cooldown(1, 10, BucketType.user)
    async def roll_dice(self, ctx, die_string: int):
        """
        Give me number of dice and I might give you the SUM of your luck.
        """
        dice = die_string
        if dice <= 25:
            rolls = [randint(1, 6) for i in range(dice)]
            await ctx.send(" + ".join(str(r) for r in rolls) + f" = {sum(rolls)}")
        else:
            await ctx.send("Woah! Hold on your dice, buddy. That's too much.")

    @roll_dice.error
    async def roll_dice_error(self, ctx, exc):
        if isinstance(exc, BadArgument):
            await ctx.send("I think number of dice is supposed to be a number.")

    @command(name="slap", aliases=["hit"])
    async def slap_member(
        self, ctx, member: Optional[Member], *, reason: Optional[str] = "for no reason"
    ):
        """
        I might slap the member you mention, or you if you don't, but you better give me a reason. I don't likr hitting for no reason.
        """
        await ctx.send(
            f"{ctx.author.mention} slapped {member.mention if member else ctx.author.mention} {reason}"
        )

    @slap_member.error
    async def slap_member_error(self, ctx, exc):
        if isinstance(exc, CommandInvokeError):
            pass
        elif isinstance(exc, MemberNotFound):
            await ctx.send(f"Now that member is hard to find.")

    @command(name="toss", aliases=["flip"])
    async def toss_coin(self, ctx):
        """
        If command name is not explaining you enough, it tosses 'the coin'. Sometimes I lose it though.
        """
        await ctx.send("It's " + choice(("Heads.", "Tails.", "uh...\ncoin's lost.")))

    @command(name="echo", aliases=["say"])
    @cooldown(1, 15, BucketType.guild)
    async def echo_message(
        self, ctx, *, message: Optional[str] = "I can't guess what you want me to say."
    ):
        """
        Use the command followed by a message. I say what you say, and make it as if you never said it.
        """
        await ctx.message.delete()
        await ctx.send(message)

    @command(name="fact")
    @cooldown(3, 60, BucketType.guild)
    async def animal_fact(self, ctx, animal: str):
        """
        For now my fact are limited to certain animals only. but my birds are on their way to bring me more.
        """
        NAMES = (
            "dog",
            "cat",
            "panda",
            "fox",
            "bird",
            "koala",
            "red_panda",
            "racoon",
            "kangaroo",
        )

        if animal and (animal := animal.lower()) in NAMES:
            FACT_URL = (
                f"https://some-random-api.ml/animal/{animal}"
                if animal != "bird"
                else "https://some-random-api.ml/animal/birb"
            )

            async with request("GET", FACT_URL) as response:
                if response.status == 200:
                    try:
                        data = await response.json()
                        embed = Embed(
                            title=f"{animal.title()} fact",
                            description=data["fact"],
                            colour=choice(
                                (
                                    0xFF00FF,
                                    0xFF0000,
                                    0x0000FF,
                                    0x00FF00,
                                    0xFFFF00,
                                    0x00FFFF,
                                )
                            ),
                        )
                        embed.set_image(url=data["image"])
                        embed.set_footer(text="Image may not relate to the fact.")
                        await ctx.send(embed=embed)
                    except Exception as e:
                        print(e)
                else:
                    await ctx.send(f"Seems like a bad API.")
        elif not animal.lower() in NAMES:
            await ctx.send(
                "Well, that creature's outta my reach! Why not choose something from - \n`"
                + "` `".join(name for name in NAMES)
                + "`"
            )

    @command(name="quote")
    @cooldown(3, 60, BucketType.guild)
    async def send_quote(self, ctx):
        """
        Ya, I do that too. I give famous qoutes by famous anime characters. (As if that's gonna help)
        """
        URL = "https://some-random-api.ml/animu/quote"

        async with request("GET", URL) as response:
            if response.status == 200:
                quote = await response.json()
                embed = Embed(
                    title="Quote",
                    description=quote["sentence"],
                    colour=choice(
                        (0xFF00FF, 0xFF0000, 0x0000FF, 0x00FF00, 0xFFFF00, 0x00FFFF)
                    ),
                )
                embed.set_footer(text=f"-{quote['characther']} from {quote['anime']}")
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"Seems like a bad API.")

    @command(name="wink")
    @cooldown(1, 5, BucketType.user)
    async def wink(self, ctx):
        """
        Do not take a wrong sign. Those are just characters winking. (Not even at you)
        """
        URL = "https://some-random-api.ml/animu/wink"
        async with request("GET", URL) as response:
            if response.status == 200:
                wink_link = await response.json()
                embed = Embed(
                    colour=choice(
                        (0xFF00FF, 0xFF0000, 0x0000FF, 0x00FF00, 0xFFFF00, 0x00FFFF)
                    )
                )
                embed.set_image(url=wink_link["link"])
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"Seems like a bad API.")

    @command(name="pat")
    @cooldown(1, 5, BucketType.user)
    async def pat(self, ctx):
        """
        Type the command properly. If you did it you get a pat.
        """
        URL = "https://some-random-api.ml/animu/pat"
        async with request("GET", URL) as response:
            if response.status == 200:
                pat_link = await response.json()
                embed = Embed(
                    colour=choice(
                        (0xFF00FF, 0xFF0000, 0x0000FF, 0x00FF00, 0xFFFF00, 0x00FFFF)
                    )
                )
                embed.set_image(url=pat_link["link"])
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"Seems like a bad API.")

    @command(name="hug")
    @cooldown(1, 5, BucketType.user)
    async def hug(self, ctx):
        """
        Ever feel alone and lost, ask for a hug. I might at least give you a gif.
        """
        URL = "https://some-random-api.ml/animu/hug"
        async with request("GET", URL) as response:
            if response.status == 200:
                hug_link = await response.json()
                embed = Embed(
                    colour=choice(
                        (0xFF00FF, 0xFF0000, 0x0000FF, 0x00FF00, 0xFFFF00, 0x00FFFF)
                    )
                )
                embed.set_image(url=hug_link["link"])
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"Seems like a bad API.")

    @command(name="facepalm", aliases=["fp"])
    @cooldown(1, 5, BucketType.user)
    async def face_palm(self, ctx):
        """
        That's "pissed" palm on face, not caressing.
        """
        URL = "https://some-random-api.ml/animu/face-palm"
        async with request("GET", URL) as response:
            if response.status == 200:
                face_palm_link = await response.json()
                embed = Embed(
                    colour=choice(
                        (0xFF00FF, 0xFF0000, 0x0000FF, 0x00FF00, 0xFFFF00, 0x00FFFF)
                    )
                )
                embed.set_image(url=face_palm_link["link"])
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"Seems like a bad API.")

    @command(name="wasted")
    @cooldown(1, 5, BucketType.user)
    async def wasted(self, ctx, member: Optional[Member]):
        """
        Wanna show someone wasted, mention them after the command, or else its you.
        """
        URL = (
            f"https://some-random-api.ml/canvas/wasted?avatar={member.avatar_url_as(format='png')}"
            if member
            else f"https://some-random-api.ml/canvas/wasted?avatar={ctx.author.avatar_url_as(format='png')}"
        )
        # async with request('GET', URL) as response
        # print(URL)
        embed = Embed(
            colour=choice((0xFF00FF, 0xFF0000, 0x0000FF, 0x00FF00, 0xFFFF00, 0x00FFFF))
        )
        embed.set_image(url=URL)
        try:
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)

    @command(name="gay")
    @cooldown(1, 5, BucketType.user)
    async def gay(self, ctx, member: Optional[Member]):
        """
        Believe me, not the command. It's doesn't do what you think it does. Or try it yourself. (Do mention someone)
        """
        URL = (
            f"https://some-random-api.ml/canvas/gay?avatar={member.avatar_url_as(format='png')}"
            if member
            else f"https://some-random-api.ml/canvas/gay?avatar={ctx.author.avatar_url_as(format='png')}"
        )
        # async with request('GET', URL) as response
        embed = Embed(
            colour=choice((0xFF00FF, 0xFF0000, 0x0000FF, 0x00FF00, 0xFFFF00, 0x00FFFF))
        )
        embed.set_image(url=URL)
        try:
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)

    @command(name="glass")
    @cooldown(1, 5, BucketType.user)
    async def glass(self, ctx, member: Optional[Member]):
        """
        This will glass the member you mention. If you don't mention someone it can be you.
        """
        URL = (
            f"https://some-random-api.ml/canvas/glass?avatar={member.avatar_url_as(format='png')}"
            if member
            else f"https://some-random-api.ml/canvas/glass?avatar={ctx.author.avatar_url_as(format='png')}"
        )
        # async with request('GET', URL) as response
        embed = Embed(
            colour=choice((0xFF00FF, 0xFF0000, 0x0000FF, 0x00FF00, 0xFFFF00, 0x00FFFF))
        )
        embed.set_image(url=URL)
        try:
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)

    @command(name="jail")
    @cooldown(1, 5, BucketType.user)
    async def jail(self, ctx, member: Optional[Member]):
        """
        Every prime has a jail, I have a command. Use it and **mention a member** or wasting my time is a crime. (It rhyme)
        """
        URL = (
            f"https://some-random-api.ml/canvas/jail?avatar={member.avatar_url_as(format='png')}"
            if member
            else f"https://some-random-api.ml/canvas/jail?avatar={ctx.author.avatar_url_as(format='png')}"
        )
        # async with request('GET', URL) as response
        embed = Embed(
            colour=choice((0xFF00FF, 0xFF0000, 0x0000FF, 0x00FF00, 0xFFFF00, 0x00FFFF))
        )
        embed.set_image(url=URL)
        try:
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)

    @command(name="license")
    @cooldown(1, 10, BucketType.user)
    async def give_license(self, ctx, member: Optional[Member]):
        """
        It's probably not a driver's license. Use it at your own risk. (Do mention someone)
        """
        URL = (
            f"https://some-random-api.ml/canvas/horny?avatar={member.avatar_url_as(format='png')}"
            if member
            else f"https://some-random-api.ml/canvas/horny?avatar={ctx.author.avatar_url_as(format='png')}"
        )
        # async with request('GET', URL) as response
        embed = Embed(
            colour=choice((0xFF00FF, 0xFF0000, 0x0000FF, 0x00FF00, 0xFFFF00, 0x00FFFF))
        )
        embed.set_image(url=URL)
        try:
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)

    @command(name="nsfw", aliases=["rule34"], hidden=True)
    @cooldown(1, 10, BucketType.guild)
    async def nsfw(self, ctx):
        """
        You re entering in an adult zone with this command. Make sure nsfw is "Turned On" and keep your thing inside.
        """
        await ctx.message.delete()
        if not ctx.channel.is_nsfw():
            embed = Embed(
                title=":x: Channel Is Not NSFW",
                color=choice(
                    (0xFF00FF, 0xFF0000, 0x0000FF, 0x00FF00, 0xFFFF00, 0x00FFFF)
                ),
            )
            embed.set_image(
                url="https://media2.giphy.com/media/W5C9c8nqoaDJWh34i6/giphy.gif"
            )
        else:
            async with ctx.channel.typing():
                memes_submissions = reddit.subreddit("rule34").hot()
                post_to_pick = random.randint(1, 100)
                for i in range(0, post_to_pick):
                    submission = memes_submissions.__next__()
                embed = Embed(
                    title=submission.title,
                    color=choice(
                        (0xFF00FF, 0xFF0000, 0x0000FF, 0x00FF00, 0xFFFF00, 0x00FFFF)
                    ),
                )
                embed.set_image(url=submission.url)
        await ctx.send(embed=embed)

    @command(name="meme", hidden=True)
    @cooldown(1, 5, BucketType.guild)
    async def meme(self, ctx):
        """
        Behind every meme there is a guy trying hard to make you smile. Respect memers!
        """
        async with ctx.channel.typing():
            memes_submissions = reddit.subreddit("meme").hot()
            post_to_pick = random.randint(1, 100)
            for i in range(0, post_to_pick):
                submission = memes_submissions.__next__()
            embed = Embed(
                title=submission.title,
                color=choice(
                    (0xFF00FF, 0xFF0000, 0x0000FF, 0x00FF00, 0xFFFF00, 0x00FFFF)
                ),
            )
            embed.set_image(url=submission.url)
        await ctx.send(embed=embed)

    @command(name="filter")
    @cooldown(1, 5, BucketType.user)
    async def give_filter(self, ctx, filter_type: str, member: Optional[Member]):
        """
        I hate this stuff. But you asked for it, you got it. Now get you avatar renovated.
        """
        FILTERS = (
            "greyscale",
            "invert",
            "brightness",
            "threshold",
            "sepia",
            "red",
            "green",
            "blue",
            "blurple",
            "pixelate",
            "blur",
        )
        if filter_type and filter_type in FILTERS:
            URL = (
                f"https://some-random-api.ml/canvas/{filter_type}/?avatar={member.avatar_url_as(format='png')}"
                if member
                else f"https://some-random-api.ml/canvas/{filter_type}/?avatar={ctx.author.avatar_url_as(format='png')}"
            )
            embed = Embed(
                colour=choice(
                    (0xFF00FF, 0xFF0000, 0x0000FF, 0x00FF00, 0xFFFF00, 0x00FFFF)
                )
            )
            embed.set_image(url=URL)
            try:
                await ctx.send(embed=embed)
            except Exception as e:
                print(e)
        # elif not filter_type:
        #     await ctx.send("How about mentioning a filter type, ay.")
        elif not filter_type in FILTERS:
            await ctx.send(
                "Maybe you would like to choose something from - \n`"
                + "` `".join(filter_avl for filter_avl in FILTERS)
                + "`"
            )

    @command(name="lyrics")
    @cooldown(1, 15, BucketType.guild)
    async def give_lyrics(self, ctx, *, song_info: str):
        """
        These days it's difficut to parse the forte and get the lyrics. Here, use this command.
        """
        URL = f"https://some-random-api.ml/lyrics?title={song_info}"
        embeds = []
        async with ctx.channel.typing():
            async with request("GET", URL) as response:
                if response.status == 200:
                    song_data = await response.json()
                    song_len = len(song_data["lyrics"])
                    n = song_len
                    len_arr = []
                    c = 0
                    while n > 0:
                        c += 1
                        len_arr.append(n)
                        n -= 2042
                    num_list = [x for x in range(c)]
                    result = zip(num_list, len_arr)
                    sorted_list = sorted(set(result))

                    for part in sorted_list[::-1]:
                        if part[0] == (len(sorted_list) - 1):
                            embed = Embed(
                                title=song_data["title"],
                                url=f"{song_data['links']['genius']}",
                                description=f"```{song_data['lyrics'][:part[1]]}```",
                                color=choice(
                                    (
                                        0xFF00FF,
                                        0xFF0000,
                                        0x0000FF,
                                        0x00FF00,
                                        0xFFFF00,
                                        0x00FFFF,
                                    )
                                ),
                            )
                            embed.set_author(name=song_data["author"])
                            if song_data["thumbnail"]["genius"]:
                                embed.set_thumbnail(
                                    url=song_data["thumbnail"]["genius"]
                                )
                            embeds.append(embed)
                        if not part[0] == 0:
                            embed = Embed(
                                description=f"```{song_data['lyrics'][part[1]:part[1]+2042]}```",
                                color=choice(
                                    (
                                        0xFF00FF,
                                        0xFF0000,
                                        0x0000FF,
                                        0x00FF00,
                                        0xFFFF00,
                                        0x00FFFF,
                                    )
                                ),
                            )
                            embeds.append(embed)
                        if part[0] == 0:
                            embed = Embed(
                                color=choice(
                                    (
                                        0xFF00FF,
                                        0xFF0000,
                                        0x0000FF,
                                        0x00FF00,
                                        0xFFFF00,
                                        0x00FFFF,
                                    )
                                ),
                            )
                            embed.set_footer(
                                text="If that's not the song, try mentioning a singer or ft. of the song in the command."
                            )
                            embeds.append(embed)
                else:
                    embed = Embed(
                        description="Seems like I don't have any result for that song."
                    )
                    embeds.append(embed)
        # print(embeds)
        for emb in embeds:
            await ctx.send(embed=emb)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")


def setup(bot):
    bot.add_cog(Fun(bot))
