# import collections
# if not hasattr(collections, 'Mapping'):
#     import collections.abc
#     collections.Mapping  = collections.abc.Mapping
#     collections.Sequence = collections.abc.Sequence

# from experta import *
# from facts import GridFact, PavilionFact, RobotFact, WarehouseFact
# from utils import (
#     calculate_number_of_bouquet_per_pavilion, 
#     calculate_number_of_bouquet_robot_has, 
#     is_load_compatible, 
#     is_unload_compatible,
#     astar
# )

# class SmartFlowerShow(KnowledgeEngine):

#     # ══════════════════════════════════════════
#     # Helper Methods for A*
#     # ══════════════════════════════════════════
#     def _build_grid(self, ignore_x, ignore_y):
#         """
#         Builds a 2D grid for the A* algorithm. 
#         Marks pavilions as obstacles (1) EXCEPT the destination we are routing to.
#         """
#         # Find grid dimensions
#         w, h = 5, 5
#         for fact in self.facts.values():
#             if isinstance(fact, GridFact):
#                 w, h = fact['x'], fact['y']
#                 break
                
#         # Initialize empty grid (0 = passable)
#         grid = [[0 for _ in range(h)] for _ in range(w)]
        
#         # Mark pavilions as obstacles
#         for fact in self.facts.values():
#             if isinstance(fact, PavilionFact):
#                 px, py = fact['pos_x'], fact['pos_y']
#                 # Don't make the destination an obstacle
#                 if not (px == ignore_x and py == ignore_y):
#                     grid[px][py] = 1 
                    
#         return grid


#     @Rule(
#         AS.pf << PavilionFact(requirements=MATCH.req),
#         AS.rf << RobotFact(max_load=MATCH.ml),
#     )
#     def assign_the_maximum_load(self, pf, rf, req, ml):
#        new_load = calculate_number_of_bouquet_per_pavilion(req)
#        if ml < new_load:
#            self.modify(rf, max_load=new_load)
           
           
#     # ══════════════════════════════════════════
#     # Movement Rules (Using A*)
#     # ══════════════════════════════════════════

#     @Rule(
#         AS.rf << RobotFact(
#             pos_x=MATCH.rx, pos_y=MATCH.ry, load=MATCH.load, 
#             g_n=MATCH.g, path=MATCH.path
#         ),
#         WarehouseFact(pos_x=MATCH.wx, pos_y=MATCH.wy),
#         PavilionFact(p_id=MATCH.p_id, pos_x=MATCH.px, pos_y=MATCH.py , requirements=MATCH.req),  # ✅ مضاف
#         # Route to warehouse IF the robot is not already there AND its load is completely empty
#         TEST(lambda rx, ry, wx, wy, load, req:
#             (rx != wx or ry != wy) and (calculate_number_of_bouquet_robot_has(load) == 0) and (calculate_number_of_bouquet_per_pavilion(req) > 0)
#             )# ✅ مضاف
#     )
        
#     def route_to_warehouse(self, rf, rx, ry, wx, wy, load, g, path):
#         grid = self._build_grid(ignore_x=wx, ignore_y=wy)
#         route = astar(grid, (rx, ry), (wx, wy))
        
#         if route:
#             distance = len(route) - 1
#             new_path = (path or ()) + (f"Drive to Warehouse via {route}",)
#             self.modify(rf, pos_x=wx, pos_y=wy, g_n=g + distance, path=new_path)


#     @Rule(
#         AS.rf << RobotFact(
#             pos_x=MATCH.rx, pos_y=MATCH.ry, load=MATCH.load, 
#             g_n=MATCH.g, path=MATCH.path
#         ),
#         AS.pf << PavilionFact(
#             p_id=MATCH.p_id, pos_x=MATCH.px, pos_y=MATCH.py, 
#             flower_type=MATCH.ftype, requirements=MATCH.req
#         ),
#         # Route to a pavilion IF not already there AND robot has flowers it can drop off there
#         TEST(lambda rx, ry, px, py, load, req, ftype: 
#              (rx != px or ry != py) and is_unload_compatible(load, req, ftype))
#     )
#     def route_to_pavilion(self, rf, rx, ry, px, py, load, g, path, req, ftype, p_id):
#         grid = self._build_grid(ignore_x=px, ignore_y=py)
#         route = astar(grid, (rx, ry), (px, py))
        
