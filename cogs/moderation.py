import discord
from discord.ext import commands
from discord import app_commands

from typing import Optional

from data.data import add_warning, get_case_number

class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    moderation = app_commands.Group(name="mod", description="A collection of all moderation commands.") # <- Creates a Group of App Commands

    @moderation.command(name="warn", description="Warn a Member")
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        # need to add in customisation for who can use commands
        await member.send(f"You have been Warned in **{interaction.guild}** for **{reason}**")
        await interaction.response.send_message(f"**{member.display_name}** has been Warned for: **{reason}**")
        caseNum = get_case_number()
        add_warning(interaction.guild_id, member.id, reason, caseNum)
        self.bot.dispatch("moderation", interaction=interaction, target=member, action="Warned", reason=reason, guild=interaction.guild, caseNum=caseNum)

    @moderation.command(name="kick", description="Kicks a member from the server.")
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        """
        Parameters:
            -   member: discord.Member - The member that is going to be kicked.
            -   reason: str - The reason behind the kick.
        """
        moderator = interaction.user # Will be used later to be passed into the listener to do logging once logging is functional.
        if not moderator.guild_permissions.moderate_members:
            await interaction.response.send_message(f"You may not use this command as you do not have the required permissions.", ephemeral=True)
            return

        await member.send(f"You have been kicked from **{interaction.guild}** for **{reason}**")
        await member.kick(reason = reason or None)
        await interaction.response.send_message(f"You have kicked **{member.mention} [ID = {member.id}, display name = {member.display_name}]** for **{reason}**", ephemeral=True)
        # Add the logging functionality when it is available.
        # possibly create a case code and then call the listener
        self.bot.dispatch("moderation", interaction=interaction, target=member, action="Kicked", reason=reason, guild=interaction.guild)

    @moderation.command(name="ban", description="Bans a user from the server")
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        """
        Parameters:
            -   member: discord.Member - The member that is going to be banned.
            -   reason: str - The reason behind the ban.
        """
        moderator = interaction.user # Will be used later to be passed into the listener to do logging once logging is functional.
        if not moderator.guild_permissions.ban_members:
            await interaction.response.send_message(f"You may not use this command as you do not have the required permissions.", ephemeral=True)
            return

        await member.send(f"You have been **banned** from **{interaction.guild}** for **{reason}**")
        await member.ban(reason= reason or None)
        await interaction.response.send_message(f"You have banned **{member.mention} [ID = {member.id}, display name = {member.display_name}]** for **{reason}**", ephemeral=True)
        # Add the logging functionality when it is available.
        # possibly create a case code and then call the listener.
        self.bot.dispatch("moderation", interaction=interaction, target=member, action="Banned", reason=reason)

    @moderation.command(name="unban", description="Unbans the specified user.")
    async def unban(self, interaction: discord.Interaction, user_id: str):
        """
        Parameters:
            -   user_id: str - The id of the member that is going to be unbanned.
        """
        if interaction.user.guild_permissions.ban_members:
            user= await self.bot.fetch_user(user_id)
            await interaction.guild.unban(user)
            await interaction.response.send_message(f"Success! You have unbanned the user: {user.name}", ephemeral=True)
        else:
            await interaction.response.send_message("🚫 You do not have Permission to Moderate Members.", ephemeral=True)
       
        self.bot.dispatch("moderation", interaction=interaction, target=user, action="Unbanned", reason="")
        
async def setup(bot):
    await bot.add_cog(Moderation(bot))