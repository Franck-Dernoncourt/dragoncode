from dragonfly import *

grammar_context = AppContext(executable="chrome")
grammar = Grammar("chrome", context = grammar_context)

top_rules = {}
for t in range(1,10):
    n = "fold " + str(t)
    top_rules[n] = Key("c-" + str(t))


r = MappingRule(
    name = "chrome",
    mapping = dict(list(top_rules.items()) + list({
        "wipe": Key("c-w"),
        "pop": Key("c-t")}.items())))

grammar.add_rule(r)
grammar.load()

def unload():
    global grammar
    if grammar:
        grammar.unload()
        grammar = None
