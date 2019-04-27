import discord
from discord.ext import commands
import os
from core.utils.dataIO import dataIO
import core.utils.chat_formatting as cf
# from sibot import bot_settings as settings
# from si_core.settings import Settings as settings
from core.gameObj.legion import Legion
current_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.join(current_dir, '../..')
data_dir = os.path.join(root_dir, 'data/')
gameObjectType = "legions"


class Legion_commands(commands.Cog):
    '''Legion commands namespace'''
    def __init__(self, bot):
        self.bot = bot

        filename = data_dir + gameObjectType + '.json'
        isValidData = dataIO.is_valid_json(filename)
        if isValidData:
            legion_data = dataIO.load_json(filename)
        else:
            raise Exception("Failed to read file {}".format(filename))

        self._description = legion_data['description']
        self._info = legion_data['info']
        self._legions = legion_data[gameObjectType]
        self._legion_names = [self._legions.get(name)['name']
                              for name in self._legions.keys()]
        self._legion_specials = self._get_legion_specials()

    @commands.group(name='legion',
                    aliases=['Legion',
                             'Legions',
                             'legions',
                             'le'],
                    case_insensitive=True)
    async def legion(self, ctx):
        '''Get information about Legions.'''
        if ctx.invoked_subcommand is None:
            embed_description = self._description
            embed = discord.Embed(colour=discord.Colour(0x6e1df7),
                                  description=embed_description)
            embed.set_author(name=gameObjectType.title())
            await ctx.send(embed=embed)
            await ctx.send(f'You can use the {cf.inline("legion list")}'
                           f' command to list Legions that are known to me,'
                           f' or {cf.inline("legion info")}'
                           f' to get information about Legions.')

    @legion.command(name="list", case_insensitive=True)
    async def legion_list(self, ctx):
        '''List available Legions'''
        await ctx.send(f'You can learn more about the following Legions:'
                       f' {cf.inline(", ".join(self._legion_names))}.'
                       f'\n\nYou can use the'
                       f' {cf.inline("legion info <name>")} command'
                       f' to get information about a specific Legion.')

    @legion.command(name="info", case_insensitive=True)
    async def legion_info(self, ctx, *, subcommand=None):
        '''Get information about a specific Legion.'''
        if subcommand is None:
            await ctx.send(f'This command provides information about Legions.'
                           f'\n\nYou can use the'
                           f' {cf.inline("legion info <name>")}'
                           f' command to learn more about a specific Legion.')
        else:
            item = subcommand.lower()
            if item in self._legions.keys():
                legion = Legion(**self._legions[item])
                embed = await legion.create_embed_portrait()
                await ctx.send(embed=embed)
            elif item == ctx.message.author.name.lower():
                await ctx.send(f'{ctx.message.author.mention},'
                               f' the legions of hell would not consider'
                               f' you worthy enough to lead them into battle.')
            else:
                await ctx.send(f'\'{subcommand}\''
                               f' is not a valid Legion name.')

    @legion.command(name="special_abilities", case_insensitive=True)
    async def legion_special_abilities(self, ctx):
        '''Get information on Legion special abilities.'''
        item = " ".join(ctx.subcommand_passed.lower().split('_'))
        embed = self._create_info_embed(item,
                                        f'{self._info[item]}'
                                        f'\n\nLegions have the following special abilities:'  # noqa: line-too-long
                                        f' {cf.inline(", ".join(self._legion_specials))}')  # noqa: line-too-long
        await ctx.send(embed=embed)
        await ctx.send(f'Use the'
                       f'{cf.inline("special_abilities <special ability>")}'
                       f' command to get info for a specific'
                       f' special ability.'
                       f'\n\nUse the'
                       f' {cf.inline("legion hasspecial <special ability>")}'
                       f' command to list Legions that have that'
                       f' special ability.')

    @legion.command(name="level", case_insensitive=True)
    async def legion_level(self, ctx, *, subcommand=None):
        '''Get information on level and leveling up a Legion.'''
        item = ctx.subcommand_passed.lower()
        if subcommand is None:
            embed = self._create_info_embed(item,
                                            self._info[item]['description'])
            await ctx.send(embed=embed)
        elif subcommand.lower() == "up":
            embed = self._create_info_embed(item + " up",
                                            self._info[item]['up'])
            await ctx.send(embed=embed)

    @legion.command(name="training", case_insensitive=True)
    async def legion_training(self, ctx):
        '''Get information on training a Legion.'''
        item = ctx.subcommand_passed.lower()
        embed = self._create_info_embed(item,
                                        self._info[item])
        await ctx.send(embed=embed)

    @legion.command(name="limitations", case_insensitive=True)
    async def legion_limitations(self, ctx):
        '''Get information on Legion limitations.'''
        item = ctx.subcommand_passed.lower()
        embed = self._create_info_embed(item,
                                        self._info[item])
        await ctx.send(embed=embed)

    @legion.command(name="luck", case_insensitive=True)
    async def legion_luck(self, ctx):
        '''Get information on Legion luck.'''
        item = ctx.subcommand_passed.lower()
        embed = self._create_info_embed(item,
                                        self._info[item])
        await ctx.send(embed=embed)

    @legion.command(name="hasspecial", case_insensitive=True)
    async def legion_hasspecial(self, ctx, *, subcommand=None):
        '''Lists Legions that have the specified special ability.'''
        if subcommand is None:
            await ctx.send(f'You must specify the special ability'
                           f' to search for Legions.'
                           f'\n\nThe following special abilities'
                           f' are available: '
                           f'{cf.inline(", ".join(self._legion_specials))}')
        else:
            item = subcommand.lower()
            if item.title() in self._legion_specials:
                legions_with_special = self._get_legion_with_special(item)

                await ctx.send(f'The following Legions were found'
                               f' with the special ability'
                               f' {cf.bold(item.title())}: {cf.inline(", ".join(legions_with_special))}'  # noqa: line-too-long
                               f'\n\nYou may use the {cf.inline("legion info <name>")}'  # noqa: line-too-long
                               f' command to get information about a specific legion.')  # noqa: line-too-long
            else:
                await ctx.send(f'No Legions have the'
                               f' special ability: {cf.inline(subcommand)}')

    def _create_info_embed(self, item, embed_description):
        '''Creates a Discord embedded object for displaying information.'''
        embed = discord.Embed(colour=discord.Colour(0x6e1df7),
                              description=embed_description)
        embed.set_author(name=item.title())
        return embed

    def _get_legion_with_special(self, special):
        '''Gets a list of Legions that have the specified special ability.'''
        legion_list_with_special = []
        for legion in self._legions.keys():
            legion_data = self._legions.get(legion)
            if special in legion_data['specials']:
                legion_list_with_special.append(legion_data['name'])
        return legion_list_with_special

    def _get_legion_specials(self):
        '''Gets a list of Legion special abilities.'''
        legion_specials = []
        for legion in self._legions.keys():
            legion_data = self._legions.get(legion)
            for special in legion_data['specials']:
                legion_specials.append(special.title())
        legion_specials = list(set(legion_specials))
        return sorted(legion_specials)


def setup(bot):
    '''Adds the namespace to the cogs.'''
    bot.add_cog(Legion_commands(bot))
