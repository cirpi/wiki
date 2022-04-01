from django.http import HttpResponse, HttpResponseRedirect
import secrets
from django.urls import reverse
import markdown2
from . import util
from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entries(request, title):
    file = util.get_entry(f'{title}')
    if not file:
        return render(request, 'encyclopedia/entry_error.html', {'title': title})
    md_file = markdown2.markdown(file)
    return render(request, 'encyclopedia/entry.html', {'entry': md_file, 'title' : title})


def search(request):
    if request.method == 'POST':
        title = request.POST.get('q')
        ne = list(map(lambda x: x.lower(), util.list_entries()))
        if title in ne:
            return HttpResponseRedirect(reverse('entries', kwargs={'title': title}))
        else:
            filtered = []
            for i in util.list_entries():
                if title in i.lower():
                    filtered.append(i)
    return render(request, 'encyclopedia/search.html', {'entries': filtered}) if filtered else render(request, 'encyclopedia/search.html')



def random(request):
    title = secrets.choice(util.list_entries())
    return HttpResponseRedirect(reverse('entries', kwargs={'title': title}))


def new_entry(request):
    if request.method == 'POST':
        title = request.POST.get('title').capitalize()
        content = request.POST.get('content')
        if not title or not content:
            return render(request, 'encyclopedia/new_entry.html', {'error': 'Title and Content required.'})
        if title in util.list_entries():
            return render(request, 'encyclopedia/new_entry.html', {'error':'Already Exists!'})
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse('entries', kwargs={'title': title}))
        
    else:
        return render(request, 'encyclopedia/new_entry.html')


def edit(request, title):
    if request.method == 'POST':
        content = request.POST.get('content')
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse('entries', kwargs={'title':title}))
    content = util.get_entry(title)
    if not content:
        return render(request, 'encyclopedia/notfound.html', {'page':title})
    
    return render(request, 'encyclopedia/edit.html', {'title': title, 'content': content})