#         if route:
#             distance = len(route) - 1
#             new_path = (path or ()) + (f"Drive to Pavilion {p_id} via {route}",)
#             self.modify(rf, pos_x=px, pos_y=py, g_n=g + distance, path=new_path)


#     # ══════════════════════════════════════════
#     # Action Rules (Load / Unload)
#     # ══════════════════════════════════════════

#     @Rule(
#         AS.rf << RobotFact(
#             pos_x=MATCH.rx, pos_y=MATCH.ry, load=MATCH.load, 
#             g_n=MATCH.g, path=MATCH.path, max_load=MATCH.ml
#         ),
#         WarehouseFact(pos_x=MATCH.wx, pos_y=MATCH.wy),
#         AS.pf << PavilionFact(
#             p_id=MATCH.p_id, flower_type=MATCH.ftype, requirements=MATCH.req
#         ),
#         # Triggers when at warehouse, robot has room, and load is compatible
#         TEST(lambda rx, ry, wx, wy, load, ml, ftype, req:
#             rx == wx and ry == wy and
#             calculate_number_of_bouquet_robot_has(load) < ml and
#             calculate_number_of_bouquet_per_pavilion(req) > 0 and 
#             calculate_number_of_bouquet_per_pavilion(req) <= (ml - calculate_number_of_bouquet_robot_has(load)) and
#             is_load_compatible(load, ftype, req) 
#         ),
#     )
#     def load_robot(self, rf, rx, ry, load, g, path, ml, p_id, ftype, req, pf):
#         new_items = {f"{ftype}_{color}": qty for color, qty in req.items() if qty > 0}
#         new_load  = {**load, **new_items} 

#         new_path = (path or ()) + (f"Load {ftype} at warehouse",)
#         self.modify(rf, load=new_load, g_n=(g + 1), path=new_path)


#     @Rule(
#         AS.rf << RobotFact(
#             pos_x=MATCH.rx, pos_y=MATCH.ry, load=MATCH.load, 
#             g_n=MATCH.g, path=MATCH.path, max_load=MATCH.ml
#         ),
#         AS.pf << PavilionFact(
#             p_id=MATCH.p_id, flower_type=MATCH.ftype, 
#             pos_y=MATCH.py, pos_x=MATCH.px, requirements=MATCH.req
#         ),
#         TEST(lambda rx, ry, px, py, load, g, ml, p_id, ftype, req:
#             rx == px and ry == py and
#             calculate_number_of_bouquet_robot_has(load) > 0 and
#             is_unload_compatible(load, req, ftype)
#         )
#     )
#     def unload_at_pavilion(self, rx, ry, px, py, load, g, path, ml, p_id, ftype, req, pf, rf):
#         new_load = dict(load)  
#         new_req = dict(req)  
        
#         unloaded_anything = False # Track if we actually unloaded anything
        
#         # 1. Process ALL matching flowers in the loop (do NOT break)
#         for type_color, qty in load.items():
#             type_, color = type_color.split('_')
            
#             if type_ == ftype and color in req and qty >= req[color] and req[color] > 0: 
#                 # Update Robot Load 
#                 new_load[type_color] -= req[color]
#                 if new_load[type_color] == 0:
#                     del new_load[type_color]
                
#                 # Update Pavilion Requirements 
#                 new_req[color] = 0
#                 unloaded_anything = True # Mark that we did an action
                
#         # 2. Modify path, g_n, and facts ONLY ONCE after the loop finishes
#         if unloaded_anything:
#             new_path = (path or ()) + (f"Unload {ftype} at pavilion {p_id}",)
            
