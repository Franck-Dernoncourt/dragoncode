from dragonfly import (Grammar, AppContext, MappingRule, Dictation,
                       Key, Text, Function, Integer, IntegerRef,
                       Literal, Repeat)

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

grammar_context = AppContext(executable="emacs") | AppContext(executable="VMware") | AppContext(executable="VirtualBox") | AppContext(executable="PuTTY") | AppContext(executable="MATLAB") | AppContext(executable="Editor") | AppContext(executable="Xming") | AppContext(executable="emacs@grok")

grammar = Grammar("emacs", context=grammar_context)
haskell_grammar = Grammar("haskell", context=grammar_context)
camel_grammar = Grammar("camel", context=grammar_context)
latex_grammar = Grammar("latex", context=grammar_context)
exec_grammar = Grammar("exec", context=grammar_context)

gunits = [grammar, exec_grammar, haskell_grammar, latex_grammar, camel_grammar]

#---------------------------------------------------------------------------
# Create a mapping rule which maps things you can say to actions.
#
# Note the relationship between the *mapping* and *extras* keyword
#  arguments.  The extras is a list of Dragonfly elements which are
#  available to be used in the specs of the mapping.  In this example
#  the Dictation("text")* extra makes it possible to use "<text>"
#  within a mapping spec and "%(text)s" within the associated action.




