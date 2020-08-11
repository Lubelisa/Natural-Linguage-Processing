from nltk.tokenize import word_tokenize
from unidecode import unidecode

###############################################################################
# 					FUNCTION TO FIND CHILDRENS OF THE NODE
###############################################################################
def find_children(parent, dict_id_parent, queue):
	for k in dict_id_parent:
		if dict_id_parent[k] == parent:
			queue.append(k)

###############################################################################
# 			FUNCTION TO FIND THE RELATION OF THE PARENT OF THE NODE
###############################################################################
def find_parent_relation(k, dict_id_parent, dict_id_relations, root):
	if dict_id_parent[k] == root:
		return 'multinuc'
	elif dict_id_relations[dict_id_parent[k]] != 'span':
		return dict_id_relations[dict_id_parent[k]]
	return find_parent_relation(dict_id_parent[k], dict_id_parent, dict_id_relations, root)

###############################################################################
# 		FUNCTION TO SPLIT THE NUCLEUS AND SATTELITES OF THE SEGMENT
###############################################################################
def determine_sentences(nucleus, satellites, dict_relations, dict_id_parent, dict_id_segments, dict_id_relations, root):
	queue = []
	tree_size_ = 0
	find_children(root, dict_id_parent, queue)
	while len(queue) > 0:
		k = queue.pop(0)
		# print('k = '+k)
		# Se o id for um grupo ou a relacao dele com o parent for span, encontrar os filhos desse id e procura a relacao do pai
		if dict_id_segments[k] == 'group' or dict_id_relations[k] == 'span':
			find_children(k, dict_id_parent, queue)
			tree_size_ += 1
			if dict_id_relations[k] == 'span':
				dict_id_relations[k] = find_parent_relation(k, dict_id_parent, dict_id_relations, root)
		
		# Se for um segmento, devo add a um dos sets
		if dict_id_segments[k] != 'group':
			if dict_relations[dict_id_relations[k]] == 'rst':
				satellites.add(dict_id_segments[k].lower())
			else:
				nucleus.add(dict_id_segments[k].lower())

###############################################################################
# 	DETERMINING THE MAX NUMBER OF CONNECTION BETWEEN A NODE AND THE ROOT
###############################################################################	
def determining_the_height_of_the_tree(set_segments, dict_id_parent):
	maxlenght = 0

	for Id in set_segments:
		sz = 0
		while 'root' != dict_id_parent[Id]:
			Id = dict_id_parent[Id]
			sz += 1
			pass
		maxlenght = max(maxlenght, sz)

	return maxlenght

###############################################################################
# 									MAIN
###############################################################################		

# READING ALL THE RST RELATIONS
lines_relations = open('all_relations.txt', 'r').readlines()
lines_relations = [lr.replace('\n', '') for lr in lines_relations]
dict_relations = dict()
for lr in lines_relations:
	lr_sp = lr.split(' ')
	dict_relations[lr_sp[0]] = lr_sp[1]

# READING ALL THE CORPUS OF BOOK REVIEWS SEGMENTS
# This file is the book reviews corpus sentences in plain text
txt_frases = open('BookReviews.txt', 'r').readlines()
# txt_frases = [unidecode(txtl.decode("utf-8")) for txtl in txt_frases]
txt_frases = [txtl.replace("\n", "") for txtl in txt_frases]
txt_frases = [txtl.replace("\r", "") for txtl in txt_frases]
txt_frases = [txtl.lower() for txtl in txt_frases]

frases_relacoes = open('frases_relacoes.csv', 'w')
frases_relacoes.write("adverbintensewords,adverbnegativewords,pontuationexclamation,pontuationinterrogation,nucleussubjwordsproportion,satelitessubjwordsproportion,")
frases_relacoes.write("relationmotivation,relationinterpretation,relationantithesis,relationenablement,relationunstatedrelation,relationevidence,relationvolitionalresult,relationrestatement,relationattribution,relationvolitionalcause,relationnonvolitionalresult,relationmeans,relationevaluation,relationconclusion,relationelaboration,relationunless,relationcircumstance,relationexplanation,relationpurpose,relationbackground,relationcondition,relationcomparison,relationsolutionhood,relationsummary,relationpreparation,relationnonvolitionalcause,relationparenthetical,relationconcession,relationjustify,relationunconditional,relationotherwise,relationconjunction,relationsameunit,relationsequence,relationlist,relationjoint,relationrestatementmn,relationdisjunction,relationcontrast,treemaxnconnections\n")

