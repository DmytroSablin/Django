from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm
# Create your views here.
def index(request):
    return render(request, 'learning_logs/index.html', {})

@login_required
def topics(request):
    topics = Topic.objects.order_by('-date_added').filter(owner=request.user)
    context = {
        'topics': topics
    }

    return render(request, 'learning_logs/topics.html', context)
@login_required
def topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    check_topic_owner(request, topic)
    
    entries = topic.entry_set.all()
    context = {
        'topic': topic,
        'entries': entries
    }
    
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Add a new topic.

    Args:
        request (_type_): _description_
    """
    if request.method != 'POST':
        #Жодних данних не відправлено; створити порожню форму.
        form = TopicForm()
    else:
        #відправленний POST; обробити дані.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')
        
    #Показати порожню або недійсну форму.
    context = {
        'form': form
    }
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Add a new entry for a particular topic.

    Args:
        request (_type_): _description_
        topic_id (_type_): _description_
    """
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        #Жодних данних не надіслано; створти порожню форму.
        form = EntryForm()
    else:
        #Отримані дані у POST-запиті; обробити дані.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    #Показати порожню або недійсну форму.
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)    

@login_required
def edit_entry(request, entry_id):
    """Edit an exsiting entry.

    Args:
        request (_type_): _description_
        entry_id (_type_): _description_
    """
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    
    check_topic_owner(request, topic)

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    
    context= {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

def check_topic_owner(request, topic):
    if topic.owner != request.user:
        raise Http404