#             self.modify(rf, load=new_load, g_n=(g + 1), path=new_path)
#             self.modify(pf, requirements=new_req)       
       
     
#     @Rule(
#         AS.rf << RobotFact(
#             pos_x=MATCH.rx, pos_y=MATCH.ry, load=MATCH.load, 
#             g_n=MATCH.g, path=MATCH.path
#         ),
#         NOT(
#                 PavilionFact(p_id=MATCH.other_id, 
#                              requirements=P(lambda req : (calculate_number_of_bouquet_per_pavilion(req) > 0)
#                                         )
#                         )
#            )
#     )
#     def print_final_path(self,rx, ry, load, g, path):  
#         print("\n=== Execution Finished ===")
#         print(f"Total Cost (g_n): {g}")
#         print("Path taken:")
#         for step in path:
#             print(f"  - {step}")
                    
                    
                    
# # --- Execution ---
# engine = SmartFlowerShow()
# engine.reset()
    
# engine.declare(GridFact(x=5, y=5))
# engine.declare(WarehouseFact(pos_x=0, pos_y=1))
    
# engine.declare(RobotFact(
#     pos_x=0, pos_y=0,
#     load={},
#     g_n=0,
#     path=(),
#     max_load=0
# ))

# engine.declare(PavilionFact(p_id=0, pos_x=4, pos_y=4, flower_type="Rose", requirements={'red': 2, 'pink': 1, 'white': 1}))
# engine.declare(PavilionFact(p_id=1, pos_x=1, pos_y=3, flower_type="Tulip", requirements={'yellow': 3, 'purple': 2}))
# engine.declare(PavilionFact(p_id=2, pos_x=3, pos_y=1, flower_type="Lily", requirements={'white': 4}))

# watch('FACTS')
# engine.run()

# # # Print Final Path
# # print("\n=== Execution Finished ===")
# # for f in engine.facts.values():
# #     if isinstance(f, RobotFact):
# #         print(f"Total Cost (g_n): {f['g_n']}")
# #         print("Path taken:")
# #         for step in f.get('path', []):
# #             print(f"  - {step}")

















import collections
if not hasattr(collections, 'Mapping'):
    import collections.abc
    collections.Mapping  = collections.abc.Mapping
    collections.Sequence = collections.abc.Sequence

from experta import *
from facts import GridFact, PavilionFact, RobotFact, WarehouseFact
from utils import (
    _build_grid,
    calculate_number_of_bouquet_per_pavilion, 
    calculate_number_of_bouquet_robot_has,
    filtered_and_mapped_items_recursivly, 
    is_load_compatible, 
    is_unload_compatible,
    astar,
    print_recursivly,
    process_unloading
)

