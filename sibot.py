import discord
from discord.ext import commands

import json
import sys, traceback, os
import configparser

# Set some useful directories
base_dir = os.path.dirname(os.path.realpath(__file__))

config = configparser.ConfigParser()
# Read the config file
config_file = base_dir + "/config.cfg"
try:
    config.read_file(open(config_file))
except FileNotFoundError as e:
    print("Failed to open config file.")
    raise

# Get the discord section
try:
    discord_config = config['DISCORD']
except configparser.NoSectionError as e:
    print("Could not find 'DISCORD' section in config")
    raise

# Get the bot token
try:
    bot_token = discord_config['bot_token']
except configparser.NoOptionError as e:
    print("bot_token not set in config file.")
    raise
if not bot_token:
    raise configparser.Error("No value was found for bot_token")
    
bot_reconnect = discord_config.getboolean('bot_reconnect')

valid_channels = discord_config['valid_channels']
valid_channels = valid_channels.split(',')

def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    # Default prefixes
    prefixes = ['!']

    # Check to see if we are outside of a guild. e.g DM's etc.
    if not message.guild:
        # Only allow ? to be used in DMs
        return '?'

    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)

extensions = discord_config['extensions']
extensions = extensions.split(',')
initial_extensions = extensions

bot = commands.Bot(command_prefix=get_prefix, description=discord_config['bot_description'])
bot.remove_command('help')

# Here we load our extensions(cogs) listed above in [initial_extensions].
if __name__ == '__main__':
    print("Bot is starting...")
    print("Loading extensions...")
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
            print(f"\t'{extension}' loaded successfully.")
        except Exception as e:
            print(f'\tFailed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()

@bot.check
async def is_valid_channel(ctx):
    if not ctx.message.guild:
        return True
    else:
        return ctx.message.channel.name.lower() in valid_channels
            
@bot.event
async def on_ready():
    """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready"""

    print(f'\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}')
    print(f'bot autoreconnect: {bot_reconnect}')

    # Changes our bots Playing Status. type=1(streaming) for a standard game you could remove type and url.
    # await bot.change_presence(game=discord.Game(name='Cogs Example', type=1, url='https://twitch.tv/kraken'))
    print(f'Successfully logged in and booted...!')

bot.run(bot_token, bot=True, reconnect=bot_reconnect)
