from dragonfly import *

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

grammar_context = AppContext(executable="emacs") | AppContext(executable="VMware") | AppContext(executable="VirtualBox") | AppContext(executable="PuTTY") | AppContext(executable="MATLAB") | AppContext(executable="Editor") | AppContext(executable="Xming") | AppContext(executable="emacs@grok")

grammar = Grammar("emacs", context=grammar_context)
haskell_grammar = Grammar("haskell", context=grammar_context)
luau_grammar = Grammar("luau", context=grammar_context)
camel_grammar = Grammar("camel", context=grammar_context)
latex_grammar = Grammar("latex", context=grammar_context)
exec_grammar = Grammar("exec", context=grammar_context)

gunits = [grammar, exec_grammar, haskell_grammar, luau_grammar, latex_grammar, camel_grammar]

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
        "of course": Text("yes")+Key("enter"),
        "no way": Text("no")+Key("enter"),
        "Emacs": Text("emacs -nw "),
        "butterfly": Key("a-x"),
        "Gmail": Key("a-x")+Text("gnus")+Key("enter"),
        "stop job": Key("c-z"),
        "putty full-screen": Key("a-enter"),
        "foreground <n>": Text("fg ")+Text("%(n)d")+Key("enter"),
        "save":            Key("c-x, c-s"),
        "open":            Key("c-x, c-f"),
        "apostate": Key("c-x/10, c-c/10"),
        "lua": Text("lua"),
        "spin": Key("enter")+Key("tab"),
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
        "no hup": Text("nohup  &")+Key("left,left"),
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
        "kill":         Key("c-x, k, enter"),
        "say <text>": Text("%(text)s"),
        "camel <text>": Function(camel_case_text),
        "studley <text>": Function(big_camel_case_text),
        "score <text>": Function(rich_case_text),
        "humble <text>": Function(big_rich_case_text),
        "dote <text>": Function(dot_case_text),
        "moth <text>": Function(big_dot_case_text),
        "tab":          Key("tab"),
        "slurp [<n>]": Key("c-space")+Key("ca-f")*Repeat(extra = "n")+Key("a-w"),
        "snap [<n>]": Key("c-space")+Key("ca-b")*Repeat(extra = "n")+Key("a-w"),
        "snake":          Key("tab"),
        "snake eyes":          Key("tab, tab"),
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
        "grape": Text("grep "),
        "wreck grape": Text("rgrep "),
        "grape soda": Text("grep -i "),
        "wreck grape soda": Text("rgrep -i "),
        "popcorn":          Text("cd ..")+Key("enter"),
        "explore":          Text("cd "),
        "survey":          Text("ls -lah | less")+Key("enter"),
        "scout":           Text("ls")+Key("enter"),
        #             "doctor":           Text("dmesg|less")+Key("enter"),
        "airhead <n>": Key("c-x, backtick")*Repeat(extra = "n"),
        "make <text>":           Key("a-colon")+Text("(compile \"make %(text)s\")")+Key("enter"),
        "new folder": Text("mkdir "),
        "exit": Text("exit")+Key("enter"),
        # window manager support for xmonad, which I no longer use
        #             "lemon":           Key("w-tab"),
        #             "pineapple":           Key("w-x"),
        #             "lime":           Key("w-space"),
        #             "coconut":           Key("w-enter"),
        #             "vacation <n>":          Key("sw-%(n)d"),
        #             "visit <n>":          Key("w-%(n)d"),
        # version control
        "get commit":           Text("git commit -a -m \"\"")+Key("left"),
        "get push":           Text("git push")+Key("enter"),
        "get pull":           Text("git pull")+Key("enter"),
        "get add":           Text("git add "),
        "get branch": Text("git branch "),
        "get checkout": Text("git checkout "),
        "get log": Text("git log "),
        "get clone": Text("git clone "),
        # file extensions
        "dot em ell": Text(".ml"),
        "dot h s": Text(".hs"),
        "oh camel": Text("ocaml"),
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
             "try": Key("c-c, t"),
             "block": Key("c-c, b"),
             "print eff": Text("Printf.printf \"\"")+Key("left"),
             "dunk": Text(";;")+Key("enter"),
             "second": Text("snd"),
             "first": Text("fst"),
        "composition": Key("space, percent, space"),
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
             "append": Text(" @ "),
             "concatenate": Text(" ^ "),
             "comment":        Text("(*  *)")+Key("left, left, left"),
             "cons": Text(" :: "),
             "int": Text("int"),
             "hash table": Text("Hashtbl."),
             "bool": Text("bool"),
             "prime": Text("'"),
             "sign": Text("sin"),
             "cosine": Text("cos"),
             "exponential": Text("exp"),
             # Merlin commands
             "inference": Key("c-c")+Key("c-t"),
             "erroneous":  Key("c-c")+Key("c-x"),
             "merlin": Key("c-c, tab"),
             # special jetty commands
             "arrow": Text(" @> "),
            },
    extras=[           # Special elements in the specs of the mapping
            Dictation("text",format=False),
            IntegerRef("n", 1, 2000)
           ],
    )