class SmartFlowerShow(KnowledgeEngine):



    @Rule(
        AS.pf << PavilionFact(requirements=MATCH.req),
        AS.rf << RobotFact(max_load=MATCH.ml),
        TEST(lambda req, ml: calculate_number_of_bouquet_per_pavilion(req) > ml)
    )
    def assign_the_maximum_load(self, pf, rf, req, ml):
       new_load = calculate_number_of_bouquet_per_pavilion(req)
       self.modify(rf, max_load=new_load)
           
           
    # ══════════════════════════════════════════
    # Movement Rules (Using A*)
    # ══════════════════════════════════════════
    @Rule(
        AS.rf << RobotFact(
            pos_x=MATCH.rx, pos_y=MATCH.ry, load=MATCH.load, 
            g_n=MATCH.g, path=MATCH.path
        ),
        WarehouseFact(pos_x=MATCH.wx, pos_y=MATCH.wy),
        PavilionFact(p_id=MATCH.p_id, pos_x=MATCH.px, pos_y=MATCH.py , requirements=MATCH.req), 
        TEST(lambda rx, ry, wx, wy, load, req:
            (rx != wx or ry != wy) and (calculate_number_of_bouquet_robot_has(load) == 0) and (calculate_number_of_bouquet_per_pavilion(req) > 0)
            )
    )
    def route_to_warehouse(self, rf, rx, ry, wx, wy, load, g, path):
        grid = _build_grid(self.facts.values(), ignore_x=wx, ignore_y=wy)
        route = astar(grid, (rx, ry), (wx, wy))
        
        #if not route:    
        #     distance = len(route) - 1
        #     new_path = (path or ()) + (f"Drive to Warehouse via {route}",)
        #     self.modify(rf, pos_x=wx, pos_y=wy, g_n=g + distance, path=new_path)
        # )
        
        (route) and (   
            self.modify(rf, pos_x=wx, pos_y=wy, g_n=(g + len(route) - 1 ), path=((path or ()) + (f"Drive to Warehouse via {route}",)))
        )


    @Rule(
        AS.rf << RobotFact(
            pos_x=MATCH.rx, pos_y=MATCH.ry, load=MATCH.load, 
            g_n=MATCH.g, path=MATCH.path
        ),
        AS.pf << PavilionFact(
            p_id=MATCH.p_id, pos_x=MATCH.px, pos_y=MATCH.py, 
            flower_type=MATCH.ftype, requirements=MATCH.req
        ),
        TEST(lambda rx, ry, px, py, load, req, ftype: 
             (rx != px or ry != py) and is_unload_compatible(load, req, ftype))
    )
    def route_to_pavilion(self, rf, rx, ry, px, py, load, g, path, req, ftype, p_id):
        grid = _build_grid(self.facts.values(), ignore_x=px, ignore_y=py)
        route = astar(grid, (rx, ry), (px, py))        
        
        # if route:
        #     distance = len(route) - 1
        #     new_path = (path or ()) + (f"Drive to Pavilion {p_id} via {route}",)
        #     self.modify(rf, pos_x=px, pos_y=py, g_n=g + distance, path=new_path)
        
        (route) and (   
            self.modify(rf, pos_x=px, pos_y=py, g_n=(g + len(route) - 1 ), path=((path or ()) + (f"Drive to Pavilion {p_id} via {route}",)))
        )


    # ══════════════════════════════════════════
    # Action Rules (Load / Unload)
    # ══════════════════════════════════════════
    # @Rule(
    #     AS.rf << RobotFact(
    #         pos_x=MATCH.rx, pos_y=MATCH.ry, load=MATCH.load, 
    #         g_n=MATCH.g, path=MATCH.path, max_load=MATCH.ml
    #     ),
    #     WarehouseFact(pos_x=MATCH.wx, pos_y=MATCH.wy),
    #     AS.pf << PavilionFact(
    #         p_id=MATCH.p_id, flower_type=MATCH.ftype, requirements=MATCH.req
    #     ),
    #     TEST(lambda rx, ry, wx, wy, load, ml, ftype, req:
    #         rx == wx and ry == wy and
    #         calculate_number_of_bouquet_robot_has(load) < ml and
    #         calculate_number_of_bouquet_per_pavilion(req) > 0 and 
    #         calculate_number_of_bouquet_per_pavilion(req) <= (ml - calculate_number_of_bouquet_robot_has(load)) and
    #         is_load_compatible(load, ftype, req) 
    #     ),
    # )
    # def load_robot(self, rf, rx, ry, load, g, path, ml, p_id, ftype, req, pf):
        
    #     def filtered_and_mapped_items_recursivly(items,filter_items):
    #         return (not items) or (items[0][1] > 0 and filter_items.add((f"{ftype}_{items[0][0]}", items[0][1])))
            
            
            
            
            
    #     # filtered_req = filter(lambda item: item[1] > 0, req.items())
    #     # mapped_items = map(lambda item: (f"{ftype}_{item[0]}", item[1]), filtered_req)

    #     mapped_items = set()
    #     filtered_and_mapped_items_recursivly(list(req.items()),mapped_items)
        
    #     new_items = dict(mapped_items)

    #     new_load  = {**load, **new_items} 

    #     new_path = (path or ()) + (f"Load {ftype} at warehouse",)
    #     self.modify(rf, load=new_load, g_n=(g + 1), path=new_path)



    @Rule(
        AS.rf << RobotFact(
            pos_x=MATCH.rx, pos_y=MATCH.ry, load=MATCH.load, 
            g_n=MATCH.g, path=MATCH.path, max_load=MATCH.ml
        ),
        WarehouseFact(pos_x=MATCH.wx, pos_y=MATCH.wy),
        AS.pf << PavilionFact(
            p_id=MATCH.p_id, flower_type=MATCH.ftype, requirements=MATCH.req
        ),
        TEST(lambda rx, ry, wx, wy, load, ml, ftype, req:
            rx == wx and ry == wy and
            calculate_number_of_bouquet_robot_has(load) < ml and
            calculate_number_of_bouquet_per_pavilion(req) > 0 and 
            calculate_number_of_bouquet_per_pavilion(req) <= (ml - calculate_number_of_bouquet_robot_has(load)) and
            is_load_compatible(load, ftype, req) 
        ),
    )
    def load_robot(self, rf, rx, ry, load, g, path, ml, p_id, ftype, req, pf):
        
        # FIXED: Proper short-circuit recursion that processes the entire list
        
        mapped_items = set()
        filtered_and_mapped_items_recursivly(list(req.items()), mapped_items, ftype)
       
        # new_items = dict(mapped_items)
        # Merge structural dictionary payloads cleanly
        
        # new_load = {**load, **new_items} 
        # new_path = (path or ()) + (f"Load {ftype} at warehouse",)
        
        self.modify(rf, load={**load, **(dict(mapped_items))} , g_n=(g + 1), path=((path or ()) + (f"Load {ftype} at warehouse",)))




    # @Rule(
    #     AS.rf << RobotFact(
    #         pos_x=MATCH.rx, pos_y=MATCH.ry, load=MATCH.load, 
    #         g_n=MATCH.g, path=MATCH.path, max_load=MATCH.ml
    #     ),
    #     AS.pf << PavilionFact(
    #         p_id=MATCH.p_id, flower_type=MATCH.ftype, 
    #         pos_y=MATCH.py, pos_x=MATCH.px, requirements=MATCH.req
    #     ),
    #     TEST(lambda rx, ry, px, py, load, g, ml, p_id, ftype, req:
    #         rx == px and ry == py and
    #         calculate_number_of_bouquet_robot_has(load) > 0 and
    #         is_unload_compatible(load, req, ftype)
    #     )
    # )
    # def unload_at_pavilion(self, rx, ry, px, py, load, g, path, ml, p_id, ftype, req, pf, rf):
    #     new_load = dict(load)  
    #     new_req = dict(req)  
        
    #     # Recursive internal function instead of a loop
    #     # def process_unloading(items, n_load, n_req, unloaded_anything):
    #     #     if not items:
    #     #         return n_load, n_req, unloaded_anything
                
    #     #     type_color, qty = items[0]
    #     #     type_, color = type_color.split('_')
            
    #     #     if type_ == ftype and color in req and req[color] > 0 and qty >= req[color]: 
    #     #         n_load[type_color] -= req[color]
    #     #         if n_load[type_color] == 0:
    #     #             del n_load[type_color]
    #     #         n_req[color] = 0
    #     #         unloaded_anything = True 
                
    #     #     return process_unloading(items[1:], n_load, n_req, unloaded_anything)



    #     def process_unloading(items, n_load, n_req, unloaded_anything):
    #         if not items:
    #             return n_load, n_req, unloaded_anything
            
    #         if items[0][0].split('_')[0] == ftype and items[0][0].split('_')[1] in req and req[items[0][0].split('_')[1]] > 0 and items[0][1] >= req[items[0][0].split('_')[1]]: 
    #             n_load[items[0][0]] -= req[items[0][0].split('_')[1]]
    #             if n_load[items[0][0]] == 0:
    #                 del n_load[items[0][0]]
    #             n_req[items[0][0].split('_')[1]] = 0
    #             unloaded_anything = True 
                
    #         return process_unloading(items[1:], n_load, n_req, unloaded_anything)



    #     new_load, new_req, unloaded = process_unloading(list(load.items()), new_load, new_req, False)

    #     unloaded and self.modify(rf, load=new_load, g_n=(g + 1), path=(path or ()) + (f"Unload {ftype} at pavilion {p_id}",)) and self.modify(pf, requirements=new_req)       
      
      
      
    
    # @Rule(
    #     AS.rf << RobotFact(
    #         pos_x=MATCH.rx, pos_y=MATCH.ry, load=MATCH.load, 
    #         g_n=MATCH.g, path=MATCH.path, max_load=MATCH.ml
    #     ),
    #     AS.pf << PavilionFact(
    #         p_id=MATCH.p_id, flower_type=MATCH.ftype, 
    #         pos_y=MATCH.py, pos_x=MATCH.px, requirements=MATCH.req
    #     ),
    #     TEST(lambda rx, ry, px, py, load, g, ml, p_id, ftype, req:
    #         rx == px and ry == py and
    #         calculate_number_of_bouquet_robot_has(load) > 0 and
    #         is_unload_compatible(load, req, ftype)
    #     )
    # )
    # def unload_at_pavilion(self, rx, ry, px, py, load, g, path, ml, p_id, ftype, req, pf, rf):
    #     new_load = dict(load)  
    #     new_req = dict(req)  

    #     def process_unloading(items, n_load, n_req, unloaded_anything):
    #         if not items:
    #             return n_load, n_req, unloaded_anything
            
    #         if items[0][0].split('_')[0] == ftype and items[0][0].split('_')[1] in req and req[items[0][0].split('_')[1]] > 0 and items[0][1] >= req[items[0][0].split('_')[1]]: 
    #             n_load[items[0][0]] -= req[items[0][0].split('_')[1]]
    #             if n_load[items[0][0]] == 0:
    #                 del n_load[items[0][0]]
    #             n_req[items[0][0].split('_')[1]] = 0
    #             unloaded_anything = True 
                
    #         return process_unloading(items[1:], n_load, n_req, unloaded_anything)

    #     new_load, new_req, unloaded = process_unloading(list(load.items()), new_load, new_req, False)
    #     unloaded and self.modify(rf, load=new_load, g_n=(g + 1), path=(path or ()) + (f"Unload {ftype} at pavilion {p_id}",)) and self.modify(pf, requirements=new_req)       
      
      
      
    @Rule(
        AS.rf << RobotFact(
            pos_x=MATCH.rx, pos_y=MATCH.ry, load=MATCH.load, 
            g_n=MATCH.g, path=MATCH.path, max_load=MATCH.ml
        ),
        AS.pf << PavilionFact(
            p_id=MATCH.p_id, flower_type=MATCH.ftype, 
            pos_y=MATCH.py, pos_x=MATCH.px, requirements=MATCH.req
        ),
        TEST(lambda rx, ry, px, py, load, g, ml, p_id, ftype, req:
            (rx == px) and (ry == py) and
            (calculate_number_of_bouquet_robot_has(load) > 0) and
            is_unload_compatible(load, req, ftype)
        )
    )
    def unload_at_pavilion(self, rx, ry, px, py, load, g, path, ml, p_id, ftype, req, pf, rf):
        # new_load = dict(load)  
        # new_req = dict(req)  
        # new_load, new_req, unloaded = process_unloading(list(load.items()), new_load, new_req, False)
        
        new_load, new_req, unloaded = process_unloading(list(load.items()), dict(load), dict(req), False, ftype)
        
        # Execute modifications only if something was unloaded
        (
            lambda: None,
            lambda: [
                self.modify(rf, load=new_load, g_n=(g + 1), path=(path or ()) + (f"Unload {ftype} at pavilion {p_id}",)),
                self.modify(pf, requirements=new_req)
            ]
        )[bool(unloaded)]()     
     
     
     
     
    @Rule(
        AS.rf << RobotFact(
            pos_x=MATCH.rx, pos_y=MATCH.ry, load=MATCH.load, 
            g_n=MATCH.g, path=MATCH.path
        ),
        NOT(
                PavilionFact(p_id=MATCH.other_id, 
                             requirements=P(lambda req : (calculate_number_of_bouquet_per_pavilion(req) > 0)
                                        )
                        )
           )
    )
    def print_final_path(self,rx, ry, load, g, path):  
        print("\n=== Execution Finished ===")
        print(f"Total Cost (g_n): {g}")
        print("Path taken:")
        # (path) and print('\n'.join(map(lambda step: f"  - {step}", path)))
        (path) and print_recursivly(path)
       

             
                    
