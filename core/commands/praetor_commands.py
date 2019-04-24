import discord
from discord.ext import commands
import os
from core.utils.dataIO import dataIO
import core.utils.chat_formatting as cf
# from sibot import bot_settings as settings
# from si_core.settings import Settings as settings
from core.gameObj.praetor import Praetor
current_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.join(current_dir, '../..')
data_dir = os.path.join(root_dir, 'data/')
gameObjectType = "praetors"


class Praetor_commands(commands.Cog):
    '''Praetor commands namespace'''
    def __init__(self, bot):
        self.bot = bot

        filename = data_dir + gameObjectType + '.json'
        isValidData = dataIO.is_valid_json(filename)
        if isValidData:
            praetor_data = dataIO.load_json(filename)
        else:
            raise Exception("Failed to read file {}".format(filename))

        self._description = praetor_data['description']
        self._info = praetor_data['info']
        self._praetors = praetor_data[gameObjectType]
        self._praetor_names = [self._praetors.get(name)['name']
                               for name in self._praetors.keys()]
        self._praetor_specials = self._get_praetor_specials()

    @commands.group(name='praetor',
                    aliases=['Praetor',
                             'praetors',
                             'Praetors',
                             'pr'],
                    case_insensitive=True)
    async def praetor(self, ctx):
        '''Get information about Praetors.'''
        if ctx.invoked_subcommand is None:
            embed_description = self._description
            embed = discord.Embed(colour=discord.Colour(0x6e1df7),
                                  description=embed_description)
            embed.set_author(name=gameObjectType.title())
            await ctx.send(embed=embed)
            await ctx.send(f'You can use the {cf.inline("praetor list")}'
                           f' command to list Praetors that are known to me,'
                           f' or {cf.inline("praetor info")}'
                           f' to get information about Praetors.')

    @praetor.command(name="list", case_insensitive=True)
    async def praetor_list(self, ctx):
        '''List available Praetors'''
        await ctx.send(f'You can learn more about the following Praetors:'
                       f' {cf.inline(", ".join(self._praetor_names))}.'
                       f'\n\nYou can use the `praetor info <name>` command'
                       f' to get information about a specific Praetor.')

    @praetor.command(name="info", case_insensitive=True)
    async def praetor_info(self, ctx, *, subcommand=None):
        '''Get information about a specific Praetor.'''
        if subcommand is None:
            await ctx.send(f'This command provides information about Praetors.'
                           f'\n\nYou can use the'
                           f' {cf.inline("praetor info <name>")}'
                           f' command to learn more about a specific Praetor.')
        else:
            item = subcommand.lower()
            if item in self._praetors.keys():
                praetor = Praetor(**self._praetors[item])
                embed = await praetor.create_embed_portrait()
                await ctx.send(embed=embed)
            elif item == ctx.message.author.name.lower():
                await ctx.send(f'{ctx.message.author.mention},'
                               f' the legions of hell would not consider'
                               f' you worthy enough to lead them into battle.')
            else:
                await ctx.send(f'\'{subcommand}\''
                               f' is not a valid Praetor name.')

    @praetor.command(name="special_abilities", case_insensitive=True)
    async def praetor_special_abilities(self, ctx):
        '''Get information on Praetor special abilities.'''
        item = " ".join(ctx.subcommand_passed.lower().split('_'))
        embed = self._create_info_embed(item,
                                        f'{self._info[item]}'
                                        f'\n\nPraetors have the following special abilities:'  # noqa: line-too-long
                                        f' {cf.inline(", ".join(self._praetor_specials))}')  # noqa: line-too-long
        await ctx.send(embed=embed)
        await ctx.send(f'Use the'
                       f'{cf.inline("special <special ability>")}'
                       f' command to get info for a specific'
                       f' special ability.'
                       f'\n\nUse the'
                       f' {cf.inline("praetor hasspecial <special ability>")}'
                       f' command to list Praetors that have that'
                       f' special ability.')

    @praetor.command(name="single_combat", case_insensitive=True)
    async def praetor_single_combat(self, ctx, *, subcommand=None):
        '''Get information on Praetor single combat.'''
        item = " ".join(ctx.subcommand_passed.lower().split('_'))
        if subcommand is None:
            embed = self._create_info_embed(item,
                                            self._info[item])
            await ctx.send(embed=embed)
            await ctx.send(f'You can use the'
                           f' {cf.inline("praetor [basic|exotic]_combat")}'
                           f' command to learn more about combat moves.')

    @praetor.command(name="basic_combat", case_insensitive=True)
    async def praetor_basic_combat(self, ctx, *, subcommand=None):
        '''Get information on Praetor basic combat moves.'''
        item = " ".join(ctx.subcommand_passed.lower().split('_')) + " moves"
        if subcommand is None:
            embed = self._create_info_embed(item,
                                            self._info[item]['description'])
            await ctx.send(embed=embed)
            await ctx.send(f'You can use the'
                           f' {cf.inline("praetor basic_combat <basic combat move>")}'  # noqa: line-too-long
                           f' command to get information about a specific combat move.')  # noqa: line-too-long
        else:
            combat_move = subcommand.lower()
            if combat_move in self._info[item].keys():
                item_desc = self._info[item][combat_move]
                embed = self._create_info_embed(combat_move,
                                                item_desc)
                await ctx.send(embed=embed)
            else:
                await ctx.send(f'\'{subcommand}\''
                               f' is not a valid Praetor basic combat move.')

    @praetor.command(name="exotic_combat", case_insensitive=True)
    async def praetor_exotic_combat(self, ctx, *, subcommand=None):
        '''Get information on Praetor exotic combat moves.'''
        item = " ".join(ctx.subcommand_passed.lower().split('_')) + " moves"
        if subcommand is None:
            exotic_combat_moves = []
            for exotic in self._info[item].keys():
                if exotic != 'description':
                    exotic_combat_moves.append(exotic.title())
            item_desc = self._info[item]["description"]
            embed = self._create_info_embed(item,
                                            f'{item_desc}'
                                            f'\n\nThe following exotic combat moves are available:'  # noqa: line-too-long
                                            f' {cf.inline(", ".join(exotic_combat_moves))}')  # noqa: line-too-long
            await ctx.send(embed=embed)
            await ctx.send(f'You may use the'
                            f' {cf.inline("praetor exotic_combat <exotic combat move>")}'  # noqa: line-too-long
                            f' command to get information about a specific combat move.')  # noqa: line-too-long
        else:
            combat_move = subcommand.lower()
            if combat_move in self._info[item].keys():
                item_desc = self._info[item][combat_move]
                embed = self._create_info_embed(combat_move,
                                                item_desc)
                await ctx.send(embed=embed)
            else:
                await ctx.send(f'\'{subcommand}\''
                               f' is not a valid Praetor exotic combat move.')

    @praetor.command(name="levelup", case_insensitive=True)
    async def praetor_levelup(self, ctx):
        '''Get information on leveling up a Praetor.'''
        item = ctx.subcommand_passed.lower()
        embed = self._create_info_embed(item,
                                        self._info[item])
        await ctx.send(embed=embed)

    @praetor.command(name="training", case_insensitive=True)
    async def praetor_training(self, ctx):
        '''Get information on training a Praetor.'''
        item = ctx.subcommand_passed.lower()
        embed = self._create_info_embed(item,
                                        self._info[item])
        await ctx.send(embed=embed)

    @praetor.command(name="limitations", case_insensitive=True)
    async def praetor_limitations(self, ctx):
        '''Get information on Praetor limitations.'''
        item = ctx.subcommand_passed.lower()
        embed = self._create_info_embed(item,
                                        self._info[item])
        await ctx.send(embed=embed)

    @praetor.command(name="luck", case_insensitive=True)
    async def praetor_luck(self, ctx):
        '''Get information on Praetor luck.'''
        item = ctx.subcommand_passed.lower()
        embed = self._create_info_embed(item,
                                        self._info[item])
        await ctx.send(embed=embed)

    @praetor.command(name="hasspecial", case_insensitive=True)
    async def praetor_hasspecial(self, ctx, *, subcommand=None):
        '''Lists Praetors that have the specified special ability.'''
        if subcommand is None:
            await ctx.send(f'You must specify the special ability'
                           f' to search for Praetors.'
                           f'\n\nThe following special abilities'
                           f' are available: '
                           f'{cf.inline(", ".join(self._praetor_specials))}')
        else:
            item = subcommand.lower()
            if item.title() in self._praetor_specials:
                praetors_with_special = self._get_praetors_with_special(item)

                await ctx.send(f'The following Praetors were found'
                               f' with the special ability'
                               f' {cf.bold(item.title())}: {cf.inline(", ".join(praetors_with_special))}'  # noqa: line-too-long
                               f'\n\nYou may use the {cf.inline("praetor info <name>")}'  # noqa: line-too-long
                               f' command to get information about a specific praetor.')  # noqa: line-too-long
            else:
                await ctx.send(f'No Praetors have the'
                               f' special ability: {cf.inline(subcommand)}')

    def _create_info_embed(self, item, embed_description):
        '''Creates a Discord embedded object for displaying information.'''
        embed = discord.Embed(colour=discord.Colour(0x6e1df7),
                              description=embed_description)
        embed.set_author(name=item.title())
        return embed

    def _get_praetors_with_special(self, special):
        '''Gets a list pf Praetors that have the specified special ability.'''
        praetor_list_with_special = []
        for praetor in self._praetors.keys():
            praetor_data = self._praetors.get(praetor)
            if special in praetor_data['specials']:
                praetor_list_with_special.append(praetor_data['name'])
        return praetor_list_with_special

    def _get_praetor_specials(self):
        '''Gets a list of Praetor special abilities.'''
        praetor_specials = []
        for praetor in self._praetors.keys():
            praetor_data = self._praetors.get(praetor)
            for special in praetor_data['specials']:
                praetor_specials.append(special.title())
        praetor_specials = list(set(praetor_specials))
        return sorted(praetor_specials)


def setup(bot):
    '''Adds the namespace to the cogs.'''
    bot.add_cog(Praetor_commands(bot))
