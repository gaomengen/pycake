from django import forms

from .models import Topic, Subject, Entry

class TopicForm(forms.ModelForm):
	class Meta:
		model = Topic
		fields = ['name', 'description']
		labels = {'name': 'Topic Name', 'description':'Description'}

class SubjectForm(forms.ModelForm):
	class Meta:
		model = Subject
		fields = ['name', 'topic']
		labels = {'name':'Subject Name', 'topic':'Subject Topic'}

class EntryForm(forms.ModelForm):
	class Meta:
		model = Entry
		fields = ['title', 'subject', 'text']
		labels = {'title': 'Entry Title', 'subject':'Entry Subject', 'text':'Entry Content'}
		widgets = {'text': forms.Textarea(attrs={'cols':500})}
