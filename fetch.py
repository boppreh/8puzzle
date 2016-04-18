from make_table import *

user_line = input('Write your current state as a list of 9 numbers,\nwith no spaces and the empty tile as 0:\n')
state_str = [user_line[:3], user_line[3:6], user_line[6:]]
state_list = [[int(i) for i in line] for line in state_str]
state = tuple(map(tuple, state_list))
print('')
print_state(state)

all_states = load_all_states()

length = 0
while state != final_state:
    print()
    print(' v ')
    print()
    state = all_states[state]
    print_state(state)
    length += 1

print('\n\n{} steps to victory.'.format(length))
