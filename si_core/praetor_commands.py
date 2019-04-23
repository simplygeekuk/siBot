import discord
from discord.ext import commands
import os
from utils.dataIO import dataIO
import utils.chat_formatting as cf
# from sibot import bot_settings as settings
# from si_core.settings import Settings as settings
from si_core.praetor import Praetor
current_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.join(current_dir, '..')
data_dir = os.path.join(root_dir, 'si_data/')
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
            await ctx.send("You may use the " + cf.inline("praetor list") +
                           " command to list Praetors that are known to me,"
                           " or " + cf.inline("praetor info") +
                           " to get information about Praetors.")

    @praetor.command(name="list", case_insensitive=True)
    async def praetor_list(self, ctx):
        '''List available Praetors'''
        await ctx.send(f'You can learn more about the following Praetors:'
                       f' {cf.inline(", ".join(self._praetor_names))}.'
                       f'\n\nYou may use the `praetor info <name>` command'
                       f' to get information about a specific Praetor.')

    @praetor.command(name="info", case_insensitive=True)
    async def praetor_info(self, ctx, *, subcommand=None):
        '''Get general information about Praetors or a specific Praetor'''
        if subcommand is None:
            await ctx.send(f'This command provides information about Praetors.'
                           f' The following items can be queried:'
                           f' {cf.inline(", ".join(self._info.keys()))}.'
                           f'\n\nYou may use the'
                           f' {cf.inline("praetor info <item>")}'
                           f' command to learn more about a specific item.')
        else:
            item = subcommand.lower()
            if item in self._praetors.keys():
                praetor = Praetor(**self._praetors[subcommand.lower()])
                embed = await praetor.create_embed_portrait()
                await ctx.send(embed=embed)
            elif item in self._info.keys():
                if item == 'special abilities':
                    embed = self._create_info_embed(subcommand,
                                                    f'{self._info[item]}'
                                                    f'\n\nPraetors have the following special abilities:'  # noqa: line-too-long
                                                    f' {cf.inline(", ".join(self._praetor_specials))}')  # noqa: line-too-long
                    await ctx.send(embed=embed)
                    await ctx.send(f'You may use the'
                                   f' {cf.inline("praetor hasspecial <special ability>")}'  # noqa: line-too-long
                                   f' command to list Praetors that have that'
                                   f' special ability.')
                elif item == 'single combat':
                    embed = self._create_info_embed(subcommand,
                                                    self._info[item])
                    await ctx.send(embed=embed)
                    await ctx.send(f'You may use the'
                                   f' {cf.inline("praetor info [basic|exotic] combat moves")}'  # noqa: line-too-long
                                   f' command to learn more about combat moves.')  # noqa: line-too-long
                elif item == "basic combat moves":
                    embed = self._create_info_embed(subcommand,
                                                    self._info[item]['description'])  # noqa: line-too-long
                    await ctx.send(embed=embed)
                    await ctx.send(f'You may use the'
                                   f' {cf.inline("praetor info <basic combat move>")}'  # noqa: line-too-long
                                   f' command to get information about a specific combat move.')  # noqa: line-too-long
                elif item == "exotic combat moves":
                    exotic_combat_moves = []
                    for exotic in self._info['exotic combat moves'].keys():
                        if exotic != 'description':
                            exotic_combat_moves.append(exotic.title())
                    item_desc = self._info[item]["description"]
                    embed = self._create_info_embed(subcommand,
                                                    f'{item_desc}'
                                                    f'\n\nThe following exotic combat moves are available:'  # noqa
                                                    f'{cf.inline(", ".join(exotic_combat_moves))}')  # noqa
                    await ctx.send(embed=embed)
                    await ctx.send(f'You may use the'
                                   f' {cf.inline("praetor info <exotic combat move>")}'  # noqa
                                   f' command to get information about a specific combat move.')  # noqa
                else:
                    embed = self._create_info_embed(subcommand,
                                                    self._info[item])
                    await ctx.send(embed=embed)
            elif item in self._info['basic combat moves'].keys():
                item_desc = self._info['basic combat moves'][item]
                embed = self._create_info_embed(subcommand,
                                                item_desc)
                await ctx.send(embed=embed)
            elif item in self._info['exotic combat moves'].keys():
                item_desc = self._info['exotic combat moves'][item]
                embed = self._create_info_embed(subcommand,
                                                item_desc)
                await ctx.send(embed=embed)
            elif item == ctx.message.author.name.lower():
                await ctx.send(f'{ctx.message.author.mention},'
                               f' the legions of hell would not consider'
                               f' you worthy enough to lead them into battle.')
            else:
                await ctx.send(f'\'{subcommand}\''
                               f'is not a valid Praetor name or item.')

    @praetor.command(name="hasspecial", case_insensitive=True)
    async def praetor_hasspecial(self, ctx, *, subcommand=None):
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
                               f' {cf.bold(item.title())}: {cf.inline(", ".join(praetors_with_special))}'  # noqa
                               f'\n\nYou may use the {cf.inline("praetor info <name>")}'  # noqa
                               f' command to get information about a specific praetor.')  # noqa
            else:
                await ctx.send(f'No Praetors have the'
                               f' special ability: {cf.inline(subcommand)}')

    def _create_info_embed(self, item, embed_description):
        embed = discord.Embed(colour=discord.Colour(0x6e1df7),
                              description=embed_description)
        embed.set_author(name=item.title())
        return embed

    def _get_praetors_with_special(self, special):
        selected_praetors = []
        for praetor in self._praetors.keys():
            praetor_data = self._praetors.get(praetor)
            if special in praetor_data['specials']:
                selected_praetors.append(praetor_data['name'])
        return selected_praetors

    def _get_praetor_specials(self):
        praetor_specials = []
        for praetor in self._praetors.keys():
            praetor_data = self._praetors.get(praetor)
            for special in praetor_data['specials']:
                praetor_specials.append(special.title())
        praetor_specials = list(set(praetor_specials))
        return sorted(praetor_specials)


def setup(bot):
    bot.add_cog(Praetor_commands(bot))
