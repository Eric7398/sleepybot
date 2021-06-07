import discord
import os
from discord import colour
from discord.ext import commands


class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    # BAN USER
    @commands.command(brief='| e ban <@user> [Reason]')
    async def ban(self, ctx, member: commands.MemberConverter, *, reason=None):
        if await self.client.is_owner(ctx.author) or ctx.message.author.guild_permissions.ban_members:

            mbed = discord.Embed(
                colour=(discord.Colour.magenta()),
                title=f'You Have Been BANNED from **{ctx.guild.name}**!',
                description=f'Banned for "{reason}"',
            )

            await ctx.channel.purge(limit=1)
            await member.send(embed=mbed)
            await member.ban(reason=reason)
            await ctx.send(f'{member} has been **Banned** for "{reason}"')
            return
        else:
            print(f"{ctx.message.author} tried to ban in {ctx.message.guild.name}")
            await ctx.send("You don't have permission to ban!")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"I don't have permission to ban this user!")

    # UNBAN USER

    @commands.command(brief='| e unban <@user>')
    async def unban(self, ctx, *, member):
        if await self.client.is_owner(ctx.author) or ctx.message.author.guild_permissions.ban_members:

            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split('#')
            for ban_entry in banned_users:
                user = ban_entry.user
                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.channel.purge(limit=1)
                    await ctx.guild.unban(user)
                    await ctx.send(f'{user.mention} has been **unbanned**')
                    return
                else:
                    print(
                        f"{ctx.message.author} tried to clear unban in {ctx.message.guild.name}")
        else:
            await ctx.send("You don't have permission to unban!")

    # KICK USER

    @commands.command(brief='| e kick <@user> [Reason]')
    async def kick(self, ctx, member: commands.MemberConverter, *, reason=None):
        if await self.client.is_owner(ctx.author) or ctx.message.author.guild_permissions.kick_members:
            invitelink = await ctx.channel.create_invite(max_uses=1, unique=True)

            mbed = discord.Embed(
                colour=(discord.Colour.magenta()),
                title=f'You Have Been KICKED from **{ctx.guild.name}**!',
                description=f'Kicked for "{reason}"\nBe more mindful next time.\nLink: {invitelink}',
            )

            await ctx.channel.purge(limit=1)
            await member.send(embed=mbed)
            await member.kick(reason=reason)
            await ctx.send(f'{member} has been **Kicked** for "{reason}"')
            return
        else:
            print(
                f"{ctx.message.author} tried to kick in {ctx.message.guild.name}")
            await ctx.send("You don't have permission to kick!")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"I don't have permission to kick this user!")

    # CLEAR CHAT LOGS
    @commands.command(brief='| e clear [Amount #]', aliases=['clr'])
    async def clear(self, ctx, amount=1):
        if await self.client.is_owner(ctx.author) or ctx.message.author.guild_permissions.manage_messages:
            if int(amount) > 10:
                await ctx.channel.purge(limit=10+1)
                return
            else:
                await ctx.channel.purge(limit=amount+1)
                return

        else:
            print(
                f"{ctx.message.author} tried to clear chatlogs in {ctx.message.guild.name}")
            await ctx.send("You don't have permission to clear chatlogs!")


def setup(client):
    client.add_cog(Admin(client))
