import os
import discord
from discord.ext import commands
import random
import json
from discord.ext.commands.cooldowns import BucketType
import asyncio
import datetime
import threading


# async def once_a_day(self, ctx):
#     ran = ''.join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])
#     lotnum = await self.lotterydata()
#     for num in lotnum:
#         print(ran, "is this a 6 digit num")
#         print(num[0], "is this the user ID?")
#         print(await self.client.fetch_user(num[0]), "is this the user name?")
#         print(num["number"], "is this the user number?")
#         if ran in num["number"]:
#             winner = num[0]
#             won = await self.client.fetch_user(winner)
#             with open("pool.json", "r") as f:
#                 amt = json.load(f)
#             total = amt["Loses"]["amount"]
#             await ctx.send(f"**{won.name} WON THE RAFFLE OF ${total}, CONGRATS!!!**")
#             await won.send(f"**YOU WON THE RAFFLE OF ${total}!**")
#             await self.update(won, total)
#             amt["Loses"]["amount"] = 0
#             return


class Money(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief="| e give <@user> [Amount]", aliases=['gift', 'send'])
    async def give(self, ctx, member: commands.MemberConverter, amount=None):
        await ctx.channel.purge(limit=1)
        await self.openacc(ctx.author)
        await self.openacc(member)
        amount = int(amount)
        urbal = await self.update(ctx.author)

        if amount == None:
            await ctx.send("Please enter amount to give!")
            return
        if member == ctx.author:
            await ctx.send("You can't steal from yourself!")
            self.give.reset_cooldown(ctx)
            return
        if int(urbal) < float(amount):
            await ctx.send(f"**{ctx.author.name}**, you don't have that much to give...")
            self.rob.reset_cooldown(ctx)
            return
        await self.update(ctx.author, -1*amount)
        await self.update(member, amount)
        amount = ("{:,}".format(amount))
        await ctx.send(f"**{ctx.author.name}** gave **${amount}** to **{member.name}**!")

####################################################################################
####################################################################################

    @commands.command(brief="| e rob <@user> (Steal from another person!)", aliases=['steal'])
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def rob(self, ctx, member: commands.MemberConverter):
        await ctx.channel.purge(limit=1)
        await self.openacc(ctx.author)
        await self.openacc(member)

        bal = await self.update(member)
        if member == ctx.author:
            await ctx.send("You can't steal from yourself!")
            self.rob.reset_cooldown(ctx)
            return

        if int(bal) < 1000:
            await ctx.send(f"**{member.name}** is already broke, **{ctx.author.name}** is a bad person...")
            self.rob.reset_cooldown(ctx)
            return
        r = random.randrange(1, 3)
        if r == 3:
            stolen = int(bal)*0.05
        elif r == 2:
            stolen = int(bal)*0.04
        else:
            stolen = int(bal)*0.03

        await self.update(ctx.author, int(stolen))
        await self.update(member, int(-1*stolen))
        stolen = ("{:,}".format(int(stolen)))
        await ctx.send(f"**{ctx.author.name}** stole **${stolen}** from <@{member.id}>!")

    @rob.error
    async def rob_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.channel.purge(limit=1)
            if int(error.retry_after) > 60:
                await ctx.send(f"**{ctx.author.name}** is on the run from stealing, try again in **{int(error.retry_after//60)} minutes** and **{int(error.retry_after % 60)} seconds!**")
            else:
                await ctx.send(f"**{ctx.author.name}** is on the run from stealing, try again in **{int(error.retry_after % 60)} seconds!**")

####################################################################################
####################################################################################

    @commands.command(brief='| e work (Gain money every hour!)')
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def work(self, ctx):
        ran = random.randint(2000, 3000)
        await self.update(ctx.author, ran)
        await ctx.channel.purge(limit=1)

        if ran <= 2100:
            await ctx.send(f"**{ctx.author.name}** robbed a 7-Eleven and got **${ran}**")
        elif ran <= 2200:
            await ctx.send(f"**{ctx.author.name}** earned **${ran}** from working overtime")
        elif ran <= 2300:
            await ctx.send(f"**{ctx.author.name}** copped Yeezys and resold for **${ran}**")
        elif ran <= 2400:
            await ctx.send(f"**{ctx.author.name}** broke into Timothy Kennedy's home and found **${ran}**")
        elif ran <= 2500:
            await ctx.send(f"**{ctx.author.name}** laundered money for Krystal and got **${ran}**")
        elif ran <= 2600:
            await ctx.send(f"**{ctx.author.name}** went to an actual casino and won **${ran}**")
        elif ran <= 2700:
            await ctx.send(f"**{ctx.author.name}** copped Jordans and resold for **${ran}**")
        elif ran <= 2800:
            await ctx.send(f"**{ctx.author.name}** started an ecommerce business and made **${ran}**")
        elif ran <= 2900:
            await ctx.send(f"**{ctx.author.name}** sold their dogecoin holdings and made **${ran}**")
        elif ran <= 3000:
            await ctx.send(f"**{ctx.author.name}** started a business and made **${ran}**")

    @work.error
    async def work_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.channel.purge(limit=1)
            if int(error.retry_after) > 60:
                await ctx.send(f"**{ctx.author.name}** is too tired to work, try again in **{int(error.retry_after//60)} minutes** and **{int(error.retry_after % 60)} seconds!**")
            else:
                await ctx.send(f"**{ctx.author.name}** is too tired to work, try again in **{int(error.retry_after % 60)} seconds!**")

