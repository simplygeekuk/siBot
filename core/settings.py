import os
import sys
import configparser

# Set some useful directories
si_core_dir = os.path.dirname(os.path.realpath(__file__))
base_dir = os.path.join(si_core_dir, '..')
base_image_url = r'http://www.simplygeek.co.uk/si/images/'
image_format = "png"
si_wiki_url = r'http://si.battlespot.com/wiki/'
# config_file = base_dir + "/config.cfg"


class Settings:
    '''siBot Settings'''
    def __init__(self, config_file='config.cfg'):
        self.image_url = base_image_url
        self.image_format = image_format
        self.si_wiki_url = si_wiki_url

        self.config = configparser.ConfigParser()
        self._get_config(config_file)

        self.default_config = self._get_config_section('DEFAULT')
        self.default = {}
        # self.default['extensions'] = self._get_section_attrib(self.default_config, 'extensions').split(',')  # noqa: line-too-long

        self.discord_config = self._get_config_section('DISCORD')
        self.discord = {}
        self.discord['bot_token'] = self._get_section_attrib(self.discord_config,  # noqa: line-too-long
                                                             'bot_token')
        self.discord['bot_description'] = self._get_section_attrib(self.discord_config,  # noqa: line-too-long
                                                                   'bot_description')  # noqa: line-too-long
        self.discord['bot_reconnect'] = self._get_section_attrib(self.discord_config,  # noqa: line-too-long
                                                                 'bot_reconnect', True)  # noqa: line-too-long
        self.discord['bot_prefix_ch'] = self._get_section_attrib(self.discord_config,  # noqa: line-too-long
                                                                 'bot_prefix_channel')  # noqa: line-too-long
        self.discord['bot_prefix_dm'] = self._get_section_attrib(self.discord_config,  # noqa: line-too-long
                                                                 'bot_prefix_message')  # noqa: line-too-long
        self.discord['bot_respond_on_mention'] = self._get_section_attrib(self.discord_config,  # noqa: line-too-long
                                                                          'bot_respond_on_mention')  # noqa: line-too-long
        self.discord['bot_valid_channels'] = self._get_section_attrib(self.discord_config,  # noqa: line-too-long
                                                                      'bot_valid_channels').split(',')  # noqa: line-too-long

        # self.dropbox_config = self._get_config_section('DROPBOX')
        # self.dropbox = {}

    def _get_config(self, config_file):
        '''Loads the configuration file.'''
        try:
            self.config.read_file(open(base_dir + "/" + config_file))
        except FileNotFoundError:
            print(f'Failed to open config file.'
                  f' {config_file} not found in {base_dir}')
            # raise
            sys.exit(1)

    def _get_config_section(self, section: str):
        '''Gets a configuration section from the config file.'''
        try:
            section_config = self.config[section]
        except (configparser.NoSectionError, KeyError):
            print("Could not find '[" + section + "]' section in config")
            raise
        return section_config

    def _get_section_attrib(self, section, attrib: str, isBool=False):
        '''Gets a specific attribute from a configuration section'''
        try:
            if isBool:
                attribValue = section.getboolean(attrib)
            else:
                attribValue = section[attrib]
        except configparser.NoOptionError:
            print(attrib + " not set in config file.")
            raise
        if not attribValue:  # Need to do more work here to properly handle booleans.  # noqa: line-too-long
            raise configparser.Error("No value was found for " + attrib)
        return attribValue


settings = Settings()
