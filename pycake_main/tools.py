def hyphenate_title(title):
	split_title = title.split(' ')
	new_title = []
	for each_word in split_title:
		keep_alpnum = ''.join(filter(str.isalnum, each_word))
		new_title.append(keep_alpnum)
	new_title = '-'.join(new_title)
	new_title = new_title.lower()
	return new_title



#entries = Entry.objects.order_by('date_added')
#for e in entries:
#	splited_title = e.title.split(' ')
#	new_title_list = []
#	
#	for title_word in splited_title:
#		alphnum_only_word = ''.join(filter(str.isalnum, title_word))
#		new_title_list.append(alphnum_only_word)
#		
#	new_title = '-'.join(new_title_list)
#	e.hyphenated_title = new_title.lower()
#	e.save()
#	print(e.hyphenated_title)
#
#for e in entries:
#	print(e.hyphenated_title)
