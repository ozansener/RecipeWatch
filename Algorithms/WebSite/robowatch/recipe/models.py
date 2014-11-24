from django.db import models



# Create your models here.
class RecipeQuery(models.Model):
    query = models.CharField(max_length=1000,unique=True)
    pub_date = models.DateTimeField('date requested')
    def __unicode__(self):
        return self.query
    def wikihow_search(self,keywords):
        from django.utils import simplejson
        import urllib2
        import re
        search_url = 'http://howtodo.isi.edu/api.php?todo='+'+'.join(keywords)

        raw = urllib2.urlopen(search_url)
        js = simplejson.load(raw)
     
        jso = []
        for rec in js['interpretations']:
            nam = re.sub('http://www.wikihow.com/', '',rec['source'])
            nam = re.sub('-','_',nam)
            
            steps = []
            for s in rec['steps']:
                st = re.sub('[\{\[<]{1,2}[^\{\]]*[\}\]>]{1,2}','',s['fulltext']).encode('utf-8')
                st = st.strip(' #*')
                steps.append(st)
            jso.append([nam,rec['rank'],steps])    
        return jso



    
    def youtube_search(self,keywords,maxr):
        from oauth2client.tools import argparser
        from apiclient.discovery import build

        DEVELOPER_KEY = "AIzaSyBDgwtalxdPqZnNOHpoaV6wV50AW75-mUk"
        YOUTUBE_API_SERVICE_NAME = "youtube"
        YOUTUBE_API_VERSION = "v3"

        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
          developerKey=DEVELOPER_KEY)

        # Call the search.list method to retrieve results matching the specified
        # query term.
        search_response = youtube.search().list(
          q=keywords,
          part="id,snippet",
          maxResults=maxr
        ).execute()

        vid_ids = []
        videos = []
        channels = []
        playlists = []

        # Add each result to the appropriate list, and then display the lists of
        # matching videos, channels, and playlists.
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                           search_result["id"]["videoId"]))
                vid_ids.append(search_result["id"]["videoId"])
            elif search_result["id"]["kind"] == "youtube#channel":
                channels.append("%s (%s)" % (search_result["snippet"]["title"],
                                             search_result["id"]["channelId"]))
            elif search_result["id"]["kind"] == "youtube#playlist":
                playlists.append("%s (%s)" % (search_result["snippet"]["title"],
                                              search_result["id"]["playlistId"]))

        #print "Videos:\n", "\n".join(videos), "\n"
        #print "Channels:\n", "\n".join(channels), "\n"
        #print "Playlists:\n", "\n".join(playlists), "\n"
        return vid_ids


class Video(models.Model):
    q = models.ForeignKey(RecipeQuery)
    link = models.CharField(max_length=200)
    def __unicode__(self):
        return self.link
class Text(models.Model):
    q = models.ForeignKey(RecipeQuery)
    js = models.CharField(max_length=200)
    def __unicode__(self):
        return self.js

class QueueElem(models.Model):
    v = models.ForeignKey(Video)
    def __unicode__(self):
        return self.v.link
