import discord, os
from gameFunctions import *
import math

client = discord.Client() #connection to discord

@client.event #register an event
async def on_ready():
    print("Gamble Bot is online!")
    await client.change_presence(activity=discord.Game(name="Made by Hemzyy. '$help'"))
    casino_channel = client.get_channel(801166940826894357)
    await casino_channel.send('Gamba bot is here, place your bets!')

@client.event #second event 
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == ('$help'):
        await message.channel.send("Type '$balance' to check your balance\ntype '$give [amount] [name#0000] to send points to another players\nType '$bet [amount] [h or t]' to bet\ntype '$rewards' to see rewards available to redeem'")

    if message.content == ('$rewards'):
        with open('rewards.txt') as f:
            file = f.read()
        await message.channel.send(file)
        

    if message.content == ('$refill'):
        refill()

    if message.content.startswith('$give'):
        msg = message.content.split(' ', 2)
        arg = int(msg[1])
        receiver = str(msg[2])
        sender = str(message.author)
        if enoughBalance(sender, abs(arg)):
            givePoints(sender, receiver, arg)
            Message = str(arg) + " have been sent to " + str(receiver)
            await message.channel.send(Message)
        else:
            await message.channel.send("You don't have enough points to give to this player")

    if message.content.startswith('$bet'): #Basically the whole point of this bot
        msg = message.content.split(' ', 2)
        arg = msg[1]
        prediction = msg[2]
        sender = message.author

        if isNewPlayer(str(sender)):
            addPlayer(str(sender))
            await message.channel.send('You have been added to the players list with a balance of 50 points.')
        else:
            if arg == '0' : await message.channel.send('You can\'t bet nothing dumbass')
            elif arg < '0': await message.channel.send('That\'s illegal')
            elif (enoughBalance(str(sender), abs(int(arg)))):
                removePoints(str(sender), abs(int(arg)))
                if isEqual(str(prediction)):
                    addPoints(str(sender), abs(int(arg))*2)
                    await message.channel.send("```Congrats, you won double your bet!```")
                else:
                    await message.channel.send("```Sorry, you lost.```")
            else:
                await message.channel.send('You don\'t have enough points.')
                
    if message.content == ('$balance'):
        sender = message.author
        if isNewPlayer(str(sender)):
            addPlayer(str(sender))
            await message.channel.send('You have been added to the players list with a balance of 50 points.')
        await message.channel.send('<@'+ str(message.author.id)+'>, '+ checkBalance(str(sender)))
                    

client.run()