import os
import discord
from discord.ext import commands
import random
import json
from discord.ext.commands.cooldowns import BucketType
import asyncio
import datetime

# os.chdir("C:\\Users\\ericw\\Desktop\\Discord\\bot\\cogs")


class Gamble(commands.Cog):
    def __init__(self, client):
        self.client = client

####################################################################################
####################################################################################

#     @commands.command(brief="| e bj [Amount]", aliases=['bj', '21'])
#     async def blackjack(self, ctx, amount=None):
#         await self.openacc(ctx.author)
#         await ctx.channel.purge(limit=1)
#         if amount == None:
#             await ctx.send(f"**{ctx.author.name}**, please enter amount for blackjack!")
#             return
#         bal = await self.update(ctx.author)
#         amount = int(amount)
#         if amount > bal:
#             await ctx.send(f"**{ctx.author.name}**, don't have enough money to play blackjack!")
#             return
#         if amount < 100:
#             await ctx.send(f"**{ctx.author.name}**, you need at least **$100** to play!")
#             return

#         deck = []
#         suits = ["Hearts", "Spades", "Diamonds", "Clubs"]
#         cards = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]
#         for suit in suits:
#             for card in cards:
#                 deck.append([suit, card])
#         print(deck)
#         print(len(deck))

# ####################################################################################
#         em = discord.Embed(
#             title="**\u2664 \u2667 BLACKJACK \u2662 \u2661**", description=f"**Enjoy your game {ctx.author.name}!**", colour=discord.Colour.gold())
#         em.add_field(name="- **type s to start**\n- **type p to join**",
#                      value=f"Current Bet: **${amount}**", inline=False)
#         await ctx.send(embed=em)
####################################################################################


####################################################################################
####################################################################################
####################################################################################
####################################################################################


    @commands.command(brief="| e crash [Amount]")
    async def crash(self, ctx, amount=None):
        await self.openacc(ctx.author)
        await ctx.channel.purge(limit=1)
        if amount == None:
            await ctx.send(f"**{ctx.author.name}**, please enter amount for crash!")
            return
        bal = await self.update(ctx.author)
        if amount == "all":
            amount = bal
        amount = int(amount)
        if amount > bal:
            await ctx.send(f"**{ctx.author.name}**, don't have enough money to play crash!")
            return
        if amount < 200:
            await ctx.send(f"**{ctx.author.name}**, you need at least **$200** to play!")
            return
        if amount > 50000 and amount != bal:
            await ctx.send(f"**{ctx.author.name}**, you can't spend more than **$50,000** on crash!")
            return
        stramount = ("{:,}".format(amount))
        crash_embed = discord.Embed(
            title="<a:crash:846885033616998400>       **Crash**       <a:crash:846885033616998400>", colour=discord.Colour.gold())
        crash_embed.add_field(name=f"\u200b  Good Luck **{ctx.author.name}**!",
                              value="**===============**", inline=False)
        crash_embed.add_field(name="**Multipler**",
                              value="1x", inline=True)
        crash_embed.add_field(
            name="**Gain**", value=f"${stramount}", inline=True)
        crash_embed.add_field(
            name="**===============**", value="\u200b  type **s** to stop", inline=False)
        crash_embed.timestamp = datetime.datetime.utcnow()

        precrash = await ctx.send(embed=crash_embed)

        crash = random.randrange(1, 100)
        if crash == 100:
            c = random.randrange(40, 200)
        elif crash >= 98:
            c = random.randrange(30, 40)
        elif crash >= 95:
            c = random.randrange(25, 30)
        elif crash >= 85:
            c = random.randrange(20, 25)
        elif crash >= 75:
            c = random.randrange(16, 20)
        elif crash >= 68:
            c = random.randrange(10, 16)
        elif crash <= 57:
            c = random.randrange(1, 6)
        else:
            c = random.randrange(8, 10)
        await asyncio.sleep(1)
        upto = 1
        i = 1

        print(
            f"{ctx.author.name} rolled a {crash} and crashing at {c * 0.25-0.25+1}x with ${amount} in {ctx.author.guild.name}")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        stopped = False
####################################################################################
        while c > i and not stopped:
            try:
                msg = await self.client.wait_for("message", check=check, timeout=1)
                stopped = True if msg.content.lower() == "s" else False
            except asyncio.TimeoutError:
                upto += 0.25
                i += 1
                uptoamt = ("{:,}".format(upto * round(float(amount))))
                newc_embed = discord.Embed(
                    title="<a:crash:846885033616998400>       **Crash**       <a:crash:846885033616998400>", colour=discord.Colour.gold())
                newc_embed.add_field(name=f"\u200b  Good Luck **{ctx.author.name}**!",
                                     value="**===============**", inline=False)
                newc_embed.add_field(name="**Multipler**",
                                     value=f"{upto}x", inline=True)
                newc_embed.add_field(
                    name="**Gain**", value=f"${uptoamt}", inline=True)
                newc_embed.add_field(
                    name="**===============**", value="\u200b  type **s** to stop", inline=False)
                newc_embed.timestamp = datetime.datetime.utcnow()

                await precrash.edit(embed=newc_embed)