example_rule = MappingRule(
    name="example",    # The name of the rule.
    mapping={          # The mapping dict: spec -> action.
        "butterfly": Key("a-x"),
        "stop job": Key("c-z"),
        "foreground <n>": Text("fg ")+Text("%(n)d")+Key("enter"),
             "save":            Key("c-x, c-s"),
             "open":            Key("c-x, c-f"),
             "apostate": Key("c-x/10, c-c/10"),
             "mac start":            Key("c-x, lparen"),
             "mac end":            Key("c-x, rparen"),
             "mac do":            Key("c-x, e"),
             "sun":             Key("c-s"),
             "run":             Key("c-r"),
             "rancor":          Key("as-5"),
             "amp": Key("ampersand"),
             "wink": Text(";"),
             "mango <n>":           Key("a-g, g")+Text("%(n)d")+Key("enter"),
             "circle":             Key("lparen, rparen, left"),
             "box":             Key("lbracket, rbracket, left"),
             "diamond":             Key("langle, rangle, left"),
             "curl":             Key("lbrace, rbrace, left"),
             "string": Text("\"\"") + Key("left"),
             "rabbit": Text("''") + Key("left"),
             "hop":             Key("c-x, o"),
    "bash":Key("a-x, s, h, e, l, l, enter"),
        "feline [<n>]": Key("c-x, right")*Repeat(extra = "n"),
        "canine [<n>]": Key("c-x, left")*Repeat(extra = "n"),
    "quit":Key("c-g"),
    "veal":Key("c-x, 3"),
    "holly":Key("c-x, 2"),
    "breathe":Key("c-x, 1"),
             "underscore": Text("_"),
    "buff":Key("c-x, c-b"),
             "leap [<n>]":            Key("ca-f")*Repeat(extra="n"),
             "trip [<n>]":         Key("ca-b")*Repeat(extra="n"),
             "paste":         Key("c-y"),
             "scratch":         Key("c-x, u"),
             "scratch that":         Key("c-x, u"),
             "mark":         Key("c-space"),
             "chop":         Key("c-w"),
             "zap":         Key("a-w"),
             "wipe":         Key("c-k"),
             "kill":         Key("c-x, k"),
             "say <text>": Text("%(text)s"),
             "camel <text>": Function(camel_case_text),
             "studley <text>": Function(big_camel_case_text),
             "score <text>": Function(rich_case_text),
             "dote <text>": Function(dot_case_text),
             "moth <text>": Function(big_dot_case_text),
             "tab":          Key("tab"),
             "dab":          Key("tab, tab"),
             "quote":        Key("dquote"),
             "slap [<n>]":        Key("enter") * Repeat(extra="n"),
             "spark":        Key("squote"),
             "inject":        Key("backtick"),
             "comma":        Key("comma"),
             "colon":        Key("colon"),
             "reach":        Key("c-e"),
             "fall":          Key("c-a"),
             "eat oh eff": Key("c-d"),
"sword [<n>]": Key('c-d')*Repeat(extra = "n"),
"pike [<n>]": Key('backspace')*Repeat(extra = "n"),
             "pounce [<n>]":        Key("a-p") * Repeat(extra="n"),
             "up [<n>]":        Key("up") * Repeat(extra="n"),
             "down [<n>]":          Key("down") * Repeat(extra="n"),
             "left [<n>]":        Key("left") * Repeat(extra="n"),
             "right [<n>]":          Key("right") * Repeat(extra="n"),
             "choose <n> [<c>]": Key("c-x, b/10, asterisk/10")+Key("s-c")+Text("ompletions*")+Key("enter")+
                                 Key("a-g, g")+Text("%(n)d")+Key("enter")+(Key("ca-f")*Repeat(extra = "c"))+Key("enter")+
                                 Key("a-x/10")+Text("kill-buffer-and-its-windows")+Key("enter/10")+
                                 Key("asterisk/10")+Key("s-c")+Text("ompletions*")+Key("enter"),
             "club [<n>]":          Key("a-backspace")*Repeat(extra = "n"),
             "chirp":          Key("c-l"),
             "zoom":          Key("as-dot"),
             "zip":          Key("as-comma"),
             "scream <text>":          Function(yell_text),
             "jive <text>":          Function(lisp_text),
             "dot":          Key("dot"),
             "slash":          Key("slash"),
             "splat":          Key("asterisk"),
             "slash":          Key("slash"),
             "divide":          Key("space") + Key("slash") + Key("space"),
             "backslash":          Key("backslash"),
             "pound":          Key("hash"),
             "tilde": Key("tilde"),
             "plus":           Key("plus"),
             "minus":          Key("minus"),
             "pipe":           Key("bar"),
        "bang": Text("!"),
             "equals":          Key("space") + Key("equal") + Key("space"),
             "congo":          Key("space") + Key("equal") + Key("equal") + Key("space"),
             "major":          Key("space") + Key("s-dot") + Key("space"),
             "minor":           Key("space") + Key("s-comma") + Key("space"),
             # Shell commands
             "odin":          Text("sudo -i")+Key("enter"),
             "summon":          Text("apt-get install "),
             "vanquish":          Text("apt-get remove "),
             "inquisition": Text("apt-cache search "),
             "popcorn":          Text("cd ..")+Key("enter"),
             "explore":          Text("cd "),
             "survey":          Text("ls -lah | less")+Key("enter"),
             "scout":           Text("ls")+Key("enter"),
             "doctor":           Text("dmesg|less")+Key("enter"),
        "airhead <n>": Key("c-x, backtick")*Repeat(extra = "n"),
             "make <text>":           Key("a-colon")+Text("(compile \"make %(text)s\")")+Key("enter"),
             "new folder": Text("mkdir "),
             "exit": Text("exit")+Key("enter"),
             # window manager support
             "lemon":           Key("w-tab"),
             "pineapple":           Key("w-x"),
             "lime":           Key("w-space"),
             "coconut":           Key("w-enter"),
             "vacation <n>":          Key("sw-%(n)d"),
             "visit <n>":          Key("w-%(n)d"),
             # version control
             "get commit":           Text("git commit -a -m \"\"")+Key("left"),
             "get push":           Text("git push")+Key("enter"),
             "get pull":           Text("git pull")+Key("enter"),
             "get add":           Text("git add "),
             "get branch": Text("git branch "),
             "get checkout": Text("git checkout "),
             "get log": Text("git log "),
             "get clone": Text("git clone "),
            },
    extras=[           # Special elements in the specs of the mapping
            Dictation("text",format=False),
            IntegerRef("n", 1, 2000),            IntegerRef("c", 1, 2000),
           ],
    defaults = {
                "n": 1, "c": 1,
               }
   )

