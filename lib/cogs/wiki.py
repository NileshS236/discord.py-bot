from random import choice
from bs4 import *
import wikipedia
import requests

from discord import Embed
from discord.ext.commands import Cog, command


class Wiki(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="wiki", aliases=["search"])
    async def search_wiki(self, ctx, *, query: str):
        """
        I'm not a knowledge storehouse. But this command here sure is something. It might give you a wikipedia reference of your query
        """
        async with ctx.channel.typing():
            # Given URL
            query = wikipedia.search(query)[0]

            url = f"https://en.wikipedia.org/wiki/{query}"

            base_url = "https://en.wikipedia.org"

            # Fetch URL Content
            r = requests.get(url)

            # Get body content
            soup = BeautifulSoup(r.text, "html.parser").select("body")[0]

            # print(soup.prettify())

            # Initialize variable
            paragraphs = []
            images = []
            link = []
            heading = []
            remaining_content = []
            content = ""

            # Iterate throught all tags
            for tag in soup.find_all():
                # Check each tag name
                # For Paragraph use p tag
                if tag.name == "p":
                    # use text for fetch the content inside p tag
                    paragraphs.append(tag.text)

                # For Image use img tag
                elif tag.name == "img":
                    # Add url and Image source URL
                    if "//upload.wikimedia.org/wikipedia/en/" in str(
                        tag["src"]
                    ) and not ".svg" in str(tag["src"]):
                        images.append("https:" + tag["src"])
                    elif "//upload.wikimedia.org/wikipedia/commons/thumb/" in str(
                        tag["src"]
                    ) and not ".svg" in str(tag["src"]):
                        images.append("https:" + tag["src"])
                    else:
                        images.append(url + tag["src"])

                # For Anchor use a tag
                elif tag.name == "a":

                    # convert into string and then check href
                    # available in tag or not
                    if "href" in str(tag):

                        # In href, there might be possible url is not there
                        # if url is not there
                        if "https://en.wikipedia.org/w/" not in str(tag["href"]):
                            link.append(base_url + tag["href"])
                        else:
                            link.append(tag["href"])

                # Similary check for heading
                # Six types of heading are there (H1, H2, H3, H4, H5, H6)
                # check each tag and fetch text
                elif "h" in tag.name:
                    if "h1" == tag.name:
                        heading.append(tag.text)
                    elif "h2" == tag.name:
                        heading.append(tag.text)
                    elif "h3" == tag.name:
                        heading.append(tag.text)
                    elif "h4" == tag.name:
                        heading.append(tag.text)
                    elif "h5" == tag.name:
                        heading.append(tag.text)
                    else:
                        heading.append(tag.text)

                # Remain content will store here
                else:
                    remaining_content.append(tag.text)

            embeds = []
            # print(title)
            embed1 = Embed(
                title=f"{query} - Wikipedia",
                url=f"{url.replace(' ', '_')}",
                colour=ctx.author.colour,
            )
            for image in images:
                if "https://upload.wikimedia.org/wikipedia/en/" in str(image):
                    embed1.set_image(url=image)
                    # print(image)
                    break
                elif "https://upload.wikimedia.org/wikipedia/commons/thumb/" in str(
                    image
                ):
                    embed1.set_image(url=image)
                    # print(image)
                    break
            embeds.append(embed1)
            for para in paragraphs:
                if not str(para).strip() == "" and len(content + str(para)) <= 997:
                    content += str(para)
                elif len(content + str(para)) > 997:
                    para = para[: (1020 - len(content))]
                    content += f"{para}..."
                    break

            print(len(content))
            embed2 = Embed(
                title="Brief",
                description=f"```{content}``` [More]({url.replace(' ', '_')})",
                colour=ctx.author.colour,
            )
            embeds.append(embed2)

            embed2.set_footer(
                text="If that not what you are looking for try giving being more accurate query."
            )

            # await ctx.send
        for embed in embeds:
            await ctx.send(embed=embed)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("wiki")


def setup(bot):
    bot.add_cog(Wiki(bot))