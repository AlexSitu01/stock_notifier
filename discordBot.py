import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import pandas as pd
import datetime
from Stocks import Stocks
from news import News

load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")

#at what time the check function is called
utc = datetime.timezone.utc
TIME = datetime.time(hour=3, minute=37, tzinfo=utc)
class Bot:
    def __init__(self):
        if not os.path.isfile("users.csv"):
            df = pd.DataFrame(columns=["user_name, user_id"])
            df.to_csv("users.csv")
        self.data = pd.read_csv("users.csv")

        #Call bot instance
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        self.bot = commands.Bot(command_prefix='!', intents=intents)
        guild = discord.Object(id=1169059604370575381)

        #Bot commands
        @self.bot.hybrid_command(name="test")
        async def test(ctx):
            await ctx.send("This is a hybrid command!")

        @self.bot.hybrid_command(name="addme")
        async def add_user(ctx):
            user_name = ctx.author.name
            user_id = ctx.author.id
            try:
                df = pd.read_csv('users.csv')
            except Exception as e:
                df = pd.DataFrame(columns=["user_name, user_id"])
                df.to_csv("users.csv")

            if user_id in df['user_id'].values:
                await ctx.send("User already exists in the database.")
                return
            new_user = {
                'user_name': [user_name],
                'user_id': [user_id]
            }
            new_df = pd.DataFrame(new_user)
            new_df.to_csv('users.csv', mode='a', index=False, header=False)
            print("added new user")
            await ctx.send("New user was successfully added.")

        @self.bot.hybrid_command(name="removeme")
        async def remove_me(ctx):
            user_name = ctx.author.name
            user_id = ctx.author.id
            if os.path.isfile("users.csv"):
               data = pd.read_csv("users.csv")
            else:
                print("user.csv file has not been created yet.")
                return

            if user_id in data["user_id"].values:
                data = data[data["user_id"] != user_id]
                data.to_csv('users.csv', mode='w', index=False, header=True)
                await ctx.send(f"{user_name} has been removed")
            else:
                await ctx.send("You were never on the list to begin with.")

        @self.bot.hybrid_command(name="send")
        async def test_send(ctx):
            for index, rows in self.data.iterrows():
                user = await self.bot.fetch_user(rows["user_id"])
                await user.send("test")

        #need to implement a stock symbol checking feature
        @self.bot.hybrid_command()
        async def add_stock(ctx, *, args: str):
            args = args.split(" ")
            for stock_symbol in args:
                await ctx.send(Stocks.add_stock(stock_symbol))

        @self.bot.hybrid_command()
        async def remove_stock(ctx, *, args: str):
            args = args.split(" ")
            for stock_symbol in args:
                await ctx.send(Stocks.remove_stock(stock_symbol))

        @tasks.loop(time=TIME)
        async def check_stocks():
            stock_symbols = Stocks.get_stock_list()
            string_output = []
            for stock_symbol in stock_symbols:
                output_stock = Stocks.check_stock(stock_symbol)
                output_news = News.get_news(stock_symbol)
                if output_stock is not None:
                    string_output.append(output_stock)
                    string_output.append(output_news)
            print(f"String Output: {string_output}")
            #send all users any information about stock price changes
            user_ids = self.data["user_id"].values
            for user_id in user_ids:
                user = await self.bot.fetch_user(user_id)
                #if string_output is empty
                if not string_output:
                    await user.send("None of the stocks have increased significantly.")
                #if one or more stocks have increased in value, then send that to the user.
                else:
                    await user.send("\n".join(string_output))

        #Events
        @self.bot.event
        async def on_ready():
            check_stocks.start()
            print(f"We have logged in as {self.bot.user}")
            try:
                #Sync to server instantly
                # bot.tree.copy_global_to(guild=guild)
                # synced = await bot.tree.sync(guild=guild)

                #takes a while to sync slash commands so just use !command to test
                synced = await self.bot.tree.sync()
                print(f"Synced {len(synced)} command(s)")
                print(synced)
            except Exception as e:
                print(f"Error syncing commands: {e}")

        @self.bot.event
        async def on_message(message):
            #ensure that we don't respond to our own messages, creating an infinite loop
            if message.author == self.bot.user:
                return

            if message.content.startswith("hello"):
                await message.channel.send("Hello!")

            #must have this line to listen for commands
            await self.bot.process_commands(message)

        self.bot.run(BOT_TOKEN)
