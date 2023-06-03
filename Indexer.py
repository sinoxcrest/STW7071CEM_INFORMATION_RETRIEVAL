import nltk as nltk
import ujson
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# Pre-processing data before indexing
with open('OutputData.json', 'r') as doc:
    scraper_output_data = doc.read()

pubName = []
pubURL = []
pubCUAuthor = []
pubDate = []
data_dict = ujson.loads(scraper_output_data)
array_length = len(data_dict)
print(array_length)

# Seperate name, url, date, author in different file
for item in data_dict:
    pubName.append(item["name"])
    pubURL.append(item["link"])
    pubCUAuthor.append(item["author"])
    pubDate.append(item["date"])
with open('name.json', 'w') as f:
    ujson.dump(pubName, f)
with open('link.json', 'w') as f:
    ujson.dump(pubURL, f)
with open('author.json', 'w') as f:
    ujson.dump(pubCUAuthor, f)
with open('date.json', 'w') as f:
    ujson.dump(pubDate, f)


# Downloading libraries to use its methods
nltk.download('stopwords')
nltk.download('punkt')

# Open a file with publication names in read mode
with open('name.json', 'r') as f:
    publication = f.read()

# Load JSON File
pubName = ujson.loads(publication)

# Predefined stopwords in nltk are used
stop_words = stopwords.words('english')
stemmer = PorterStemmer()
pub_list_first_stem = []
pub_list = []
pub_list_wo_sc = []
print(len(pubName))

for file in pubName:
    # Splitting strings to tokens(words)
    words = word_tokenize(file)
    stem_word = ""
    for i in words:
        if i.lower() not in stop_words:
            stem_word += stemmer.stem(i) + " "
    pub_list_first_stem.append(stem_word)
    pub_list.append(file)

# Removing all below characters
special_characters = '''!()-—[]{};:'"\, <>./?@#$%^&*_~0123456789+=’‘'''
for file in pub_list:
    word_wo_sc = ""
    if len(file.split()) ==1 : pub_list_wo_sc.append(file)
    else:
        for a in file:
            if a in special_characters:
                word_wo_sc += ' '
            else:
                word_wo_sc += a
        # print(word_wo_sc)
        pub_list_wo_sc.append(word_wo_sc)

# Stemming Process
pub_list_stem_wo_sw = []
for name in pub_list_wo_sc:
    words = word_tokenize(name)
    stem_word = ""
    for a in words:
        if a.lower() not in stop_words:
            stem_word += stemmer.stem(a) + ' '
    pub_list_stem_wo_sw.append(stem_word.lower())

data_dict = {}

# Indexing process
for a in range(len(pub_list_stem_wo_sw)):
    for b in pub_list_stem_wo_sw[a].split():
        if b not in data_dict:
             data_dict[b] = [a]
        else:
            data_dict[b].append(a)


print(len(pub_list_wo_sc))
print(len(pub_list_stem_wo_sw))
print(len(pub_list_first_stem))
print(len(pub_list))

# with open('publication_list.json', 'w') as f:
#     ujson.dump(pub_list, f)

with open('listStemmed.json', 'w') as f:
    ujson.dump(pub_list_first_stem, f)

with open('indexedDictionary.json', 'w') as f:
    ujson.dump(data_dict, f)

# Open a file with publication names in read mode
with open('author.json', 'r') as f:
    authors = f.read()

# Load JSON File
pubCUAuthor = ujson.loads(authors)

# Predefined stopwords in nltk are used
stop_words2 = stopwords.words('english')
stemmer2 = PorterStemmer()
pub_list_first_stem2 = []
pub_list2 = []
pub_list_wo_sc2 = []
print(len(pubCUAuthor))

for file in pubCUAuthor:
    # Splitting strings to tokens(words)
    words = word_tokenize(file)
    stem_word = ""
    for i in words:
        if i.lower() not in stop_words:
            stem_word += stemmer2.stem(i) + " "
    pub_list_first_stem2.append(stem_word)
    pub_list2.append(file)

# Removing all below characters
special_characters = '''!()-—[]{};:'"\, <>./?@#$%^&*_~0123456789+=’‘'''
for file in pub_list2:
    word_wo_sc = ""
    if len(file.split()) ==1 : pub_list_wo_sc2.append(file)
    else:
        for a in file:
            if a in special_characters:
                word_wo_sc += ' '
            else:
                word_wo_sc += a
        # print(word_wo_sc)
        pub_list_wo_sc2.append(word_wo_sc)

# Stemming Process
pub_list_stem_wo_sw2 = []
for name in pub_list_wo_sc2:
    words = word_tokenize(name)
    stem_word = ""
    for a in words:
        if a.lower() not in stop_words:
            stem_word += stemmer2.stem(a) + ' '
    pub_list_stem_wo_sw2.append(stem_word.lower())

data_dict2 = {}

# Indexing process
for a in range(len(pub_list_stem_wo_sw2)):
    for b in pub_list_stem_wo_sw2[a].split():
        if b not in data_dict2:
             data_dict2[b] = [a]
        else:
            data_dict2[b].append(a)


print(len(pub_list_wo_sc2))
print(len(pub_list_stem_wo_sw2))
print(len(pub_list_first_stem2))
print(len(pub_list2))

# with open('publication_list.json', 'w') as f:
#     ujson.dump(pub_list, f)

with open('listStemmed2.json', 'w') as f:
    ujson.dump(pub_list_first_stem2, f)

with open('indexedDictionary2.json', 'w') as f:
    ujson.dump(data_dict2, f)