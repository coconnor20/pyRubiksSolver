import rubik
import typing

def shortest_path(start, end):
    """
    Using 2-way BFS, finds the shortest path from start_position to
    end_position. Returns a list of moves. 

    You can use the rubik.quarter_twists move set.
    Each move can be applied using rubik.perm_apply
    """
    if start == end:
        return []

    path = []

    #list of dicts that store precalculated fronts
    start_fronts = []
    end_fronts = []
    intercept = rubik.Position

    # next four variables are type List[Tuple[r.pos, r.perm]]
    current_f_front = []
    current_e_front = []
    previous_f_front = List[Tuple[rubik.Position, rubik.Permutation]]
    previous_e_front = List[Tuple[rubik.Position, rubik.Permutation]]

    #current front
    f = 0
    found = False
    while found != True:
        #generate first layer with the start and end positions
        if f == 0:
            for i in rubik.quarter_twists_names:
                current_f_front.append((rubik.perm_apply(i, start), i))
                current_e_front.append((rubik.perm_apply(i, end), i))
        else:
            for i in previous_f_front:
                for j in rubik.quarter_twists_names:
                    if rubik.perm_apply(j, i[0]) in start_fronts:
                        continue
                    else:
                        current_f_front.append = ((rubik.perm_apply(j, i[0]), j))
            for i in previous_e_front:
                for j in rubik.quarter_twists_names:
                    if rubik.perm_apply(j, i[0]) in end_fronts:
                        continue
                    else:
                        current_e_front.append((rubik.perm_apply(j, i[0]), j))
        #add last front to the dictonary for storage
        start_fronts.append(dict(current_f_front))
        end_fronts.append(dict(current_e_front))
        #make the current front the last one
        previous_f_front = current_f_front 
        previous_e_front = current_e_front

    #end condition check
        for i in start_fronts[f].keys():
           if i in end_fronts[f].keys():
                intercept = i
                #end the while loop, solution found
                found = True

        if found == False:
            f += 1
        

    s_f = intercept
    e_f = intercept
    while True:
        if s_f == start and e_f == end:
            break
        else:
            path.insert(0, start_fronts[f][s_f])
            path.append(end_fronts[f][e_f])
            s_f = rubik.perm_apply(rubik.perm_inverse(start_fronts[f][s_f]), s_f)
            e_f = rubik.perm_apply(rubik.perm_inverse(end_fronts[f][e_f]), e_f)
            f -= 1

    return path
