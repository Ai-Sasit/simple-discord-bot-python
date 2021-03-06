from discord.ext import commands as com
import discord as dis
from func import *

client = com.AutoShardedBot(command_prefix= "!")
Token_ID = 'YOUR_DISCORD_TOKEN_ID'

@client.event
async def on_ready():
  print(f"Connected to Discord as {client.user.name}. ")
  await client.change_presence(activity = dis.Activity(type = dis.ActivityType.listening, name = "No Music"))

@client.command(aliases=['Play', 'P', 'p', 'play'])
async def Youtube(ctx, *text):
  channel = ctx.author.voice.channel
  if ctx.voice_client is None:
    try:
      await channel.connect()
      print(f"[Log] {checktime()} - Joining to {channel}.")
    except:
      conn_err = dis.Embed(color=0x00ff9d)
      conn_err.add_field(name='Error Detected',value=f"Couldn't connect to {channel}", inline=False)
      await ctx.send(embed=conn_err)
      print(f"[Log] {checktime()} - Error Detected | Couldn't connect to {channel}")
  if ctx.voice_client.is_playing() is False:
    np_name = Title = PyTube(" ".join(text))
    print(f"[Log] {checktime()} - Playing Youtube | {np_name}")
  else:
    Queue_Title = AddTubeList(" ".join(text))
    Show_Adding = dis.Embed(color=0x00ff9d)
    Show_Adding.add_field(name='Adding to queue ...',value=Queue_Title, inline=False)
    await ctx.send(embed=Show_Adding)
    print(f"[Log] {checktime()} - Adding Youtube | {Queue_Title}")
    return None
  Show_Playing = dis.Embed(color=dis.Color.dark_green())
  Show_Playing.add_field(name="Start Playing ...", value=Title, inline=False)
  await ctx.send(embed=Show_Playing)
  ctx.voice_client.play(dis.FFmpegPCMAudio("$music_temp.mp4"), after=lambda e: PlayQueue(ctx,dis))

@client.command(aliases=['view', 'pro'])
async def Profile(ctx, member: dis.Member):
  Author = f"{ctx.author.name}#{ctx.author.discriminator}"
  print(f"[Log] {checktime()} - Viewing picture profile of {member} by {Author}")
  Show_Profile = dis.Embed(title=f"{member} Profile Picture",url=f'{member.avatar_url}', color=dis.Color.dark_gold())
  Show_Profile.set_image(url=f'{member.avatar_url}')
  Show_Profile.set_footer(text=f"Request by {Author}")
  await ctx.send(embed=Show_Profile)

@client.command()
async def stop(ctx):
  try:
    ctx.voice_client.pause()
    print(f"[Log] {checktime()} - Stopping Youtube | {np_name}")
    await ctx.send(":white_check_mark: Music is Paused!")
  except:
    await ctx.send(":warning: Somethings is Wrong!")

@client.command(aliases=["re"])
async def resume(ctx):
  try:
    ctx.voice_client.resume()
    print(f"[Log] {checktime()} - Resuming Youtube | {np_name}")
    await ctx.send(":white_check_mark: Music is Resumed!")
  except:
    await ctx.send(":warning: Somethings is Wrong!")

@client.command(aliases=['sk'])
async def skip(ctx):
  try:
    ctx.voice_client.stop()
    print(f"[Log] {checktime()} - Skipping Youtube | {np_name}")
    await ctx.send(":white_check_mark: Music is Skipped!")
  except:
    await ctx.send(":warning: Somethings is Wrong!")

@client.command()
async def join(ctx):
  channel = ctx.author.voice.channel
  print(f"[Log] {checktime()} - Joining to {channel}.")
  await ctx.send(":beginner: In your service.")
  await channel.connect()

@client.command(aliases=['dc', 'leave', 'quit', 'exit'])
async def Disconnect(ctx):
  print(f"[Log] {checktime()} - Disconnect from {ctx.author.voice.channel}.")
  await ctx.voice_client.disconnect()

@client.command(aliases=['Q', 'q', 'qu'])
async def Queue(ctx):
  print(f"[Log] {checktime()} - Check queue list.")
  if(len(TubeList) == 0):
    await ctx.send(":package: Queue is empty!")
  else:
    Show_Queue = dis.Embed(color=0x00ff9d)
    Show_Queue.add_field(name="In Queue.", value='\n'.join(NameList), inline=False)
    await ctx.send(embed=Show_Queue)

