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

# test_16()

# Re import for easier submission
import queue

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

    visited = [[[False for _ in range(m + 1)] for _ in range(c + 1)] for _ in range(2)] # m cols, c rows, 2 depth
    initial_state = State(m, c, -1)
    frontier = queue.Queue()
    frontier.put(initial_state)
    new_upper_limit = (m + 1) * (c + 1) * 2

    while not frontier.empty():
        state:State = frontier.get()
        if len(state.steps) > new_upper_limit:
            return False

        # Visit this state
        if visited[0 if state.direction < 0 else 1][state.left_c][state.left_m]:
            continue
        visited[0 if state.direction < 0 else 1][state.left_c][state.left_m] = True

        for action_step in action(state):
            new_state = transition(state, action_step[0], action_step[1])
            
            # End goal
            if new_state.left_m == 0 and new_state.left_c == 0:
                return new_state.steps

            # Checks if missionaries are not eaten and new state is not visited
            if check_not_eaten(new_state, m, c):
                frontier.put(new_state)
    return False


# Test cases for Task 1.7
def test_17():
    expected = ((2, 0), (1, 0), (1, 1))
    assert(mnc_graph_search(2,1) == expected)

    expected = ((1, 1), (1, 0), (2, 0), (1, 0), (1, 1))
    assert(mnc_graph_search(2,2) == expected)

    expected = ((1, 1), (1, 0), (0, 2), (0, 1), (2, 0), (1, 1), (2, 0), (0, 1), (0, 2), (1, 0), (1, 1))
    assert(mnc_graph_search(3,3) == expected)   

    # print(mnc_graph_search(4, 4))
    assert(mnc_graph_search(4, 4) == False)

# test_17()

# Re-import for easier submission
from collections import deque
import copy

def pitcher_search(p1, p2, p3, a):
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

    class Pitcher:
        def __init__(self, capacity:int, name:str):
            self.name = name
            self.capacity = capacity
            self.volume:int = 0

        def empty(self) -> None:
            self.volume = 0

        def fill(self) -> None:
            self.volume = self.capacity

        def is_full(self) -> bool:
            return self.volume == self.capacity
        
        def take_in(self, new_volume:int) -> None:
            self.volume += new_volume
        
        def take_out(self, old_volume:int) -> None:
            self.volume -= old_volume

        def find_amount_to_pour(self, other_volume:int) -> int:
            return min(other_volume, self.capacity - self.volume)
        
        def __str__(self) -> str:
            return self.name

        def __eq__(self, other):
            if isinstance(other, Pitcher):
                return self.volume == other.volume
            return False

        def __hash__(self) -> int:
            return hash(self.volume)

    # Define the initial state
    initial_state = (Pitcher(p1, "P1"), Pitcher(p2, "P2"), Pitcher(p3, "P3"))
    
    # Initialize the queue for BFS
    queue = deque([(initial_state, [])])  # Each element is a tuple (state, steps)
    
    # Initialize a set to keep track of visited states
    visited = set()
    
    while queue:
        current_state, steps = queue.popleft()
        
        # Check if any pitcher contains 'a' in any amount
        for state in current_state:
            if a == state.volume:
                return tuple(steps)
        
        # Generate possible successor states
        successor_states = []
        successor_steps:list[str] = []
        
        # Pour water from one pitcher to another (considered as a step)
        for i in range(3):
            for j in range(3):
                amount_to_pour = current_state[j].find_amount_to_pour(current_state[i].volume)
                if i != j and amount_to_pour > 0:
                    new_state = copy.deepcopy(current_state)
                    new_state[i].take_out(amount_to_pour)
                    new_state[j].take_in(amount_to_pour)
                    successor_states.append(new_state)
                    successor_steps.append(f'{new_state[i]}=>{new_state[j]}')
                if not current_state[i].is_full():
                    new_state = copy.deepcopy(current_state)
                    new_state[i].fill()
                    successor_states.append(new_state)
                    successor_steps.append(f'Fill {new_state[i]}')         
                if current_state[i].volume > 0:
                    new_state = copy.deepcopy(current_state)
                    new_state[i].empty()
                    successor_states.append(new_state)
                    successor_steps.append(f'Empty {new_state[i]}')
                
        # Enqueue successor states with the updated steps
        for successor_state, step in zip(successor_states, successor_steps):
            if successor_state not in visited:
                visited.add(successor_state)
                queue.append((successor_state, steps + [step]))
    
    # If no solution is found
    return False
                

# Test cases for Task 2.3
def test_23():
    expected = ('Fill P2', 'P2=>P1')
    assert(pitcher_search(2,3,4,1) == expected)

    expected = ('Fill P3', 'P3=>P1', 'Empty P1', 'P3=>P1')
    assert(pitcher_search(1,4,9,7) == expected)

    assert(pitcher_search(2,3,7,8) == False)

test_23()