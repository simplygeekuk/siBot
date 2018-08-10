import discord
from discord.ext import commands
import json, os
import configparser

# Set some useful directories
si_dir = os.path.dirname(os.path.realpath(__file__))
base_dir = os.path.join(si_dir, '..')
sipedia_dir = os.path.join(base_dir, 'sipedia/')
# print(sipedia_dir)

config = configparser.ConfigParser()
# Read the config file
config_file = base_dir + "/config.cfg"
try:
    config.read_file(open(config_file))
except FileNotFoundError as e:
    print("Failed to open config file.")
    raise

# Get the default section
try:
    discord_default_config = config['DEFAULT']
except configparser.NoSectionError as e:
    print("Could not find 'DEFAULT' section in config")
    
# Get the Solium section
try:
    discord_solium_config = config['SOLIUM']
except configparser.NoSectionError as e:
    print("Could not find 'SOLIUM' section in config")

# Get configs - need some defaults here.
base_image_url = discord_default_config['base_image_url']
image_format = discord_default_config['image_format']
si_wiki_url = discord_solium_config['si_wiki_url']
gameObjectType = "praetors"


class Praetors:
    def __init__(self, bot):
        self.bot = bot
        with open(sipedia_dir + gameObjectType + '.json') as json_file:
            praetors_file = json.load(json_file)
            self.description = praetors_file['description']
            self.info = praetors_file['info']
            self.praetors = praetors_file[gameObjectType]


    @commands.command(name='praetor', aliases=['Praetor', 'praetors', 'Praetors', 'pr'])
    async def get_praetor(self, ctx, subcommand=None, *, item=None):
        '''- Get information about Praetors.'''
        praetor_names = []
        for praetor in self.praetors.keys():
            praetor_data = self.praetors.get(praetor)
            praetor_names.append(praetor_data['name'])
            praetor_names = sorted(praetor_names)
        if subcommand is None:
            embed_description = self.description
            embed = discord.Embed(colour=discord.Colour(0x6e1df7), description=embed_description)
            embed.set_author(name="Praetors")
            await ctx.send(embed=embed)
            await ctx.send("You may use the `praetor list` command to list Praetors that are known to me or `praetor info` to get information about Praetors.")
        elif subcommand.lower() == 'list':
            await ctx.send("You can learn more about the following Praetors: `" + "`, `".join(praetor_names) + "`.\n\nYou may use the `praetor info <name>` command to get information about a specific Praetor.")
        elif subcommand.lower() == 'info':
            if item is None:
                await ctx.send("This command provides information about Praetors. The following items can be queried: `" + "`, `".join(self.info.keys()) + "`\n\n" +
                "You may use the `praetor info <item>` command to learn more about a specific item.")
            elif item.lower() in self.praetors.keys():
                self.get_praetor_data(item)
                self.create_praetor_embed()
                await ctx.send(embed=self.embed)
            elif item.lower() in self.info.keys():
                if item.lower() == 'special abilities':
                    praetor_specials = self.get_praetor_specials()
                    praetor_specials = sorted(praetor_specials)
                    embed = self.create_info_embed(item, self.info[item.lower()] + "\n\nPraetors have the following special abilities: `" + "`, `".join(praetor_specials) + "`")
                    await ctx.send(embed=embed)
                    await ctx.send("You may use the `praetor hasspecial <special>` command to list Praetors that have that special ability.")
                elif item.lower() == 'single combat':
                    embed = self.create_info_embed(item, self.info[item.lower()])
                    await ctx.send(embed=embed)
                    await ctx.send("You may use the `praetor info [basic|exotic] combat moves` command to learn more about combat moves.")
                elif item.lower() == "basic combat moves":
                    embed = self.create_info_embed(item, self.info[item.lower()]['description'])
                    await ctx.send(embed=embed)
                    await ctx.send("You may use the `praetor info <basic combat move>` command to get information about a specific combat move.")
                elif item.lower() == "exotic combat moves":
                    exotic_combat_moves = []
                    for exotic in self.info['exotic combat moves'].keys():
                        if exotic != 'description':
                            exotic_combat_moves.append(exotic.title())
                    embed = self.create_info_embed(item, self.info[item.lower()]['description'] + "\n\nThe following exotic combat moves are available: `" + "`, `".join(exotic_combat_moves) + "`")
                    await ctx.send(embed=embed)
                    await ctx.send("You may use the `praetor info <exotic combat move>` command to get information about a specific combat move.")                
                else:
                    embed = self.create_info_embed(item, self.info[item.lower()])
                    await ctx.send(embed=embed)
            elif item.lower() in self.info['basic combat moves'].keys():
                embed = self.create_info_embed(item, self.info['basic combat moves'][item.lower()])
                await ctx.send(embed=embed)
            elif item.lower() in self.info['exotic combat moves'].keys():
                embed = self.create_info_embed(item, self.info['exotic combat moves'][item.lower()])
                await ctx.send(embed=embed)
            elif item.lower() == ctx.message.author.name.lower():
                await ctx.send(f"{ctx.message.author.mention}, the legions of hell would not consider you worthy enough to lead them into battle.")
            else:
                await ctx.send(f"'{item}' is not a valid Praetor name or item.")
        elif subcommand.lower() == 'hasspecial':
            praetor_specials = self.get_praetor_specials()
            if item is None:
                await ctx.send("You must specify the special ability to search for Praetors.")
            elif item.title() in praetor_specials:
                praetors_with_special = self.get_praetors_with_special(item.lower())
                await ctx.send("The following Praetors were found with the special ability `" + item.title() + "`: `" + "`, `".join(praetors_with_special) + 
                "`\n\nYou may use the `praetor info <name>` command to get information about a specific praetor.")
            else:
                await ctx.send(f"No Praetors have the special ability: `{item}`")

                
    def get_praetor_data(self, praetor_name):
        praetor_data = self.praetors[praetor_name.lower()]
        self.name = praetor_data['name']
        self.desc =  praetor_data['description']
        self.img =  praetor_data['img']
        self.loyalty = praetor_data['loyalty']
        self.level = praetor_data['level']
        self.hp = praetor_data['hp']
        self.attack = praetor_data['attack']
        self.defense = praetor_data['defense']
        self.infernal = praetor_data['infernal']
        self.luck = praetor_data['luck']
        self.specials = praetor_data['specials']
        # self.cost = praetor_data['cost']
        # self.upkeep = praetor_data['upkeep']

        
    def create_praetor_embed(self):
        specials = []
        self.embed = discord.Embed(colour=discord.Colour(0xd0021b), description=self.desc)
        self.embed.set_thumbnail(url=base_image_url + gameObjectType + "/" + self.img + "." + image_format)
        self.embed.set_author(name=self.name, url=si_wiki_url + self.name.replace(" ", "_"))
        self.embed.add_field(name="Level", value=self.level, inline=True)
        self.embed.add_field(name="Loyalty", value=self.loyalty, inline=True)
        self.embed.add_field(name="Hit Points", value=self.hp, inline=True)
        self.embed.add_field(name="Luck", value=self.luck, inline=True)
        self.embed.add_field(name="Attack/Defense/Infernal", value=self.attack + " / " + self.defense + " / " + self.infernal, inline=True)
        for special, modifier in self.specials.items():
            if modifier is not None:
                specials.append("- " + special.title() + " " + modifier)
            else:
                specials.append(special.title())
        self.embed.add_field(name="Specials", value="\n".join(specials))
        # embed.add_field(name="Minimum Bid", value="Prestige: " + praetor_cost['prestige'] 
        #                                    + ", Souls: " + praetor_cost['souls'] + ", Ichor: " + praetor_cost['ichor'] 
        #                                    + ", Hellfire: " + praetor_cost['hellfire'] + ", Darkness: " + praetor_cost['darkness'])
        # self.embed.add_field(name="Upkeep", value="Prestige: " + self.upkeep['prestige'] 
                                            # + ", Souls: " + self.upkeep['souls'] + ", Ichor: " + self.upkeep['ichor'] 
                                            # + ", Hellfire: " + self.upkeep['hellfire'] + ", Darkness: " + self.upkeep['darkness'])


    def create_info_embed(self, item, embed_description):
        embed = discord.Embed(colour=discord.Colour(0x6e1df7), description=embed_description)
        embed.set_author(name=item.title())
        return embed
                                            
    def get_praetors_with_special(self, special):
        selected_praetors = []
        for praetor in self.praetors.keys():
            praetor_data = self.praetors.get(praetor)
            if special in praetor_data['specials']:
                selected_praetors.append(praetor_data['name'])
        return selected_praetors

        
    def get_praetor_specials(self):
        praetor_specials = []
        for praetor in self.praetors.keys():
            praetor_data = self.praetors.get(praetor)
            for special in praetor_data['specials']:
                praetor_specials.append(special.title())
        praetor_specials = list(set(praetor_specials))
        return praetor_specials

    
# The setup function below is necessary. Remember we give bot.add_cog() the name of the class, in this case MembersCog.
# When we load the cog, we use the name of the class.
def setup(bot):
    bot.add_cog(Praetors(bot))