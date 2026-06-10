# import heapq


# def get_manhattan_distance(x1, y1, x2, y2):
#     return abs(x1 - x2) + abs(y1 - y2)

# # Replace the old heuristic function with this one:
# def heuristic(pos, goal):
#     """
#     Standard A* heuristic: Manhattan distance from the current position to the specific goal.
#     """
#     return get_manhattan_distance(pos[0], pos[1], goal[0], goal[1])


# def astar(grid, start, goal):
#     rows, cols = len(grid), len(grid[0])
    
#     open_list = []
#     heapq.heappush(open_list, (0, start))
    
#     came_from = {}
#     g_score = {start: 0}
    
#     directions = [(0,1),(1,0),(0,-1),(-1,0)]
    
#     while open_list:
#         _, current = heapq.heappop(open_list)
        
#         if current == goal:
#             path = []
#             while current in came_from:
#                 path.append(current)
#                 current = came_from[current]
#             path.append(start)
#             return path[::-1]
        
#         for d in directions:
#             neighbor = (current[0] + d[0], current[1] + d[1])
            
#             if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
#                 if grid[neighbor[0]][neighbor[1]] == 1:
#                     continue  # obstacle
                
#                 tentative_g = g_score[current] + 1
                
#                 if neighbor not in g_score or tentative_g < g_score[neighbor]:
#                     came_from[neighbor] = current
#                     g_score[neighbor] = tentative_g
#                     f_score = tentative_g + heuristic(neighbor, goal)
#                     heapq.heappush(open_list, (f_score, neighbor))
    
#     return None



# def calculate_number_of_bouquet_per_pavilion(req:dict)->int:
#     sum = 0
#     for color ,qty in req.items():
#         sum+= qty
    
#     return sum    


# def calculate_number_of_bouquet_robot_has(load:dict)->int:
#     sum = 0    
#     for type_color, qty in load.items():
#         sum+= qty
        
#     return sum



# def is_load_compatible(load: dict, new_ftype: str, new_req: dict) -> bool:
#     """
#     هل يمكن إضافة هذه الباقات للحمولة الحالية؟
#     Option A: نفس اللون، أنواع مختلفة
#     Option B: نفس النوع، ألوان مختلفة
#     """
#     # print(f"Checking load compatibility: current load={load}, new type={new_ftype}, new req={new_req}")
#     if not load:
#         return True  # الحمولة فارغة — أي خيار مسموح

#     existing_types  = set(k.split('_')[0] for k in load)
#     existing_colors = set(k.split('_')[1] for k in load)
#     new_colors      = set(new_req.keys())

#     # Option B: نفس النوع
#     if existing_types == {new_ftype}:
#         return True

#     # # Option A: نفس اللون
#     # if existing_colors & new_colors:  # يوجد لون مشترك
#     #     return True
    
    
#     # Option A: الخيار أ (نفس اللون)
#     # يجب أن يكون الطلب الجديد بلون واحد فقط، ويطابق اللون الوحيد في الحمولة
#     if len(existing_colors) == 1 and len(new_colors) == 1 and existing_colors == new_colors:
#         return True

#     return False  # لا يتوافق مع أي خيار


# def is_unload_compatible(load: dict, pavilion_req: dict,ftype:str) -> bool:
#     """
#     هل يمكن تفريغ هذه الباقات في الجناح؟
#     يجب أن تحتوي الحمولة على كل ما يحتاجه الجناح، لكن يمكن أن تحتوي على المزيد.
#     """
#     for type_color, qty in load.items():
#         type_, color = type_color.split('_')
#         if type_ == ftype and color in pavilion_req and qty >= pavilion_req[color]:
#             return True  # يوجد نوع مطابق مع لون كافٍ

#     return False  # لا يوجد أي نوع مطابق أو الألوان غير كافية





import heapq
from facts import GridFact, PavilionFact



def search_grid_fact_recursively(facts, fact_type):
    facts_list = list(facts)
    return ((not facts_list) and None) or (isinstance(facts_list[0], fact_type) and facts_list[0]) or search_grid_fact_recursively(facts_list[1:], fact_type)

def search_pavilion_fact_recursively(facts, fact_type,facts_list):
    facts = list(facts)
    return ((not facts) and None) or (isinstance(facts[0], fact_type) and facts_list.add(facts[0])) or search_grid_fact_recursively(facts[1:], fact_type)


