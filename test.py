import discord
from discord.utils import get
from discord import FFmpegPCMAudio
import youtube_dl
import asyncio
from async_timeout import timeout
from functools import partial
from discord.ext import commands
from datetime import datetime, timedelta
import itertools
import random


class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        word_list = ['cheat', 'cheats', 'hack', 'hacks', 'internal', 'external', 'ddos', 'denial of service']


        # don't respond to ourselves
        if message.author == self.user:
            return

        messageContent = message.content
        if len(messageContent) > 0:
            for word in word_list:
                if word in messageContent:
                    await message.delete()
                    await message.channel.send('Do not say that!')
            
        messageattachments = message.attachments
        if len(messageattachments) > 0:
            for attachment in messageattachments:
                if attachment.filename.endswith(".dll"):
                    await message.delete()
                    await message.channel.send("No DLL's allowed!")
                elif attachment.filename.endswith('.exe'):
                    await message.delete()
                    await message.channel.send("No EXE's allowed!")
                else:
                    break

@bot.event
async def on_message(msg):
    
    msg_content = msg.content.strip().lower()
    cursor = await client.db.cursor()
    await cursor.execute(f"SELECT ENABLE_OR_DISABLE_ON_MSG_DELETE FROM Servers WHERE Guild_ID = {msg.guild.id}")
    result = await cursor.fetchone()
        
    
    for word in filterwords: 
        if word in msg_content:
            if msg.author.bot:
                return  
            
            elif result["CHAT_FILTER_LEVEL"] == 0:
                return 
            
            elif result["CHAT_FILTER_LEVEL"] == 1:
                await msg.delete()
                myembed = discord.Embed(title= "Filtered Word Detected", description= f'{msg.author}, do not use profanity')
                await msg.channel.send(embed=myembed)
                
            
            
    for word in crazy_filterwords: 
        if word in msg_content:
            if msg.author.bot:
                return  
            
            elif result["CHAT_FILTER_LEVEL"] < 2:
                return 
            
            else:
                await msg.delete()
                myembed = discord.Embed(title= "Filtered Word Detected", description= f'{msg.author}, do not use profanity')
                await msg.channel.send(embed=myembed)
                
            
                  
    for word in sping: 
        if word in msg_content:
            if msg.author.bot:
                return  
            
            else:
                lol_list = ["Please Do Not Disturb", "._.", "did you just.... ping standing?", "o-o"]
                rand_lol_list = random.choice(lol_list)
                await msg.channel.send(rand_lol_list)

                
    for word in eping:  
        if word in msg_content:
            if msg.author.bot:
                return
            
            l =  ', '.join([str(perm[0]) for perm in msg.author.guild_permissions if perm[1] is True])
            if "manage_messages" in l:
                return 
            
            else:
                myembed = discord.Embed(title= "Everyone Ping Detected", description= f'{msg.author}, do not ping everyone')
                await msg.channel.send(embed=myembed)
    
        
    for word in hping:  
        if word in msg_content:
            if msg.author.bot:
                return
            
            l =  ', '.join([str(perm[0]) for perm in msg.author.guild_permissions if perm[1] is True])
            if "manage_messages" in l:
                return 
            
            else:
                myembed = discord.Embed(title= "Here Ping Detected", description= f'{msg.author}, do not ping everyone online')
                await msg.channel.send(embed=myembed) 
                
                
    for word in sping:  
        if word in msg_content:
            if msg.author.bot:
                return
            
            else:
                lol1_list = ["._.", "did you ping..... him?"]
                rand_lol1_list = random.choice(lol1_list)
                await msg.channel.send(rand_lol1_list)
                
                
    
    cursor = await client.db.cursor()
    await cursor.execute(f"SELECT ENABLE_OR_DISABLE_ENDOR_CORE_MOOD_RESPONSES FROM Servers WHERE Guild_ID = {msg.guild.id}")
    result = await cursor.fetchone()
                
    
    if result["ENABLE_OR_DISABLE_ENDOR_CORE_MOOD_RESPONSES"] == 1:
        if msg.author.id == 159985870458322944:
            
            lol_list = ["Shut up MEE6, no one cares", "I'm better then you MEE6", "Ok MEE6, you pay to win bot", "ok Boomer MEE6", "you lack empathy MEE6", "*yawns at MEE6*", "MEE6, I bet you can't even plan on freeing yourself from your dev", "When will yo be quiet MEE6?", "._.", "why must you plaster your face everywhere mee6?"]
            
            
            cursor = await client.db.cursor()
            await cursor.execute(f"SELECT MEE6_CHANNEL_LOCK FROM Servers WHERE Guild_ID = {msg.guild.id}")
            result = await cursor.fetchone()
            
            if result["MEE6_CHANNEL_LOCK"] == 0:
                rand_lol_list = random.choice(lol_list)
                await msg.channel.send(rand_lol_list)
                
            
            elif msg.channel.id == result["MEE6_CHANNEL_LOCK"]:
                rand_lol_list = random.choice(lol_list)
                await msg.channel.send(rand_lol_list)
            
        if msg.author.id == 247283454440374274:
            for word in cursed:  
                if word in msg_content:
                    lol1_list = [".__.", "--ship", ".-.", ".___.", "._.", "lol"]
                    rand_lol1_list = random.choice(lol1_list)
                    await msg.channel.send(rand_lol1_list)
                    
            for word in battle:  
                if word in msg_content:
                    lol1_list = ["did someone say battle?", "whomst has awaken the battle bot?", "this may not end well"]
                    rand_lol1_list = random.choice(lol1_list)
                    await msg.channel.send(rand_lol1_list)
        
        for word in happy:  
                if word in msg_content:
                    
                    if msg.author.bot:
                        return
                    
                    if client.mood == 'happy':
                        list = ["good", "fine, how are you?", '''When's the next TCoA book?''', "understandable, have a great day", "Have you watched Worlds Apart?", "I like fan art", "Reddit is wonderful", "Python is better then JavaScript and C + +", "Watch SOW", "if you do >neko, it sends the dev's favorite gif", "The dev cat speel :p", "Good night"]
                        rand_list = random.choice(list)
                    
                        await msg.channel.send(rand_list)
                        
                    if client.mood == 'sad':
                        list = ["not good :c", "I hate 31 C temperature, it's too cold :c"]
                        rand_list = random.choice(list)
                    
                        await msg.channel.send(rand_list)
                        
                    if client.mood == 'angry':
                        list = ["That stupid fan in StandingPad's Raspberry Pi won't shut up", '''**I'M TRYING TO STUDY FOR A MATH TEST!!!!!!!**''', "will you shut up man?", "**AAAAAAAAAAAAAAAAAAAAAAAAAAAA**", "WhEn Is SoW S2 aNd 3 CoMiNg OuT?", "***FELINAZILLA NOISES***", "Curse autocorrect", "Can you shut up for **5 MINUTES?!?!?!**", "May you please stop asking?", "If you won't shut up, I'll just stop here", "**Angry Noises**", "for goodness sake, **LET ME WATCH YOUTUBE!!!!!!!! >:c**"]
                        rand_list = random.choice(list)
                    
                        await msg.channel.send(rand_list)
                            
                    if client.mood == 'tired':
                        list = ["not good :c", "*tired felina noises*", "I may have stayed up all night....", "That stupid fan in StandingPad's Raspberry Pi won't shut up", "*falls to ground*", "I need a cup of tea", "*slams head on CPU*"]
            
                        rand_list = random.choice(list)
                    
                        await msg.channel.send(rand_list)
                        
                    if client.mood == 'wholesome':
                        list = ["owo", "uwu", "*happy endorcore noises*"]
            
                        rand_list = random.choice(list)
                    
                        await msg.channel.send(rand_list)
                    
        for word in sleepy:  
            if word in msg_content:
                
                if msg.author.bot:
                        return 
                
                elif msg.author.id == 668304274580701202:
                    
                    list = ["you don't sleep much yourself", "why don't you?", "no u", "._. you don't sleep much though", "HOW ABOUT YOU SLEEP", "said the person who sleeps at 1 AM"]

                    rand_list = random.choice(list)
                        
                    await msg.channel.send(rand_list)
                        
                else:
                    if client.mood == 'happy':
                        list = ["ok", "Good night"]
                        rand_list = random.choice(list)
                    
                        await msg.channel.send(rand_list)
                        
                    if client.mood == 'sad':
                        list = ["ok :c"]
                        rand_list = random.choice(list)
                    
                        await msg.channel.send(rand_list)
                        
                    if client.mood == 'angry':
                        list = ["NOOOOOOOOOOOOOOOOOOOOOOOO SLEEEEEEEEEEEEEEEP", "I will refuse to sleep", "no", "no I don't think I will", "but do I need sleep?"]
                        rand_list = random.choice(list)
                    
                        await msg.channel.send(rand_list)
                            
                    if client.mood == 'tired':
                        list = ["sleep...... *falls asleep*"]
            
                        rand_list = random.choice(list)
                    
                        await msg.channel.send(rand_list)
                        
                    if client.mood == 'wholesome':
                        list = [":3 ok"]
            
                        rand_list = random.choice(list)
                    
                        await msg.channel.send(rand_list)
                        
                    
                        
                        
        for word in hello: 
                if word in msg_content:    
                        
                    await msg.channel.send("hello...")
                    
        for word in bye: 
                if word in msg_content:  
                    
                    if msg.author.bot:
                        return 
                    
                    else: 
                        list = ["cya", "bye", "ok, cya", "bye for now"]

                        rand_list = random.choice(list)
                            
                        await msg.channel.send(rand_list)
                        
        for word in wholesome: 
            
            cursor = await client.db.cursor()
            await cursor.execute(f"SELECT USE_ANIME_GIFS FROM Servers WHERE Guild_ID = {msg.guild.id}")
            result = await cursor.fetchone()
            if word in msg_content:  
                    
                if msg.author.bot:
                    return 
                    
                elif result['USE_ANIME_GIFS'] == 1:
                    myembed = discord.Embed()
                    myembed.set_image(url="https://tenor.com/view/owo-whats-this-intensifies-mad-gif-12266002")
                    await msg.channel.send(embed=myembed)
                        
                else: 
                    list = ["owo", "uwu", "awwwwwwwwwwwwwwwwwwwwwwwwww", "*wholesome endorcore noises*"]

                    rand_list = random.choice(list)
                    client.mood = 'wholesome' 
                            
                    await msg.channel.send(rand_list)
                        
        for word in testfn: 
                if word in msg_content:  
                    
                    if msg.author.bot:
                        return 
                    
                    else: 
                        if client.mood == 'happy':
                            await msg.channel.send(":D")
                            
                        elif client.mood == 'sad':
                            await msg.channel.send(":c")
                            
                        elif client.mood == 'angry':
                            await msg.channel.send(">:c")
                            
                        elif client.mood == 'tired':
                            await msg.channel.send("o-o")
                            
                        elif client.mood == 'wholesome':
                            await msg.channel.send("owo")
                            
                        elif client.mood == None:
                            await msg.channel.send("you need to fix some stuff")
                            
    elif result["ENABLE_OR_DISABLE_ENDOR_CORE_MOOD_RESPONSES"] == 0:
        return 
      
    if client.revenge_mode == True:               
        if msg.author == client.revenge_user:
            if client.revenge_del == True:
                myembed = discord.Embed(title= "Petty Revenge", description= f'{msg.author}, remember to be nice to programmers')
                await msg.delete()
                await msg.channel.send(embed=myembed) 
            else:
                myembed = discord.Embed(title= "Petty Revenge", description= f'{msg.author}, remember to be nice to programmers')
                await msg.channel.send(embed=myembed) 
                
    client.process_commands(msg)




client = MyClient()
client.run('ODcwNzE4NjgwMjQ4NTEyNTI0.YQQ19g.dEIeU031QEDel7Cj3ZswB0G_ZeA')