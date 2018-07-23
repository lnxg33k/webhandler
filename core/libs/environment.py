try:
    import readline
except ImportError:
    print '\n[!] The "readline" module is required to provide elaborate line editing and history features'
else:
    pass


class ARLCompleter:
    def __init__(self, logic):
        self.logic = logic

    def traverse(self, tokens, tree):
        if tree is None:
            return []
        elif len(tokens) == 0:
            return []
        if len(tokens) == 1:
            return [x + ' ' for x in tree if x.startswith(tokens[0])]
        else:
            if tokens[0] in tree.keys():
                return self.traverse(tokens[1:], tree[tokens[0]])
            else:
                return []
        return []

    def complete(self, text, state):
        try:
            tokens = readline.get_line_buffer().split()
            if not tokens or readline.get_line_buffer()[-1] == ' ':
                results = [x + ' ' for x in list(logic[tokens[0]]) if x.startswith(text)] + [None]
                return results[state]
                tokens.append()
            results = self.traverse(tokens, self.logic) + [None]
            return results[state]
        except Exception:
            pass

logic = {
         '@brute':
         {
          'mysql': None,
          'ftp': None,
          },
         '@enum':
         {
          'group': None,
          'history': None,
          'network': None,
          'os': None,
          'passwd': None,
          'system': None,
          'writable': None,
          },
         '@backdoor':
         {'bash': None,
          'msf': None,
          'perl': None,
          'php': None,
          'netcat': None,
          'python': None,
          'ruby': None,
          'spread': None,
          },
         '@info': {},
         '@update': {},
         '@download': {},
         '@upload': {},
         '@history': {},
         'exit': {},
         'clear': {},
         'banner': {},
         '@mysql': {},
         '@scan': {},
         ':alias': {},
         }

readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
completer = ARLCompleter(logic)
