
# Damselfly Copyright (C) 2013 Tristen Hayfield GNU GPL 3+
#
# Damselfly is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Damselfly is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Damselfly.  If not, see <http://www.gnu.org/licenses/>.

import natlinkstatus

import sys
import re

from dragonfly import *

from dragonfly.actions.action_base import DynStrActionBase


import natlinkstatus

import sys
import re

from dragonfly import *

from dragonfly.actions.action_base import DynStrActionBase


myName = 'Damselfly'
myVersion='2013-09-30'
myID = myName + ' v. ' + myVersion 
print myID

## need to figure out where natlink resides
status = natlinkstatus.NatlinkStatus()

# fifos to SnapDragonServer

## is this a reasonable way of divining the natlink path?
natLinkPath = status.getCoreDirectory().rstrip('core')

serverOut = natLinkPath + 'damselServerOut'
serverIn = natLinkPath + 'damselServerIn'

connected = False
fpO = None
fpI = None

windowCache = {}

class ConnectionDropped(Exception):
    def __init__(self, value = None):
        self.value = value
    def __str__(self):
        return repr(self.value)

class CommandFailure(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def connect():
    global fpO, fpI, connected

    if not connected:
        try:
            print 'Attempting to open input fifo from server (could block)... ',
            sys.stdout.flush()

            fpI = open(serverOut, 'rU')
            print 'Success'

            print 'Attempting to open output fifo to server (could block)... ',
            sys.stdout.flush()

            fpO = open(serverIn, 'w')
            print 'Success'
            connected = True

            print 'Sending greeting (could block)... ',
            fpO.write(myID+'\n')
            fpO.flush()
            print 'Success'

            print 'Waiting for response (could block)... ',
            response = fpI.readline()
            print 'Success, response :', response

        except IOError as ee:
            print 'IOError: ', ee
            disconnect()
        except:
            print 'Unknown error: ', sys.exc_info()[0]
            disconnect()


def disconnect():
    global fpO, fpI, connected

    if fpO is not None:
        fpO.close()
        fpO = None

    if fpI is not None:
        fpI.close()
        fpI = None

    print 'Disconnected'

    connected = False

def resumeServer():
    if connected:
        try:
            fpO.write('doResume\n')
            fpO.flush()

            res = fpI.readline().strip()

            if res != 'Success':
                raise CommandFailure(res)
        except (CommandFailure, KeyboardInterrupt, IOError) as e:
            print "caught exception:" +  str(e) + 'aborting and disconnecting'
            disconnect()
            raise ConnectionDropped()

def getXCtx():
    if connected:
        try:
            print 'Requesting X context... ',
            fpO.write('getXCtx\n')
            fpO.flush()
            print 'request sent'

            xctx = []
            print 'waiting for response... ',
            xctx.append(fpI.readline().strip())
            if xctx[0].startswith('Failure'):
                raise CommandFailure(xctx[0])
            xctx.append(fpI.readline().strip())
            xctx.append(int(fpI.readline().strip()))
            print 'response received: ', xctx
            return xctx
        except (KeyboardInterrupt, IOError) as e:
            print "caught exception:" +  str(e) + 'aborting and disconnecting'
            disconnect()
            raise ConnectionDropped()

# custom contexts

def reCmp(pattern, string):
    return pattern.search(string) is not None

def strCmp(sub, string):
    return sub in string

class XAppContext(Context):
    def __init__(self, wmname = None, wmclass = None, wid = None, usereg = False):
        self.wmname = wmname
        
        if wmclass is None:
            self.wmclass = wmname
            self.either = True
        else:
            self.wmclass = wmclass
            self.either = False
                
        self.wid = wid

        if usereg:
            self.myCmp = reCmp

            if self.wmname:
                self.wmname = re.compile(self.wmname)

            if self.wmclass:
                self.wmclass = re.compile(self.wmclass)

        else:
            self.myCmp = strCmp

        self.emptyCtx = (wmname is None) & (wmclass is None) & (wid is None) 
        self._str = "name: " + str(wmname) + ", " + "class: " + str(wmclass) + ", " + "id: " + str(wid)


    def matches(self, executable, title, handle):
        if connected:
            if self.emptyCtx:
                return True
            else :
#                if (executable != '') or (title != '') or (handle != 0):
#                    return False
        
                iMatch = True        

                try:
                    ctx = getXCtx()
                except CommandFailure:
                    resumeServer()
                    return False
                except ConnectionDropped:
                    return False

                if self.either:
                    iMatch &= self.myCmp(self.wmname, ctx[0]) | self.myCmp(self.wmclass, ctx[1])
                else:
                    if self.wmname:                   
                        iMatch &= self.myCmp(self.wmname, ctx[0])

                    if self.wmclass:
                        iMatch &= self.myCmp(self.wmclass, ctx[1])
                
                    
                if self.wid:
                    iMatch &= (ctx[2] == self.wid)

                return iMatch
        else :
            return False

# custom actions: prepare for the babbyscape
def dispatchAndHandle(mess):
    if connected:
        try:
            print 'sending request'
            fpO.write(mess)
            fpO.flush()
            print 'request sent'
            print 'waiting for response... ',
            res = fpI.readline().strip()
            print 'response received: ', res
        
            if res.startswith('Failure'):
                raise CommandFailure(res)
            elif res != 'Success':
                raise Exception(res)

        except CommandFailure as e:
            print 'Execution failed: ' + str(e)
            return False
        except (KeyboardInterrupt, IOError) as e:
            print "Caught exception:" +  str(e) + ': aborting and disconnecting'
            disconnect()
            raise ConnectionDropped()
    else:
        return False

class FocusXWindow(DynStrActionBase):
    def __init__(self, spec, search = None, static = False):
        DynStrActionBase.__init__(self, spec = spec, static = static)
        if not search:
            self.search = 'any'
        else:
            self.search = str(search)

    def _execute_events(self, events):
        if (self.search == 'any') and (self._pspec in windowCache):
            mymess = 'focusXWindow\n' + 'id' + '\n' + windowCache[self._pspec] + '\n'
        else:
            mymess = 'focusXWindow\n' + self.search + '\n' + str(self._pspec) + '\n'
        return(dispatchAndHandle(mymess))

    def _parse_spec(self, spec):
        self._pspec = spec
        return self

class HideXWindow(DynStrActionBase):
    def __init__(self, spec = None, search = None, static = False):
        DynStrActionBase.__init__(self, spec = str(spec), static = (spec is None))
        if not search:
            self.search = 'any'
        else:
            self.search = str(search)

    def _execute_events(self, events):
        if (self.search == 'any') and (self._pspec in windowCache):
            mymess = 'hideXWindow\n' + 'id' + '\n' + windowCache[self._pspec] + '\n'
        else:
            mymess = 'hideXWindow\n' + self.search + '\n' + str(self._pspec) + '\n'
        return(dispatchAndHandle(mymess))

    def _parse_spec(self, spec):
        self._pspec = spec
        return self

class CacheXWindow(DynStrActionBase):
    def __init__(self, spec, static = False, forget = False):
        DynStrActionBase.__init__(self, spec = str(spec), static = static)
        self.search = 'id'
        self.forget =  forget

    def _execute_events(self, events):
        global windowCache
        if not self.forget:            
            xctx = getXCtx()
            if xctx:
                windowCache[self._pspec] = str(xctx[2])
            else:
                return False
        else:
            if self._pspec == 'all':
                windowCache = {}
            elif self._pspec in windowCache:
                del windowCache[self._pspec]
            else:
                return False
            
    def _parse_spec(self, spec):
        self._pspec = spec
        return self


class BringXApp(ActionBase):
    def __init__(self, execname, winname = None, timeout = 5.0):
        ActionBase.__init__(self)
        self.execname = execname
        if winname == None:
            self.winname = execname
        else:
            self.winname = winname
        self.timeout = timeout

    def _execute(self, data=None):
        mymess = 'bringXApp\n' + self.winname + '\n' + self.execname + '\n'
        mymess += str(self.timeout) + '\n'
        return(dispatchAndHandle(mymess))

class WaitXWindow(ActionBase):
    def __init__(self, title, timeout = 5.0):
        ActionBase.__init__(self)
        self.winname = title
        self.timeout = timeout

    def _execute(self, data=None):
        mymess = 'waitXWindow\n' + self.title + '\n' + str(self.timeout) + '\n'
        return(dispatchAndHandle(mymess))

class StartXApp(ActionBase):
    def __init__(self, execname):
        ActionBase.__init__(self)
        self.execname = execname

    def _execute(self, data=None):
        mymess = 'startXApp\n' + self.execname + '\n'
        return(dispatchAndHandle(mymess))

class XKey(DynStrActionBase):
    def _execute_events(self, events):
        mymess = 'sendXKeys\n' + self._pspec + '\n'
        return(dispatchAndHandle(mymess))

    def _parse_spec(self, spec):
        self._pspec = spec
        return self

class XMouse(DynStrActionBase):
    def _execute_events(self, events):
        mymess = 'sendXMouse\n' + self._pspec + '\n'
        return(dispatchAndHandle(mymess))

    def _parse_spec(self, spec):
        self._pspec = spec
        return self

## neither autoformat nor pause are considered atm
class XText(DynStrActionBase):
    def __init__(self, spec, static = False, space = True, title = False, upper = False):
        DynStrActionBase.__init__(self, spec = str(spec), static = static)
        self.space = space
        self.title = title
        self.upper = upper

    def _parse_spec(self, spec):
        self._pspec = spec
        return self

    def _execute_events(self, events):
        tspec = self._pspec
        if self.title:
            tspec = tspec.title()
        elif self.upper:
            tspec = tspec.upper()
            
        if not self.space:
            tspec = tspec.replace(' ','')

        #tspec = tspec.replace('\\','\\backslash ')
        # split on newlines
        tspec = tspec.split("\n")
        success = True
        for j,ts in enumerate(tspec):
            if len(tspec) > 1 and j > 0:
                dispatchAndHandle('sendXKeys\nenter\n')
            mymess = 'sendXText\n' + ts + '\n'
#            print mymess
            success = dispatchAndHandle(mymess) and success
        return success
#        return(dispatchAndHandle(mymess))

class ShellCommand(DynStrActionBase):
    def __init__(self, spec, static = False):
        DynStrActionBase.__init__(self, spec = str(spec), static = static)

    def _parse_spec(self, spec):
        self._pspec = spec
        return self

    def _execute_events(self, events):
        tspec = self._pspec

        #tspec = tspec.replace('\\','\\backslash ')
        return dispatchAndHandle('manual\n' + tspec.strip() + '\n')
    

class DoNothing(ActionBase):
    def __init__(self, message = 'Recognition event consumed.'):
        self.message = message
        
    def _execute(self, data=None):
        print self.message
        
# custom grammars



# rules
class ConnectRule(CompoundRule):
    spec = "damselfly connect"

    def _process_recognition(self, node, extras):
        connect()

class DisconnectRule(CompoundRule):
    spec = "damselfly disconnect"

    def _process_recognition(self, node, extras):
        disconnect()

class ResumeRule(CompoundRule):
    spec = "damselfly resume"

    def _process_recognition(self, node, extras):
        resumeServer()
        print 'Resumed.'


# rudimentary wm control
class WMRule(MappingRule):
    mapping = {
        "win hide" : HideXWindow(),
        "launch Emacs": XKey("w-e"),
        "launch terminal": XKey("w-t"),
        "launch Firefox": XKey("w-w") + Function(lambda *ignore: load_mapping("Firefox")),
        "snore": Mimic("go to sleep"),
        "switch window": XKey("a-tab"),
        "win hide <text>" : HideXWindow("%(text)s"),
        "win cache <text>" : CacheXWindow("%(text)s"),
        "win forget <text>" : CacheXWindow("%(text)s", forget = True),
        "win focus <text>" : FocusXWindow("%(text)s"),
        "wort right": XKey("ca-right"),
        "wort left": XKey("ca-left"),
        }
    extras = [
        Dictation("text")
        ]
    
# these rules consume events which could cause dragon to hang or behave
# strangely in linux

class DNSOverride(MappingRule):
    mapping = {
        "type [<text>]" : DoNothing(),
        "MouseGrid [<text>]" : DoNothing(),
        "mouse [<text>]" : DoNothing(),
        "copy [(that | line)]" : DoNothing(),
        }
    extras = [
        Dictation("text")
        ]




def capitalizeFirst(w):
    return w[0].upper()+w[1:]

def process_dictation(text):
    XText(' '.join(map(removeAnnotations,text.words))).execute()


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
    XText(newText).execute()

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
    XText(newText).execute()

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
    XText(newText).execute()


def lisp_text(text):
    newText = ''
    for word in text.words:
        word = removeAnnotations(word)
        if len(word)  < 1: pass
        elif newText == '':
            newText = word.lower()
        else:
            newText = '%s-%s' % (newText, word.lower())
    return XText(newText).execute()

def dot_case_text(text):
    newText = ''
    for word in text.words:
        word = removeAnnotations(word)
        if len(word)  < 1: pass
        elif newText == '':
            newText = word.lower()
        else:
            newText = '%s.%s' % (newText, word.lower())
    return XText(newText).execute()

def big_dot_case_text(text):
    newText = ''
    for word in text.words:
        word = removeAnnotations(word)
        if len(word)  < 1: pass
        elif newText == '':
            newText = capitalizeFirst(word)
        else:
            newText = '%s.%s' % (newText, capitalizeFirst(word))
    return XText(newText).execute()

def big_camel_case_text(text):
    newText = _bigcamelify(text.words)
    XText(newText).execute()

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
    XText(newText).execute()

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
    XText(newText).execute()

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



composite_options = []

class Mapping:
    def __init__(self, name=None, mapping=None, fundamental = False):
        global composite_options
        composite_options.append(self)
        self.name = name
        # split atomic from composite actions
        c = {}
        a = {}
        for k,v in mapping.iteritems():
            if '<text>' in k or '<a>' in k:
                a[k] = v
            else:
                c[k] = v
        self.mapping = c
        self.atomic = a
        self.fundamental = fundamental
        self.enabled = fundamental




# code for spelling out individual letters

letters = {
    "aff": 'a',
    "brav": 'b',
    "cai": 'c',
    "delt": 'd',
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
    "osc": 'o',
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
    letter_rules[k] = XKey(l)
    letter_rules["cap "+k] = XKey('s-'+l)
    letter_rules["control "+k] = XKey('c-'+l)
    letter_rules["meta "+k] = XKey('a-'+l)
    letter_rules["option "+k] = XText(" -")+XKey(l)+XText(" ")
    letter_rules["option cap "+k] = XText(" -")+XKey('s-'+l)+XText(" ")

alpha_mapping = Mapping(
    fundamental = True,
    name="keyboard",    # The name of the rule.
    mapping=dict(list(letter_rules.items()) + list({
        # dictation
        "scream <text>":          Function(yell_text),
        "jive <text>":          Function(lisp_text),
        "say <text>": XText("%(text)s"),
        "sentence <text>": Function(sentence_text),
        "camel <text>": Function(camel_case_text),
        "studley <text>": Function(big_camel_case_text),
        "score <text>": Function(rich_case_text),
        "humble <text>": Function(big_rich_case_text),
        "dote <text>": Function(dot_case_text),
        "moth <text>": Function(big_dot_case_text),
        "<text>": Function(process_dictation),
        # keys
        "meta blank": Function(lambda *ignore: ShellCommand("xdotool key Alt").execute()),
        "dole sword": XKey("Delete"),
        "lace": XText("{"),
        "race": XText("}"),
        "lark": XText("("),
        "fark": XText(")"),
        "lack": XText("["),
        "rack": XText("]"),
        "see sale": XText("csail"),
        "MIT EDU": XText("mit.edu"),
        "page up": XKey("pgup"),
        "page down": XKey("pgdown"),
        "circle":             XKey("lparen, rparen, left"),
        "box":             XKey("lbracket, rbracket, left"),
        "diamond":             XKey("langle, rangle, left"),
        "curl":             XKey("lbrace, rbrace, left"),
        "string": XText("\"\"") + XKey("left"),
        "rabbit": XText("''") + XKey("left"),
        "snake":          XKey("tab"),
        "spin": XKey("enter")+XKey("tab"),
        "row": XKey("enter"),
        "money": XText("$"),
        "dack":          XKey("backslash"),
        "dot":          XKey("dot"),
        "comma":        XKey("comma"),
        "per": XKey("percent"),
        "colon":        XKey("colon"),
        "amp": XKey("ampersand"),
        "divide":          XKey("space") + XKey("slash") + XKey("space"),
        "plus":           XKey("space,plus,space"),
        "minus":          XKey("space,minus,space"),
#        "wager":          XKey("space") + XKey("s-dot") + XText("=") + XKey("space"),
#        "Weiner":           XKey("space") + XKey("s-comma") + XText("=") + XKey("space"),
        "carrot": XKey("s-6"),
        "phone": XText("@"),
        "congo":          XKey("space") + XKey("equal") + XKey("equal") + XKey("space"),
        "diff go": XText(" != "),
        "equals":          XKey("space") + XKey("equal") + XKey("space"),
        "dash": XKey("minus"),
        "cross": XKey("plus"),
        "increment": XText(" += "),
        "decrement": XText(" -= "),
        "splat":          XKey("asterisk"),
        "slash":          XKey("slash"),
        "hash":          XKey("hash"),
        "wave": XKey("tilde"),
        "pipe":           XKey("bar"),
        "wink": XText(";"),
        "bang": XText("!"),
        "query": XText("?"),
        "sub": XText("_"),
        "quote":        XKey("dquote"),
        "spark":        XKey("squote"),
        "inject":        XKey("backtick"),
        "dash": XText("-"),
        "ace": XKey("space"),
        "fun one": XKey("f1"),
        "fun two": XKey("f2"),
        "fun three": XKey("f3"),
        "fun four": XKey("f4"),
        "fun five": XKey("f5"),
        "fun six": XKey("f6"),
        "fun seven": XKey("f7"),
        "fun eight": XKey("f8"),
        "fun nine": XKey("f9"),
        "fun ten": XKey("f10"),
        "fun eleven": XKey("f11"),
        "fun twelve": XKey("f12"),
        "zero": XText("0"),
        "one": XText("1"),
        "two": XText("2"),
        "three": XText("3"),
        "four": XText("4"),
        "five": XText("5"),
        "six": XText("6"),
        "seven": XText("7"),
        "eight": XText("8"),
        "nine": XText("9"),
        "zero": XText("0"),
        "up":        XKey("up"),
        "down":          XKey("down"),
        "left":        XKey("left"),
        "right":          XKey("right"),
    }.items())))

def tab_Firefox(a,b = None,c = None,d = None,e = None,f = None):
    k = "xdotool keydown Alt key "
    for argument in [a,b,c,d,e,f]:
        if argument != None:
            k += str(argument) + " "
    k += "keyup Alt"
    ShellCommand(k).execute()

def touch_Firefox(a,b = None,c = None,d = None,e = None,f = None):
    k = "xdotool keydown Control key "
    for argument in [a,b,c,d,e,f]:
        if argument != None:
            k += str(argument) + " "
    k += "keyup Control"
    ShellCommand(k).execute()

Firefox_mapping = Mapping(
    name = "Firefox",
    mapping = {
        "touch <a> [<b>] [<c>] [<d>] [<e>] [<f>]": Function(touch_Firefox),
        "go tab <a> [<b>] [<c>] [<d>] [<e>] [<f>]": Function(tab_Firefox),
        "fire next": XKey("a-right"),
        "fire back": XKey("a-left"),
    })

def teleport(a,b = None,c = None,d = None,e = None,f = None):
    print "teleporting"
    XKey("a-g,g").execute()
    for argument in [a,b,c,d,e,f]:
        if argument != None:
            XKey(str(argument)).execute()
    XKey("enter").execute()


emacs_mapping = Mapping(
    name = "editor",
    fundamental = True,
    mapping = {
        "transp": XKey('c-t'),
        "Coconut": XKey("a-x") + XText('erase-buffer') + XKey('enter'),
        "chump dir": XKey("a-x") + XText('cd') + XKey('enter'),
        "edit voice commands": XKey("c-g, c-f") + XText("~/voice/_Damselfly.py") + XKey("enter"),
        "build file": XKey("c-c, c-c, enter"),
        "of course": XText('yes')+XKey('enter'),
        "no way": XText('no')+XKey('enter'),
        "airhead <n>": XKey("c-x, backtick")*Repeat(extra = "n"),
        "butterfly": XKey("a-x"),
        "save":            XKey("c-x, c-s"),
        "open":            XKey("c-x, c-f"),
        "apostate": XKey("c-x/10, c-c/10"),
        "mac start":            XKey("c-x, lparen"),
        "mac end":            XKey("c-x, rparen"),
        "mac do":            XKey("c-x, e"),
        "meta per":          XKey("as-5"),
        "sorch":             XKey("c-s"),
        "rorch":             XKey("c-r"),
        "hop":             XKey("c-x, o"),
        "bash":		XKey("a-x, s, h, e, l, l, enter"),
        "quit":		XKey("c-g"),
        "split veal":		XKey("c-x, 3"),
        "split holly":		XKey("c-x, 2"),
        "breathe":		XKey("c-x, 1"),
        "quit":		XKey("c-g"),
        "buff":		XKey("c-x, c-b"), #+XKey("c-x, o"),
        "paste":         XKey("c-y"),
        "scratch":         XKey("c-x, u"),
        "scratch that":         XKey("c-x, u"),
        "mara":         XKey("c-space"),
        "chop":         XKey("c-w"),
        "zap":         XKey("a-w"),
        "wipe":         XKey("c-k"),
        "lepton":         XKey("c-x, k, enter"),
        "reach":        XKey("c-e"),
        "fall":          XKey("c-a"),
        "chirp top":          XKey("c-l")*2,
        "chirp bot":          XKey("c-l")*3,
        "chirp":          XKey("c-l"),
        "zoom":          XKey("as-dot"),
        "Tele <a> [<b>] [<c>] [<d>] [<e>] [<f>]": Function(teleport),
        # used for selecting a buffer
        "Apple <n>": XKey("a-g,g") + XText("%(n)i") + XKey("enter")*2,
        "zip":          XKey("as-comma"),
        # these used to have numbers as arguments
        "club":          XKey("a-backspace"),
        "Ford": XKey("a-f"),
        "board": XKey("a-b"),
        "leap":            XKey("ca-f"),
        "trip":         XKey("ca-b"),
        "slurp": XKey("c-space")+XKey("ca-f") + XKey("a-w"),
        "snap": XKey("c-space")+XKey("ca-b") + XKey("a-w"),
        "sword": XKey('c-d'),
        "barb": XKey('backspace'),
        "pounce":        XKey("a-p"),
        # here are the same versions with a suffix indicating that they take a number
        "clubber <n>":          XKey("a-backspace") * Repeat(extra="n"),
        "upper <n>":        XKey("up") * Repeat(extra="n"),
        "downer <n>":          XKey("down") * Repeat(extra="n"),
        "Forder <n>": XKey("a-f")*Repeat(extra="n"),
        "boarder <n>": XKey("a-b")*Repeat(extra="n"),
        "lefter <n>":        XKey("left") * Repeat(extra="n"),
        "righter <n>":          XKey("right") * Repeat(extra="n"),
        "leaper <n>":            XKey("ca-f") * Repeat(extra = "n"),
        "tripper <n>":         XKey("ca-b") * Repeat(extra = "n"),
        "slurper <n>": XKey("c-space")+XKey("ca-f") * Repeat(extra = "n") + XKey("a-w"),
        "snapper <n>": XKey("c-space")+XKey("ca-b") * Repeat(extra = "n") + XKey("a-w"),
        "rower <n>":        XKey("enter") * Repeat(extra = "n"),
        "sworder <n>": XKey('c-d') * Repeat(extra = "n"),
        "barber <n>": XKey('backspace') * Repeat(extra = "n"),
        "pouncer <n>":        XKey("a-p") * Repeat(extra = "n"),
    })

python_mapping = Mapping(
    name="python",    # The name of the rule.
    mapping={          # The mapping dict: spec -> action.
        "major":          XKey("space") + XKey("s-dot") + XKey("space"),
        "minor":           XKey("space") + XKey("s-comma") + XKey("space"),
        "num P": XText("np."),
        "lambda": XText("lambda : ") + XKey("left")*2,
        "selfish": XText("self"),
        "indent right": XKey("cs-dot"),
        "indent left": XKey("cs-comma"),
        "comprehend": XText("for  in ") + XKey("left")*4,
        "for loop": XText("for  in :") + XKey("left")*5,
        "for range loop": XText("for  in range():") + XKey("left")*12,
        "for length loop": XText("for  in range(len()):") + XKey("left")*17,
        "while loop": XText("while :") + XKey("left"),
        "conditional":             XText("if :") + XKey("left"),
        "defun": XText("def ():") + XKey("left")*3,
        "return": XText("return "),
        "truth E ness": XText("True"),
        "falsity": XText("False"),
        "length": XText("len()") + XKey("left"),
        "else if":             XText("elif :") + XKey("left"),
        "otherwise": XText("else:"),
        "print": XText("print "),
        "def class": XText("class ():")+XKey("enter,tab")+XText("def __init__(self):")+XKey("up,c-e")+XKey("left")*3,
        "nunnery": XText("None"),
    })



shell_mapping = Mapping(
    name = "shell",
    mapping = {
        "S C P": XText("scp "),
        "run evince": XText("evince "),
        "putty S C P": XText("pscp "),
        "foreground <n>": XText("fg ")+XText("%(n)d")+XKey("enter"),
        "stop job": XKey("c-z"),
        "no hup": XText("nohup  &")+XKey("left,left"),
        "kit cat": XText("cat "),
        "odin":          XText("sudo -i")+XKey("enter"),
        "untar gizz": XText("tar xzvf "),
        "tar gizz": XText("tar czvf "),
        "apt get install":          XText("apt-get install "),
        "apt get remove":          XText("apt-get remove "),
        "apt cache search": XText("apt-cache search "),
        "pythonic": XText("python "),
        "grape": XText("grep "),
        "are grape": XText("rgrep "),
        "grape eye": XText("grep -i "),
        "are grape eye": XText("rgrep -i "),
        "popcorn":          XText("cd ..")+XKey("enter"),
        "explore":          XText("cd "),
        "survey":          XText("ls -lah | less")+XKey("enter"),
        "scout":           XText("ls")+XKey("enter"),
        "new folder": XText("mkdir "),
        "exit": XText("exit")+XKey("enter"),
        "Emacs": XText("emacs -nw "),
        # version control
        "get commit":           XText("git commit -a -m \"\"")+XKey("left"),
        "get push":           XText("git push")+XKey("enter"),
        "get pull":           XText("git pull")+XKey("enter"),
        "get add":           XText("git add "),
        "get branch": XText("git branch "),
        "get checkout": XText("git checkout "),
        "get log": XText("git log "),
        "get diff": XText("git diff "),
        "get clone": XText("git clone "),
        "oh camel": XText("ocaml")
    })

haskell_mapping = Mapping(
    name="haskell",    # The name of the rule.
    mapping={          # The mapping dict: spec -> action.
        "dagger": XText("DAG"),
        "data":            XText("data ")+XText(" = ")+XKey("left")*4,
             "lexical":            XText("let x = x")+XKey("enter, i, n, space, tab, up, c-e, backspace, left, left, left, backspace"),
             "type":            XText("type ")+XText(" = ")+XKey("left")*4,
             "lambda":            XKey("backslash, space, space, minus,  s-dot, space, left, left, left, left"),
             "case":            XText("case  of")+XKey("left, left, left"),
             "do":            XText("do "),
             "where":            XText("where  = ")+XKey("left, left, left"),
             "assign":            XText(" <- "),
             "infix": XText("``")+XKey("left"),
             "goes to":            XText(" -> "),
             "has type":            XText(" :: "),
             "not equal":            XText(" /= "),
             "and":             XText(" && "),
             "or":             XText(" || "),
             "not":            XText("not "),
             "compose":            XText(" . "),
             "comment":        XText(" -- "),
             "magic": XKey("ca-i"),
             "local": XKey("a-slash"),
             "temp": XKey("a-t"),
             "dollar": XText(" $ "),
             "branch":            XText("if x")+XKey("enter")+XText("then x")+XKey("enter")+XText("else x")+XKey("tab, up, tab, up, c-e, backspace, down, c-e, backspace, down, c-e, backspace, up, up"),
             "return": XText("return "),
             "import": XText("import "),
             "qualified": XText("import qualified  as ") + XKey("enter, up, c-e, left, left, left, left"),
             "module": XText("module  where") + XKey("enter, enter, up, up, c-e, left, left, left, left, left, left"),
             "bind": XText(">>="),
             "double": XText("Double"),
             "int": XText("Int"),
             "evaluate": XKey("c-c, c-l"),
             "prime": XText("'"),
            })
camel_mapping = Mapping(
    name="camel",    # The name of the rule.
    mapping={          # The mapping dict: spec -> action.
             "lexical":            XText("let  =  in")+XKey("left, left, left, left, left, left"),
        "fatal exception": XText("raise (Failure \"\")")+XKey("left, left"),
        "summary": XText("Some()") + XKey("left"),
        "nunnery": XText("None"),
             "recursive": XText("let rec "),
             "reference": XText("ref "),
             "for loop": XKey("c-c, f"),
             "while loop": XKey("c-c, w"),
             "try": XKey("c-c, t"),
             "block": XText("begin  end") + XKey("left")*4,
             "record assign":            XText(" <- "),
        "conditional": XText("if  then  else ")+XKey("left")*12,
             "print eff": XText("Printf.printf \"\"")+XKey("left"),
             "dunk": XText(";;")+XKey("enter"),
             "second": XText("snd"),
             "first": XText("fst"),
        "composition": XKey("space, percent, space"),
             "ADT type":            XText("type  = ") + XKey("left")*3,
             "lambda":            XText("fun  -> ")+XKey("left, left, left, left"),
             "match":            XText("match  with")+XKey("left, left, left, left, left"),
             "assign":            XText(" := "),
             "goes to":            XText(" -> "),
             "went to":            XText(" <- "),
             "has type":            XText(" : "),
             "not equal":            XText(" <> "),
             "and":             XText(" && "),
             "or":             XText(" || "),
             "not":            XText("not "),
             "send to": XText(" |> "),
             "apply to": XText(" @@ "),
             "append": XText(" @ "),
             "concatenate": XText(" ^ "),
             "comment":        XText("(*  *)")+XKey("left, left, left"),
             "cons": XText(" :: "),
             "int": XText("int"),
             "hash table": XText("Hashtbl."),
             "bool": XText("bool"),
             "prime": XText("'"),
             "sign": XText("sin"),
             "cosine": XText("cos"),
             "exponential": XText("exp"),
             # Merlin commands
             "inference": XKey("c-c")+XKey("c-t"),
             "erroneous":  XKey("c-c")+XKey("c-x"),
             "merlin": XKey("c-c, tab"),
             # special jetty commands
             "arrow": XText(" @> "),
            })

java_mapping = Mapping(
    name="java",    # The name of the rule.
    mapping={          # The mapping dict: spec -> action.
             "integer":            XText("int "),
        "minor": XText(" < "),
        "major": XText(" > "),
        "return": XText("return "),
             "reference": XText("ref "),
        "conditional": XText("if () {}") + XKey("left")*4,
             "for loop": XText("for (int  = ; ; ) {}") + XKey("left")*11,
             "while loop": XText("while () {}") + XKey("left")*4,
             "lodge and":             XText(" && "),
             "lodge or":             XText(" || "),
             "comment":        XText("/*  */")+XKey("left, left, left"),
            })

luau_mapping = Mapping(
    name="luau",    # The name of the rule.
    mapping={          # The mapping dict: spec -> action.
        "torch": XText("torch"),
        "conditional": XText('if  then end') + XKey('left')*9,
             "lexical":            XText("local  = ")+XKey("left, left, left"),
        "nil": XText("nil"),
        "block": XText("do  end")+XKey("left,left,left,left"),
             "for loop": XText("for  = , ")+XKey("left,left,left,left,left"),
             "while loop": XText("while  do  end")+XKey("left,left,left,left,left,left,left,left,left,left"),
             "dee fun":            XText("function ()  end")+XKey("left")*7,
        "print": XText("print()") + XKey("left"),
        "lambda":            XText("function ()  end")+XKey("left, left, left, left"),
             "not equal":            XText(" ~= "),
#        "Congo": XText(" == "),
        "return": XText("return "),
             "lodge and":             XText(" and "),
             "lodge or":             XText(" or "),
        "truth E ness": XText("true"),
        "falsity": XText("false"),
             "not":            XText("not "),
             "length": XText(" #"),
             "concatenate": XText(" .. "),
             "comment":        XText("-- "),
        "major": XText(" > "),
        "minor": XText(" < "),
            })


closure_mapping = Mapping(
    name="closure",    # The name of the rule.
    mapping={          # The mapping dict: spec -> action.
        "closure": XText("clojure"),
        "test eak": XText("(= )") + XKey("left"),
        "do seek": XText("(doseq [])") + XKey("left")*2,
        "recurse": XText("(recur )") + XKey("left"),
        "for loop": XText("(for [])") + XKey("left")*2,
        "def mac": XText("(defmacro [])") + XKey("left")*2,
        "major": XText("(> )") + XKey('left'),
        "minor": XText("(< )") + XKey('left'),
        "conditional": XText('(if )') + XKey('left')*1,
        "nil": XText("nil"),
        "truth E ness": XText("true"),
        "falsity": XText("false"),
             "not":            XText("not "),
             "comment":        XText("; "),
        "print": XText("(println )") + XKey("left"),
        "define": XText("(def )") + XKey("left"),
        "defun": XText("(defn )") + XKey("left"),
        "lambda": XText("(fn [] )") + XKey("left")*3,
        "lexical": XText("(let [])") + XKey("left")*2,
            })

latex_mapping = Mapping(
    name="latex",    # The name of the rule.
    mapping={          # The mapping dict: spec -> action.
        "english": XText("\\mbox{}")+XKey("left"),
        "summation": XText("\\sum"),
        "minipage": XText("\\begin{minipage}\n\\end{minipage}")+XKey("up, c-e")+XKey("enter"),
        "compile latex": XKey("c-c, c-c, enter"),
        "math cal": XText("\\mathcal{}") + XKey("left"),
        "emphasis": XText("\\emph{}") + XKey("left"),
        "Beemer frame": XText("\\begin{frame}{}")+XKey("enter")+XKey("enter")+XText("\\end{frame}")+XKey("up")+XKey("up")+XKey("c-e, left"),
        "infinity": XText("\\infty"),
        "supremum": XText("\\sup "),
        "infinum": XText("\\inf "),
        "member": XText("\\in "),
        "for all": XText("\\forall "),
        "there exists": XText("\\exists"),
        "power": XText("^{}")+XKey("left"),
        "compile": XKey("c-c, c-c"),
        "subsection": XText("\\subsection{}")+XKey("left"),
        "equation": XKey("backslash")+XText("begin{equation}")+XKey("enter,backslash")+XText("end{equation}")+XKey("up, c-e")+XKey("enter"),
        "equation array": XText("\\begin{eqnarray}\n\\end{eqnarray}")+XKey("up, c-e")+XKey("enter"),
        "sinusoid": XText("\\sin "),
        "cosine": XText("\\cos "),
        "math": XText("$$")+XKey("left"),
        "label": XText("\\label{}")+XKey("left"),
        "refer": XText("\\ref{}")+XKey("left"),
        "package": XText("\\usepackage{}")+XKey("left"),
        "preamble": XText("\\documentclass{article}\n\n\n\\begin{document}\n\n\n\\end{document}")+XKey("up, up"),
        "degree": XText("\\circ "),
        "citation": XText("\\cite{}")+XKey("left"),
        "compile bibliography": XKey("c-c,tab"),
        "section": XText("\\section{}")+XKey("left"),
        "figure": XText("\\begin{figure}\n\\end{figure}")+XKey("up, c-e, enter"),
        "code box": XText("\\begin{codebox}\n\\end{codebox}")+XKey("up, c-e, enter"),
        "text box": XText("\\text{}")+XKey("left"),
        "square root": XText("\\sqrt{}")+XKey("left"),
        "dack dash": XText("\\\\"),
        "fraction": XKey("backslash") + XText("frac{}{}")+XKey("left")+XKey("left")+XKey("left"),
        "itemize": XText("\\begin{itemize}\n\n\\end{itemize}")+XKey("up"),
        "if and only if": XText(" iff "),
        #Greek letters
        "alpha": XText("\\alpha"),
        "beta": XText("\\beta"),
        "theta": XText("\\theta"),
        "gamma": XText("\\gamma"),
        "mu": XText("\\mu"),
        "delta": XText("\\delta"),
    })


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


xcon = XAppContext()

exec_grammar = Grammar("exec", context=xcon)






# composite_grammar holds all of the ccr commands
composite_grammar = Grammar("composite", context = xcon) 

# atomic_grammar holds all of the commands that can't be chained together
atomic_grammar = Grammar("atomic",context = xcon)


def merge_mappings(mappings):
    c = mappings[0].mapping.copy()
    a = mappings[0].atomic.copy()
    n = mappings[0].name
    for mp in mappings[1:]:
        c.update(mp.mapping)
        a.update(mp.atomic)
        n += "+"+mp.name
    c = MappingRule(name = 'MERGE_COMPOSITE_' + n,
                    mapping = c,
                    extras = [ IntegerRef("n", 1, 100)])
    a = MappingRule(name = 'MERGE_ATOMIC_' + n,
                    mapping = a,
                    extras = [ Dictation("text",format=False),
                               IntegerRef("a", 0, 10),
                               IntegerRef("b", 0, 10),
                               IntegerRef("c", 0, 10),
                               IntegerRef("d", 0, 10),
                               IntegerRef("e", 0, 10),
                               IntegerRef("f", 0, 10),])
    return c,a

def clobber_grammar(g):
    if len(g._rules) > 0:
        g.unload()
        toremove = g._rules[:]
        for r in toremove:
            g.remove_rule(r)
    
    

def update_composition():
    global composite_grammar,atomic_grammar
    
    enabled_mappings = [ option for option in composite_options if option.enabled ]
    clobber_grammar(composite_grammar)
    clobber_grammar(atomic_grammar)
    c,a = merge_mappings(enabled_mappings)
    print c._name, a._name
    composite_grammar.add_rule(create_repetition(c))
    composite_grammar.load()
    atomic_grammar.add_rule(a)
    atomic_grammar.load()

update_composition() # load defaults

def mappings_consistent(m1,m2):
    for k in m1.mapping.keys():
        if k in m2.mapping: return False
    for k in m1.atomic.keys():
        if k in m2.atomic: return False
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




password_dictionary = {}
for line in open(natLinkPath+"passwords", "r"):
    parts = line.split("|")
    password_dictionary[parts[0]] = XText(parts[1].rstrip())
    
password_rule = MappingRule(
    name="passwords",    # The name of the rule.
    mapping=password_dictionary)


## construct one grammar to rule them all
grammar = Grammar("Damselfly")
grammar.add_rule(ConnectRule())                     
grammar.add_rule(DisconnectRule())
grammar.add_rule(ResumeRule())
grammar.add_rule(DNSOverride())
grammar.add_rule(WMRule(context = xcon))
grammar.add_rule(password_rule)

def unload():
    global xcon, windowCache

    disconnect()

    ## does this suffice?
    xcon = None
    windowCache = None
    
    if grammar.loaded:
        grammar.unload()
    global exec_grammar
    if exec_grammar:
        exec_grammar.unload()
    exec_grammar = None
    global atomic_grammar
    atomic_grammar.unload()
    atomic_grammar = None
    global composite_grammar
    composite_grammar.unload()
    composite_grammar = None





grammar.load()                                   
exec_grammar.load()