haskell_rules = MappingRule(
    name="haskell",    # The name of the rule.
    mapping={          # The mapping dict: spec -> action.
"dagger": Text("DAG"),
             "data <text>":            Text("data ")+Function(big_camel_case_text)+Text(" = "),
             "lexical":            Text("let x = x")+Key("enter, i, n, space, tab, up, c-e, backspace, left, left, left, backspace"),
             "type <text>":            Text("type ")+Function(big_camel_case_text)+Text(" = "),
             "lambda":            Key("backslash, space, space, minus,  s-dot, space, left, left, left, left"),
             "case":            Text("case  of")+Key("left, left, left"),
             "do":            Text("do "),
             "where":            Text("where  = ")+Key("left, left, left"),
             "assign":            Text(" <- "),
             "infix": Text("``")+Key("left"),
             "goes to":            Text(" -> "),
             "has type":            Text(" :: "),
             "not equal":            Text(" /= "),
             "and":             Text(" && "),
             "or":             Text(" || "),
             "not":            Text("not "),
             "compose":            Text(" . "),
             "comment":        Text(" -- "),
             "magic": Key("ca-i"),
             "local": Key("a-slash"),
             "temp": Key("a-t"),
             "dollar": Text(" $ "),
             "branch":            Text("if x")+Key("enter")+Text("then x")+Key("enter")+Text("else x")+Key("tab, up, tab, up, c-e, backspace, down, c-e, backspace, down, c-e, backspace, up, up"),
             "return": Text("return "),
             "import": Text("import "),
             "qualified": Text("import qualified  as ") + Key("enter, up, c-e, left, left, left, left"),
             "module": Text("module  where") + Key("enter, enter, up, up, c-e, left, left, left, left, left, left"),
             "bind": Text(">>="),
             "double": Text("Double"),
             "int": Text("Int"),
             "evaluate": Key("c-c, c-l"),
             "prime": Text("'"),
            },
    extras=[           # Special elements in the specs of the mapping
            Dictation("text",format=False),
            IntegerRef("n", 1, 2000)
           ],
    )
camel_rules = MappingRule(
    name="camel",    # The name of the rule.
    mapping={          # The mapping dict: spec -> action.
             "lexical":            Text("let  =  in")+Key("left, left, left, left, left, left"),
             "recursive": Text("let rec "),
             "reference": Text("ref "),
             "for loop": Key("c-c, f"),
             "while loop": Key("c-c, w"),
             "try": Key("c-c, i"),
             "block": Key("c-c, b"),
             "dunk": Text(";;")+Key("enter"),
             "type <text>":            Text("type ")+Function(camel_case_text)+Text(" = "),
             "lambda":            Text("fun  -> ")+Key("left, left, left, left"),
             "match":            Text("match  with")+Key("left, left, left, left, left"),
             "assign":            Text(" := "),
             "goes to":            Text(" -> "),
             "went to":            Text(" <- "),
             "has type":            Text(" : "),
             "not equal":            Text(" <> "),
             "and":             Text(" && "),
             "or":             Text(" || "),
             "not":            Text("not "),
             "send to": Text(" |> "),
             "apply to": Text(" @@ "),
             "comment":        Text("(*  *)")+Key("left, left, left"),
             "int": Text("int"),
             "hash table": Text("Hashtbl."),
             "bool": Text("bool"),
             "prime": Text("'"),
             # Merlin commands
             "inference": Key("c-c")+Key("c-t"),
             "erroneous":  Key("c-c")+Key("c-x"),
             "merlin": Key("c-c, tab"),
            },
    extras=[           # Special elements in the specs of the mapping
            Dictation("text",format=False),
            IntegerRef("n", 1, 2000)
           ],
    )

latex_rules = MappingRule(
    name="latex",    # The name of the rule.
    mapping={          # The mapping dict: spec -> action.
"summation": Text("\\sum"),
"infinity": Text("\\infty"),
"supremum": Text("\\sup "),
"infinum": Text("\\inf "),
"member": Text("\\in "),
"for all": Text("\\forall "),
"there exists": Text("\\exists"),
"power": Text("^{}")+Key("left"),
"compile": Key("c-c, c-c"),
"subsection": Text("\\subsection{}")+Key("left"),
"equation": Text("\\begin{equation}\n\\end{equation}")+Key("up, c-e")+Key("enter"),
"equation array": Text("\\begin{eqnarray}\n\\end{eqnarray}")+Key("up, c-e")+Key("enter"),
"math": Text("$$")+Key("left"),
"label": Text("\\label{}")+Key("left"),
"refer": Text("\\ref{}")+Key("left"),
"package": Text("\\usepackage{}")+Key("left"),
"preamble": Text("\\documentclass{article}\n\n\n\\begin{document}\n\n\n\\end{document}")+Key("up, up"),
"degree": Text("\\circ "),
"section": Text("\\section{}")+Key("left"),
"figure": Text("\\begin{figure}\n\\end{figure}")+Key("up, c-e, enter"),
"code box": Text("\\begin{codebox}\n\\end{codebox}")+Key("up, c-e, enter"),
"text box": Text("\\text{}")+Key("left"),
"square root": Text("\\sqrt{}")+Key("left"),
"dack dash": Text("\\\\"),
"fraction": Text("\\frac{}{}")+Key("left")+Key("left")+Key("left"),
"itemize": Text("\\begin{itemize}\n\n\\end{itemize}")+Key("up"),
"if and only if": Text(" iff "),
#Greek letters
"alpha": Text("\\alpha"),
"beta": Text("\\beta"),
"theta": Text("\\theta"),
"gamma": Text("\\gamma"),
"mu": Text("\\mu"),
"delta": Text("\\delta"),
            },
    extras=[           # Special elements in the specs of the mapping
            Dictation("text",format=False),
            IntegerRef("n", 1, 2000)
           ],
    )