# def _build_grid(facts, ignore_x, ignore_y):
#     # Now it uses the 'facts' passed as an argument instead of 'self.facts.values()'
#     # grid_facts = list(filter(lambda f: isinstance(f, GridFact), facts))
#     # w = grid_facts[0]['x'] if grid_facts else 5
#     # h = grid_facts[0]['y'] if grid_facts else 5

#     grid_facts = search_grid_fact_recursively(facts, GridFact)
#     w = grid_facts and grid_facts['x'] or 5
#     h = grid_facts and grid_facts['y'] or 5
    
#     # w = grid_facts['x'] if grid_facts else 5
#     # h = grid_facts['y'] if grid_facts else 5


                
#     # grid = list(map(lambda _: [0] * h, range(w)))
#     grid = [ [0] * h ] * w
    
#     pavilion_facts = set()
#     search_pavilion_fact_recursively(facts, PavilionFact, pavilion_facts)    
#     pavilion_facts = list(pavilion_facts)
        
#     # Recursive function to mark obstacles
#     # def mark_obstacles(pav_facts):
#     #     if not pav_facts: return
#     #     fact = pav_facts[0]
#     #     px, py = fact['pos_x'], fact['pos_y']
#     #     if not (px == ignore_x and py == ignore_y):
#     #         grid[px][py] = 1 
#     #     mark_obstacles(pav_facts[1:])
    
    
#     def mark_obstacles(pav_facts):
#         # if not pav_facts: return
#         return (not pav_facts) or (not (pav_facts[0]['pos_x'] == ignore_x and pav_facts[0]['pos_y'] == ignore_y)
#                 and grid[pav_facts[0]['pos_x']][pav_facts[0]['pos_y']] = 1 ) and (mark_obstacles(pav_facts[1:]))
        
#         # if not (pav_facts[0]['pos_x'] == ignore_x and pav_facts[0]['pos_y'] == ignore_y):
#         #     grid[pav_facts[0]['pos_x']][pav_facts[0]['pos_y']] = 1 
#         # mark_obstacles(pav_facts[1:])
                    
#     mark_obstacles(pavilion_facts)
#     return grid





def _build_grid(facts, ignore_x, ignore_y):
    grid_facts = search_grid_fact_recursively(facts, GridFact)
    
    # Safely get w and h
    w = grid_facts and grid_facts['x'] or 5
    h = grid_facts and grid_facts['y'] or 5
    
    # SAFE 2D Array Definition without loops/map/shared references
    # We use a list multiplication on independent row creations 
    # built recursively if your constraints are strict, or via numpy.
    # Assuming pure python, we can make independent rows via a small recursion:
    def create_grid(rows_left, cols):
        return bool(rows_left) and ([ [0] * cols ] + create_grid(rows_left - 1, cols)) or []
    
    grid = create_grid(w, h)
    
    pavilion_facts = set()
    search_pavilion_fact_recursively(facts, PavilionFact, pavilion_facts)    
    pavilion_facts = list(pavilion_facts)
    
    def mark_obstacles(pav_facts):
        return bool(pav_facts) and (
            (
                # If it's NOT the ignored coordinates, mutate the grid
                not (pav_facts[0]['pos_x'] == ignore_x and pav_facts[0]['pos_y'] == ignore_y)
                and (grid[pav_facts[0]['pos_x']].__setitem__(pav_facts[0]['pos_y'], 1) or True)
            ) 
            # Continue the recursion regardless of whether the condition above was True or False
            or True 
        ) and mark_obstacles(pav_facts[1:])
                    
    mark_obstacles(pavilion_facts)
    return grid




# def get_manhattan_distance(x1, y1, x2, y2):
#     return abs(x1 - x2) + abs(y1 - y2)



# def heuristic(pos, goal):
#     """
#     Standard A* heuristic: Manhattan distance from the current position to the specific goal.
#     """
#     return get_manhattan_distance(pos[0], pos[1], goal[0], goal[1])



# def astar(grid, start, goal):
#     rows, cols = len(grid), len(grid[0])
#     directions = [(0,1), (1,0), (0,-1), (-1,0)]
    
#     # Recursive helper to reconstruct the final path
#     def reconstruct_path(came_from, current, path):
#         if current in came_from:
#             return reconstruct_path(came_from, came_from[current], [current] + path)
#         return [current] + path

#     # Recursive helper to check all 4 directions without a for-loop
#     def process_neighbors(neighbors, current, open_list, came_from, g_score):
#         if not neighbors:
#             return
#         d = neighbors[0]
#         neighbor = (current[0] + d[0], current[1] + d[1])
#         if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
#             if grid[neighbor[0]][neighbor[1]] != 1:  # Not an obstacle
#                 tentative_g = g_score[current] + 1
#                 if neighbor not in g_score or tentative_g < g_score[neighbor]:
#                     came_from[neighbor] = current
#                     g_score[neighbor] = tentative_g
#                     f_score = tentative_g + heuristic(neighbor, goal)
#                     heapq.heappush(open_list, (f_score, neighbor))
        
