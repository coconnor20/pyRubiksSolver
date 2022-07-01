from typing import Dict, List
from typing import Optional
import rubik

"""
Extra credit:
any sequence of moves will bring you back to where you started because of two facts,
all quarter turns can be undone with the perm inverse, or by doing the move three more times in the 
same direcetion. This will create a cycle in the graph. By the same logic, a sequence of any moves, performed
in inverse order will undo the moves, or performing the sequence enough times will eventally loop back 
to the place that it started. This will also create a cycle in the graph.
"""


def shortest_path(start: rubik.Position, end: rubik.Position,) -> Optional[List[rubik.Permutation]]:

    #if the start and end are the same then you found the shortest path... There is no shortest path
    if start == end:
        return []

    #return path
    path = []

    #what weve seen on both sides
    start_seen = {}
    end_seen = {}
    #what were looking at
    current_s_front = []
    current_e_front= []
    #what were applying to
    prev_s_front = []
    prev_e_front = []

    found = False
    #the layer we are seatching, if the layer is 7 and we have not found it then the solution can't exist
    f = 0

    '''Invariants of first while loop
        Initilization: We start the loop by stating we have not found the intersection between the two
        cube states, so we need to do some BFS. The layer is set to 0 and we generate all the possible 
        position permutations from the start and end.

        Matinance: We know we are making progress because no matter what, f is going to be incremented
        everytime the loop runs, if f gets to 7 and we have not found our answer, then we know there is
        no valid solution so we terminate.

        Termination: We terminate this loop if we find an intersection, or if we find that the answer is
        non-existant. If f == 7, the answer does not exist, if a key in the start side seen dict equals a 
        key in the end side dict, we know there is a link and that we can start to walk the found path
    '''
    while found != True:
        if f == 7 and found != True:
            return None
        if f == 0:
            for i in rubik.quarter_twists_names:
                current_s_front.append(rubik.perm_apply(i, start))
                current_e_front.append(rubik.perm_apply(i,end))
                start_seen.update({rubik.perm_apply(i, start): i})
                end_seen.update({rubik.perm_apply(i, end): i})
        else:
            for i in prev_s_front:
                for j in rubik.quarter_twists_names:
                    if rubik.perm_apply(j, i) in start_seen:
                        continue
                    else:
                        current_s_front.append(rubik.perm_apply(j,i))
                        start_seen.update({rubik.perm_apply(j, i): j})
            for i in prev_e_front:
                for j in rubik.quarter_twists_names:
                    if rubik.perm_apply(j, i) in end_seen:
                        continue
                    else:
                        current_e_front.append(rubik.perm_apply(j,i))
                        end_seen.update({rubik.perm_apply(j, i): j})
        
        prev_e_front = current_e_front.copy()
        prev_s_front = current_s_front.copy()
        current_s_front.clear()
        current_e_front.clear()
        f += 1

        for i in start_seen.keys():
            if i in end_seen.keys():
                intercept = i
                found = True
                break

    # s_i and e_i are both positions, and you perm inverse them to walk the graph
    s_i = intercept
    e_i = intercept

    if e_i == end:
        path.append(s_i)
        return path

    '''Invariants of second while loop
        Initilization: We start the loop by setting the start side intersection and end side intersection to
        the intersection of the two frontiers. We make the statement that both of the intersections are not the 
        start or end, and begin to walk through the graph.

        Matinance: We know we are making progress because no matter what, we are going to apply the inverse
        permutation to both side of the intersection, thus forcing the path back towards the start and end 
        position

        Termination: We terminate this loop once we have walked fully through the graph and find the start and end
        of the graph. Once we have found this, we know that the path has been fully reconstructed.
    '''
    while s_i != start and e_i != end:
        if s_i != start and e_i != end:
            path.insert(0, start_seen[s_i])
            s_i = rubik.perm_apply(rubik.perm_inverse(start_seen[s_i]), s_i)
            path.append(rubik.perm_inverse(end_seen[e_i]))
            e_i = rubik.perm_apply(rubik.perm_inverse(end_seen[e_i]), e_i)
        if s_i != start and e_i == end:
            path.insert(0, start_seen[s_i])
            s_i = rubik.perm_apply(rubik.perm_inverse(start_seen[s_i]), s_i)
        if s_i == start and e_i != end:
            path.append(rubik.perm_inverse(end_seen[e_i]))
            e_i = rubik.perm_apply(rubik.perm_inverse(end_seen[e_i]), e_i)

    return path


