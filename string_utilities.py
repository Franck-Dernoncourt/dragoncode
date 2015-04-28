from dragonfly.all import Key, Text


def capitalizeFirst(w):
    return w[0].upper()+w[1:]


def removeAnnotations(word):
    i = 0
    w = ""
    while i < len(word):
        if word[i] == '\\': return w
        w = w+word[i]
        i+= 1
    return w


def camel_case_text(text):
    newText = _camelify(text.words)
    Text(newText).execute()

def _camelify(words):
    newText = ''
    for word in words:
        word = removeAnnotations(word)
        if len(word)  < 1: pass
        elif newText == '':
            newText = word[:1].lower() + word[1:]
        else:
            newText = '%s%s' % (newText, capitalizeFirst(word))
    return newText

def yell_text(text):
    words = text.words
    newText = ''
    for word in words:
        word = removeAnnotations(word)
        if len(word)  < 1: pass
        else:
            newText = '%s%s' % (newText, word.upper())
    Text(newText).execute()

def sentence_text(text):
    words = text.words
    newText = ''
    for word in words:
        word = removeAnnotations(word)
        if len(word)  < 1: pass
        elif newText == '':
            newText = capitalizeFirst(word)
        else:
            newText = '%s %s' % (newText, word)
    Text(newText).execute()


def lisp_text(text):
    newText = ''
    for word in text.words:
        word = removeAnnotations(word)
        if len(word)  < 1: pass
        elif newText == '':
            newText = word.lower()
        else:
            newText = '%s-%s' % (newText, word.lower())
    return Text(newText).execute()

def dot_case_text(text):
    newText = ''
    for word in text.words:
        word = removeAnnotations(word)
        if len(word)  < 1: pass
        elif newText == '':
            newText = word.lower()
        else:
            newText = '%s.%s' % (newText, word.lower())
    return Text(newText).execute()

def big_dot_case_text(text):
    newText = ''
    for word in text.words:
        word = removeAnnotations(word)
        if len(word)  < 1: pass
        elif newText == '':
            newText = capitalizeFirst(word)
        else:
            newText = '%s.%s' % (newText, capitalizeFirst(word))
    return Text(newText).execute()

def big_camel_case_text(text):
    newText = _bigcamelify(text.words)
    Text(newText).execute()

def _bigcamelify(words):
    newText = ''
    for word in words:
        word = removeAnnotations(word)
        if len(word)  < 1: pass
        elif newText == '':
            newText = word[:1].capitalize() + word[1:]
        else:
            newText = '%s%s' % (newText, capitalizeFirst(word))
    return newText

def rich_case_text(text):
    newText = _richify(text.words)
    Text(newText).execute()

def _richify(words):
    newText = ''
    for word in words:
        word = removeAnnotations(word)
        if len(word)  < 1: pass
        elif newText == '':
            newText = word[:1] + word[1:]
        else:
            newText = '%s_%s' % (newText, word)
    return newText

def big_rich_case_text(text):
    newText = big_richify(text.words)
    Text(newText).execute()

def big_richify(words):
    newText = ''
    for word in words:
        word = removeAnnotations(word)
        if len(word)  < 1: pass
        elif newText == '':
            newText = word[:1].capitalize() + word[1:]
        else:
            newText = '%s_%s' % (newText, word)
    return newText
