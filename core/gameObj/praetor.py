from core.settings import Settings as settings
import discord
# from discord.ext import commands


class Praetor:
    """Creates an instance of a Praetor."""
    def __init__(self, name, description, img, loyalty, level, hp,
                 attack, defense, infernal, luck, specials):
        self.name = name
        self.description = description
        self.img = img
        self.loyalty = loyalty
        self.level = level
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.infernal = infernal
        self.luck = luck
        self.specials = specials
        self._object_type = "praetors"
        self._settings = settings()

    async def create_embed_portrait(self):
        '''Creates an embedded Praetor portrait.'''
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
        self._embed.add_field(name="Luck",
                              value=self.luck,
                              inline=True)
        self._embed.add_field(name="Attack/Defense/Infernal",
                              value=self.attack + " / " +
                              self.defense + " / " +
                              self.infernal,
                              inline=True)
        for special, modifier in self.specials.items():
            if modifier is not None:
                specials.append("- " + special.title() + " " + modifier)
            else:
                specials.append(special.title())
        self._embed.add_field(name="Specials",
                              value="\n".join(specials))
        return self._embed
