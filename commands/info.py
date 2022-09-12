import discord
import os

from discord.ext import commands
from utils import config
from utils import codeblock
from utils import cmdhelper
from utils import shortener
from utils import embed as embedmaker

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cfg = config.Config()

    @commands.command(name="info", description="Information commands.", aliases=["information"], usage="")
    async def info(self, ctx, selected_page: int = 1):
        cfg = config.Config()
        pages = cmdhelper.generate_help_pages(self.bot, "Info")

        if cfg.get("theme")["style"] == "codeblock":
            msg = codeblock.Codeblock(
                f"{cfg.get('theme')['emoji']} info commands",
                description=pages["codeblock"][selected_page - 1],
                extra_title=f"Page {selected_page}/{len(pages['codeblock'])}"
            )

            await ctx.send(msg, delete_after=cfg.get("message_settings")["auto_delete_delay"])

        else:
            embed = embedmaker.Embed(title="Info Commands", description=pages["image"][selected_page - 1], colour=cfg.get("theme")["colour"])
            embed.set_footer(text=f"Page {selected_page}/{len(pages['image'])}")
            embed.set_thumbnail(url=cfg.get("theme")["image"])
            embed_file = embed.save()

            await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
            os.remove(embed_file)

    @commands.command(name="userinfo", description="Get information about a user.", aliases=["ui"], usage="[user]")
    async def userinfo(self, ctx, user: discord.User = None):
        cfg = config.Config()
        if user is None: user = ctx.author
        created_at = user.created_at.strftime("%d %B, %Y")

        if cfg.get("theme")["style"] == "codeblock":
            msg = codeblock.Codeblock(title=f"user info", extra_title=f"{user.name}#{user.discriminator}", description=f"""Username   :: {user.name}
ID         :: {user.id}
Created at :: {created_at}""")
            await ctx.send(msg + shortener.shorten(f"{user.avatar_url}"), delete_after=cfg.get("message_settings")["auto_delete_delay"])

        else:
            embed = embedmaker.Embed(title=f"{user} information", description=f"**Username:** {user.name}\n**ID:** {user.id}\n**Created at:** {created_at}", colour=cfg.get("theme")["colour"])
            embed.set_thumbnail(url=str(user.avatar_url))
            embed.set_footer(text=cfg.get("theme")["footer"])
            embed_file = embed.save()

            await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
            os.remove(embed_file)

    @commands.command(name="serverinfo", description="Get information about the server.", aliases=["si"], usage="")
    async def serverinfo(self, ctx):
        cfg = config.Config()

        if cfg.get("theme")["style"] == "codeblock":
            msg = codeblock.Codeblock(title=f"server info", extra_title=f"{ctx.guild.name}", description=f"""Name    :: {ctx.guild.name}
ID      :: {ctx.guild.id}
Owner   :: {ctx.guild.owner}
Members :: {ctx.guild.member_count}""")
            await ctx.send(msg + shortener.shorten(f"{ctx.guild.icon_url}"), delete_after=cfg.get("message_settings")["auto_delete_delay"])

        else:
            embed = embedmaker.Embed(title=f"{ctx.guild.name} information", description=f"**ID:** {ctx.guild.id}\n**Owner:** {ctx.guild.owner.name}\n**Members:** {ctx.guild.member_count}", colour=cfg.get("theme")["colour"])
            embed.set_thumbnail(url=str(ctx.guild.icon_url))
            embed.set_footer(text=cfg.get("theme")["footer"])
            embed_file = embed.save()

            await ctx.send(file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
            os.remove(embed_file)

    @commands.command(name="avatar", description="Get the avatar of a user.", aliases=["av"], usage="[user]")
    async def avatar(self, ctx, user: discord.User = None):
        cfg = config.Config()

        if user is None:
            user = ctx.author

        if cfg.get("theme")["style"] == "codeblock":
            await ctx.send(str(codeblock.Codeblock(title="avatar", extra_title=str(user))) + shortener.shorten(f"{user.avatar_url}"), delete_after=cfg.get("message_settings")["auto_delete_delay"])

        else:
            embed = embedmaker.Embed(title=f"{user.name}'s avatar", description="The link has been added above for a higher quality image.", colour=cfg.get("theme")["colour"])
            embed.set_thumbnail(url=str(user.avatar_url))
            embed.set_footer(text=cfg.get("theme")["footer"])
            embed_file = embed.save()

            await ctx.send(content=f"<{shortener.shorten(str(user.avatar_url))}>", file=discord.File(embed_file, filename="embed.png"), delete_after=cfg.get("message_settings")["auto_delete_delay"])
            os.remove(embed_file)

def setup(bot):
    bot.add_cog(Info(bot))