@client.command()
async def clear(ctx):
  print(f"[Log] {checktime()} - Clearing queue list.")
  if(len(TubeList) == 0):
    await ctx.send(":warning: Queue is already clear!")
  else:
    TubeList.clear()
    NameList.clear()
    await ctx.send(":broom: Queue is clearing completed!")

@client.command(aliases=['np'])
async def NowPlaying(ctx):
  print(f"[Log] {checktime()} - Check now playing | {np_name}")
  Show_NP = dis.Embed(color=0xffd333)
  Show_NP.add_field(name="Current Playing ...", value=np_name, inline=False)
  await ctx.send(embed=Show_NP)

@client.command(aliases=["rq"])
async def removequeue(ctx, index:int):
  print(f"[Log] {checktime()} - Remove queue list | {NameList[index-1]}")
  Remove = dis.Embed(color=0xff0066)
  Remove.add_field(name="Remove queue! ", value=NameList.pop(index-1), inline=False)
  TubeList.pop(index-1)
  await ctx.send(embed=Remove)

@client.command()
async def ping(ctx):
  print(f"[Log] {checktime()} - request check ping.")
  await ctx.send('Pong! {0} ms.'.format(round(client.latency, 1)))

@client.command(aliases=['CV',"cv"])
async def checkCovid(ctx, options = 'overall'):
  if options == 'overall':
    print(f"[Log] {checktime()} - request covid report overall.")
    CC = dis.Embed(color=0xfff700, title=f"Covid-19 Status In Thailand | {nowDate()}", url="https://covid19.workpointnews.com/")
    CC.set_thumbnail(url="https://assets.website-files.com/5d9ba0eb5f6edb77992a99d0/5e6f353a0f8bc38b8bbcc052_iconfinder_29-Doctor_5929215.png")
    CC.add_field(name="???????????????????????? :sneezing_face:", value="{:,}".format(cth["todayCases"]))
    CC.add_field(name="???????????????????????? :skull:", value="{:,}".format(cth["todayDeaths"]))
    CC.add_field(name="???????????????????????? :star_struck:", value="{:,}".format(cth["todayRecovered"]))
    CC.add_field(name="???????????????????????????????????? :mask:", value="{:,}".format(cth["cases"]))
    CC.add_field(name="????????????????????? :skull_crossbones:", value="{:,}".format(cth["deaths"]))
    CC.add_field(name="????????????????????? :partying_face:", value="{:,}".format(cth["recovered"]))
    CC.add_field(name="??????????????????????????????????????????????????????????????? :thermometer_face:", value="{:,}".format(cth["active"]))
    CC.add_field(name="???????????????????????????????????? :face_vomiting:", value="{:,}".format(cth["critical"]))
    CC.add_field(name="??????????????????????????????????????? :syringe:", value=nowVaccine())
    CC.add_field(name="?????????????????????????????????????????? :busts_in_silhouette:", value="{:,}".format(cth['population']))
    CC.set_footer(text="Base on disease.sh | Create by Ai Sasit")
    await ctx.send(embed=CC)
  else:
    print(f"[Log] {checktime()} - request covid report {options}.")
    mop = requests.get('https://covid19.ddc.moph.go.th/api/Cases/today-cases-by-provinces').json()
    for i in mop:
      if i['province'] == options:
        thp = dis.Embed(color=0xfff700, title=f"?????????????????????????????????????????????????????????????????? {options}")
        thp.set_thumbnail(url="https://assets.website-files.com/5d9ba0eb5f6edb77992a99d0/5e6f353a0f8bc38b8bbcc052_iconfinder_29-Doctor_5929215.png")
        thp.add_field(name="???????????????????????? :sneezing_face:", value="{:,}".format(i["new_case"]))
        thp.add_field(name="???????????????????????????????????? :mask:", value="{:,}".format(i["total_case"]))
        thp.add_field(name="???????????????????????? :skull:", value="{:,}".format(i["new_death"]))
        thp.add_field(name="????????????????????? :skull_crossbones:", value="{:,}".format(i["total_death"]))
        thp.add_field(name="?????????????????????????????? :alarm_clock:", value=f"{i['update_date']}")
        thp.set_footer(text="Base on covid19.ddc.moph.go.th | Create by Ai Sasit")
        await ctx.send(embed=thp)
        break


client.run(Token_ID)