# OBTAINING THE POINTS
points = open("punctuation.txt", "r").readlines()
# points = [unidecode(p.decode("utf-8")) for p in points]
points = [p.replace("\n", "") for p in points]
points = [p.replace("\r", "") for p in points]
points = [p.lower() for p in points]

# SETTING THE EXCLAMATION AND INTERROGATION SIGNALS
exclamation = ('!', '?!')
interrogation = '?'

# OBTAINING THE POSITIVE SENTIMENT WORDS
subpos = open("SentiLexPT_pos.txt", "r").readlines()
# subpos = [unidecode(p.decode("utf-8")) for p in subpos]
subpos = [p.replace("\n", "") for p in subpos]
subpos = [p.replace("\r", "") for p in subpos]
subpos = [p.lower() for p in subpos]

# OBTAINING THE NEGATIVE SENTIMENT WORDS
subneg = open("SentiLexPT_neg.txt", "r").readlines()
# subneg = [unidecode(p.decode("utf-8")) for p in subneg]
subneg = [p.replace("\n", "") for p in subneg]
subneg = [p.replace("\r", "") for p in subneg]
subneg = [p.lower() for p in subneg]

# OBTAINING THE STOPWORDS
# IF YOU WANT TO REMOVE STOPWORDS, YOU UNCOMMENT THIS 5 LINES
# stopwords = open("stopwords.txt", "r").readlines()
# # stopwords = [unidecode(stw.decode("utf-8")) for stw in stopwords]
# stopwords = [stw.replace("\n", "") for stw in stopwords]
# stopwords = [stw.replace("\r", "") for stw in stopwords]
# stopwords = [p.lower() for p in stopwords]

# INTENSITY ADVERBS
advintens = open("adverbios_intensidade.txt", "r").readlines()
# advintens = [unidecode(stw.decode("utf-8")) for stw in advintens]
advintens = [stw.replace("\n", "") for stw in advintens]
advintens = [stw.replace("\r", "") for stw in advintens]
advintens = [p.lower() for p in advintens]

# NEGATION ADVERBS
advneg = open("adverbios_negacao.txt", "r").readlines()
# advneg = [unidecode(stw.decode("utf-8")) for stw in advneg]
advneg = [stw.replace("\n", "") for stw in advneg]
advneg = [stw.replace("\r", "") for stw in advneg]
advneg = [p.lower() for p in advneg]

dict_isthere_relations = dict()

