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

def print_state(state):
    print('\n'.join(''.join(map(str, line)) for line in state))

def load_all_states():
    return pickle.load(open('all.pkl', 'rb'))

if __name__ == '__main__':
    all_states = {}
    boundary = Queue()
    boundary.put((None, final_state))
    while not boundary.empty():
        parent, state = boundary.get()
        all_states[state] = parent
        for next_state in next_states(state):
            if next_state not in all_states:
                boundary.put((state, next_state))
        if len(all_states)%1000==0:
            print(len(all_states), boundary.qsize())

    pickle.dump(all_states, open('all.pkl', 'wb'))
    print(state)
