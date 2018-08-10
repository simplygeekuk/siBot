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
gameObjectType = "legions"
		
class Legions:
    def __init__(self, bot):
        self.bot = bot
        with open(sipedia_dir + gameObjectType + '.json') as json_file:
            legions_file = json.load(json_file)
            self.description = legions_file['description']
            self.info = legions_file['info']
            self.legions = legions_file[gameObjectType]
			
    @commands.command(name='legion', aliases=['Legion', 'legions', 'Legions', 'le'])
    async def get_legion(self, ctx, subcommand=None, *, item=None):
        '''- Get information about Legions.'''
        legion_names = []
        for legion in self.legions.keys():
            legion_data = self.legions.get(legion)
            legion_names.append(legion_data['name'])
            legion_names = sorted(legion_names)
        if subcommand is None:
            embed_description = self.description
            embed = discord.Embed(colour=discord.Colour(0x6e1df7), description=embed_description)
            embed.set_author(name=gameObjectType.title())
            await ctx.send(embed=embed)
            await ctx.send("You may use the `legion list` command to list Legions that are known to me or `legion info` to get information about Legions.")
        elif subcommand.lower() == 'list':
            await ctx.send("You can learn more about the following Legions: `" + "`, `".join(legion_names) + "`.\n\nYou may use the `legion info <name>` command to get information about a specific Legion.")
        elif subcommand.lower() == 'info':
            if item is None:
                await ctx.send("This command provides information about Praetors. The following items can be queried: `" + "`, `".join(self.info.keys()) + "`\n\n" +
                "You may use the `praetor info <item>` command to learn more about a specific item.")
            elif item.lower() in self.legions.keys():
                self.get_legion_data(item)
                self.create_legion_embed()
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

                
    def get_legion_data(self, legion_name):
        legion_data = self.legions[legion_name.lower()]
        self.name = legion_data['name']
        self.desc =  legion_data['description']
        self.img =  legion_data['img']
        self.loyalty = legion_data['loyalty']
        self.level = legion_data['level']
        self.hp = legion_data['hp']
        self.ranged = legion_data['ranged']
        self.melee = legion_data['melee']
        self.infernal = legion_data['infernal']
        self.move = legion_data['move']
        self.specials = legion_data['specials']
        self.upkeep = legion_data['upkeep']

        
    def create_legion_embed(self):
        specials = []
        self.embed = discord.Embed(colour=discord.Colour(0xd0021b), description=self.desc)
        self.embed.set_thumbnail(url=base_image_url + gameObjectType + "/" + self.img + "." + image_format)
        self.embed.set_author(name=self.name, url=si_wiki_url + self.name.replace(" ", "_"))
        self.embed.add_field(name="Level", value=self.level, inline=True)
        self.embed.add_field(name="Loyalty", value=self.loyalty, inline=True)
        self.embed.add_field(name="Hit Points", value=self.hp, inline=True)
        self.embed.add_field(name="Movement", value=self.move, inline=True)
        self.embed.add_field(name="Ranged/Melee/Infernal", value=self.ranged + " / " + self.melee + " / " + self.infernal, inline=True)
        for special, modifier in self.specials.items():
            if modifier is not None:
                specials.append("- " + special.title() + " " + modifier)
            else:
                specials.append(special.title())
        self.embed.add_field(name="Specials", value="\n".join(specials))
        if self.upkeep:
            self.embed.add_field(name="Upkeep", value="Souls: " + self.upkeep['souls'] + 
                                                ", Ichor: " + self.upkeep['ichor'] +
                                                ", Hellfire: " + self.upkeep['hellfire'] + 
                                                ", Darkness: " + self.upkeep['darkness'])


    def create_info_embed(self, item, embed_description):
        embed = discord.Embed(colour=discord.Colour(0x6e1df7), description=embed_description)
        embed.set_author(name=item.title())
        return embed
                                            
    def get_legions_with_special(self, special):
        selected_legions = []
        for legion in self.legions.keys():
            legion_data = self.legions.get(legion)
            if special in legion_data['specials']:
                selected_legions.append(legion_data['name'])
        return selected_legions

        
    def get_legions_specials(self):
        legion_specials = []
        for legion in self.legions.keys():
            legion_data = self.legions.get(legion)
            for special in legion_data['specials']:
                legion_specials.append(special.title())
        legion_specials = list(set(legion_specials))
        return legion_specials

    
# The setup function below is necessary. Remember we give bot.add_cog() the name of the class, in this case MembersCog.
# When we load the cog, we use the name of the class.
def setup(bot):
    bot.add_cog(Legions(bot))