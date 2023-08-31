# Task 1.6
import queue

def mnc_tree_search(m:int, c:int):  
    '''
    Solution should be the action taken from the root node (initial state) to 
    the leaf node (goal state) in the search tree.

    Parameters
    ----------    
    m: no. of missionaries
    c: no. of cannibals
    
    Returns
    ----------    
    Returns the solution to the problem as a tuple of steps. Each step is a tuple of two numbers x and y, indicating the number of missionaries and cannibals on the boat respectively as the boat moves from one side of the river to another. If there is no solution, return False.
    '''

    class State:
        def __init__(self, m:int, c:int, direction:int, steps:tuple=tuple()) -> None:
            self.steps = steps
            self.left_m = m
            self.left_c = c
            self.direction = direction # -1 represents left, 1 represents right

        def __str__(self):
            return f"{self.left_m} {self.left_c} {self.steps}"
        
        
    def check_not_eaten(state:State, initial_m:int, initial_c:int) -> bool:
        right_m = initial_m - state.left_m
        right_c = initial_c - state.left_c

        # If missionaries at on side is 0, the other side will always have m >= c
        if state.left_m == 0 or right_m == 0:
            return True
        
        # Checks both banks for satisfaction of m >= c
        result = state.left_m >= state.left_c and right_m >= right_c
        return result
    
    def transition(state:State, m_on_boat:int, c_on_boat:int) -> State:
        new_left_m = state.left_m + state.direction * m_on_boat
        new_left_c = state.left_c + state.direction * c_on_boat
        next_step = state.steps + ((m_on_boat, c_on_boat),)
        return State(new_left_m, new_left_c, -state.direction, next_step)
    
    def action(state:State) -> list:
        possiblities = [(1, 0), (2, 0), (0, 1), (1, 1), (0, 2)]
        actions = []
        for possible in possiblities:
            new_left_m = state.left_m + state.direction * possible[0]
            new_left_c = state.left_c + state.direction * possible[1]
            if not (new_left_m < 0 or new_left_c < 0 or new_left_m > m or new_left_c > c):
                actions.append(possible)
        return actions
    
    if m < c or m < 0 or c < 0:
        return False

    initial_state = State(m, c, -1)
    frontier = queue.Queue()
    frontier.put(initial_state)
    new_upper_limit = (m + 1) * (c + 1) * 2

    while not frontier.empty():
        state:State = frontier.get()
        if len(state.steps) > new_upper_limit:
            return False

        for action_step in action(state):
            new_state = transition(state, action_step[0], action_step[1])
            
            # End goal
            if new_state.left_m == 0 and new_state.left_c == 0:
                return new_state.steps

            # Checks if missionaries are not eaten
            if check_not_eaten(new_state, m, c):
                frontier.put(new_state)

# Test cases for Task 1.6
def test_16():
    expected = ((2, 0), (1, 0), (1, 1))
    assert(mnc_tree_search(2,1) == expected)

    expected = ((1, 1), (1, 0), (2, 0), (1, 0), (1, 1))
    assert(mnc_tree_search(2,2) == expected)

    expected = ((1, 1), (1, 0), (0, 2), (0, 1), (2, 0), (1, 1), (2, 0), (0, 1), (0, 2), (1, 0), (1, 1))
    assert(mnc_tree_search(3,3) == expected)   

    assert(mnc_tree_search(4, 4) == False)

test_16()

# Task 1.7
def mnc_graph_search(m, c):
    '''
    Graph search requires to deal with the redundant path: cycle or loopy path.
    Modify the above implemented tree search algorithm to accelerate your AI.

    Parameters
    ----------    
    m: no. of missionaries
    c: no. of cannibals
    
    Returns
    ----------    
    Returns the solution to the problem as a tuple of steps. Each step is a tuple of two numbers x and y, indicating the number of missionaries and cannibals on the boat respectively as the boat moves from one side of the river to another. If there is no solution, return False.
    '''
    # TODO: add your solution here and remove `raise NotImplementedError`
    raise NotImplementedError


# Test cases for Task 1.7
def test_17():
    expected = ((2, 0), (1, 0), (1, 1))
    assert(mnc_graph_search(2,1) == expected)

    expected = ((1, 1), (1, 0), (2, 0), (1, 0), (1, 1))
    assert(mnc_graph_search(2,2) == expected)

    expected = ((1, 1), (1, 0), (0, 2), (0, 1), (2, 0), (1, 1), (2, 0), (0, 1), (0, 2), (1, 0), (1, 1))
    assert(mnc_graph_search(3,3) == expected)   

    assert(mnc_graph_search(4, 4) == False)

#test_17()

    

# Task 2.3
def pitcher_search(p1,p2,p3,a):
    '''
    Solution should be the action taken from the root node (initial state) to 
    the leaf node (goal state) in the search tree.

    Parameters
    ----------    
    p1: capacity of pitcher 1
    p2: capacity of pitcher 2
    p3: capacity of pitcher 3
    a: amount of water we want to measure
    
    Returns
    ----------    
    Returns the solution to the problem as a tuple of steps. Each step is a string: "Fill Pi", "Empty Pi", "Pi=>Pj". 
    If there is no solution, return False.
    '''
    # TODO: add your solution here and remove `raise NotImplementedError`
    raise NotImplementedError

# Test cases for Task 2.3
def test_23():
    expected = ('Fill P2', 'P2=>P1')
    assert(pitcher_search(2,3,4,1) == expected)

    expected = ('Fill P3', 'P3=>P1', 'Empty P1', 'P3=>P1')
    assert(pitcher_search(1,4,9,7) == expected)

    assert(pitcher_search(2,3,7,8) == False)

#test_23()