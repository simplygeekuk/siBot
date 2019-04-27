from core.settings import Settings as settings
import discord
# from discord.ext import commands


class Legion:
    """Creates an instance of a Legion."""
    def __init__(self, name, description, img, loyalty, level, hp,
                 ranged, melee, infernal, move, specials, upkeep):
        self.name = name
        self.description = description
        self.img = img
        self.loyalty = loyalty
        self.level = level
        self.hp = hp
        self.ranged = ranged
        self.melee = melee
        self.infernal = infernal
        self.move = move
        self.specials = specials
        self.upkeep = upkeep
        self._object_type = "legions"
        self._settings = settings()

    async def create_embed_portrait(self):
        '''Creates a Discord embedded object for the Legion portrait.'''
        specials = []
        self._embed = discord.Embed(colour=discord.Colour(0xd0021b),
                                    description=self.description)
        self._embed.set_thumbnail(url=self._settings.image_url +
                                  self._object_type +
                                  "/" + self.img +
                                  "." + self._settings.image_format)
        self._embed.set_author(name=self.name,
                               url=self._settings.si_wiki_url +
                               self.name.replace(" ", "_"))
        self._embed.add_field(name="Level",
                              value=self.level,
                              inline=True)
        self._embed.add_field(name="Loyalty",
                              value=self.loyalty,
                              inline=True)
        self._embed.add_field(name="Hit Points",
                              value=self.hp,
                              inline=True)
        self._embed.add_field(name="Move Points",
                              value=self.move,
                              inline=True)
        self._embed.add_field(name="Ranged/Melee/Infernal",
                              value=self.ranged + " / " +
                              self.melee + " / " +
                              self.infernal,
                              inline=True)

        if self.specials.items():
            for special, modifier in self.specials.items():
                if modifier is not None:
                    specials.append("- " + special.title() + " " + modifier)
                else:
                    specials.append(special.title())
        else:
            specials.append("None")
        self._embed.add_field(name="Specials Abilities",
                              value="\n".join(specials))

        if self.upkeep:
            resources = self.upkeep.split(',')
            souls = resources[0]
            ichor = resources[1]
            hellfire = resources[2]
            darkness = resources[3]
            self.embed.add_field(name="Upkeep",
                                 value="Souls: " + souls +
                                 ", Ichor: " + ichor +
                                 ", Hellfire: " + hellfire +
                                 ", Darkness: " + darkness)
        return self._embed