####################################################################################
####################################################################################

    @commands.command(brief='| e work (Gain money every hour!)')
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        await self.update(ctx.author, 10000)
        await ctx.channel.purge(limit=1)
        await ctx.send(f"**{ctx.author.name}** recieved **$10,000** for their daily allowance.")

    @daily.error
    async def daily_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.channel.purge(limit=1)
            if int(error.retry_after) > 3600:
                await ctx.send(f"**{ctx.author.name}** already claimed the daily reward, try again in **{int(error.retry_after//3600)} hours** and **{int(error.retry_after%60)} minutes!**")
            elif int(error.retry_after) > 60:
                await ctx.send(f"**{ctx.author.name}** already claimed the daily reward, try again in **{int(error.retry_after//60)} minutes** and **{int(error.retry_after % 60)} seconds!**")
            else:
                await ctx.send(f"**{ctx.author.name}** already claimed the daily reward, try again in **{int(error.retry_after % 60)} seconds!**")


####################################################################################
####################################################################################

    @commands.command(aliases=['poor', 'broke', 'slum'], brief="| e slums [Amount #] (Default is 5)")
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def slums(self, ctx, x=5):
        await ctx.channel.purge(limit=1)
        users = await self.data()
        leader_board = {}
        total = []
        for user in users:
            name = int(user)
            total_amount = users[user]["wallet"]
            leader_board[total_amount] = name
            total.append(total_amount)
        total = sorted(total)

        if int(x) > 10:
            x = 10

        em = discord.Embed(title=f"**Top {x} Poorest People**",
                           description="💵💵💵💵💵💵💵💵", color=discord.Color.red())
        index = 1
        for amt in total:
            if int(amt) == 0:
                continue
            id_ = leader_board[amt]
            member = self.client.get_user(id_)
            name = member.name
            amt = ("{:,}".format(int(amt)))

            em.add_field(name=f"**{index}. {name}**",
                         value=f"${amt}",  inline=False)
            if index == x:
                break
            else:
                index += 1
        em.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=em)

    @slums.error
    async def slums_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.channel.purge(limit=1)
            if int(error.retry_after) > 60:
                await ctx.send(f"**{ctx.author.name}**, you can try checking again in **{int(error.retry_after//60)} minutes** and **{int(error.retry_after % 60)} seconds!**")
            else:
                await ctx.send(f"**{ctx.author.name}**, you can try checking again in **{int(error.retry_after % 60)} seconds!**")

####################################################################################
####################################################################################

    @commands.command(brief="| e lb [Amount #] (Default is 5)", aliases=["lb", 'rich', 'money'])
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def leaderboard(self, ctx, x=5):
        await ctx.channel.purge(limit=1)
        users = await self.data()
        leader_board = {}
        total = []
        for user in users:
            name = int(user)
            total_amount = users[user]["wallet"]
            leader_board[total_amount] = name
            total.append(total_amount)
        total = sorted(total, reverse=True)
        u = total.index(await self.update(ctx.author))
        uramt = await self.update(ctx.author)
        if uramt == 0:
            u = len(users)
        check = True
        if u <= x:
            check = False
        if int(x) > 10:
            x = 10
        em = discord.Embed(title=f"**Top {x} Richest People**",
                           description="💵💵💵💵💵💵💵💵", color=discord.Color.green())
        index = 1
        for amt in total:
            id_ = leader_board[amt]
            member = self.client.get_user(id_)
            name = member.name
            if name == ctx.author.name:
                name = f"{member.name}  <---  (YOU)"
            amt = ("{:,}".format(int(amt)))
            em.add_field(name=f"**{index}. {name}**",
                         value=f"${amt}",  inline=False)
            if index == x:
                break
            else:
                index += 1
        if check == True:
            uramt = ("{:,}".format(int(uramt)))
            em.add_field(name=f"**{u}. {ctx.author.name}  <---  (YOU)**",
                         value=f"${uramt}", inline=False)
        # em.set_thumbnail(url="https://media1.tenor.com/images/74090c93f4ee1dfa68839e154589bfa4/tenor.gif?itemid=8106915")
        em.timestamp = datetime.datetime.utcnow()
        em.set_footer(text=f"Total: {len(users)}")
        await ctx.send(embed=em)

    @leaderboard.error
    async def leaderboard_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.channel.purge(limit=1)
            if int(error.retry_after) > 60:
                await ctx.send(f"**{ctx.author.name}**, you can try checking again in **{int(error.retry_after//60)} minutes** and **{int(error.retry_after % 60)} seconds!**")
            else:
                await ctx.send(f"**{ctx.author.name}**, you can try checking again in **{int(error.retry_after % 60)} seconds!**")

