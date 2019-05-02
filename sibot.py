import discord
from discord.ext import commands
import os
import sys
import traceback
from core.settings import Settings
from os import listdir
from os.path import isfile, join


# Set some useful directories.
cogs_dir = 'core/commands/'
current_path = os.path.dirname(os.path.realpath(__file__))
cogs_path = os.path.join(current_path, cogs_dir)

# Get all the settings.
bot_settings = Settings()
bot_default_settings = bot_settings.default
bot_discord_settings = bot_settings.discord
# initial_extensions = bot_default_settings['extensions']
valid_channels = bot_discord_settings['bot_valid_channels']
bot_description = bot_discord_settings['bot_description']
bot_token = bot_discord_settings['bot_token']
bot_reconnect = bot_discord_settings['bot_reconnect']
disabled_extensions = ['']


async def get_prefix(bot, message):
    """A callable Prefix for our bot."
    " This could be edited to allow per server prefixes."""

    # Default prefixes
    prefixes = ['!']

    # Check to see if we are outside of a guild. e.g DM's etc.
    if not message.guild:
        # Only allow ? to be used in DMs
        return '!'

    # If we are in a guild, we allow for the user to mention us
    # or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)


def load_extensions(bot):
    '''Load our extensions(cogs) from the commands directory'''
    print("\nLoading extensions...")
    extensions = [ext.split('.')[0] for ext in listdir(cogs_path)
                  if isfile(join(cogs_path, ext))
                  and ext != '__init__.py'
                  and ext.split('.')[0] not in disabled_extensions]
    cogs_dotted_path = cogs_dir.replace('/', '.')
    if extensions:
        for extension in extensions:
            try:
                bot.load_extension(cogs_dotted_path + extension)
                print(f"\t'{extension}' loaded successfully.")
            except Exception:
                print(f'\tFailed to load extension {extension}.',
                      file=sys.stderr)
                traceback.print_exc()  # print traceback without halting.
    else:
        print(f'\tNo extensions found.')


def setup_bot(description):
    bot = commands.Bot(command_prefix=get_prefix, description=description)
    # bot.remove_command('help')
    return bot


bot = setup_bot(bot_description)

if __name__ == '__main__':
    print("Bot is starting...")
    load_extensions(bot)


@bot.check
async def is_valid_channel(ctx):
    if not ctx.message.guild:
        return True
    else:
        return ctx.message.channel.name.lower() in valid_channels


@bot.event
async def on_ready():
    """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready"""

    print(f'\nLogged in as: {bot.user.name} - {bot.user.id}'
          f'\nDiscord Version: {discord.__version__}')
    print(f'Bot Autoreconnect: {bot_reconnect}')
    print(f'Successfully logged in and started.')


bot.run(bot_token, bot=True, reconnect=bot_reconnect)
