import pickle
from queue import Queue

final_state = ((1, 2, 3), (8, 0, 4), (7, 6, 5))

def index_0(state):
    for i in range(3):
        if 0 in state[i]:
            return (state[i].index(0), i)

def swap(state, src_index, dst_index):
    src_x, src_y = src_index
    dst_x, dst_y = dst_index
    src = state[src_y][src_x]
    dst = state[dst_y][dst_x]
    mut = list(map(list, state))
    mut[dst_y][dst_x] = src
    mut[src_y][src_x] = dst
    return tuple(map(tuple, mut))

def next_states(state):
    x, y = index_0(state)
    if x >= 1:
        yield swap(state, (x, y), (x-1, y))
    if x <= 1:
        yield swap(state, (x, y), (x+1, y))
    if y >= 1:
        yield swap(state, (x, y), (x, y-1))
    if y <= 1:
        yield swap(state, (x, y), (x, y+1))

def format_state(state):
    return '\n'.join(''.join(map(str, line)) for line in state)

def make_table():
    all_states = {}
    boundary = Queue()
    boundary.put((None, final_state))
    while not boundary.empty():
        parent, state = boundary.get()
        all_states[state] = parent
        for next_state in next_states(state):
            if next_state not in all_states:
                boundary.put((state, next_state))
        if len(all_states)%10000==0:
            print(len(all_states))
    print('Last state reached: {}'.format(format_state(state)))

    pickle.dump(all_states, open('table.pkl', 'wb'))
    return all_states

def load_table():
    return pickle.load(open('table.pkl', 'rb'))

def path_to_victory(state, all_states):
    if state == final_state:
        return [final_state]
    else:
        return [state] + path_to_victory(all_states[state], all_states)

def parse_state(str_state):
    ints = [int(c) for c in str_state]
    return (tuple(ints[:3]), tuple(ints[3:6]), tuple(ints[6:]))

if __name__ == '__main__':
    try:
        all_states = load_table()
    except IOError:
        print('Generating table...')
        all_states = make_table()
        print('Table created.\n\n')

    message = """Write your current state as a list of 9 numbers,
with no spaces and the empty tile as 0:
"""
    state = parse_state(input(message))

    if state not in all_states:
        print('Unreachable state.')
        exit()

    steps = path_to_victory(state, all_states)
    print('\n v\n'.join(format_state(s) for s in steps))
    print('\n\n{} steps to victory.'.format(len(steps)))
