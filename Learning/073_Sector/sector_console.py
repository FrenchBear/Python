# sector_console.py
# Run sector game in text mode using console
#
# 2020-08-21    PV
# 2025-08-22    PV      Fixed set_sub_dir_N/_E not existing anymore

import sector_engine
import re

se = sector_engine.sector_engine()


def direction(dir_N: int, dir_E: int) -> str:
    i = (dir_N+1)*3+(dir_E+1)
    return ['SW', 'S ', 'SE', 'W ', '0', 'E ', 'NW', 'N ', 'NE'][i]


def print_help():
    print('Sector Commands:')
    print('  q, quit:     Terminate game')
    print('  h, help, ?:  Show help')
    print('  b, boats:    Show boats status')
    print('  n, next:     Select next boat, move submarine')
    print('  r, range:    Show distance from current boat')
    print('  s#, speed#:  Set current boat speed from 0 to 9')
    print('  dXX, dirXX:  Set compass direction to XX, where XX in E, NE, N, NW, W, SW, S, SE')
    print('  m, move:     Move current boat')
    print('  fXX, fireXX: Set fire direction to XX, where XX in E, NE, N, NW, W, SW, S, SE')
    print('  f#, fire#:   Fire sub at given depth, from 1 to 3')
    print('  t, teach:    Set teach mode')
    print('  e, evasive:  Set evasive mode')
    print('  show:        Show boats and sub info (warning: cheat!)')
    print('  test:        Dev command, set up predefined game situation')


def show_sub():
    print(f'sub:    {se.sub_N}N {se.sub_E}E dir={direction(se.sub_dir_N, se.sub_dir_E)} depth={se.sub_depth}')
    if se.sub_evasive:
        print('Sub in evasive mode')


def show_boat(b: int):
    print(
        f'boat {b+1}: {se.boat_N[b]}N {se.boat_E[b]}E dir={direction(se.boat_dir_N[b], se.boat_dir_E[b])} speed={se.boat_speed[b]}')


def run_console():
    print('Sector hunt starts!')
    while True:
        print()
        show_boat(se.b)
        (_, infirerange) = se.get_range()
        if infirerange:
            print(f'In fire range!  Fire dir={direction(se.fire_dir_N, se.fire_dir_E)}')
        if se.moved:
            print('Boat already moved')
        if se.fired:
            print('Boat already fired')

        print()
        rep = str.lower(str(input(f'[{se.b+1}] Command? ')))

        if rep == 'q' or rep == 'quit':
            break

        if rep == 'h' or rep == 'help' or rep == '?':
            print_help()
            continue

        if rep == 'b' or rep == 'boats':
            for b in range(4):
                print(
                    f'boat {b+1}: N={se.boat_N[b]} E={se.boat_E[b]} dir={direction(se.boat_dir_N[b], se.boat_dir_E[b])} speed={se.boat_speed[b]}')
            continue

        if rep == 'n' or rep == 'next':
            se.next_boat()
            continue

        if rep == 'r' or rep == 'range':
            (rng, infirerange) = se.get_range()
            print(f'Range: {rng}')
            if infirerange:
                print('In fire range!')
            continue

        if ma := re.fullmatch(r'(s|speed) *([0-9])', rep):
            s = int(ma.group(2))
            if se.set_speed(s):
                print('Speed set successfully')
            else:
                print('Error setting speed')
            continue

        if ma := re.fullmatch(r'(d|dir) *(e|ne|n|nw|w|sw|s|se)', rep):
            dir = str.lower(ma.group(2))
            ddir_N = {'e': 0, 'ne': 1, 'n': 1, 'nw': 1, 'w': 0, 'sw': -1, 's': -1, 'se': -1}
            ddir_E = {'e': 1, 'ne': 1, 'n': 0, 'nw': -1, 'w': -1, 'sw': -1, 's': 0, 'se': 1}
            dir_N = ddir_N.get(dir, -2)
            dir_E = ddir_E.get(dir, -2)
            if se.set_dir(dir_N, dir_E):
                print('Direction set successfully')
            else:
                print('Error setting direction')
            continue

        if rep == 'm' or rep == 'move':
            if se.moved:
                print('Already moved!')
                continue
            (status, success) = se.move()
            if success:
                print('Boat moved successfully')
            else:
                print(f'Error moving boat: {status}')
            continue

        if ma := re.fullmatch(r'(f|fire) *(e|ne|n|nw|w|sw|s|se)', rep):
            dir = str.lower(ma.group(2))
            ddir_N = {'e': 0, 'ne': 1, 'n': 1, 'nw': 1, 'w': 0, 'sw': -1, 's': -1, 'se': -1}
            ddir_E = {'e': 1, 'ne': 1, 'n': 0, 'nw': -1, 'w': -1, 'sw': -1, 's': 0, 'se': 1}
            dir_N = ddir_N.get(dir, -2)
            dir_E = ddir_E.get(dir, -2)
            if se.set_fire_dir(dir_N, dir_E):
                print('Fire direction set successfully')
            else:
                print('Error setting fire direction')
            continue

        if ma := re.fullmatch(r'(f|fire) *([1-3])', rep):
            depth = int(ma.group(2))
            (status, success) = se.fire(depth)
            if success:
                print('Fire result: ', status)
            else:
                print('Error firing: ', status)
            continue

        if ma := re.fullmatch(r'(j|jump) *(\d\d)(,|( +))(\d\d)', rep):
            new_N = int(ma.group(2))
            new_E = int(ma.group(5))
            if se.jump(new_N, new_E):
                print('Jump successful')
            else:
                print('Jump failed')
            continue

        if rep == 't' or rep == 'teach':
            se.teach_mode()
            print('Teach mode started')
            continue

        if rep == 'e' or rep == 'evasive':
            se.set_evasive_mode()
            print('Sub in evasive mode')
            continue

        if rep == 'show':
            show_sub()
            for i in range(4):
                show_boat(i)
            continue

        if rep == 'test':
            se.sub_N = 32
            se.sub_E = 31
            se.set_sub_dir(5)
            show_sub()
            se.next_boat()
            show_sub()
            se.next_boat()
            show_sub()
            se.next_boat()
            show_sub()
            se.next_boat()
            show_sub()
            continue

        print('Unknown command, enter h for help')


if __name__ == '__main__':
    run_console()
