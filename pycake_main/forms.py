from django import forms

from .models import Topic, Entry

class TopicForm(forms.ModelForm):
	class Meta:
		model = Topic
		fields = ['name', 'description']
		labels = {'name': 'Topic Name', 'description':'Description'}

class EntryForm(forms.ModelForm):
	class Meta:
		model = Entry
		fields = ['title', 'text']
		labels = {'title': 'Entry Title', 'text':'Entry Content'}
		widgets = {'text': forms.Textarea(attrs={'cols':500})}
