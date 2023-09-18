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


##############################################################################################################
# wrapper / decorator
message_lastseen = datetime.now()
message2_lastseen = datetime.now()
message3_lastseen = datetime.now()
message4_lastseen = datetime.now()
message5_lastseen = datetime.now()
message6_lastseen = datetime.now()
bot = commands.Bot(command_prefix='=',help_command=None)
youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}
ffmpeg_options = {
    'options': '-vn',
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5" ## song will end if no this line
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester
        self.title = data.get('title')
        self.web_url = data.get('webpage_url')
        # YTDL info dicts (data) have other useful information you might want
        # https://github.com/rg3/youtube-dl/blob/master/README.md
    def __getitem__(self, item: str):
        """Allows us to access attributes similar to a dict.
        This is only useful when you are NOT downloading.
        """
        return self.__getattribute__(item)
    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False):
        loop = loop or asyncio.get_event_loop()
        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        await ctx.send(f'```ini\n[Added {data["title"]} to the Queue.]\n```') #delete after can be added
        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}
        return cls(discord.FFmpegPCMAudio(source, **ffmpeg_options), data=data, requester=ctx.author)
    @classmethod
    async def regather_stream(cls, data, *, loop):
        """Used for preparing a stream, instead of downloading.
        Since Youtube Streaming links expire."""
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']
        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)
        return cls(discord.FFmpegPCMAudio(data['url'], **ffmpeg_options), data=data, requester=requester)
class MusicPlayer:
    """A class which is assigned to each guild using the bot for Music.
    This class implements a queue and loop, which allows for different guilds to listen to different playlists
    simultaneously.
    When the bot disconnects from the Voice it's instance will be destroyed.
    """
    __slots__ = ('bot', '_guild', '_channel', '_cog', 'queue', 'next', 'current', 'np', 'volume')
    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog
        self.queue = asyncio.Queue()
        self.next = asyncio.Event()
        self.np = None  # Now playing message
        self.volume = .5
        self.current = None
        ctx.bot.loop.create_task(self.player_loop())
    async def player_loop(self):
        """Our main player loop."""
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            self.next.clear()
            try:
                # Wait for the next song. If we timeout cancel the player and disconnect...
                async with timeout(300):  # 5 minutes...
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                return await self.destroy(self._guild)
            if not isinstance(source, YTDLSource):
                # Source was probably a stream (not downloaded)
                # So we should regather to prevent stream expiration
                try:
                    source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
                except Exception as e:
                    await self._channel.send(f'There was an error processing your song.\n'
                                             f'```css\n[{e}]\n```')
                    continue
            source.volume = self.volume
            self.current = source
            self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            self.np = await self._channel.send(f'**Now Playing:** `{source.title}` requested by '
                                               f'`{source.requester}`')
            await self.next.wait()
            # Make sure the FFmpeg process is cleaned up.
            source.cleanup()
            self.current = None
            try:
                # We are no longer playing this song...
                await self.np.delete()
            except discord.HTTPException:
                pass

    async def destroy(self, guild):
        """Disconnect and cleanup the player."""
        del players[self._guild]
        await self._guild.voice_client.disconnect()
        return self.bot.loop.create_task(self._cog.cleanup(guild))
class MyClient(discord.Client):

    
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

                    break

##############################################################################################################
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
@bot.command()
async def test(ctx, *, par):
    await ctx.channel.send("You typed {0}".format(par))
