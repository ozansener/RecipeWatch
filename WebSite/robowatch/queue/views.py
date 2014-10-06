from django.shortcuts import render,get_object_or_404

from django.http import HttpResponse
from django.template import RequestContext, loader

from recipe.models  import RecipeQuery,Video,QueueElem
from django.utils import timezone
from django.core.exceptions import MultipleObjectsReturned,ObjectDoesNotExist

def index(request):
    QMs = QueueElem.objects.all()
    qLs = [q.v.link for q in QMs]
    template = loader.get_template('queue/videos.html')
    context = RequestContext(request,{'videos':qLs})
    return HttpResponse(template.render(context))


