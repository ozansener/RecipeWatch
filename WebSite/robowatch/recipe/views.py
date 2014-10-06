from django.http import HttpResponse
from django.template import RequestContext, loader

from recipe.models import Video


from oauth2client.tools import argparser
from apiclient.discovery import build


DEVELOPER_KEY = "AIzaSyBDgwtalxdPqZnNOHpoaV6wV50AW75-mUk"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(keywords,maxr):
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

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the poll index.")

def search(request,pid):
    return HttpResponse("Hello, world. You're at the poll index."+pid)

def detail(request,pid):
    vid_list = Video.objects.all()
    print vid_list
    template = loader.get_template('recipe/index.html')
    context = RequestContext(request,{'vid_list':vid_list,})
    #A = youtube_search(pid,10)
    #for i in range(len(A)):
    #    A[i] = 'https://www.youtube.com/watch?v='+A[i]
    return HttpResponse(template.render(context))