# FOR EACH RST FILE...
for cnt in range(1, 351):
	# print('**********************'+str(cnt)+'***********************')

	set_segments = set()

	tree_size_ = 0

	dict_isthere_relations = dict()
	for lrel in dict_relations.keys():
		dict_isthere_relations[lrel] = 0

	lines = open('frase'+str(cnt)+'.rs3', 'r').readlines()
	# lines = [unidecode(l.decode('utf-8')) for l in lines]
	lines = [l.replace("\n", "") for l in lines]
	lines = [l.replace("\r", "") for l in lines]

	dict_id_segments = dict()
	dict_id_relations = dict()
	dict_id_parent = dict()
	root = '-1'
	for l in lines:
		possegment = l.find('segment id')
		posgroup = l.find('group id')
		if possegment != -1:
			possegment += len('segment id=\"')
			myId = l[possegment:(l.find('\"', possegment, len(l)))]
			set_segments.add(myId)
			posparent = l.find('parent')
			if posparent == -1:
				dict_id_parent[myId] = 'root'
				root = myId
			else:
				posparent += len('parent=\"')
				myParent = l[posparent:(l.find('\"', posparent, len(l)))]
				dict_id_parent[myId] = myParent
			posrel = l.find('relname')
			if posrel != -1:
				posrel += len('relname=\"')
				myRelation = l[posrel:(l.find('\"', posrel, len(l)))]
				dict_id_relations[myId] = myRelation
				if myRelation != 'span':
					dict_isthere_relations[myRelation] = 1
			posrel = l.find('>', posrel, len(l)) + 1
			mySentence = l[posrel:(l.find('<', posrel, len(l)))]
			dict_id_segments[myId] = mySentence
		elif posgroup != -1:
			posgroup += len('group id=\"')
			myId = l[posgroup:(l.find('\"', posgroup, len(l)))]
			# dict_id_segments[myId] = 'group'
			posparent = l.find('parent')
			if posparent == -1:
				dict_id_parent[myId] = 'root'
				root = myId
			else:
				posparent += len('parent=\"')
				myParent = l[posparent:(l.find('\"', posparent, len(l)))]
				dict_id_parent[myId] = myParent
				dict_id_segments[myId] = 'group'
			posrel = l.find('relname')
			if posrel != -1:
				posrel += len('relname=\"')
				myRelation = l[posrel:(l.find('\"', posrel, len(l)))]
				dict_id_relations[myId] = myRelation
				if myRelation != 'span':
					dict_isthere_relations[myRelation] = 1

	dict_relations['multinuc'] = 'multinuc'
	nucleus = set()
	satellites = set()
	determine_sentences(nucleus, satellites, dict_relations, dict_id_parent, dict_id_segments, dict_id_relations, root)

	######################################################
	# Presence of exclamation and/or interrogation marks
	######################################################

	frase = txt_frases[cnt-1]


	exclamation_bool = 0
	interrogation_bool = 0

	adv_intense_words = 0
	adv_neg_words = 0

	for w in exclamation:
		if w in frase:
			exclamation_bool = 1
			frase = frase.replace(w, '')

	if interrogation in frase:
		interrogation_bool = 1
		frase = frase.replace(interrogation, '')

	for p in points:
		frase = frase.replace(p, '')

	# IF YOU WANT TO REMOVE STOPWORDS, YOU UNCOMMENT THIS 2 LINES
	# for stw in stopwords:
	# 	frase = frase.replace(' '+stw+' ', ' ')

	############################################
	# Intensity and negation adverbs proportion
	############################################

	for intense in advintens:
		adv_intense_words += frase.count(intense)
	for neg in advneg:
		adv_neg_words += frase.count(neg)

	frase = frase.replace('  ', ' ')
	lista_size = frase.split(' ')
	lista_size = len(lista_size)

	adv_intense_words = float(adv_intense_words)/float(lista_size)
	adv_neg_words = float(adv_neg_words)/float(lista_size)

	lista_size = adv_intense_words+adv_neg_words

	if lista_size != 0:
		adv_intense_words /= lista_size
		adv_neg_words /= lista_size

	########################################################
	# Subjective words proportion in nucleus and satellites
	########################################################

	for p in points:
		nucleus = [fr.replace(p, '') for fr in nucleus]
		satellites = [fr.replace(p, '') for fr in satellites]
	nucleus = [fr.replace('  ', ' ') for fr in nucleus]
	satellites = [fr.replace('  ', ' ') for fr in satellites]

	subjwords_nuc_proportion = 0.0
	subjwords_sat_proportion = 0.0

	subjword = 0

	for fr in nucleus:
		subjword = 0
		for word in subpos:
			subjword += fr.count(word)
		for word in subneg:
			subjword += fr.count(word)
		# for stp in stopwords:
		# 	fr = fr.replace(stp, '')
		fr = fr.replace('  ', ' ')
		lista_size = fr.split(' ')
		lista_size = len(lista_size)
		subjwords_nuc_proportion += float(subjword)/float(lista_size)

	for fr in satellites:
		subjword = 0
		for word in subpos:
			subjword += fr.count(word)
		for word in subneg:
			subjword += fr.count(word)
		# for stp in stopwords:
		# 	fr = fr.replace(stp, '')
		fr = fr.replace('  ', ' ')
		lista_size = fr.split(' ')
		lista_size = len(lista_size)
		subjwords_sat_proportion += float(subjword)/float(lista_size)

	total_aux = subjwords_sat_proportion + subjwords_nuc_proportion

	if total_aux != 0:
		subjwords_nuc_proportion = subjwords_nuc_proportion/total_aux
		subjwords_sat_proportion = subjwords_sat_proportion/total_aux

	##########################################
	#	Determining the tree height
	##########################################

	maxlenght = determining_the_height_of_the_tree(set_segments, dict_id_parent)

	########################################################
	# 			Building the csv file
	########################################################

	frases_relacoes.write('\"'+str(adv_intense_words)+'\",\"'+str(adv_neg_words)+'\",\"'+str(exclamation_bool)+'\",\"'+str(interrogation_bool)+'\",\"'+str(subjwords_nuc_proportion)+'\",\"'+str(subjwords_sat_proportion)+'\"')

	for k in dict_isthere_relations.keys():
		if k != 'rst' and k != 'span' and k != 'multinuc':
			# print(k)
			frases_relacoes.write(',\"'+str(dict_isthere_relations[k])+'\"')
	frases_relacoes.write(','+str(maxlenght)+'\n')
