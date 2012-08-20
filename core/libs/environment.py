import re

try:
    import readline
except ImportError:
    print '\n[!] The "readline" module is required to provide elaborate line editing and history features'
else:
    pass

from modules.info import info

COMMANDS = info.available_commands
RE_SPACE = re.compile('.*\s+$', re.M)


#http://stackoverflow.com/questions/5637124/tab-completion-in-pythons-raw-input
class Completer(object):
    '''
    internal readline buffer to determine the state of the overall completion,
    which makes the state logic a bit simpler
    '''
    def complete(self, text, state):
        "Generic readline completion entry point."
        buffer = readline.get_line_buffer()
        line = readline.get_line_buffer().split()
        # show all commands
        if not line:
            return [c + ' ' for c in COMMANDS][state]
        # account for last argument ending in a space
        if RE_SPACE.match(buffer):
            line.append('')
        # resolve command to the implementation function
        cmd = line[0].strip()
        if cmd in COMMANDS:
            impl = getattr(self, 'complete_%s' % cmd)
            args = line[1:]
            if args:
                return (impl(args) + [None])[state]
            return [cmd + ' '][state]
        results = [c + ' ' for c in COMMANDS if c.startswith(cmd)] + [None]
        return results[state]

    def tab(self):
        # to work with non nix systems
        try:
            readline.set_completer_delims(' \t\n;')
            readline.parse_and_bind("tab: complete")
            readline.set_completer(self.complete)
        except:
            pass

complete = Completer()
