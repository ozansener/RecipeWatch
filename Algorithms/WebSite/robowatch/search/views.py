from django.shortcuts import render,get_object_or_404

from django.http import HttpResponse
from django.template import RequestContext, loader

from recipe.models  import RecipeQuery,Video,QueueElem
from django.utils import timezone
from django.core.exceptions import MultipleObjectsReturned,ObjectDoesNotExist

def index(request):
        # Create a search object somewhere
    template = loader.get_template('search/index.html')
    context = RequestContext(request) #,{'vid_list':vid_list,})
    return HttpResponse(template.render(context))

def search_k(request,pid):
    try:
        q = RecipeQuery.objects.get(query=pid)
    except ObjectDoesNotExist:
        q = RecipeQuery(query=pid,pub_date=timezone.now())
        q.save()
    except MultipleObjectsReturned:
        print 'DB is messed up'

    videos=q.youtube_search(pid,25)

    for i in videos:
        try:
            v = Video.objects.get(q=q,link=i)
        except ObjectDoesNotExist:
            v = Video(q=q,link=i)
            v.save()
    print videos
    template = loader.get_template('search/videos.html')
    context = RequestContext(request,{'videos':videos,'pid':pid})
    return HttpResponse(template.render(context))


def search(request):
    keys = request.POST['keys']
    keys = keys.encode('ascii',errors='ignore')
    keys = '+'.join(keys.split())
    print keys
    return search_k(request,keys)


def searchS(request):
    keys = request.POST['q']
    qu = RecipeQuery.objects.get(query=keys)

    Vids = Video.objects.all().filter(q=qu)
    vL = []
    for v in Vids:
        if str(v.link) in request.POST:
            vL.append(v.link)

    QMs = QueueElem.objects.all()
    qLs = [q.v.link for q in QMs]
    for v in vL:
        if not v in qLs:
            for vv in Vids:
                if vv.link==v:
                    q=QueueElem(v=vv)
                    q.save()


    template = loader.get_template('search/videos.html')
    context = RequestContext(request,{'videos':vL,'pid':keys})
    return HttpResponse(template.render(context))