@bot.command() 
async def help(ctx):
    # help
    # test
    # send
    emBed = discord.Embed(title="Tutorial Bot help", description="All available bot commands", color=0x42f5a7)
    emBed.add_field(name="help", value="Get help command", inline=False)
    emBed.add_field(name="test", value="Respond message that you've send", inline=False)
    emBed.add_field(name="send", value="Send hello message to user", inline=False)
    emBed.set_thumbnail(url='https://media-exp1.licdn.com/dms/image/C560BAQFHd3L0xFcwcw/company-logo_200_200/0/1550868149376?e=2159024400&v=beta&t=LyKtz-V4W8Gfwzi2ZqmikaI9GcUXI3773_aa3F3nIhg')
    emBed.set_footer(text='test footer', icon_url='https://media-exp1.licdn.com/dms/image/C560BAQFHd3L0xFcwcw/company-logo_200_200/0/1550868149376?e=2159024400&v=beta&t=LyKtz-V4W8Gfwzi2ZqmikaI9GcUXI3773_aa3F3nIhg')
    await ctx.channel.send(embed=emBed)

@bot.command()
async def send(ctx):
    print(ctx.channel)
    await ctx.channel.send('Hello')
@bot.event #async/await
async def on_message(message):
    global message_lastseen, message2_lastseen, message3_lastseen, message4_lastseen, message5_lastseen 
    if message.content == '!user':
        await message.channel.send(str(message.author.name) + ' Hello')
    elif message.content == 'นายชื่ออะไร' and datetime.now() >= message_lastseen:
        message_lastseen = datetime.now() + timedelta(seconds=5)
        await message.channel.send('ผมชื่อ ' + str(bot.user.name))
        #logging 
        print('{0} เรียกใช้ นายชื่ออะไร ตอน {1} และจะใช้ได้อีกทีตอน {2}'.format(message.author.name,datetime.now(),message_lastseen))
    elif message.content == 'ผมชื่ออะไร' and datetime.now() >= message2_lastseen:
        message2_lastseen = datetime.now() + timedelta(seconds=5)
        await message.channel.send('เธอชื่อ ' + str(message.author.name))

    elif message.content == 'สวัสดี' and datetime.now() >= message3_lastseen:
        message3_lastseen = datetime.now() + timedelta(seconds=5)
        await message.channel.send('สวัสดีครับ'+ str(message.author.name))

    elif message.content == 'ใครคือผู้สร้างนาย' and datetime.now() >= message4_lastseen:
        message4_lastseen = datetime.now() + timedelta(seconds=5)
        await message.channel.send('คุณSunny ยังไงล่ะ!!!')

    elif message.content == 'ไปแล้วนะ' and datetime.now() >= message5_lastseen:
        message5_lastseen = datetime.now() + timedelta(seconds=5)
        await message.channel.send('โชคดีค้าบบบบ'+ str(message.author.name))
    
    elif message.content == 'สักหมัดไหมซัน' and datetime.now() >= message5_lastseen:
        message5_lastseen = datetime.now() + timedelta(seconds=5)
        await message.channel.send('ก็มาสิค้าบ'+ str(message.author.name))
    
    



    elif message.content == '!logout':
        await bot.logout()
    await bot.process_commands(message)