# --- Execution ---
if __name__ == "__main__":
    engine = SmartFlowerShow()
    engine.reset()
        
    engine.declare(GridFact(x=7, y=5))
    engine.declare(WarehouseFact(pos_x=0, pos_y=1))
        
    engine.declare(RobotFact(
        pos_x=0, pos_y=0,
        load={},
        g_n=0,
        path=(),
        max_load=0
    ))

    engine.declare(PavilionFact(p_id=0, pos_x=4, pos_y=4, flower_type="Rose", requirements={'red': 2, 'pink': 1, 'white': 1}))
    engine.declare(PavilionFact(p_id=1, pos_x=1, pos_y=3, flower_type="Tulip", requirements={'yellow': 3, 'purple': 2}))
    engine.declare(PavilionFact(p_id=2, pos_x=3, pos_y=1, flower_type="Lily", requirements={'white': 4}))

    watch('FACTS')
    engine.run()

# # --- Execution (Test Cases) ---
# if __name__ == "__main__":
#     engine = SmartFlowerShow()
#     engine.reset()
        
#     # 1. اختبار مساحة أكبر لتحدي خوارزمية A* في إيجاد المسار
#     engine.declare(GridFact(x=7, y=7))
    
#     # تحديد المستودع في الزاوية
#     engine.declare(WarehouseFact(pos_x=0, pos_y=0))
        
