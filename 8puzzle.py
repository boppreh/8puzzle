import pickle
from queue import Queue

final_state = (1, 2, 3,
               8, 0, 4,
               7, 6, 5)

def swap(state, src_index, dst_index):
    """ Swaps the numbers at the two given indexes. """
    s = list(state)
    s[src_index], s[dst_index] = s[dst_index], s[src_index]
    return tuple(s)

def next_states(state):
    """ Given a state generates the next (up to four) states one edit away. """
    i = state.index(0)
    if i%3 >= 1:
        yield swap(state, i, i-1)
    if i%3 <= 1:
        yield swap(state, i, i+1)
    if i//3 >= 1:
        yield swap(state, i, i-3)
    if i//3 <= 1:
        yield swap(state, i, i+3)

def str_to_state(str_state):
    """ Reads a sequence of 9 digits and returns the corresponding state. """
    assert len(str_state) == 9 and sorted(str_state) == list('012345678')
    return tuple(int(c) for c in str_state)

def pretty_print(state):
    """ Returns a 3x3 string matrix representing the given state. """
    assert len(state) == 9
    str_state = [str(i) for i in state]
    lines = [' '.join(map(str, l)) for l in [state[:3], state[3:6], state[6:]]]
    return '\n'.join(lines)

def make_table():
    """
    Generates a dict with all reachable states and their "parent" (the next
    state closest to the solution). This table has ~180000 entries and is
    persisted in a Pickle file "table.pkl".
    """
    parents = {}
    boundary = Queue()
    boundary.put((None, final_state))

    while not boundary.empty():
        parent, state = boundary.get()
        parents[state] = parent
        if len(parents)%10000==0:
            print(len(parents))

        for next_state in next_states(state):
            if next_state not in parents:
                boundary.put((state, next_state))

    print('Last state reached: {}'.format(pretty_print(state)))

    pickle.dump(parents, open('table.pkl', 'wb'))
    return parents

def load_table():
    """ Loads a previously generated table. """
    return pickle.load(open('table.pkl', 'rb'))

def path_to_victory(state, parents):
    """
    Given a path a the parents table, returns a list of the steps to solution.
    """
    if state == final_state:
        return [final_state]
    else:
        return [state] + path_to_victory(parents[state], parents)

if __name__ == '__main__':
    try:
        parents = load_table()
        print('Loaded existing table.\n\n')
    except IOError:
        print('Generating table...')
        parents = make_table()
        print('Table created.\n\n')

    while True:
        line = input('Current state (e.g. 587106324): ')
        if line.lower() in ('q', 'exit', 'quit'):
            break

        try:
            state = str_to_state(line)
        except (AssertionError, ValueError):
            print('Invalid state.\n')
            continue

        if state not in parents:
            print('Unreachable state.')
            continue

        steps = path_to_victory(state, parents)
        print('\n\n  v\n\n'.join(pretty_print(s) for s in steps))
        print('\n\n{} steps to victory.\n\n'.format(len(steps)))