@bot.listen('on_message') 
async def stuff(message):
    
    if message.content.startswith("hi"): # this tells the bot what to listen for. If a user types `buttlerprefix` in any text channel, it will respond with what's below
        msg = await message.channel.send("Yahooooo") # set the sending message equal to a variable so that you can manipulate it later like I did with the timer, and delete function below
    elif message.content.startswith("ไง"): 
        msg = await message.channel.send('ว่าไง')
    elif message.content.startswith("หวัดดีครับ"): 
        msg = await message.channel.send('สวัสดีครับ')
    elif message.content.startswith("คุณซัน"): 
        msg = await message.channel.send('ว่ายังไงค้าบ')
    elif message.content.startswith("Sun"): 
        msg = await message.channel.send('ว่าไงค้าบ')
    elif message.content.startswith("พี่ซัน"): 
        msg = await message.channel.send('ว่าไงค้าบน้อง')
    elif message.content.startswith("พี่ตะวัน"): 
        msg = await message.channel.send('ค้าบผม')
    elif message.content.startswith("คุณตะวัน"): 
        msg = await message.channel.send('ค้าบผม')
    elif message.content.startswith("ตะวัน"): 
        msg = await message.channel.send('ค้าบผม')
    elif message.content.startswith("ซัน"): 
        msg = await message.channel.send('ครับผม')
    
    #yos/no
    elif message.content.startswith("ไม่"): 
        msg = await message.channel.send('จริงอ่ะป่าว')
    elif message.content.startswith("จริง"): 
        msg = await message.channel.send('แน่ใจ??')
    elif message.content.startswith("ใช่"): 
        msg = await message.channel.send('จริงหรือป่าว')
    elif message.content.startswith("หรือเปล่า"): 
        msg = await message.channel.send('ก็อาจจะนะครับ')
    
    #ฝันดี
    elif message.content.startswith("นอนแล้วนะ"): 
        msg = await message.channel.send('โรตีสวัสดิ์ครับ')
    elif message.content.startswith("ฝันดีครับ"): 
        msg = await message.channel.send('โรตีสวัสดิ์ครับ')
    elif message.content.startswith("ฝันดีค่ะ"): 
        msg = await message.channel.send('โรตีสวัสดิ์ครับ')
    elif message.content.startswith("ฝันดี"): 
        msg = await message.channel.send('โรตีสวัสดิ์ครับ')
    elif message.content.startswith("ฝันหวาน"): 
        msg = await message.channel.send('โรตีสวัสดิ์ครับ')
    elif message.content.startswith("จะไปนอนแล้ว"): 
        msg = await message.channel.send('โรตีสวัสดิ์ครับ')
    
    #คำชม
    elif message.content.startswith("ผมหล่อไหม"): 
        msg = await message.channel.send('หล่อมากเลยครับ')
    elif message.content.startswith("หนูสวยไหม"): 
        msg = await message.channel.send('สวยมักๆเลยครับ')
    elif message.content.startswith("หนูน่ารักไหม"): 
        msg = await message.channel.send('น่ารักมากๆเลยยย //ลูปหัวๆ')
    elif message.content.startswith("หนูไม่น่ารักหรอคะ"): 
        msg = await message.channel.send('คนน่ารักต้องไม่ดื้อนะครับ')
    elif message.content.startswith("หนูทำตัวไม่น่ารักหรอคะ"): 
        msg = await message.channel.send('น่ารักครับถ้าไม่ดื้อ')
    elif message.content.startswith("เอ็นดู"): 
        msg = await message.channel.send('ผมเอ็นดูนะครับบ')

    #คำถามทั่วไป
    elif message.content.startswith("นอนตอนไหน"):
        msg = await message.channel.send('ตอนที่ง่วงครับบ')
    elif message.content.startswith("หนาว"):
        msg = await message.channel.send('กอดไหมครับ')
    elif message.content.startswith("วันนี้เป็นยังไงบ้าง"):
        msg = await message.channel.send('ก็ดีครับ')
    elif message.content.startswith("ทานข้าวรึยัง"):
        msg = await message.channel.send('รอทานพร้อมคุณครับ')
    elif message.content.startswith("ทานไรยัง"): 
        msg = await message.channel.send('รอทานพร้อมคุณครับ')
    elif message.content.startswith("กินข้าวรึยัง"): 
        msg = await message.channel.send('รอกินพร้อมคุณครับ')
    elif message.content.startswith("หิวข้าวไหม"): 
        msg = await message.channel.send('รอทานพร้อมคุณครับ')
    elif message.content.startswith("กินข้าวยัง"): 
        msg = await message.channel.send('รอกินพร้อมคุณครับ')
    elif message.content.startswith("รัก"): 
        msg = await message.channel.send('ผมก็รักนะครับ')
    elif message.content.startswith("เรียกมิวสิ"): 
        msg = await message.channel.send('มิวว')
    elif message.content.startswith("ชอบผชหรือผญ"): 
        msg = await message.channel.send('ชอบคุณโอบอุ้มครับ')
    elif message.content.startswith("ชอบผู้ชายหรือผู้หญิง"): 
        msg = await message.channel.send('ชอบคุณโอบอุ้มครับ')
    elif message.content.startswith("มอนิ่ง"): 
        msg = await message.channel.send('วัวไม่ขยับครับ')
    
    
    

