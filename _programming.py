# main file

from dragonfly import *
from verbatim import *
from programming_languages import *
from verbal_keyboard import *


grammar_context = AppContext(executable="emacs") | AppContext(executable="VMware") | AppContext(executable="VirtualBox") | AppContext(executable="PuTTY") | AppContext(executable="MATLAB") | AppContext(executable="Editor") | AppContext(executable="Xming") | AppContext(executable="emacs@grok") | AppContext(executable="Command Prompt") | AppContext(executable="cmd")



def create_repetition(atomic):
    single_action = Alternative([RuleRef(rule=atomic)])
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
    return RepeatRule()


dictation_grammar = Grammar("dictation", context=grammar_context)
exec_grammar = Grammar("exec", context=grammar_context)

gunits = [exec_grammar, dictation_grammar]


# composite_grammar holds all of the ccr commands
composite_grammar = Grammar("composite", context = grammar_context) 


def merge_mappings(mappings):
    m = mappings[0].mapping.copy()
    n = 'MERGE_' + mappings[0].name
    for mp in mappings[1:]:
        m.update(mp.mapping)
        n += "+"+mp.name
    return MappingRule(name = n,
                       mapping = m,
                       extras = [ IntegerRef("n", 1, 100)])

def update_composition():
    global composite_grammar
    
    enabled_mappings = [ option for option in composite_options if option.enabled ]
    if len(composite_grammar._rules) > 0:
        composite_grammar.unload()
        toremove = composite_grammar._rules[:]
        for r in toremove:
            composite_grammar.remove_rule(r)
    merged = merge_mappings(enabled_mappings)
    print merged._name
    composite_grammar.add_rule(create_repetition(merged))
    composite_grammar.load()

update_composition() # load defaults

def mappings_consistent(m1,m2):
    for k in m1.mapping.keys():
        if k in m2.mapping: return False
    return True

def load_mapping(name):
    new_mapping = None
    for o in composite_options:
        if o.name == name:
            o.enabled = True
            new_mapping = o
            break
    for o in composite_options:
        if (not o.fundamental) and o != new_mapping:
            if not mappings_consistent(new_mapping, o):
                o.enabled = False
    update_composition()

def unload_mapping(name):
    for o in composite_options:
        if o.name == name:
            if not o.fundamental:
                o.enabled = False
                update_composition()
                break

def reset_mappings():
    for o in composite_options:
        o.enabled = o.fundamental
    update_composition()


executive_mapping = {}
def register_mapping(n):
    executive_mapping["engage " + n] = Function(lambda: load_mapping(n))
    executive_mapping["chill " + n] = Function(lambda: unload_mapping(n))

for m in composite_options: 
    if not m.fundamental:
        register_mapping(m.name)
executive_mapping["chill everything"] = Function(reset_mappings)


executive_rules= MappingRule(
    name="executive",    # The name of the rule.
    mapping=executive_mapping,
    )
exec_grammar.add_rule(executive_rules)

dictation_rule = MappingRule(
    name="dictation",    # The name of the rule.
    mapping={          # The mapping dict: spec -> action.
        "scream <text>":          Function(yell_text),
        "jive <text>":          Function(lisp_text),
        "say <text>": Text("%(text)s"),
        "sentence <text>": Function(sentence_text),
        "camel <text>": Function(camel_case_text),
        "studley <text>": Function(big_camel_case_text),
        "score <text>": Function(rich_case_text),
        "humble <text>": Function(big_rich_case_text),
        "dote <text>": Function(dot_case_text),
        "moth <text>": Function(big_dot_case_text),
        "<text>": Function(process_dictation),
        #        "compile <text>":           Key("a-colon")+Text("(compile \"make %(text)s\")")+Key("enter"),
    },
    extras=[           # Special elements in the specs of the mapping
            Dictation("text",format=False)
           ])


dictation_grammar.add_rule(dictation_rule)


#---------------------------------------------------------------------------
# Load the grammar instance and define how to unload it.

for g in gunits:
    g.load()

# Unload function which will be called by natlink at unload time.
def unload():
    global gunits
    if gunits:
        for g in gunits:
            g.unload()
    gunits = None
    global composite_grammar
    composite_grammar.unload()
    composite_grammar = None

