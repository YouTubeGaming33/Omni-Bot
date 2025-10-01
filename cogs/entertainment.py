from random import choice
import discord
from discord import app_commands
from discord.ext import commands
import asyncpraw as praw

from core.config import REDDIT_C_ID, REDDIT_C_SECRET, GUILD_ID

class Entertainment(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.reddit = praw.Reddit(
            client_id=REDDIT_C_ID,
            client_secret = REDDIT_C_SECRET,
            user_agent = "script: Random Meme:v1.0 (by u/Different_Profit_274)"
        )

    entertainment = app_commands.Group(name="entertainment", description="A group of entertainment commands.")

    @entertainment.command(name="meme", description="Pulls a random meme from r/memes")
    async def meme(self, interaction: discord.Interaction):
        subreddit = await self.reddit.subreddit("memes")
        posts_list = []

        async for post in subreddit.hot(limit=50):
            if not post.over_18 and post.author is not None and any (post.url.endswith(ext) for ext in[".png", ".jpg", ".jpeg", ".gif", ".webm"]):
                author_name = post.author.name
                posts_list.append((post.url, author_name))

            if post.author is None:
                posts_list.append((post.url, "N/A"))

        if posts_list:
            post_chosen = choice(posts_list)
            postEmbed = discord.Embed(
                title="Random Meme",
                description="Fectches random meme from r/memes",
                color = discord.Color.dark_gold())
            postEmbed.set_author(name=f"Meme requested by {interaction.user.name}", icon_url=interaction.user.avatar)
            postEmbed.set_image(url=post_chosen[0])
            postEmbed.set_footer(text=f"Meme posted by: {post_chosen[1]} in r/memes")
            await interaction.response.send_message(embed=postEmbed)
        else:
            await interaction.response.send_message("An error has occured, this is probably due to Reddit API being down.")
    
async def setup(bot):
    await bot.add_cog(Entertainment(bot))
