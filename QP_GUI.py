from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import ujson

stemmer = PorterStemmer()
stop_words = stopwords.words('english')
tfidf = TfidfVectorizer()

with open('listStemmed.json', 'r') as a:
    pub_list_first_stem = ujson.load(a)
with open('indexedDictionary.json', 'r') as a:
    pub_index = ujson.load(a)
with open('listStemmed2.json', 'r') as a:
    pub_list_first_stem2 = ujson.load(a)
with open('indexedDictionary2.json', 'r') as a:
    pub_index2 = ujson.load(a)
with open('name.json', 'r') as a:
    pub_name = ujson.load(a)
with open('link.json', 'r') as a:
    link = ujson.load(a)
with open('author.json', 'r') as a:
    pub_author = ujson.load(a)
with open('date.json', 'r') as a:
    pub_date = ujson.load(a)


def pub_qp_data(input=None):
    outputData.delete(1.0, END)
    outcome.delete(0, END)
    inputText = inputBar.get()
    abc = {}
    if operator.get() == 2:
        outputData.configure(fg='blue')
        inputText = inputText.lower().split()
        pointer = []
        for token in inputText:
            if len(inputText) < 2:
                messagebox.showinfo(title="Hello!!!", message="Please enter at least two words to apply any operator.")
                break
            if len(token) <= 3:
                messagebox.showinfo("Error!!!", "Please enter more than 4 characters.")
                break
            stem_temp = ""
            stem_word_file = []
            temp_file = []
            word_list = word_tokenize(token)

            for x in word_list:
                if x not in stop_words:
                    stem_temp += stemmer.stem(x) + " "
            stem_word_file.append(stem_temp)

            indexed_from = 1
            if pub_index.get(stem_word_file[0].strip()):
                pointer = pub_index.get(stem_word_file[0].strip())
            else:
                # stem_word_file = []
                if len(inputText) == 1:
                    pointer = []

            if len(pointer) == 0:
                if pub_index2.get(stem_word_file[0].strip()):
                    pointer = pub_index2.get(stem_word_file[0].strip())
                indexed_from = 2

            if len(pointer) == 0:
                abc = {}
            else:
                if indexed_from == 1:
                    for j in pointer:
                        temp_file.append(pub_list_first_stem[j])
                if indexed_from == 2:
                    for j in pointer:
                        temp_file.append(pub_list_first_stem2[j])
                temp_file = tfidf.fit_transform(temp_file)
                cosine_output = cosine_similarity(temp_file, tfidf.transform(stem_word_file))

                if indexed_from == 1:
                    if pub_index.get(stem_word_file[0].strip()):
                        for j in pointer:
                            abc[j] = cosine_output[pointer.index(j)]

                if indexed_from == 2:
                    if pub_index2.get(stem_word_file[0].strip()):
                        print("writing")
                        for j in pointer:
                            abc[j] = cosine_output[pointer.index(j)]
    else:
        outputData.configure(fg='brown')
        inputText = inputText.lower().split()

        indexed_from = 1
        pointer = []
        match_word = []
        for token in inputText:
            if len(inputText) < 2:
                messagebox.showinfo("Error!!!", "Please enter at least 2 words to apply operator.")
                break
            if len(token) <= 3:
                messagebox.showinfo("Error!!!", "Please enter more than 4 characters.")
                break
            temp_file = []
            set2 = set()
            stem_word_file = []
            word_list = word_tokenize(token)
            stem_temp = ""
            for x in word_list:
                if x not in stop_words:
                    stem_temp += stemmer.stem(x) + " "
            stem_word_file.append(stem_temp)

            if pub_index.get(stem_word_file[0].strip()):
                set1 = set(pub_index.get(stem_word_file[0].strip()))
                pointer.extend(list(set1))

                if match_word == []:
                    match_word = list({z for z in pointer if z in set2 or (set2.add(z) or False)})
                else:
                    match_word.extend(list(set1))
                    match_word = list({z for z in match_word if z in set2 or (set2.add(z) or False)})
                indexed_from = 1
            else:
                if pub_index2.get(stem_word_file[0].strip()):
                    set1 = set(pub_index2.get(stem_word_file[0].strip()))
                    pointer.extend(list(set1))

                    if match_word == []:
                        match_word = list({z for z in pointer if z in set2 or (set2.add(z) or False)})
                    else:
                        match_word.extend(list(set1))
                        match_word = list({z for z in match_word if z in set2 or (set2.add(z) or False)})
                else:
                    pointer = []
                indexed_from = 2

        if len(inputText) > 1:
            match_word = {z for z in match_word if z in set2 or (set2.add(z) or False)}

            if len(match_word) == 0:
                abc = {}
            else:
                if indexed_from == 1:
                    for j in list(match_word):
                        temp_file.append(pub_list_first_stem[j])
                if indexed_from == 2:
                    for j in list(match_word):
                        temp_file.append(pub_list_first_stem2[j])

                temp_file = tfidf.fit_transform(temp_file)
                cosine_output = cosine_similarity(temp_file, tfidf.transform(stem_word_file))

                for j in list(match_word):
                    abc[j] = cosine_output[list(match_word).index(j)]
        else:
            if len(pointer) == 0:
                abc = {}
            else:
                if indexed_from == 1:
                    for j in pointer:
                        temp_file.append(pub_list_first_stem[j])
                if indexed_from == 2:
                    for j in pointer:
                        temp_file.append(pub_list_first_stem2[j])

                temp_file = tfidf.fit_transform(temp_file)
                cosine_output = cosine_similarity(temp_file, tfidf.transform(stem_word_file))

                for j in pointer:
                    abc[j] = cosine_output[pointer.index(j)]
    aa = 0
    rank_sorting = sorted(abc.items(), key=lambda z: z[1], reverse=True)
    for a in rank_sorting:
        outputData.insert(INSERT, "Rank: ")
        outputData.insert(INSERT, "{:.2f}".format(a[1][0]))
        outputData.insert(INSERT, "\n")
        outputData.insert(INSERT, 'Title: ' + pub_name[a[0]] + "\n")
        outputData.insert(INSERT, 'URL: ' + link[a[0]] + "\n")
        outputData.insert(INSERT, 'Date: ' + pub_date[a[0]] + "\n")
        outputData.insert(INSERT, 'Cov_Uni_Author: ' + pub_author[a[0]] + "\n")
        outputData.insert(INSERT, "\n")
        aa = aa + 1
    if aa == 0:
        messagebox.showinfo("Error ......", "No results found.Please Try again...")
    outcome.insert(END, aa)


# GUI build steps
window = Tk()
window.configure(bg='#e8103f')
window.geometry('1000x750')
label = Label(window, text="Search Engine", bg="#e8103f", fg="white", font="'Arial' 21 bold")
label.config(anchor=CENTER)
label.pack()
apply = Label(window, text='Apply :')
count = Label(window, text='Count :')
outcome = Entry(window, width=10)
inputBar = Entry(window, width=50)
inputBar.pack()
inputBar.place(x=50, y=50)
count.place(x=820, y=50)
outcome.place(x=880, y=50)
outputData = scrolledtext.ScrolledText(window, width=110, height=37)
outputData.place(x=50, y=90)
search = Button(window, text='Search', bg="#D4D7D9", fg="#e8103f", font="'Arial' 10", command=pub_qp_data)
search.place(x=370, y=50)
operator = IntVar()
operator.set(2)
rb_and = Radiobutton(window, text='AND', value=1, variable=operator, command=pub_qp_data)
rb_or = Radiobutton(window, text='OR', value=2, variable=operator, command=pub_qp_data)
apply.place(x=620, y=50)
rb_and.place(x=680, y=50)
rb_or.place(x=750, y=50)
window.bind('<Return>', pub_qp_data)
window.mainloop()