#     # 2. اختبار الروبوت: حمولة مبدئية صفر (لنجعل قاعدة assign_the_maximum_load تعمل)
#     engine.declare(RobotFact(
#         pos_x=0, pos_y=0,
#         load={},
#         g_n=0,
#         path=(),
#         max_load=0 
#     ))

#     # 3. سيناريوهات الأجنحة:
    
#     # الجناح 0: يطلب كمية كبيرة جداً (لاختبار تعديل سعة الروبوت تلقائياً)
#     engine.declare(PavilionFact(
#         p_id=0, pos_x=6, pos_y=6, 
#         flower_type="Rose", 
#         requirements={'red': 5, 'pink': 3, 'white': 2} # المجموع 10
#     ))
    
#     # الجناح 1: يقع في المنتصف تماماً (يعمل كعقبة في طريق الجناح 0 وخوارزمية A*)
#     engine.declare(PavilionFact(
#         p_id=1, pos_x=3, pos_y=3, 
#         flower_type="Tulip", 
#         requirements={'yellow': 3, 'purple': 1}
#     ))
    
#     # الجناح 2: يطلب لون مشترك (white) مع الجناح 0 لاختبار التوافق (is_load_compatible)
#     engine.declare(PavilionFact(
#         p_id=2, pos_x=0, pos_y=5, 
#         flower_type="Lily", 
#         requirements={'white': 4, 'orange': 2}
#     ))

#     # الجناح 3: جناح قريب جداً من المستودع بطلب صغير
#     engine.declare(PavilionFact(
#         p_id=3, pos_x=1, pos_y=0, 
#         flower_type="Orchid", 
#         requirements={'blue': 1}
#     ))

#     watch('FACTS')
#     engine.run()

