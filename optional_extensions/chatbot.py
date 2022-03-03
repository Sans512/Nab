import discord
import _chatbot
from discord.ext import commands


class ChatBot(commands.Cog):
    """Command/event category for the AI chatbot"""
    def __init__(self, bot: commands.Bot):
        self.chatbot = _chatbot.init_chatbot() # Initialise the chatbot model from the _chatbot module
        self.bot = bot

        self.enabled_channels = [] # A list of all the channels AI chat is enabled in (!!! THIS MIGHT BE DODGY !!!)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Gets a response from the AI chatbot when someone sends a message"""

        if message.author.bot or message.channel not in self.enabled_channels:
            return # Do nothing if the bot sent the message or if this isn't an enabled channel

        response_ = self.chatbot.get_response(message.content)
        await message.channel.send(f"{message.author.mention}: {response_}")

    @commands.command(name="aienable", aliases=["ai", "enableaichat"],
                      description="Enables AI chatbot responses to all messages within a channel."
                                + "Requires 'Manage channels' permissions")
    @commands.has_permissions(manage_channels=True)
    async def enable_ai_chat(self, ctx: commands.Context):
        """Enables AI chatbot responses in a text channel"""

        # Add the channel to the list. Check in on_message if this is an enabled channel
        self.enabled_channels.append(ctx.channel)
        await ctx.send("✅ Done! I will now use AI to respond to all messages in this channel\n" +
                       "You can use ```.aidisable``` or ```.disableaichat``` to disable chatbot responses")

    @enable_ai_chat.error
    async def enable_ai_chat_error(self, ctx: commands.Context, error):
        """Called when the enable AI chat command throws an error"""

        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to enable AI chat in this channel")

    @commands.command(name="aidisable", aliases=["disableaichat"])


def setup(bot: commands.Bot):
    """Adds the 'ChatBot' cog to the bot"""
    bot.add_cog(ChatBot(bot))
