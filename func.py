import glob as G
from pytube import YouTube
import requests, datetime, pytz
from youtube_search import YoutubeSearch
from os import remove, rename

TubeList, NameList = [], []
cth = requests.get('https://disease.sh/v3/covid-19/countries/th').json()
vcc = requests.get('https://disease.sh/v3/covid-19/vaccine/coverage/countries?lastdays=1').json()
tz = pytz.timezone('Asia/Bangkok')
now1 = datetime.datetime.now(tz)

def PyTube(search):
  if ("$music_temp.mp4" in G.glob("*.mp4")): remove("$music_temp.mp4")
  if ("www" in search or "http" in search): 
    result = YouTube(search)
  else:
    results = YoutubeSearch(search, max_results=1).to_dict()
    result = YouTube("www.youtube.com" + dict(results[0])["url_suffix"])
  m4a = result.streams.filter(type="audio").first()
  m4a.download()
  name = G.glob("*.mp4")[0]
  rename(name, "$music_temp.mp4")
  return result.title

def AddTubeList(Search):
  if ("www" in Search or "http" in Search): 
    TubeList.append(Search)
    NameList.append(YouTube(Search).title)
  else:
    Y = YoutubeSearch(Search, max_results=1).to_dict()
    TubeList.append("www.youtube.com" + dict(Y[0])["url_suffix"])
    NameList.append(dict(Y[0])["title"])
  return NameList[-1]

def PlayQueue(ctx, dis):
  global np_name 
  print(f"[Log] Music was ended.")
  if ("$music_temp.mp4" in G.glob("*.mp4")): remove("$music_temp.mp4")
  if len(TubeList) != 0:
    Inlist = TubeList.pop(0)
    NameList.pop(0)
  else:
    np_name = "Nothing is playing."
    return None
  result = YouTube(Inlist)
  np_name = result.title
  m4a = result.streams.filter(type="audio").first()
  m4a.download()
  name = G.glob("*.mp4")[0]
  rename(name, "$music_temp.mp4")
  ctx.voice_client.play(dis.FFmpegPCMAudio("$music_temp.mp4"), after=lambda e: PlayQueue(ctx, dis))

def nowDate():
    month_name = 'x มกราคม กุมภาพันธ์ มีนาคม เมษายน พฤษภาคม มิถุนายน กรกฎาคม สิงหาคม กันยายน ตุลาคม พฤศจิกายน ธันวาคม'.split()[now1.month]
    thai_year = now1.year + 543
    return "%d-%s-%d"%(now1.day, month_name, thai_year)

def nowVaccine():
  for i in vcc:
    if i["country"] == "Thailand":
      date = now1.strftime("%m/%d/%y").split("/")
      date = list(map(str, date))
      try:
        return "{:,}".format(i["timeline"]["/".join(date)])
      except:
        date[1] = str(int(date[1]) - 1)
        try:
          return "{:,}".format(i["timeline"]["/".join(date)])
        except: 
          return '-'