#         # Process the rest of the directions
#         process_neighbors(neighbors[1:], current, open_list, came_from, g_score)

#     # Recursive main loop for A*
#     def astar_recursive(open_list, came_from, g_score):
#         if not open_list:
#             return None
#         _, current = heapq.heappop(open_list)
        
#         if current == goal:
#             return reconstruct_path(came_from, current, [])
            
#         process_neighbors(directions, current, open_list, came_from, g_score)
#         return astar_recursive(open_list, came_from, g_score)

#     open_list = []
#     heapq.heappush(open_list, (0, start))
#     return astar_recursive(open_list, {}, {start: 0})





def get_manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def heuristic(pos, goal):
    return get_manhattan_distance(pos[0], pos[1], goal[0], goal[1])

def astar(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    directions = [(0,1), (1,0), (0,-1), (-1,0)]
    
    # 1. Recursive path reconstruction without 'if'
    def reconstruct_path(came_from, current, path):
        return (current in came_from) and (
            reconstruct_path(came_from, came_from[current], [current] + path)
        ) or ([current] + path)

    # 2. Process directions recursively without 'for' or 'if'
    def process_neighbors(neighbors, current, open_list, came_from, g_score):
        # Base case: stop when neighbors list is empty
        return bool(neighbors) and (
            (lambda n_coord: (
                # Guard 1: In-bounds check AND not an obstacle
                (0 <= n_coord[0] < rows and 0 <= n_coord[1] < cols and grid[n_coord[0]][n_coord[1]] != 1) and (
                    # Guard 2: Better path discovered?
                    (lambda tentative_g: (
                        (n_coord not in g_score or tentative_g < g_score[n_coord]) and (
                            # Mutate state inline using dictionary/heap methods wrapped to keep evaluating
                            came_from.__setitem__(n_coord, current) or
                            g_score.__setitem__(n_coord, tentative_g) or
                            heapq.heappush(open_list, (tentative_g + heuristic(n_coord, goal), n_coord)) or True
                        )
                    ))(g_score[current] + 1)
                ) or True
            ))((current[0] + neighbors[0][0], current[1] + neighbors[0][1]))
            
            # Recurse through the remaining directions
            and process_neighbors(neighbors[1:], current, open_list, came_from, g_score)
        )

    # 3. Recursive main A* loop without 'while' or 'if'
    def astar_recursive(open_list, came_from, g_score):
        # Base Case 1: Open list is empty (No path found)
        return bool(open_list) and (
            # The entire lambda is wrapped in parentheses and immediately invoked with the popped node
            (lambda current: (
                # Base Case 2: Goal reached -> Reconstruct path
                (current == goal) and reconstruct_path(came_from, current, [])
                
                # Otherwise, process neighbors and continue the search
                or (
                    process_neighbors(directions, current, open_list, came_from, g_score) or True
                ) and astar_recursive(open_list, came_from, g_score)
            ))(heapq.heappop(open_list)[1])
        )

    # Kickstart the execution
    open_list = []
    heapq.heappush(open_list, (0, start))
    
    # Run the main engine loop and guarantee a clean list or None output
    return astar_recursive(open_list, {}, {start: 0}) or None












# def calculate_number_of_bouquet_per_pavilion(req: dict) -> int:    
#     # return sum(req.values())

def calculate_number_of_bouquet_per_pavilion(req: dict) -> int:
    items_list = list(req.items())
    
    def recursive_sum(items: list) -> int:
        # Base Case: If items list is empty, bool(items) is False, so it short-circuits and returns 0.
        # Recursive Step: If items has data, bool(items) is True, so it evaluates the right side.
        return bool(items) and (items[0][1] + recursive_sum(items[1:]))

    return recursive_sum(items_list)    
    

# def calculate_number_of_bouquet_robot_has(load: dict) -> int:
#     return sum(load.values())



def calculate_number_of_bouquet_robot_has(load: dict) -> int:
    items_list = list(load.items())
    
    def recursive_sum(items: list) -> int:
        # Base Case: If items list is empty, bool(items) is False, so it short-circuits and returns 0.
        # Recursive Step: If items has data, bool(items) is True, so it evaluates the right side.
        return bool(items) and (items[0][1] + recursive_sum(items[1:]))

    return recursive_sum(items_list)  


# def is_load_compatible(load: dict, new_ftype: str, new_req: dict) -> bool:
#     if not load:
#         return True  # الحمولة فارغة — أي خيار مسموح

#     existing_types  = set(map(lambda k: k.split('_')[0], load.keys()))
#     existing_colors = set(map(lambda k: k.split('_')[1], load.keys()))
#     new_colors      = set(new_req.keys())

#     # Option B: نفس النوع
#     if existing_types == {new_ftype}:
#         return True
    
#     # Option A: الخيار أ (نفس اللون)
#     if len(existing_colors) == 1 and len(new_colors) == 1 and existing_colors == new_colors:
#         return True

#     return False 



def is_load_compatible(load: dict, new_ftype: str, new_req: dict) -> bool:
    result = False
    

    existing_types  = set(map(lambda k: k.split('_')[0], load.keys()))
    existing_colors = set(map(lambda k: k.split('_')[1], load.keys()))
    new_colors      = set(new_req.keys())

    # Option B: نفس النوع
    # Option A: الخيار أ (نفس اللون)
    
    result = (not load) or (existing_types == {new_ftype})  or (len(existing_colors) == 1 and len(new_colors) == 1 and existing_colors == new_colors )

    return result  

# def is_unload_compatible(load: dict, pavilion_req: dict, ftype: str) -> bool:
#     # هل يمكن تفريغ هذه الباقات في الجناح؟
#     return any(
#         map(lambda item: item[0].split('_')[0] == ftype and 
#                          item[0].split('_')[1] in pavilion_req and 
#                          item[1] >= pavilion_req[item[0].split('_')[1]], 
#             load.items())
#     )
    

def print_recursivly(path):
    return (not path) or (print(f"  - {path[0]}") or print_recursivly(path[1:]))       


def filtered_and_mapped_items_recursivly(items, filter_items,ftype):
    return bool(items) and (
                (
                    # If quantity > 0, safely append to set, wrapped with 'or True'
                    items[0][1] > 0 and 
                    (filter_items.add((f"{ftype}_{items[0][0]}", items[0][1])) or True)
                ) or True # Ensure fallback step continues even if qty was 0
            ) and filtered_and_mapped_items_recursivly(items[1:], filter_items, ftype)


def process_unloading(items, n_load, n_req, unloaded_anything,ftype):
            # 1. Base Case: Reached the end of the items
    base_case = lambda: (n_load, n_req, unloaded_anything)
            
            # 2. Recursive Case: Process the current item
    def recursive_case():
        item_key = items[0][0]
        item_count = items[0][1]
        parts = item_key.split('_')
        item_ftype = parts[0]
        item_color = parts[1] 
                
        # Use .get() to avoid KeyError if color isn't in req
        # Default to -1 so that missing requirements automatically fail the > 0 check
        req_amt = n_req.get(item_color, -1)
                
        # Evaluate our boolean unloading conditions
        can_unload = (item_ftype == ftype) and (req_amt > 0) and (item_count >= req_amt)
                
        def perform_unload():
            # Deduct the requirement from the load
            n_load[item_key] -= req_amt
                    
            # Pop the item and conditionally add it back if remaining > 0
            remaining = n_load.pop(item_key)
            n_load.update(({}, {item_key: remaining})[remaining > 0])
                    
            # Fulfill the requirement entirely
            n_req[item_color] = 0
                    
            return process_unloading(items[1:], n_load, n_req, True, ftype)
                    
        def skip_unload():
            return process_unloading(items[1:], n_load, n_req, unloaded_anything, ftype)
                    
        # Trigger branch based on condition without an 'if'
        return (skip_unload, perform_unload)[bool(can_unload)]()

    # Trigger base case or recursion based on whether the list is empty
    return (base_case, recursive_case)[bool(items)]()



def is_unload_compatible(load: dict, pavilion_req: dict, ftype: str) -> bool:
    items_list = list(load.items())

    def recursive_check(items: list) -> bool:
        # Base case: if list is empty, return False (using short-circuiting instead of 'if')
        # If items is empty, 'and' stops and returns [], which evaluates to False
        return bool(items) and (
            (
                items[0][0].split('_')[0] == ftype and 
                items[0][0].split('_')[1] in pavilion_req and 
                items[0][1] >= pavilion_req[items[0][0].split('_')[1]]
            ) 
            or recursive_check(items[1:]) # Recursive step with slicing
        )

    return recursive_check(items_list)