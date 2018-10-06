import pdb

from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Subject, Entry
from .forms import TopicForm, SubjectForm, EntryForm
from .tools import hyphenate_title

# Get topics

# Create your views here.
def index(request):
	"""The home page for Learning Log."""
	topics = Topic.objects.order_by('date_added')
	context = {'topics': topics}
	return render(request, 'pycake_main/index.html', context)

def topics(request):
	"""Show all topics."""
	topics = Topic.objects.order_by('date_added')
	context = {'topics': topics}
	return render(request, 'pycake_main/topics.html', context)

#@login_required
def topic(request, hyphenated_topic):
	"""Show a single topic and all its entries."""
	topics = Topic.objects.order_by('date_added')
	topic = Topic.objects.get(hyphenated_topic=hyphenated_topic)
	subjects = Subject.objects.all() 
	#Make sure the topic belongs to the current user.
	#if topic.owner != request.user:
	#	raise Http404

	entries = topic.entry_set.order_by('-date_added')
	context = {'topics': topics, 'topic': topic, 'subjects': subjects, 'entries': entries}
	return render(request, 'pycake_main/topic.html', context)

#@login_required
def subject(request, hyphenated_name):
	"""Show single subject under certain topic."""
	topics = Topic.objects.order_by('date_added')
	topic = Subject.objects.get(hyphenated_name=hyphenated_name)
	entries_of_subject = Subject.objects.get(hyphenated_name=hyphenated_name)
	subjects = Subject.objects.all()
	
	entries = entries_of_subject.entry_set.order_by('-date_added')
	context = {'topics':topics, 'topic':topic, 'subjects':subjects, 'entries':entries}
	return render(request, 'pycake_main/topic.html', context)
		

@login_required
def new_topic(request):
	"""Add a new topic."""
	if request.method != 'POST':
		#No data submitted; create a blank form.
		form = TopicForm()
	else:
		#POST data submitted; process data.
		form = TopicForm(data=request.POST)
		if form.is_valid():
			new_topic = form.save(commit=False)
			if Topic.objects.filter(name=new_topic.name).exists():
				return HttpResponseRedirect(reverse('pycake_main:index'))
			else:
				new_topic.owner = request.user
				new_topic.hyphenated_topic = hyphenate_title(form.cleaned_data['name'])
				new_topic.save()
				return HttpResponseRedirect(reverse('pycake_main:topics'))

	context = {'form': form}
	return render(request, 'pycake_main/new_topic.html', context)

#Add new subject function
@login_required
def new_subject(request):
	"""Add a new subject"""
	if request.method != 'POST':
		#No data submitted; create a blank form.
		form = SubjectForm()
	else:
		#POST data submitted; process data.
		form = SubjectForm(data=request.POST)
		if form.is_valid():
			new_subject = form.save(commit=False)
			if Subject.objects.filter(name=new_subject.name).exists():
				return HttpResponseRedirect(reverse('pycake_main:index'))
			else:
				new_subject.owner = request.user
				new_subject.hyphenated_name = hyphenate_title(form.cleaned_data['name']) 
				new_subject.save()
				return HttpResponseRedirect(reverse('pycake_main:topics'))
	context = {'form':form}
	return render(request, 'pycake_main/new_subject.html', context)

@login_required
def edit_topic(request, topic_name):
	"""Edit a topic"""
	#Get all topics for nav-bar
	topics = Topic.objects.order_by('date_added')
	#Check if the topic exists
	if Topic.objects.filter(name=topic_name).exists():
		#Get target topic
		topic_to_edit = Topic.objects.get(name=topic_name)
		#Check whether the user has the right to edit it
		if topic_to_edit.owner == request.user:
			if request.method != 'POST':
				#Initial request; pre-fill form with the current topic
				form = TopicForm(instance=topic_to_edit)
			else:	#Post data submitted; process data
				form = TopicForm(instance=topic_to_edit, data=request.POST)
				if form.is_valid():
					edit_topic = form.save(commit=False)
					edit_topic.hyphenated_topic = hyphenate_title(form.cleaned_data['name'])
					edit_topic.save()
					return HttpResponseRedirect(reverse('pycake_main:topics'))
	context = {'topics': topics, 'form': form, 'topic': topic_name}
	return render(request, 'pycake_main/edit_topic.html', context)

