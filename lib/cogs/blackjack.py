from typing import Optional
import random
import asyncio

from discord.ext.commands import Cog, command
from discord import Embed
import discord


playing = True

spade = "♠"
heart = "♥"
diamond = "♦"
club = "♣"


suits = (heart, diamond, spade, club)
ranks = (
    "Two",
    "Three",
    "Four",
    "Five",
    "Six",
    "Seven",
    "Eight",
    "Nine",
    "Ten",
    "Jack",
    "Queen",
    "King",
    "Ace",
)
values = {
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
    "Six": 6,
    "Seven": 7,
    "Eight": 8,
    "Nine": 9,
    "Ten": 10,
    "Jack": 10,
    "Queen": 10,
    "King": 10,
    "Ace": 11,
}

total = 100


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.values = values

    def __str__(self):
        return self.suit + " " + str(self.values[self.rank])


class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_comp = ""
        for card in self.deck:
            deck_comp += "\n" + card.__str__()
        return "The dack has: " + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]

    def adjust_for_aces(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:
    def __init__(self):
        global total
        self.total = total
        self.bet = 0

    def win_bet(self):
        per = str(random.randint(60, 130))
        bet_msg = f"You won {per}%"
        self.total += (self.bet * int(per)) // 100
        return bet_msg

    def lose_bet(self):
        bet_msg = f"You lose 100%"
        self.total -= self.bet
        return bet_msg


class BlackJack(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(
        name="blackjack",
        aliases=["bj"],
        description="Play some blackjack. (Don't get addicted though!)",
    )
    async def play_blackjack(self, ctx):
        global playing
        # This is not the ideal way of doing it. But deal with it.
        self.bot.get_command("blackjack").enabled = False

        async def take_bet(chips):
            while True:
                try:
                    await ctx.send(
                        embed=Embed(
                            title=f"{ctx.author.name}, you'll have to bet some chips `MAX - 100`",
                            colour=0x48A14D,
                        )
                    )
                    x = await self.bot.wait_for(
                        "message",
                        check=lambda message: message.author == ctx.author
                        and message.channel == ctx.channel,
                    )
                    if x:
                        print("take bet ====>>>>", x)
                        chips.bet = int(x.content)
                    else:
                        print("there is no x")
                except ValueError:
                    await ctx.send(
                        embed=Embed(description="I doesn't seen to be counted, tbh.")
                    )
                except Exception as e:
                    print(e)
                else:
                    if chips.bet > chips.total:
                        print(
                            f"You don't have enough chips. You have {chips.total} chips."
                        )
                    else:
                        break

        def hit(deck, hand):
            hand.add_card(deck.deal())
            hand.adjust_for_aces()

        async def show_some(player, dealer):
            print("\nDealer's Hand:")
            print(" <card hidden>")
            print("", dealer.cards[1])
            print("\nPlayer's Hand:", *player.cards, sep="\n ")

            embed = Embed(colour=ctx.author.colour)

            embed.add_field(
                name=ctx.author.name,
                value=f"Cards-{' '.join('`'+str(card)+'`' for card in player.cards)}"
                + "\n"
                + f"Total-{player.value}",
            )
            embed.add_field(
                name="boNo_101",
                value=f"Cards-`{dealer.cards[1]}` `?`" + "\n" + f"Total-`?`",
            )
            embed.set_footer(text="K, Q, J = 10 | A = 1 or 11")

            embed.set_author(
                name=f"{ctx.author.name}'s blackjack game",
                icon_url=ctx.author.avatar_url_as(format="png"),
            )
            await ctx.send("Type `h` to hit or type `s` to stand", embed=embed)

        async def show_all(player, dealer, string, colour, bet_msg, pc):
            print("\nDealer's Hand:", *dealer.cards, sep="\n ")
            print("Dealer's Hand =", dealer.value)
            print("\nPlayer's Hand:", *player.cards, sep="\n ")
            print("Player's Hand =", player.value)

            embed = Embed(
                description=f"**{string}**" + "\n" + f"You now have {pc.total} chips",
                colour=colour,
            )

            embed.add_field(
                name=ctx.author.name,
                value=f"Cards-{' '.join('`'+str(card)+'`' for card in player.cards)}"
                + "\n"
                + f"Total-{player.value}",
            )
            embed.add_field(
                name="boNo_101",
                value=f"Cards-{' '.join('`'+str(card)+'`' for card in dealer.cards)}"
                + "\n"
                + f"Total-{dealer.value}",
            )
            embed.set_author(
                name=f"{ctx.author.name}'s blackjack game",
                icon_url=ctx.author.avatar_url_as(format="png"),
            )
            embed.set_footer(text=bet_msg)
            await ctx.send(embed=embed)

        async def hit_or_stand(deck, hand, playing):
            # global playing
            while True:
                # x = input("Hit or Stand? Enter h or s: ")
                x = await self.bot.wait_for(
                    "message",
                    check=lambda message: message.author == ctx.author
                    and message.channel == ctx.channel
                    and message.content.lower() in ["h", "s"],
                )
                print("hit or stand ====>>>>", x)
                if x.content[0].lower() == "h":
                    hit(deck, hand)
                elif x.content[0].lower() == "s":
                    print("Player Stands. Dealer's turn")
                    playing = False
                    return playing
                else:
                    await ctx.send(
                        embed=Embed(
                            description="FYI, valid input only. Enter again (h/s)"
                        )
                    )
                    continue
                break

        def player_busts(player, dealer, chips):
            string = "You are Busted!"
            colour = 0xB33F40
            bet_msg = chips.lose_bet()
            return (string, colour, bet_msg)

        def player_wins(player, dealer, chips):
            if player.value == 21:
                string = "You Win! You have 21."
            else:
                string = "You Win!"
            colour = 0x48A14D
            bet_msg = chips.win_bet()
            return (string, colour, bet_msg)

        def dealer_busts(player, dealer, chips):
            string = "You Win! You Opponent Busted!"
            colour = 0x48A14D
            bet_msg = chips.win_bet()
            return (string, colour, bet_msg)

        def dealer_wins(player, dealer, chips):
            if dealer.value == 21:
                string = "You Opponent Wins! 21!"
            else:
                string = "Your Opponent Wins!"
            colour = 0xB33F40
            bet_msg = chips.lose_bet()
            return (string, colour, bet_msg)

        def push(player, dealer):
            colour = 0xEDD94C
            string = "You tied with your opponent!"
            return (string, colour)

        print("Welcome To BlackJack!!")
        deck = Deck()
        deck.shuffle()

        player_hand = Hand()
        player_hand.add_card(deck.deal())
        player_hand.add_card(deck.deal())

        dealer_hand = Hand()
        dealer_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())

        player_chips = Chips()
        playing = True
        await take_bet(player_chips)

        await show_some(player_hand, dealer_hand)

        while playing:
            string = ""
            bet_msg = "You total remains unchanged."
            colour = 0xFFFFFF
            play = await hit_or_stand(deck, player_hand, playing)
            if type(play) == "NoneType":
                playing = True
            elif play == False:
                self.bot.get_command("blackjack").enabled = True
                playing = False

            if player_hand.value >= 21:
                string, colour, bet_msg = player_busts(
                    player_hand, dealer_hand, player_chips
                )
                await show_all(
                    player_hand, dealer_hand, string, colour, bet_msg, player_chips
                )
                break
            elif playing:
                await show_some(player_hand, dealer_hand)

        if player_hand.value <= 21:
            while dealer_hand.value < 17:
                hit(deck, dealer_hand)

            if dealer_hand.value > 21:
                string, colour, bet_msg = dealer_busts(
                    player_hand, dealer_hand, player_chips
                )
            elif dealer_hand.value > player_hand.value:
                string, colour, bet_msg = dealer_wins(
                    player_hand, dealer_hand, player_chips
                )
            elif dealer_hand.value < player_hand.value:
                string, colour, bet_msg = player_wins(
                    player_hand, dealer_hand, player_chips
                )
            else:
                string, colour = push(player_hand, dealer_hand)

            await show_all(
                player_hand, dealer_hand, string, colour, bet_msg, player_chips
            )

        self.bot.get_command("blackjack").enabled = True
        print(f"\n Player total chips are at {player_chips.total}")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("blackjack")


def setup(bot):
    bot.add_cog(BlackJack(bot))