"""This is another urls.py different than the one under pycake_main/, 
which redirects the domain to the namespace pycake_main. 
Then with the help of this urls.py, 
Djando knows how to parse the url and leads to the pages rendered in views."""

from django.urls import path, re_path
from . import views

app_name = 'pycake_main'
urlpatterns = [



        #Home page displays all topics.
	path('', views.index, name='index'),
	#re_path(r'^(?P<topic_name>\w+)/$', views.topic, name='topic'),
        path('topics/', views.topics, name='topics'),

        #Show individual topic by topic id
        #path('topics/<topic_id>/', views.topic, name='topic'),

	#Show individual topic by topic name
	path('t/<hyphenated_topic>/', views.topic, name='show_topic'),

	#Show subject
	path('subject/<hyphenated_name>/', views.subject, name='show_subject'),

	#Show individual entry by entry hyphnated title
	path('article/<entry_hyphenated_title>/', views.show_entry, name='show_entry'),

        #Page for adding a new topic
        path('new_topic/', views.new_topic, name='new_topic'),

	#Page for adding a new subject
	path('new_subject/', views.new_subject, name='new_subject'),

	#Edit topic
	path('edit_topic/<topic_name>', views.edit_topic, name='edit_topic'),

	#Delete a topic
	path('delete_topic/<topic_name>', views.delete_topic, name='delete_topic'),

        #Page for adding a new entry
        path('new_entry/<topic_name>/', views.new_entry, name='new_entry'),

        #Page for editting an entry
        path('edit_entry/<entry_id>', views.edit_entry, name='edit_entry'),

	#Pattern for deleting an entry
	path('delete_entry/<entry_id>', views.delete_entry, name='delete_entry'),
]

