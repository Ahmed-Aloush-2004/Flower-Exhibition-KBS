import heapq


def get_manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

# Replace the old heuristic function with this one:
def heuristic(pos, goal):
    """
    Standard A* heuristic: Manhattan distance from the current position to the specific goal.
    """
    return get_manhattan_distance(pos[0], pos[1], goal[0], goal[1])


def astar(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    
    open_list = []
    heapq.heappush(open_list, (0, start))
    
    came_from = {}
    g_score = {start: 0}
    
    directions = [(0,1),(1,0),(0,-1),(-1,0)]
    
    while open_list:
        _, current = heapq.heappop(open_list)
        
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]
        
        for d in directions:
            neighbor = (current[0] + d[0], current[1] + d[1])
            
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if grid[neighbor[0]][neighbor[1]] == 1:
                    continue  # obstacle
                
                tentative_g = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_list, (f_score, neighbor))
    
    return None



def calculate_number_of_bouquet_per_pavilion(req:dict)->int:
    sum = 0
    for color ,qty in req.items():
        sum+= qty
    
    return sum    


def calculate_number_of_bouquet_robot_has(load:dict)->int:
    sum = 0    
    for type_color, qty in load.items():
        sum+= qty
        
    return sum



def is_load_compatible(load: dict, new_ftype: str, new_req: dict) -> bool:
    """
    هل يمكن إضافة هذه الباقات للحمولة الحالية؟
    Option A: نفس اللون، أنواع مختلفة
    Option B: نفس النوع، ألوان مختلفة
    """
    # print(f"Checking load compatibility: current load={load}, new type={new_ftype}, new req={new_req}")
    if not load:
        return True  # الحمولة فارغة — أي خيار مسموح

    existing_types  = set(k.split('_')[0] for k in load)
    existing_colors = set(k.split('_')[1] for k in load)
    new_colors      = set(new_req.keys())

    # Option B: نفس النوع
    if existing_types == {new_ftype}:
        return True

    # # Option A: نفس اللون
    # if existing_colors & new_colors:  # يوجد لون مشترك
    #     return True
    
    
    # Option A: الخيار أ (نفس اللون)
    # يجب أن يكون الطلب الجديد بلون واحد فقط، ويطابق اللون الوحيد في الحمولة
    if len(existing_colors) == 1 and len(new_colors) == 1 and existing_colors == new_colors:
        return True

    return False  # لا يتوافق مع أي خيار


def is_unload_compatible(load: dict, pavilion_req: dict,ftype:str) -> bool:
    """
    هل يمكن تفريغ هذه الباقات في الجناح؟
    يجب أن تحتوي الحمولة على كل ما يحتاجه الجناح، لكن يمكن أن تحتوي على المزيد.
    """
    for type_color, qty in load.items():
        type_, color = type_color.split('_')
        if type_ == ftype and color in pavilion_req and qty >= pavilion_req[color]:
            return True  # يوجد نوع مطابق مع لون كافٍ

    return False  # لا يوجد أي نوع مطابق أو الألوان غير كافية