@login_required
def delete_topic(request, topic_name):
	"""Delete a topic."""
	#Check whether the topic name exists.
	if Topic.objects.filter(name=topic_name).exists():
		#Get target topic..
		target_topic = Topic.objects.filter(name=topic_name)

		#Check whether the user has the right to delete topic.
		if target_topic[0].owner == request.user:
			target_topic.delete()
			return HttpResponseRedirect(reverse('pycake_main:topics'))
		else:
			error_msg = 'You cannot delete a topic you do not own.'
		
	else:
		error_msg = 'Topic does not exist.'	
		
	context = {'error_msg': error_msg}
	return render(request, 'pycake_main/error.html', context)	

@login_required
def new_entry(request, topic_name):
	"""Add a new entry under a topic."""
	topic = Topic.objects.get(name=topic_name)	
	
	if request.method != 'POST':
		#No data submitted; create a blank form.
		form = EntryForm()
	else:
		# POST data submitted; process data.
		form = EntryForm(data=request.POST)
		if form.is_valid():
			new_entry = form.save(commit=False)
			new_entry.hyphenated_title = hyphenate_title(form.cleaned_data['title'])
			new_entry.topic = topic
			new_entry.owner = request.user
			new_entry.save()
			return HttpResponseRedirect(reverse('pycake_main:show_topic', args=[topic_name]))

	topics = Topic.objects.order_by('date_added')

	context = {'topics': topics, 'topic': topic, 'form': form}
	return render(request, 'pycake_main/new_entry.html', context)

@login_required
def delete_entry(request, entry_id):
	"""Delete an entry"""
	#Check if the entry exists
	if Entry.objects.filter(id=entry_id).exists:
		#Get the entry
		target_entry = Entry.objects.filter(id=entry_id)
		#Check if the user owns the entry
		if target_entry[0].owner == request.user:
			topic_name = target_entry[0].topic
			target_entry.delete()
			return HttpResponseRedirect(reverse('pycake_main:show_topic', args=[topic_name]))
		else:
			error_msg = 'You cannot delete an entry you do not own.'
	else:
		error_msg = 'Entry does not exist.'
	context = {'error_msg':error_msg}
	return render(request, 'pycake_main/error.html', context)


#@login_required
def show_entry(request, entry_hyphenated_title):
	"""Show single entry"""
	topics = Topic.objects.order_by('date_added')
	entry = Entry.objects.get(hyphenated_title=entry_hyphenated_title)
	
	context = {'topics': topics, 'entry':entry}
	return render(request, 'pycake_main/show_entry.html', context)
		

@login_required
def edit_entry(request, entry_id):
	"""Edit an existing entry."""
	entry = Entry.objects.get(id=entry_id)
	topic = entry.topic
	if entry.owner != request.user:
		raise Http404

	if request.method != 'POST':
		#Initial request; pre-fill form with the current entry.
		form = EntryForm(instance=entry)
	else:
		#POST data submitted; process data.
		form = EntryForm(instance=entry, data=request.POST)
		if form.is_valid():
			edit_entry = form.save(commit=False)
			edit_entry.hyphenated_title = hyphenate_title(form.cleaned_data['title'])
			edit_entry.topic = topic
			edit_entry.owner = request.user
			edit_entry.save()

			return HttpResponseRedirect(reverse('pycake_main:show_topic', args=[topic.hyphenated_topic]))

	topics = Topic.objects.order_by('date_added')
	context = {'topics': topics, 'entry': entry, 'topic': topic, 'form': form}
	return render(request, 'pycake_main/edit_entry.html', context)
