from .utils.dataIO import dataIO

class Praetor:
    """Praetor instance class"""
    def __init__(self, **praetor_data):
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
        
    def create_embed(self):
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