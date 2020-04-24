# -*- coding: byfon -*-
import functools
import itertools

import byfon

tp = byfon.Transpiler(optimise_clears=False)  # Known-zero optimization breaks the program and I don't know why. This makes the output file a few KB larger, but I don't know how to fix this right now.


def read_line(most):
    if most:
        values = []
        writer = tp.alloc()
        for _ in range(most):
            val = tp.alloc().read()
            if! ~val == 10:
                byfon.write_literal(writer, "... ")
            values.append(val)
    else:
        # save allocating `writer`
        values = []
    temp = tp.alloc(init=1)
    while! temp:
        temp.read()
        temp -= ord("\n")
    temp.free()
    return values

def gen_random(state):
    state <- (state * 105) + 17
    return state

def mod(cell, const):
    register = tp.alloc(init=const)
    while! cell:
        register -= 1
        if! (~register).not:
            register += const
        cell -= 1
    return const - register

def output_location(x):
    tens = tp.alloc()
    x += 1
    running = (~x != 0).and_((~x != 1).and_((~x != 2).and_((~x != 3).and_((~x != 4).and_((~x != 5).and_((~x != 6).and_((~x != 7).and_((~x != 8).and_((~x != 9))))))))))
    while! running:
        tens += 1
        x -= 10
        if! (~x == 0 or! ~x == 1 or! ~x == 2 or! ~x == 3 or! ~x == 4 or! ~x == 5 or! ~x == 6 or! ~x == 7 or! ~x == 8 or! ~x == 9):
            running -= 1
    running.free()
    if! ~tens:
        (tens + 48).write()
    (x + 48).write()

def is_repeat(cell, checks):
    check = ~cell == ~checks[0]
    for check_cell in checks[1:]:
        check = check.or_(~cell == ~check_cell)
    return check

def gen_uniq_positions(count, rngs):
    positions = []
    for _, rng in zip(range(count), itertools.cycle(rngs)):
        new_val = mod(~gen_random(rng), 20)
        if positions:
            whilex! is_repeat(new_val, positions):
                new_val <- mod(~gen_random(rng), 20)
        positions.append(new_val)
    return positions

ROOM_RELATIONS = {
    0: [1, 4, 7],
    1: [0, 2, 9],
    2: [1, 3, 11],
    3: [2, 4, 13],
    4: [3, 5, 0],
    5: [4, 6, 14], 
    6: [5, 7, 16],
    7: [6, 8, 0],
    8: [7, 9, 17],
    9: [8, 10, 1],
    10: [9, 11, 18],
    11: [10, 12, 2],
    12: [11, 13, 19],
    13: [12, 14, 3],
    14: [13, 15, 5], 
    15: [14, 16, 19],
    16: [15, 17, 6], 
    17: [16, 18, 8],
    18: [17, 19, 10],
    19: [12, 15, 18]
}

def connected_rooms(room):
    r1, r2, r3 = tp.alloc(), tp.alloc(), tp.alloc()
    s = byfon.Switch(room)
    for source, (c1, c2, c3) in ROOM_RELATIONS.items():
        with s.case(source):
            r1 <- c1; r2 <- c2; r3 <- c3
    return r1, r2, r3

def read_num():
    f = tp.alloc().read()
    s = tp.alloc().read()
    r = tp.alloc()
    if! ~s != ord("\n"):
        read_line(0)  # eat until newline
        (f - 48).mov((r, 10))
        r += s
        r -= 48
        # lol
        f.freed = False
        s.freed = False
    if! s == ord("\n"):
        r += f
        r -= 48
    return r


bf_print = functools.partial(byfon.write_literal, tp.alloc())
bf_print("""Welcome to Hunt the Wumpus!
Implemented in Brainfuck, generated using byfon. Original byfon source code, and byfon itself, provided and written by LyricLy.
All rights reserved, LyricLy 2020
==========
Please enter a seed value (6 chars): """)

