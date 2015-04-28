from dragonfly import *


password_grammar = Grammar("password")
password_dictionary = {}
for line in open("C:/natlink/natlink/macrosystem/passwords", "r"):
    parts = line.split("|")
    password_dictionary[parts[0]] = Text(parts[1].rstrip())
    
password_rule = MappingRule(
    name="passwords",    # The name of the rule.
    mapping=password_dictionary)

password_grammar.add_rule(password_rule)
password_grammar.load()

def reload_dragonfly():
    w = Window.get_foreground()
    FocusWindow(executable = "natspeak",
                title = "Messages from Python Macros").execute()
    Pause("10").execute()
    Key("a-f, r").execute()
    Pause("10").execute()
    w.set_foreground()

window_grammar = Grammar("window_grammar")
window_rule = MappingRule(name = "window_rule",mapping = {
    "switch window": Key("a-tab"),
    "putty full-screen": Key("a-enter"),
#not working    "reset dragonfly": Function(reload_dragonfly),
    "snore": Mimic("go to sleep")})

window_grammar.add_rule(window_rule)
window_grammar.load()

def unload():
    global password_grammar
    if password_grammar:
        password_grammar.unload()
        password_grammar = None
    global window_grammar
    if window_grammar:
        window_grammar.unload()
        window_grammar = None
