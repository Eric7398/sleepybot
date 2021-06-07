import os
import discord
from discord.ext import commands
import requests
from datetime import datetime


class Essential(commands.Cog):
    def __init__(self, client):
        self.client = client


#   commands.Cog.listener is an event listener


    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'{member} has joined {member.guild.name}!')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member} is no longer in {member.guild.name}!')


#   commands.command is a client command function


    @commands.command(brief='| e ping (Checks Server Latency)')
    async def ping(self, ctx):
        await ctx.channel.purge(limit=1)
        await ctx.send(f"{ctx.author.name}, Pong! **{round(self.client.latency * 1000)}ms**")

    @commands.command(brief='| e quote')
    async def quote(self, ctx):
        await ctx.channel.purge(limit=1)
        response = requests.get("https://zenquotes.io/api/random")
        json = response.json()
        await ctx.send(f"**{json[0]['q']}**\n- *{json[0]['a']}*")

    @commands.command(brief='| e joke', aliases=['jokes'])
    async def joke(self, ctx):
        await ctx.channel.purge(limit=1)
        response = requests.get(
            "https://official-joke-api.appspot.com/random_joke")
        json = response.json()
        await ctx.send(f"**{json['setup']}**\n\n**||{json['punchline']}||**")

    # @commands.command(brief="| e weather [city]", aliases=['temp'])
    # async def weather(self, ctx, *, location):
    #     await ctx.channel.purge(limit=1)
    #     url = "https://community-open-weather-map.p.rapidapi.com/weather"
    #     querystring = {"q": location, "cnt": "0", "mode": "null", "lon": "0",
    #                    "type": "link, accurate", "lat": "0", "units": "imperial"}
    #     headers = {
    #         'x-rapidapi-key': "02aabb0dd2mshc232505e035a807p105762jsna4964d73bc31",
    #         'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
    #     }

    #     response = requests.request(
    #         "GET", url, headers=headers, params=querystring)
    #     response = response.json()
    #     country = response["sys"]["country"]
    #     city = response["name"]
    #     temp = response["main"]["temp"]
    #     desc = response["weather"][0]["description"]
    #     min = response["main"]["temp_min"]
    #     max = response["main"]["temp_max"]
    #     sr = response["sys"]["sunrise"]
    #     ss = response["sys"]["sunset"]
    #     sr = datetime.fromtimestamp(sr).strftime("%#I:%M %p")
    #     ss = datetime.fromtimestamp(ss).strftime("%#I:%M %p")

    #     em = discord.Embed(title=f"**{city}**, {country}\n{int(temp)} °F",
    #                        description=f"Expect {desc}", color=discord.Color.blue())
    #     em.add_field(name=f"L: {int(min)} °F       H: {int(max)} °F",
    #                  value=f"Sunrise **{sr}**\nSunset **{ss}**", inline=True)
    #     await ctx.send(embed=em)

    # @weather.error
    # async def weather_error(self, ctx, error):
    #     if isinstance(error, commands.CommandInvokeError):
    #         await ctx.send("Error in finding the city, try to be more specific!")


def setup(client):
    client.add_cog(Essential(client))