def pumpUp(text):
    for word in text.words:
        word = word.lower()
        for g in gunits:
            if g.name == word:
                g.enable()
    Text("").execute()
def chillOut(text):
    for word in text.words:
        word = word.lower()
        for g in gunits:
            if g.name == word:
                g.disable()
    Text("").execute()

executive_rules= MappingRule(
    name="executive",    # The name of the rule.
    mapping={          # The mapping dict: spec -> action.
             "engage <text>":            Function(pumpUp),
             "chill <text>":            Function(chillOut)
            },
    extras=[           # Special elements in the specs of the mapping
            Dictation("text",format=False)
           ],
    )

# Add the action rule to the grammar instance.
grammar.add_rule(example_rule)
haskell_grammar.add_rule(haskell_rules)
camel_grammar.add_rule(camel_rules)
latex_grammar.add_rule(latex_rules)
exec_grammar.add_rule(executive_rules)

# code for spelling out individual letters
alpha_grammar = Grammar("alpha")
alpha_rule = MappingRule(
    name="alpha",    # The name of the rule.
    mapping={          # The mapping dict: spec -> action.
#        "cap": Key('capslock'),
"aff": Key('a'), "cap aff": Key('s-a'),
"brav": Key('b'), "cap brav": Key('s-b'),
"cai": Key('c'), "cap cai": Key('s-c'),
"doy": Key('d'), "cap doy": Key('s-d'),
"delt": Key('d'), "cap delt": Key('s-d'),
"delta": Key('d'), "cap delta": Key('s-d'),
"eck": Key('e'), "cap eck": Key('s-e'),
"echo": Key('e'), "cap echo": Key('s-e'),
"fay": Key('f'), "cap fay": Key('s-f'),
"goff": Key('g'), "cap goff": Key('s-g'),
"hoop": Key('h'), "cap hoop": Key('s-h'),
"ish": Key('i'), "cap ish": Key('s-i'),
"jo": Key('j'), "cap jo": Key('s-j'),
"keel": Key('k'), "cap keel": Key('s-k'),
"lee": Key('l'), "cap lee": Key('s-l'),
"mike": Key('m'), "cap mike": Key('s-m'),
"noy": Key('n'), "cap noy": Key('s-n'),
"osh": Key('o'), "cap osh": Key('s-o'),
"pom": Key('p'), "cap pom": Key('s-p'),
"queen": Key('q'), "cap queen": Key('s-q'),
"ree": Key('r'), "cap ree": Key('s-r'),
"soi": Key('s'), "cap soi": Key('s-s'),
"tay": Key('t'), "cap tay": Key('s-t'),
"uni": Key('u'), "cap uni": Key('s-u'),
"van": Key('v'), "cap van": Key('s-v'),
"wes": Key('w'), "cap wes": Key('s-w'),
"xanth": Key('x'), "cap xanth": Key('s-x'),
"yaa": Key('y'), "cap yaa": Key('s-y'),
"zul": Key('z'), "cap zul": Key('s-z'),
"lace": Text("{"),
"race": Text("}"),
"lark": Text("("),
"fark": Text(")"),
"lack": Text("["),
"rack": Text("]"),
"ace": Text(" "),
"one": Text("1"),
"two": Text("2"),
"three": Text("3"),
"four": Text("4"),
"five": Text("5"),
"six": Text("6"),
"seven": Text("7"),
"eight": Text("8"),
"nine": Text("9"),
"zero": Text("0")
})

alpha_grammar.add_rule(alpha_rule)
alpha_grammar.load()

#---------------------------------------------------------------------------
# Load the grammar instance and define how to unload it.

for g in gunits:
    g.load()
    if g != grammar and g != exec_grammar:
        g.disable()

# Unload function which will be called by natlink at unload time.
def unload():
    global gunits
    if gunits:
        for g in gunits:
            g.unload()
    gunits = None
    global alpha_grammar
    if alpha_grammar:
        alpha_grammar.unload()
    alpha_grammar = None