####################################################################################
        if stopped == True:

            p = (upto * round(float(amount))) - amount
            print(f"{ctx.author.name} won {p} at {upto}x")
            r = await self.update(ctx.author, int(p))
            uptoamt = ("{:,}".format(upto * round(float(amount))))
            p = ("{:,}".format(int(p)))
            r = ("{:,}".format(int(r)))

            await ctx.channel.purge(limit=1)
            newc_embed = discord.Embed(
                title=":dollar:       **Crash**       :dollar:", colour=discord.Colour.green())
            newc_embed.add_field(name=f"\u200b          You Won!",
                                 value="**===============**", inline=False)
            newc_embed.add_field(name="**Multipler**",
                                 value=f"{upto}x", inline=True)
            newc_embed.add_field(
                name="**Gain**", value=f"${uptoamt}", inline=True)
            newc_embed.add_field(
                name="**===============**", value=f"**{ctx.author.name}** won **${p}**\nBalance **${r}**", inline=False)
            newc_embed.timestamp = datetime.datetime.utcnow()

            await precrash.edit(embed=newc_embed)
####################################################################################
        elif i == c:
            print(f"{ctx.author.name} lost {-1*amount}")
            await self.loses(amount)
            r = await self.update(ctx.author, -1*amount)
            uptoamt = ("{:,}".format(upto * round(float(amount))))
            amt = ("{:,}".format(int(amount)))
            r = ("{:,}".format(int(r)))

            newc_embed = discord.Embed(
                title=":boom:       **Crash**       :boom:", colour=discord.Colour.red())
            newc_embed.add_field(name=f"\u200b      You Crashed!",
                                 value="**===============**", inline=False)
            newc_embed.add_field(name="**Multipler**",
                                 value=f"{upto}x", inline=True)
            newc_embed.add_field(
                name="**Profit**", value=f"${uptoamt}", inline=True)
            newc_embed.add_field(
                name="**===============**", value=f"**{ctx.author.name}** lost **${amt}**\nBalance **${r}**", inline=False)
            newc_embed.timestamp = datetime.datetime.utcnow()
            await precrash.edit(embed=newc_embed)


####################################################################################
####################################################################################
####################################################################################
####################################################################################


    @ commands.command(brief='| e slot [Amount]', aliases=['slots'])
    async def slot(self, ctx, amount=None):
        await self.openacc(ctx.author)
        await ctx.channel.purge(limit=1)
        if amount == None:
            await ctx.send(f"**{ctx.author.name}**, please enter amount for slot!")
            return
        bal = await self.update(ctx.author)
        if amount == "all":
            amount = bal
        amount = int(amount)
        if amount > bal:
            await ctx.send(f"**{ctx.author.name}**, doesn't have enough money to play slot!")
            return
        if amount < 100:
            await ctx.send(f"**{ctx.author.name}**, you need at least **$100** to play slot!")
            return
        final = []

        for i in range(3):
            a = random.choice(["💯", "❄️", "💎",
                               "💵", "🥇", "🏆"])
            final.append(a)

        if final[0] == "💯" and final[1] == "💯" and final[2] == "💯":
            m = await self.update(ctx.author, 10 * amount)
            nm = ("{:,}".format(round(m)))
            mbal = ("{:,}".format(round(m-bal)))
            r = "**100!!!**"
            c = discord.Colour.green()
            f = (f"**{ctx.author.name}** won **${mbal}**")
            b = (f"**New Balance ${nm}**")
            print(f"{ctx.author.name} won 10x slots in {ctx.author.guild.name}")

        elif final[0] == final[1] and final[0] == final[2]:
            m = await self.update(ctx.author, 5 * amount)
            nm = ("{:,}".format(round(m)))
            mbal = ("{:,}".format(round(m-bal)))
            r = "WINNER!"
            c = discord.Colour.green()
            f = (f"**{ctx.author.name}** won **${mbal}**")
            b = (f"**New Balance ${nm}**")
            print(f"{ctx.author.name} won 5x slots in {ctx.author.guild.name}")

        elif final[0] == final[1] or final[1] == final[2]:
            m = await self.update(ctx.author, 3 * amount)
            nm = ("{:,}".format(round(m)))
            mbal = ("{:,}".format(round(m-bal)))
            r = "You Won!"
            c = discord.Colour.green()
            f = (f"**{ctx.author.name}** won **${mbal}**")
            b = (f"**New Balance ${nm}**")
            print(f"{ctx.author.name} won 3x slots in {ctx.author.guild.name}")

        else:
            await self.loses(amount)
            m = await self.update(ctx.author, -1*amount)
            nm = ("{:,}".format(round(m)))
            mbal = ("{:,}".format(round(bal-m)))
            r = "You Lost!"
            c = discord.Colour.red()
            f = (
                f"**{ctx.author.name}** lost **${mbal}**")
            b = (f"**Balance ${nm}**")
            print(f"{ctx.author.name} lost on slots in {ctx.author.guild.name}")
        amount = ("{:,}".format(round(amount)))
        icon = ""
        icon += f"\u200b  **|**   <a:cycle:846646908164374539>   "
        icon += f"**|**   <a:cycle:846646908164374539>   "
        icon += f"**|**   <a:cycle:846646908164374539>   **|**"

        slot_embed = discord.Embed(
            title="-      **Slot Machine**      -")
        slot_embed.add_field(name=f"\u200b   Good Luck **{ctx.author.name}**!",
                             value="**=================**", inline=False)

        slot_embed.add_field(
            name=f"  {icon}  ", value="**=================**", inline=False)

        slot_embed.add_field(name="\u200b            Spinning...",
                             value=f"Current Bet: **${amount}**", inline=False)
        slot_embed.timestamp = datetime.datetime.utcnow()
        sent_embed = await ctx.send(embed=slot_embed)
        current_slot_pics = ["<a:cycle:846646908164374539>",
                             "<a:cycle:846646908164374539>",
                             "<a:cycle:846646908164374539>"]

