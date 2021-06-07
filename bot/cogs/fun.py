import os
import discord
from discord.ext import commands
import random


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief='| e ask [Yes or No questions!]', aliases=['8ball'])
    async def ask(self, ctx, *, question):
        ball = [
            "As I see it, yes",
            "It is certain",
            "It is decidedly so",
            "Most likely",
            "Outlook good",
            "Signs point to yes",
            "Without a doubt",
            "Yes",
            "Yes - definitely",
            "You may rely on it",
            "Better not tell you now",
            "Concentrate and ask again",
            "Don't count on it",
            "My reply is no",
            "My sources say no",
            "Outlook not so good",
            "Very doubtful",
            "Definitly not",
            "You're trolling if you think yes",
            "Reconsider it",
            "I do not approve!",
            "There’s a hundred percent chance that I’m going to say ‘no’ to this one"
        ]
        await ctx.channel.purge(limit=1)
        await ctx.send(f'**{ctx.author.name}**: {question}\n\n**Answer**: {random.choice(ball)}')


def setup(client):
    client.add_cog(Fun(client))