#@bot.message_handler(commands=['start', 'help'])
#def send_welcome(message):
	#bot.reply_to(message, "Howdy, how are you doing?")

#@bot.message_handler(func=lambda message: True)
#def echo_all(message):
	#bot.reply_to(message, message.text)




@bot.command() 
async def play(ctx,* ,search: str):
    channel = ctx.author.voice.channel
    voice_client = get(bot.voice_clients, guild=ctx.guild)
    
    if voice_client == None:
        await ctx.channel.send("Joined👍")
        await channel.connect()
        voice_client = get(bot.voice_clients, guild=ctx.guild)
    await ctx.trigger_typing()
    _player = get_player(ctx)
    source = await YTDLSource.create_source(ctx, search, loop=bot.loop, download=False)
    await _player.queue.put(source)
players = {}
def get_player(ctx):
    try:
        player = players[ctx.guild.id]
    except:
        player = MusicPlayer(ctx)
        players[ctx.guild.id] = player
    
    return player
    
@bot.command()
async def stop(ctx):
    voice_client = get(bot.voice_clients, guild=ctx.guild)
    if voice_client == None:
        await ctx.channel.send("Bot is not connected to vc")
        return
    if voice_client.channel != ctx.author.voice.channel:
        await ctx.channel.send("The bot is currently connected to {0}".format(voice_client.channel))
        return
    voice_client.stop()
@bot.command()
async def pause(ctx):
    voice_client = get(bot.voice_clients, guild=ctx.guild)
    if voice_client == None:
        await ctx.channel.send("Bot is not connected to vc")
        return
    if voice_client.channel != ctx.author.voice.channel:
        await ctx.channel.send("The bot is currently connected to {0}".format(voice_client.channel))
        return
    voice_client.pause()
    
@bot.command()
async def resume(ctx):
    voice_client = get(bot.voice_clients, guild=ctx.guild)
    if voice_client == None:
        await ctx.channel.send("Bot is not connected to vc")
        return
    if voice_client.channel != ctx.author.voice.channel:
        await ctx.channel.send("The bot is currently connected to {0}".format(voice_client.channel))
        return
    voice_client.resume()
    

@bot.command()
async def leave(ctx):
    del players[ctx.guild.id]
    await ctx.voice_client.disconnect()


@bot.command()
async def queueList(ctx):
    voice_client = get(bot.voice_clients, guild=ctx.guild)

    if voice_client == None or not voice_client.is_connected():
        await ctx.channel.send("Bot is not connected to vc", delete_after=10)
        return

    player = get_player(ctx)
    if player.queue.empty():
        return await ctx.send('There are currently no more queued songs')

    # 1 2 3
    upcoming = list(itertools.islice(player.queue._queue,0,player.queue.qsize()))
    fmt = '\n'.join(f'**`{_["title"]}`**' for _ in upcoming)
    embed = discord.Embed(title=f'Upcoming - Next {len(upcoming)}', description=fmt)
    await ctx.send(embed=embed)

@bot.command()
async def skip(ctx):
    voice_client = get(bot.voice_clients, guild=ctx.guild)

    if voice_client == None or not voice_client.is_connected():
        await ctx.channel.send("Bot is not connected to vc", delete_after=10)
        return

    if voice_client.is_paused():
        pass
    elif not voice_client.is_playing():
        return

    voice_client.stop()
    await ctx.send(f'**`{ctx.author}`**: Skipped the song!')


bot.run('ODcwNzE4NjgwMjQ4NTEyNTI0.GG14Nc.-kkInOyyc0ctqawcezjTnuw1rW4SkJFjv43nL0')