luau_rules = MappingRule(
    name="luau",    # The name of the rule.
    mapping={          # The mapping dict: spec -> action.
        "torch": Text("torch"),
             "lexical":            Text("local  = ")+Key("left, left, left, left"),
        "nil": Text("nil"),
        "block": Text("do  end")+Key("left,left,left,left"),
             "for loop": Text("for  = , ")+Key("left,left,left,left,left"),
             "while loop": Text("while  do  end")+Key("left,left,left,left,left,left,left,left,left,left"),
             "lambda":            Text("function ()  end")+Key("left, left, left, left"),
             "not equal":            Text(" ~= "),
        "Congo": Text(" == "),
        "return": Text("return "),
             "and":             Text(" and "),
             "or":             Text(" or "),
        "true": Text("true"),
        "false": Text("false"),
             "not":            Text("not "),
             "length": Text(" #"),
             "concatenate": Text(" .. "),
             "comment":        Text("-- "),
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
        "sinusoid": Text("\\sin "),
        "cosine": Text("\\cos "),
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
luau_grammar.add_rule(luau_rules)
latex_grammar.add_rule(latex_rules)
exec_grammar.add_rule(executive_rules)

# code for spelling out individual letters

letters = {
    "aff": 'a',
    "brav": 'b',
    "cai": 'c',
    "doy": 'd',
    "delt": 'd',
    "delta": 'd',
    "eck": 'e',
    "echo": 'e',
    "fay": 'f',
    "goff": 'g',
    "hoop": 'h',
    "ish": 'i',
    "jo": 'j',
    "keel": 'k',
    "lima": 'l',
    "mike": 'm',
    "noy": 'n',
    "osh": 'o',
    "pom": 'p',
    "queen": 'q',
    "ree": 'r',
    "soi": 's',
    "tay": 't',
    "uni": 'u',
    "van": 'v',
    "wes": 'w',
    "xanth": 'x',
    "yaa": 'y',
    "zul": 'z'
}

letter_rules = {}
for k in letters:
    l = letters[k]
    letter_rules[k] = Key(l)
    letter_rules["cap "+k] = Key('s-'+l)
    letter_rules["opt "+k] = Text(" -")+Key(l)+Text(" ")
    letter_rules["opt cap "+k] = Text(" -")+Key('s-'+l)+Text(" ")
    letter_rules["per "+k] = Key("percent")+Key(l)
    letter_rules["per cap "+k] = Key("percent")+Key('s-'+l)
    letter_rules["est "+k] = Key("backslash")+Key(l)
    letter_rules["est cap "+k] = Key("backslash")+Key('s-'+l)


alpha_grammar = Grammar("alpha")
alpha_rule = MappingRule(
    name="alpha",    # The name of the rule.
    mapping=dict(list(letter_rules.items()) + list({
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
    }.items())))

alternatives = []
alternatives.append(RuleRef(rule=alpha_rule))
single_action = Alternative(alternatives)
sequence = Repetition(single_action, min=1, max=16, name="sequence")

class RepeatRule(CompoundRule):
    spec     = "<sequence>"
    extras   = [
                sequence
               ]
    def _process_recognition(self, node, extras):
        sequence = extras["sequence"]   # A sequence of actions.
        for action in sequence:
            action.execute()

alpha_grammar.add_rule(RepeatRule())
alpha_grammar.load()


password_grammar = Grammar("password")
password_dictionary = {}
for line in open("C:/natlink/natlink/macrosystem/passwords", "r"):
    parts = line.split("|")
    password_dictionary[parts[0]] = Text(parts[1])
    
password_rule = MappingRule(
    name="passwords",    # The name of the rule.
    mapping=password_dictionary)

password_grammar.add_rule(password_rule)
password_grammar.load()

window_grammar = Grammar("window_grammar")
window_rule = MappingRule(name = "window_rule",mapping = {
        "switch window": Key("a-tab")})
window_grammar.add_rule(window_rule)
window_grammar.load()

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
    global password_grammar
    if password_grammar:
        password_grammar.unload()
    password_grammar = None
    global window_grammar
    if window_grammar:
        window_grammar.unload()
    window_grammar = None