# initialize RNG
placer_rng, placer_rng_d, relative_rng, relative_rng_d, placer2_rng, placer2_rng_d = read_line(6)
placer_rng += placer_rng_d
relative_rng += relative_rng_d
placer2_rng += placer2_rng_d

# run the RNGs different numbers of times to seperate them if they started equal, with 3 base calls to exacerbate small differences
gen_random(gen_random(gen_random(placer_rng)))
gen_random(gen_random(gen_random(gen_random(relative_rng))))
gen_random(gen_random(gen_random(gen_random(gen_random(placer2_rng)))))


player, wumpus, pit1, pit2, bat1, bat2 = gen_uniq_positions(6, [placer_rng, placer2_rng])
game_running = tp.alloc(init=1)

while! game_running:
    bf_print("\nYou are in room "); output_location(~player); bf_print(".\n")

    rooms = connected_rooms(~player)
    bf_print("This room is connected to rooms ")
    for room in rooms[:-1]:
        output_location(~room); bf_print(", ")
    bf_print("and "); output_location(~rooms[-1]); bf_print(".\n")

    for room in rooms:
        if! ~room == ~wumpus:
            bf_print("You smell a wumpus.\n")
        if! (~room == ~pit1 or! ~room == ~pit2):
            bf_print("You feel a draft.\n")
        if! (~room == ~bat1 or! ~room == ~bat2):
            bf_print("You hear the flapping of wings.\n")

    invalid = tp.alloc(init=1)
    woke_wumpus = tp.alloc(init=0)
    while! invalid:
        bf_print("Would you like to move or shoot? (S/M) ")
        c, = read_line(1)
        s = byfon.Switch(c)

        with s.case(ord("S")):
            invalid -= 1
            woke_wumpus += 1

            spaces_invalid = tp.alloc(init=1)
            while! spaces_invalid:
                bf_print("How many spaces should the arrow go (1-5)? ")
                count = tp.alloc().read() - 48
                read_line(0)
                for i in range(1, 5):
                    if! ~count == i:
                        spaces_invalid -= 1
                        arrow = ~player
                        wumpus_shot = tp.alloc()
                        for _ in range(i):
                            bf_print("Where should the arrow go next? ")
                            n = read_num() - 1
                            spots = connected_rooms(~arrow)
                            els = tp.alloc(init=1)
                            if! is_repeat(n, spots):
                                els -= 1
                                arrow <- n
                                if! ~arrow == ~wumpus:
                                    wumpus_shot += 1
                            if! els:
                                arrow <- byfon.index(spots, mod(~gen_random(relative_rng), 3))
                        if! wumpus_shot:
                            bf_print("You hit the Wumpus! You win!\n")
                            game_running -= 1

        with s.case(ord("M")):
            invalid -= 1
            # move
            cave_invalid = tp.alloc(init=1)
            while! cave_invalid:
                bf_print("To where? ")
                n = read_num() - 1

                placer_rng += ~n
                relative_rng += ~n
                relative_rng -= 3

                if! is_repeat(n, rooms):
                    cave_invalid -= 1
                    player <- n

                    whilex! (~player == ~bat1).or_(~player == ~bat2):
                        bf_print("Super bat snatch!\n")
                        player <- mod(~gen_random(placer_rng), 20)
                    if! (~player == ~pit1 or! ~player == ~pit2):
                        bf_print("You fell in a pit and died. You lose!\n")
                        game_running -= 1
                    if! ~player == ~wumpus:
                        bf_print("You bumped into the Wumpus!\n")
                        woke_wumpus += 1

                if! ~cave_invalid:
                    bf_print("Invalid room.\n")
        if! ~invalid:
            bf_print("Invalid input.\n")

    if! woke_wumpus:
        woke_wumpus -= 1
        wumpus <- byfon.index(connected_rooms(~wumpus) + (wumpus,), mod(~gen_random(relative_rng), 4))
        if! ~wumpus == ~player:
            bf_print("The wumpus got you. You lose!\n")
            game_running -= 1


print(tp.result)