####################################################################################
####################################################################################
####################################################################################
####################################################################################

    @commands.command(brief='| e bal (First use will reward $5000)', aliases=['bal'])
    async def balance(self, ctx):
        await self.openacc(ctx.author)
        user = ctx.author
        users = await self.data()
        wallet = users[str(user.id)]["wallet"]
        amt = ("{:,}".format(round(wallet)))
        em = discord.Embed(
            title=f"{ctx.author.name}'s Wallet", colour=discord.Colour.blue())
        em.add_field(name="Balance", value="$" + amt)
        em.timestamp = datetime.datetime.utcnow()
        em.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.channel.purge(limit=1)
        await ctx.send(embed=em)
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
####################################################################################

    async def data(self):
        with open("wallet.json", "r") as f:
            users = json.load(f)
        return users
####################################################################################

    async def update(self, user, change=0, mode="wallet"):
        users = await self.data()
        users[str(user.id)][mode] += change
        with open("wallet.json", "w") as f:
            json.dump(users, f)
        bal = users[str(user.id)]["wallet"]
        return bal

####################################################################################
####################################################################################
####################################################################################
####################################################################################

    async def lotterynum(self, user, number):
        users = await self.lotterydata()
        if str(user.id) in users:
            return False
        else:
            users[str(user.id)] = {}
            users[str(user.id)]["number"] = number
        with open("lottery.json", "w") as f:
            json.dump(users, f)
        return True
####################################################################################

    async def lotterydata(self):
        with open("lottery.json", "r") as f:
            users = json.load(f)
        return users
####################################################################################

    async def updatelottery(self, user, number):
        users = await self.lotterydata()
        users[str(user.id)]["number"] = number
        # print(await self.client.fetch_user(user.id))
        with open("lottery.json", "w") as f:
            json.dump(users, f)
        num = users[str(user.id)]["number"]
        return num

####################################################################################
####################################################################################

    @commands.command(brief="| e raffle [Number]", aliases=["lottery"])
    async def raffle(self, ctx, number):
        if len(number) != 6:
            await ctx.send(f"**{ctx.author.name}**, you need to enter the raffle with a 6 digit number!")
            return
        await self.lotterynum(ctx.author, number)
        await self.updatelottery(ctx.author, number)
        await ctx.send(f"**{ctx.author.name}**, your raffle number: **{number}**")

    @commands.command(brief="| e check (Money lost now goes into the prize pool!)", aliases=["prize", "pool"])
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def check(self, ctx):
        await ctx.channel.purge(limit=1)
        with open("pool.json", "r") as f:
            amt = json.load(f)
        total = amt["Loses"]["amount"]

        with open("lottery.json", "r") as f:
            users = json.load(f)
        user = ctx.author
        lotnum = users[str(user.id)]["number"]

        em = discord.Embed(title="**Raffle Prize Pool!**",
                           description=f"**${total}**", color=discord.Color.gold())
        em.add_field(
            name=f"**{ctx.author.name}'s Number**", value=f"#{lotnum}")
        await ctx.send(embed=em)

    @check.error
    async def check_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.channel.purge(limit=1)
            if int(error.retry_after) > 60:
                await ctx.send(f"**{ctx.author.name}**, you can try checking again in **{int(error.retry_after//60)} minutes** and **{int(error.retry_after % 60)} seconds!**")
            else:
                await ctx.send(f"**{ctx.author.name}**, you can try checking again in **{int(error.retry_after % 60)} seconds!**")

####################################################################################
####################################################################################
    # async def background_task():
    #     now = datetime.utcnow()
    #     WHEN = time(18, 0, 0)
    #     # Make sure loop doesn't start after {WHEN} as then it will send immediately the first time as negative seconds will make the sleep yield instantly
    #     if now.time() > WHEN:
    #         tomorrow = datetime.combine(
    #             now.date() + timedelta(days=1), time(0))
    #         # Seconds until tomorrow (midnight)
    #         seconds = (tomorrow - now).total_seconds()
    #         # Sleep until tomorrow and then the loop will start
    #         await asyncio.sleep(seconds)
    #     while True:
    #         now = datetime.now()
    #         target_time = datetime.combine(
    #             now.date(), WHEN)
    #         seconds_until_target = (target_time - now).total_seconds()
    #         await asyncio.sleep(seconds_until_target)
    #         await once_a_day()  # Call the helper function that sends the message
    #         tomorrow = datetime.combine(
    #             now.date() + timedelta(days=1), time(0))
    #         # Seconds until tomorrow (midnight)
    #         seconds = (tomorrow - now).total_seconds()
    #         # Sleep until tomorrow and then the loop will start a new iteration
    #         await asyncio.sleep(seconds)


def setup(client):
    client.add_cog(Money(client))
