from collections import defaultdict, namedtuple

# assert tape.startswith('mctf{')
# assert tape[-1] == '}'
# tape = list(tape)
# position = 0
# state = 1
# while state != 0:
#    letter, move, state = table[(state, tape[position])]
#    tape[position] = letter
#    if move == 'L': position -= 1
#    elif move == 'R': position += 1
# result = ''.join(tape)
# print(result)
# 8qxe78ui}2kcvn3kjg7km2tl7hc0o{xs


def move_c(c):
    return {'S': 0, 'L': -1, 'R': 1}[c]


Kek = namedtuple('Kek', 'c,move,state,from_state,from_c')


with open('1939.csv') as f:
    d = f.readlines()

head = d.pop(0)
head = head.strip().split(',')
head.pop(0)
sub = defaultdict(dict)
reversed = defaultdict(dict)
ends = []
al = []
for row in d:
    row = row.strip().split(',')
    state = int(row.pop(0))
    for c, x in zip(head, row):
        s = sub[state][c] = Kek(x[0], move_c(x[1]), int(x[2:]), state, c)
        # reversed[s.state][s.c] = Kek(s.from_c, s.move*-1, s.from_state, s.state, s.c)
        if s.c in reversed[s.state]:
            raise None
        reversed[s.state][s.c] = s
        al.append(s)
        if s.state == 0:
            ends.append(s)
del c, d, f, state, x


def search_ways(tape, state, position):
    res = []
    for shift in [-1, 0, 1]:
        pos = position + shift
        if pos < 0 or pos >= len(tape):
            continue
        c = tape[pos]
        if (c == '}' and pos == 31) or c not in reversed[state]:
            continue
        s = reversed[state][c]
        if s.move == -shift:
            res.append(shift)
    return res


def dfs(tape, state, position):
    while position != 0 and state != 1:
        _, _, _, state, letter = reversed[state][tape[position]]
        del _
        tape[position] = letter
        shifts = search_ways(tape, state, position)
        if len(shifts) == 0:
            return
        if len(shifts) > 1:
            for shift in shifts[1:]:
                dfs(tape.copy(), state, position + shift)
        position += shifts[0]
    print(''.join(tape))


tape = list('8qxe78ui}2kcvn3kjg7km2tl7hc0o{xs')
state = 0
position = len(tape) - 1
dfs(tape, state, position)


