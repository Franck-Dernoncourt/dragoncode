from dragonfly import *
from programming_languages import *

# code for spelling out individual letters

letters = {
    "aff": 'a',
    "brav": 'b',
    "cai": 'c',
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
    letter_rules["control "+k] = Key('c-'+l)
    letter_rules["meta "+k] = Key('a-'+l)
    letter_rules["option "+k] = Text(" -")+Key(l)+Text(" ")
    letter_rules["option cap "+k] = Text(" -")+Key('s-'+l)+Text(" ")


alpha_mapping = Mapping(
    fundamental = True,
    name="keyboard",    # The name of the rule.
    mapping=dict(list(letter_rules.items()) + list({
        "lace": Text("{"),
        "race": Text("}"),
        "lark": Text("("),
        "fark": Text(")"),
        "lack": Text("["),
        "rack": Text("]"),
        "page up": Key("pgup"),
        "page down": Key("pgdown"),
        "circle":             Key("lparen, rparen, left"),
        "box":             Key("lbracket, rbracket, left"),
        "diamond":             Key("langle, rangle, left"),
        "curl":             Key("lbrace, rbrace, left"),
        "string": Text("\"\"") + Key("left"),
        "rabbit": Text("''") + Key("left"),
        "snake":          Key("tab"),
        "spin": Key("enter")+Key("tab"),
        "row": Key("enter"),
        "money": Text("$"),
        "dack":          Key("backslash"),
        "dot":          Key("dot"),
        "comma":        Key("comma"),
        "per": Key("percent"),
        "colon":        Key("colon"),
        "amp": Key("ampersand"),
        "divide":          Key("space") + Key("slash") + Key("space"),
        "plus":           Key("space,plus,space"),
        "minus":          Key("space,minus,space"),
        "major":          Key("space") + Key("s-dot") + Key("space"),
        "minor":           Key("space") + Key("s-comma") + Key("space"),
        "carrot": Key("s-6"),
        "phone": Text("@"),
        "congo":          Key("space") + Key("equal") + Key("equal") + Key("space"),
        "equals":          Key("space") + Key("equal") + Key("space"),
        "dash": Key("minus"),
        "cross": Key("plus"),
        "increment": Text(" += "),
        "decrement": Text(" -= "),
        "splat":          Key("asterisk"),
        "slash":          Key("slash"),
        "hash":          Key("hash"),
        "wave": Key("tilde"),
        "pipe":           Key("bar"),
        "wink": Text(";"),
        "bang": Text("!"),
        "query": Text("?"),
        "sub": Text("_"),
        "quote":        Key("dquote"),
        "spark":        Key("squote"),
        "inject":        Key("backtick"),
        "dash": Text("-"),
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
        "zero": Text("0"),
        "up":        Key("up"),
        "down":          Key("down"),
        "left":        Key("left"),
        "right":          Key("right"),
    }.items())))
