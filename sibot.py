import discord
from discord.ext import commands
import time
import json
import os

base_dir = os.path.dirname(os.path.realpath(__file__))
sipedia_dir = os.path.join(base_dir, 'sipedia/')
# print(sipedia_dir)
base_image_url = "http://www.simplygeek.co.uk/si/images/"
image_format = "png"
si_wiki_url = "http://si.battlespot.com/wiki/"


bot = commands.Bot(command_prefix='!', description='The Solium Infernum Helper Bot.')
#Defines a bot's prefix and description. There is one predefined command in the bot, the help command. This command shows you the full list of commands you have created.

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    
#The @bot.event defines a bot event. The on_ready event occurs when the bot is ready / is logged in to the Client. In this example, the "I'm here!" message will be printed to the console.

@bot.command()
async def praetor(ctx, name=None):
    image_folder = "praetors"
    specials = []
    
    '''Get information about Praetors.'''
    with open(sipedia_dir + 'praetors.json') as json_file:
        praetors_file = json.load(json_file)
        praetors = praetors_file['praetors']


    praetor_names = []
    for praetor in praetors.keys():
        praetor_data = praetors.get(praetor)
        praetor_names.append(praetor_data['name'])

    if name is None or name == 'list':
        await ctx.send("The following Praetors are known to me: " + ", ".join(praetor_names) + ". Use !praetor <name> to get information about a specific Praetor.")
    elif name.title() in praetor_names:
        for praetor in praetors.keys():
            praetor_data = praetors.get(praetor)
            praetor_name = praetor_data['name']
            praetor_desc =  praetor_data['description']
            praetor_loyalty = praetor_data['loyalty']
            praetor_level = praetor_data['level']
            praetor_hp = praetor_data['hp']
            praetor_attack = praetor_data['attack']
            praetor_defense = praetor_data['defense']
            praetor_infernal = praetor_data['infernal']
            praetor_luck = praetor_data['luck']
            praetor_specials = praetor_data['specials']
            praetor_cost = praetor_data['cost']
            praetor_upkeep = praetor_data['upkeep']
                
        embed = discord.Embed(colour=discord.Colour(0xd0021b), description=praetor_desc)
        embed.set_thumbnail(url=base_image_url + image_folder + "/" + praetor_name + "." + image_format)
        embed.set_author(name=praetor_name, url=si_wiki_url + praetor_name)
        embed.add_field(name="Level", value=praetor_level, inline=True)
        embed.add_field(name="Loyalty", value=praetor_loyalty, inline=True)
        embed.add_field(name="Hit Points", value=praetor_hp, inline=True)
        embed.add_field(name="Luck", value=praetor_luck, inline=True)
        embed.add_field(name="Attack/Defense/Infernal", value=praetor_attack + " / " + praetor_defense + " / " + praetor_infernal, inline=True)
        for special, modifier in praetor_specials.items():
            if modifier is not None:
                specials.append("- " + special.title() + " " + modifier)
            else:
                specials.append(special.title())
        embed.add_field(name="Specials", value="\n".join(specials))
        embed.add_field(name="Minimum Bid", value="Prestige: " + praetor_cost['prestige'] 
                                            + ", Souls: " + praetor_cost['souls'] + ", Ichor: " + praetor_cost['ichor'] 
                                            + ", Hellfire: " + praetor_cost['hellfire'] + ", Darkness: " + praetor_cost['darkness'])
        embed.add_field(name="Upkeep", value="Prestige: " + praetor_upkeep['prestige'] 
                                            + ", Souls: " + praetor_upkeep['souls'] + ", Ichor: " + praetor_upkeep['ichor'] 
                                            + ", Hellfire: " + praetor_upkeep['hellfire'] + ", Darkness: " + praetor_upkeep['darkness'])
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"The Praetor '{name}', is not known to me.")

# @bot.command()
# async def sipedia(ctx, subcommand=None, item=None):
    # """Get information from the Solium Infernum encyclopedia."""
    # subcommands = ("artifact", "event", "legion", "manuscripts", "objective", "praetor", "relic", "ritual")
    # praetors = ("abraxas", "astarte", "aaraqiel", "Barbatos")
    # print(subcommand)
    # print(item)
    # if subcommand is not None and item is not None:
      # if subcommand in subcommands:
        # if subcommand.lower() == "praetor":
          # if item.lower() in praetors:
            # subcommand = subcommand.title()
            # item = item.title()
            # embed = discord.Embed(title="Abraxas", colour=discord.Colour(0xd0021b), description="Abraxas is a crowd favorite in the 'Infernal Arena of Pandemonium'.")

            # embed.set_thumbnail(url="https://i.pinimg.com/736x/c1/22/aa/c122aae470ebe02c0a51b47d8a9c73b6--memento-mori-chronic-pain.jpg")

            # embed.add_field(name="Stats", value="Level: 1\t\t\t\tLoyalty: 3\t\t\t Hit Points: 9\nAttack: 7\t\t\tDefense: 7\t\t\tInfernal: 3\t\t\t\tLuck: 3", inline=False)
            # embed.add_field(name="Specials", value="- **Melee +3**: Add +3 to melee attribute\n\n- **Level Roll +3**: Add +3 to legion's level for purposes of combat and resistance rolls and determining the number of attachment slots")
            # embed.add_field(name="Minimum Bid", value="Prestige: 0, Souls: 1, Ichor: 1, Hellfire: 0, Darkness: 0")
            # embed.add_field(name="Upkeep", value="Prestige: 0, Souls: 0, Ichor: 0, Hellfire: 0, Darkness: 0")

            # await ctx.send(embed=embed)
            # #await ctx.send(f"{item}: It seems as if Bune sours over our arrangements. I have reason to believe he positions himself for the responsibilities that you and I share." )
          # elif item.lower() == "list":
            # await ctx.send("The following Praetors are known to me: " + ", ".join(praetors))
          # else:
            # await ctx.send(f"The {subcommand}: {item}, is not known to me.")

# @bot.command()
# async def say(ctx, subcommand, item):
    # """Get information from the Solium Infurnum encyclopedia."""
    # subcommands = ("artifact", "event", "legion", "manuscripts", "objective", "praetor", "relic", "ritual")
    
    # if something is None:
        # await ctx.send("What do you want to say?")
        # return
        
    # await ctx.send(f"{ctx.message.author.mention} said: **{something}**")

# @bot.command()
# async def myid(ctx):
    # await ctx.send(ctx.message.author.id)

# @bot.command()
# async def getusers(ctx):
    # client = discord.Client()
    # guild = ctx.message.guild
    # print(guild.name)
    # print(guild.members)
    # await ctx.send(f"{guild.members}")

# @bot.command()
# async def ping(ctx):
    # """Pong!"""
    # await ctx.send("Pong!")

#@bot.event
#async def on_message(message):
  #print(message)
  #if len(ctx.message.embeds) > 0:
  #await ctx.send_message(ctx.message.channel, "check")
  #print(message.embeds[0].title)

bot.run("NDczMTYwMzg1MzAyODg4NDcw.DkEKEw.VP78VqjrMkkWE-RxSiUWtZBrsG4")
