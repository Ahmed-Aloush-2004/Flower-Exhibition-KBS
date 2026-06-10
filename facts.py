
# from experta import Fact, Field





# class GridFact(Fact):
#     x = Field(int, default=5)
#     y = Field(int, default=5)
    
    

# class WarehouseFact(Fact):
#     pos_x = Field(int)
#     pos_y = Field(int)    
    



# class RobotFact(Fact):
#     pos_x = Field(int, default=0)
#     pos_y = Field(int, default=0)
#     load  = Field(dict, mandatory=False)   # {flower_type: {color: qty}}
#     g_n   = Field(int, default=0)          # ✅ التكلفة الفعلية — ضرورية لـ A*
#     # path  = Field(list, mandatory=False)   # ✅ سجل العمليات — ضرورية للطباعة
#     path  = Field(tuple, mandatory=False)   # ← غيّر list إلى tuple
#     max_load = Field(int, default=0)       # ✅ الحمولة القصوى



# class PavilionFact(Fact):
#     p_id        = Field(int)    # ✅ ضروري للتمييز بين الأجنحة
#     pos_x       = Field(int)
#     pos_y       = Field(int)
#     flower_type = Field(str)
#     requirements = Field(dict)  # {'red': 2, 'pink': 1}



    
    
    
    
from experta import Fact, Field





class GridFact(Fact):
    x = Field(int, default=5)
    y = Field(int, default=5)
    
    

class WarehouseFact(Fact):
    pos_x = Field(int)
    pos_y = Field(int)   
    
    
     

class RobotFact(Fact):
    pos_x = Field(int, default=0)
    pos_y = Field(int, default=0)
    load  = Field(dict, mandatory=False)   # {flower_type: {color: qty}}
    g_n   = Field(int, default=0)          # ✅ التكلفة الفعلية — ضرورية لـ A*
    path  = Field(tuple, mandatory=False)  # ✅ غيّر list إلى tuple
    max_load = Field(int, default=0)       # ✅ الحمولة القصوى
    
    
    

class PavilionFact(Fact):
    p_id        = Field(int)    # ✅ ضروري للتمييز بين الأجنحة
    pos_x       = Field(int)
    pos_y       = Field(int)
    flower_type = Field(str)
    requirements = Field(dict)  # {'red': 2, 'pink': 1}
    