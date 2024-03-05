import discord
import yaml
from discord import app_commands
from discord.ext import commands

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

allowed_roles = data["AllowedRoles"]

class CreateEmbedModal(discord.ui.Modal, title='Create Embed'):
    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=None)
        self.bot = bot

    embed_title = discord.ui.TextInput(
        label="What is the embed title?",
        placeholder='Type the embed title here...',
        max_length=256,
        style=discord.TextStyle.short,
        required=False,
    )

    embed_description = discord.ui.TextInput(
        label="What is the embed description?",
        placeholder='Type the embed description here...',
        max_length=4000,
        style=discord.TextStyle.long,
        required=False,
    )

    embed_author = discord.ui.TextInput(
        label="What is the embed author?",
        placeholder='Type the embed author here...',
        max_length=256,
        style=discord.TextStyle.short,
        required=False,
    )

    embed_icon_url = discord.ui.TextInput(
        label="What is the embed icon url?",
        placeholder='Type the embed icon url here...',
        max_length=1000,
        style=discord.TextStyle.short,
        required=False,
    )

    embed_color = discord.ui.TextInput(
        label="What is the embed color?",
        placeholder='Type the embed hex color here...',
        max_length=7,
        style=discord.TextStyle.short,
        required=False,
    )

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed()

        if self.embed_title.value:
            embed.title = self.embed_title.value
        if self.embed_description.value:
            embed.description = self.embed_description.value
        if self.embed_author.value:
            if self.embed_icon_url.value:
                if "https://" in self.embed_icon_url.value:
                    embed.set_author(name=self.embed_author.value, icon_url=self.embed_icon_url.value)
                else:
                    embed.set_author(name=self.embed_author.value)
            else:
                embed.set_author(name=self.embed_author.value)
        elif self.embed_icon_url.value:
            if "https://" in self.embed_icon_url.value:
                embed.set_author(icon_url=self.embed_icon_url)
        if self.embed_color.value:
            embed.color = discord.Color.from_str(self.embed_color.value)
        
        try:
            await interaction.channel.send(embed=embed)
            embed = discord.Embed(description="Successfully sent!", color=discord.Color.green())
        except:
            embed = discord.Embed(description="Failed to send embed. Some values are required!", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)

class EditEmbedModal(discord.ui.Modal, title='Edit Embed'):
    def __init__(self, bot: commands.Bot, message: discord.Message):
        super().__init__(timeout=None)
        self.bot = bot
        self.message = message

    embed_title = discord.ui.TextInput(
        label="What is the embed title?",
        placeholder='Type the embed title here...',
        max_length=256,
        style=discord.TextStyle.short,
        required=False,
    )

    embed_description = discord.ui.TextInput(
        label="What is the embed description?",
        placeholder='Type the embed description here...',
        max_length=4000,
        style=discord.TextStyle.long,
        required=False,
    )

    embed_author = discord.ui.TextInput(
        label="What is the embed author?",
        placeholder='Type the embed author here...',
        max_length=256,
        style=discord.TextStyle.short,
        required=False,
    )

    embed_icon_url = discord.ui.TextInput(
        label="What is the embed icon url?",
        placeholder='Type the embed icon url here...',
        max_length=1000,
        style=discord.TextStyle.short,
        required=False,
    )

    embed_color = discord.ui.TextInput(
        label="What is the embed color?",
        placeholder='Type the embed hex color here...',
        max_length=7,
        style=discord.TextStyle.short,
        required=False,
    )

    async def on_submit(self, interaction: discord.Interaction):

        embed = discord.Embed()

        if self.embed_title.value:
            embed.title = self.embed_title.value
        if self.embed_description.value:
            embed.description = self.embed_description.value
        if self.embed_author.value:
            if self.embed_icon_url.value:
                if "https://" in self.embed_icon_url.value:
                    embed.set_author(name=self.embed_author.value, icon_url=self.embed_icon_url.value)
                else:
                    embed.set_author(name=self.embed_author.value)
            else:
                embed.set_author(name=self.embed_author.value)
        elif self.embed_icon_url.value:
            if "https://" in self.embed_icon_url.value:
                embed.set_author(icon_url=self.embed_icon_url)
        if self.embed_color.value:
            embed.color = discord.Color.from_str(self.embed_color.value)
        
        try:
            await self.message.edit(embed=embed)
            embed = discord.Embed(description="Successfully edited!", color=discord.Color.green())
        except:
            embed = discord.Embed(description="Failed to edit embed. Some values are required!", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)

class EmbedCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="createembed", description="Creates an embed!")
    async def createembed(self, interaction: discord.Interaction) -> None:
        if any(role.id in allowed_roles for role in interaction.user.roles):
            await interaction.response.send_modal(CreateEmbedModal(self.bot))
        else:
            embed = discord.Embed(description="You do not have the required permissions to use this command!", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="editembed", description="Edits an embed!")
    @app_commands.describe(channel="What channel is the message you want to edit in?")
    @app_commands.describe(message_id="What message id do you want to edit?")
    async def editembed(self, interaction: discord.Interaction, channel: discord.TextChannel, message_id: str) -> None:
        if any(role.id in allowed_roles for role in interaction.user.roles):
            try:
                message_id = int(message_id)
                try:
                    message = await channel.fetch_message(message_id)
                    await interaction.response.send_modal(EditEmbedModal(self.bot, message))
                except:
                    embed = discord.Embed(description=f"Failed to fetch the message. Perhaps the message isn't in {channel.mention}?", color=discord.Color.red())
                    await interaction.response.send_message(embed=embed, ephemeral=True)
            except:
                embed = discord.Embed(description=f"Failed to convert **{message_id}** to an integer!", color=discord.Color.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(description="You do not have the required permissions to use this command!", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(EmbedCog(bot))