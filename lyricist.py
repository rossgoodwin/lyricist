import random
import nltk
import AutumnLeaves
import re
import operator
from sys import argv
from nltk.corpus import cmudict
from nltk.probability import LidstoneProbDist

script, book = argv

ss = AutumnLeaves.syl_struc

d = cmudict.dict()

banned_words = ['the', 'of', 'in']

print "importing source text..."
f = open(book)
print "reading source text..."
t = f.read()
print "tokenizing words..."
w = nltk.word_tokenize(t)


def make_word_list():
    print "making word list..."
    word_list = []
    for i in w:
        try:
            d[i.lower()]
        except KeyError:
            pass
        else:
            if i.lower() == "'s":
                pass
            elif i[-1] == ".":
                pass
            else:
                word_list.append((i.lower(), d[i.lower()][0]))
    return word_list
    
word_list = make_word_list()


def valid_words():
    print "extracting words from word list..."
    vw = []
    for (x, y) in word_list:
        vw.append(x)
    return vw
    
vw = valid_words()


def unique(s):
    print "making unique word list..."
    u = []
    for x in s:
        if x not in u:
            u.append(x)
        else:
            pass
    return u
    
word_list_u = unique(word_list)


def sylcount(s):
    try:
        d[s]
    except KeyError:
        return None
    else:
        if len(d[s]) <= 1:
            sj = ''.join(d[s][0])
            sl = re.split('0|1|2', sj)
            return len(sl) - 1
        else:
            sj0 = ''.join(d[s][0])
            sl0 = re.split('0|1|2', sj0)
            sj1 = ''.join(d[s][1])
            sl1 = re.split('0|1|2', sj1)
            if len(sl1) < len(sl0):
                return len(sl1) - 1
            else:
                return len(sl0) - 1
        
        
def line_sylcount(line):
    count = 0
    for word in line:
        count += sylcount(word)
    return count
    

def meter(word):
    pron = d[word]
    m1 = []
    m2 = []
    mx = []
    if len(pron) == 1:
        for i in pron[0]:
            if '0' in i:
                m1.append(0)
            elif '1' in i:
                m1.append(1)
            elif '2' in i:
                m1.append(2)
            else:
                pass
        mx = [m1]
    elif len(pron) >= 2:
        for i in pron[0]:
            if '0' in i:
                m1.append(0)
            elif '1' in i:
                m1.append(1)
            elif '2' in i:
                m1.append(2)
            else:
                pass
        for i in pron[1]:
            if '0' in i:
                m2.append(0)
            elif '1' in i:
                m2.append(1)
            elif '2' in i:
                m2.append(2)
            else:
                pass
        mx = [m1, m2]
    m = []
    if len(mx) == 1:
        w0 = reduce(operator.mul, mx[0], 1)
        if w0 >= 2:
            for i in mx[0]:
                if i == 1:
                    m.append('u')
                elif i == 2:
                    m.append('s')
        elif w0 == 1:
            for i in mx[0]:
                m.append('s')
        elif w0 == 0:
            for i in mx[0]:
                if i == 0:
                    m.append('u')
                elif i == 1 or i == 2:
                    m.append('s')
    elif len(mx) == 2:
        w0 = reduce(operator.mul, mx[0], 1)
        w1 = reduce(operator.mul, mx[1], 1)
        if w0 >= 2 and w1 >= 2:
            for (i, j) in zip(mx[0], mx[1]):
                if i * j == 1:
                    m.append('u')
                elif i * j == 4:
                    m.append('s')
                elif i * j == 2:
                    m.append('x')
        elif w0 == 1 and w1 == 1:
            for (i, j) in zip(mx[0], mx[1]):
                m.append('s')
        elif w0 == 0 and w1 == 0:
            for (i, j) in zip(mx[0], mx[1]):
                if i == j and i * j >= 1:
                    m.append('s')
                elif i != j and i * j == 0:
                    m.append('x')
                elif i == j and i * j == 0:
                    m.append('u')
        elif w0 >= 2 and w1 == 0:
            for (i, j) in zip(mx[0], mx[1]):
                if i == 1 and j == 0:
                    m.append('u')
                elif i == 2 and j == 0:
                    m.append('x')
                elif i == 1 and j == 1:
                    m.append('x')
                elif i == 1 and j == 2:
                    m.append('x')
                elif i == 2 and j == 1:
                    m.append('s')
                elif i == 2 and j == 2:
                    m.append('s')
        elif w0 == 0 and w1 >= 2:
            for (i, j) in zip(mx[0], mx[1]):
                if i == 0 and j == 1:
                    m.append('u')
                elif i == 0 and j == 2:
                    m.append('x')
                elif i == 1 and j == 1:
                    m.append('x')
                elif i == 2 and j == 1:
                    m.append('x')
                elif i == 1 and j == 2:
                    m.append('s')
                elif i == 2 and j == 2:
                    m.append('s')
        elif w0 == 1 and w1 >= 2:
            for (i, j) in zip(mx[0], mx[1]):
                if j == 1:
                    m.append('x')
                elif j == 2:
                    m.append('s')
        elif w0 >= 2 and w1 == 1:
            for (i, j) in zip(mx[0], mx[1]):
                if i == 1:
                    m.append('x')
                elif i == 2:
                    m.append('s')
        elif w0 == 1 and w1 == 0:
            for (i, j) in zip(mx[0], mx[1]):
                if j == 0:
                    m.append('x')
                elif j == 1:
                    m.append('s')
                elif j == 2:
                    m.append('s')
        elif w0 == 0 and w1 == 1:
            for (i, j) in zip(mx[0], mx[1]):
                if i == 0:
                    m.append('x')
                if i == 1:
                    m.append('s')
                if i == 2:
                    m.append('s')       
    return m