#######################################################################
        await asyncio.sleep(1.5)
        current_slot_pics[0] = final[0]
        new_slot_embed = None
        new_slot_embed = discord.Embed(
            title="-      **Slot Machine**      -",)
        slot_results_str = ""
        for thisSlot in current_slot_pics:
            slot_results_str += f"**|**   {thisSlot}   "
        new_slot_embed.add_field(name=f"\u200b   Good Luck **{ctx.author.name}**!",
                                 value="**=================**", inline=False)
        new_slot_embed.add_field(
            name=f"\u200b  {slot_results_str}**|**", value="**=================**")
        new_slot_embed.add_field(name="\u200b            Spinning...",
                                 value=f"Current Bet: **${amount}**", inline=False)
        new_slot_embed.timestamp = datetime.datetime.utcnow()
        await sent_embed.edit(embed=new_slot_embed)
#######################################################################
        await asyncio.sleep(1.5)
        current_slot_pics[1] = final[1]
        new_slot_embed = None
        new_slot_embed = discord.Embed(
            title="-      **Slot Machine**      -",)
        slot_results_str = ""
        for thisSlot in current_slot_pics:
            slot_results_str += f"**|**   {thisSlot}   "
        new_slot_embed.add_field(name=f"\u200b   Good Luck **{ctx.author.name}**!",
                                 value="**=================**", inline=False)
        new_slot_embed.add_field(
            name=f"\u200b  {slot_results_str}**|**", value="**=================**")
        new_slot_embed.add_field(name="\u200b            Spinning...",
                                 value=f"Current Bet: **${amount}**", inline=False)
        new_slot_embed.timestamp = datetime.datetime.utcnow()
        await sent_embed.edit(embed=new_slot_embed)
#######################################################################
        await asyncio.sleep(1.5)
        current_slot_pics[2] = final[2]
        new_slot_embed = None
        new_slot_embed = discord.Embed(
            title="-      **Slot Machine**      -",
            colour=c)
        slot_results_str = ""
        for thisSlot in current_slot_pics:
            slot_results_str += f"**|**   {thisSlot}   "
        new_slot_embed.add_field(name="\u200b             "+r,
                                 value="**=================**",  inline=False)
        new_slot_embed.add_field(
            name=f"\u200b  {slot_results_str}**|**", value="**=================**")
        new_slot_embed.add_field(name=f,
                                 value=b, inline=False)
        new_slot_embed.timestamp = datetime.datetime.utcnow()

        await sent_embed.edit(embed=new_slot_embed)

####################################################################################
####################################################################################
####################################################################################
####################################################################################

    async def openacc(self, user):
        users = await self.data()
        if str(user.id) in users:
            return False
        else:
            users[str(user.id)] = {}
            users[str(user.id)]["wallet"] = 5000
        with open("wallet.json", "w") as f:
            json.dump(users, f)
        return True

    async def data(self):
        with open("wallet.json", "r") as f:
            users = json.load(f)
        return users

    async def update(self, user, change=0):
        users = await self.data()
        users[str(user.id)]["wallet"] += change
        with open("wallet.json", "w") as f:
            json.dump(users, f)
        bal = users[str(user.id)]["wallet"]
        return bal

####################################################################################
####################################################################################
####################################################################################
####################################################################################
    async def loses(self, amount):
        with open("pool.json", "r") as f:
            total = json.load(f)
        total["Loses"]["amount"] += amount

        with open("pool.json", "w") as f:
            json.dump(total, f)
        num = total["Loses"]["amount"]
        return num


def setup(client):
    client.add_cog(Gamble(client))