def strip_numbers(x):
    xj = '.'.join(x)
    xl = re.split('0|1|2', xj)
    xjx = ''.join(xl)
    xlx = xjx.split('.')
    return xlx
    

def last_stressed_vowel(word):
    if len(d[word]) <= 1:
        pron = d[word][0]
    else:
        p0 = d[word][0]
        p1 = d[word][1]
        sj0 = ''.join(p0)
        sl0 = re.split('0|1|2', sj0)
        sj1 = ''.join(p1)
        sl1 = re.split('0|1|2', sj1)
        if len(sl1) < len(sl0):
            pron = p1
        else:
            pron = p0
    mtr = meter(word)
    vowel_index = []
    if len(mtr) == 1:
        lsv = -1
    elif mtr[-1] == 's' or mtr[-1] == 'x':
        lsv = -1
    elif mtr[-2] == 's' or mtr[-3] == 'x':
        lsv = -2
    elif mtr[-3] == 's' or mtr[-3] == 'x':
        lsv = -3
    elif mtr[-4] == 's' or mtr[-4] == 'x':
        lsv = -4
    elif mtr[-5] == 's' or mtr[-5] == 'x':
        lsv = -5
    elif mtr[-6] == 's' or mtr[-6] == 'x':
        lsv = -6
    elif mtr[-7] == 's' or mtr[-7] == 'x':
        lsv = -7
    elif mtr[-8] == 's' or mtr[-8] == 'x':
        lsv = -8
    elif mtr[-9] == 's' or mtr[-9] == 'x':
        lsv = -9
    elif mtr[-10] == 's' or mtr[-10] == 'x':
        lsv = -10
    else:
        lsv = -1
    for i in pron:
        if '0' in i or '1' in i or '2' in i:
            vowel_index.append(pron.index(i))
        else:
            continue
    return vowel_index[lsv]


def rhyme_finder(word):
    rhyming_words = []
    if len(d[word]) <= 1:
        pron = d[word][0]
    else:
        p0 = d[word][0]
        p1 = d[word][1]
        sj0 = ''.join(p0)
        sl0 = re.split('0|1|2', sj0)
        sj1 = ''.join(p1)
        sl1 = re.split('0|1|2', sj1)
        if len(sl1) < len(sl0):
            pron = p1
        else:
            pron = p0
    pron = strip_numbers(pron)
    lsv = last_stressed_vowel(word)
    rhyme_part = pron[lsv:]
    lrp = len(rhyme_part) * -1
    for (x, y) in word_list_u:
        ps = strip_numbers(y)
        if ps[lrp:] == rhyme_part and ps[lrp-1:] != pron[lsv-1:]:
            rhyming_words.append(x)
        else:
            pass
    rw = [i for i in rhyming_words if not i == word]
    return rw


print "building content model..."
estimator = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)
content_model = nltk.NgramModel(3, vw, estimator=estimator)


def sw():
    sw1 = random.randint(0, len(vw) - 1)
    return [vw[sw1]]


def generate_words(s, l):
    lyrics = []
    for i in l:
        lyrics += i
    syl_count = 0
    words = []
    l_c = lyrics
    while syl_count != s:
        if syl_count < s:
            starting_words = sw()
            word = content_model.generate(1, starting_words + l_c)
            word = word[-1]
            words.append(word)
            l_c.append(word)
            syl_count = line_sylcount(words)
        elif syl_count > s:
            words = []
            l_c = lyrics
            syl_count = 0
    return words


def generate_rhyme(n, l):
    lyrics = []
    for i in l:
        lyrics += i
    other_2s = []
    vw_r = vw
    random.shuffle(vw_r)
    for i in reversed(range(len(ss[0:n]))):
        if ss[i][0] == 2:
            other_2s.append(i)
        else:
            continue
    if other_2s == [] or len(other_2s) % 2 == 0:
        starting_words = sw()
        word = content_model.generate(1, starting_words + lyrics)
        word = word[-1]
        count = 0
        while sylcount(word) != 1 or rhyme_finder(word) == [] or not 1 in [sylcount(j) for j in rhyme_finder(word)] or word in banned_words:
            word = vw_r[count]
            count += 1
    else:
        prev_2 = other_2s[0]
        word_to_rhyme = l[prev_2][0]
        rhyming_words = rhyme_finder(word_to_rhyme)
        random.shuffle(rhyming_words)
        for i in rhyming_words:
            if sylcount(i) == 1:
                word = i
                break
            else:
                continue
    return word


def same_word(n, l):
    lyrics = []
    for i in l:
        lyrics += i
    other_3s = []
    vw_r = vw
    random.shuffle(vw_r)
    for i in reversed(range(len(ss[0:n]))):
        if ss[i][0] == 3:
            other_3s.append(i)
        else:
            continue
    if other_3s == []:
        starting_words = sw()
        word = content_model.generate(1, starting_words + lyrics)
        word = word[-1]
        count = 0
        while sylcount(word) != 1 or word in banned_words:
            word = vw_r[count]
            count += 1
    else:
        prev_3 = other_3s[0]
        word = l[prev_3][0]
    return word



def generate_lyrics():
    lyrics = []
    for i in range(len(ss)):
        if ss[i][0] == 1:
            syllables = len(ss[i])
            words = generate_words(syllables, lyrics)
            lyrics += [words]
        elif ss[i][0] == 2:
            word = generate_rhyme(i, lyrics)
            lyrics.append([word])
        elif ss[i][0] == 3:
            word = same_word(i, lyrics)
            lyrics.append([word])
        elif ss[i][0] == 0:
            lyrics.append(["REST"])
    return lyrics


print generate_lyrics()









