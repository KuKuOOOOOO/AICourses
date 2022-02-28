import random as rd
import copy
from matplotlib import pyplot as plt
import time

#--------------------------Define Distance--------------------------------
def DistanceHereToInitial(From, Initial):
    return Distance[From][Initial]

#---------------------------Define Route----------------------------------
class Route:
    def __init__(self, path):
        # path is a list of Location obj
        self.path = path
        self.length = self._set_length()

    def _set_length(self):
        total_length = 0
        path_copy = self.path[:]
        from_here = path_copy.pop(0)
        init_node = copy.deepcopy(from_here)
        while path_copy:
            to_there = path_copy.pop(0)
            total_length += DistanceHereToInitial(from_here, init_node)
            from_here = copy.deepcopy(to_there)
        total_length += DistanceHereToInitial(from_here, init_node)
        return total_length

# -----------------------------Define Genetic Algorithm-------------------------------
class GeneticAlgo:
    def __init__(self, locs, level=10, populations=100, cross=0.5, variant=3, mutate_percent=0.01, elite_save_percent=0.1, levelbest=[], levelworst=[], levelaverage=[]):
        self.locs = locs
        self.level = level
        self.variant = variant
        self.populations = populations
        self.cross = cross
        self.mutates = int(populations * mutate_percent)
        self.elite = int(populations * elite_save_percent)
        self.levelbest = levelbest
        self.levelworst = levelworst
        self.levelaverage = levelaverage

#----------------------Initial Population-----------------------------------------
    def _find_path(self):
        # locs is a list containing all the Location obj
        locs_copy = self.locs[:]
        path = []
        while locs_copy:
            to_there = locs_copy.pop(locs_copy.index(rd.choice(locs_copy)))
            path.append(to_there)
        return path

    def _init_routes(self):
        routes = []
        for _ in range(self.populations):
            path = self._find_path()
            routes.append(Route(path))
        return routes

# -----------------------Fitness Function + Selection---------------------------
    def _get_next_route(self, routes):
        routes.sort(key=lambda x: x.length, reverse=False)
        self.levelbest.append(routes[0])
        self.levelworst.append(routes[-1])
        SumRoutes = 0
        for sum_routes in routes:
            SumRoutes += sum_routes.length
        self.levelaverage.append(SumRoutes/len(routes))
        elites = routes[:self.elite][:]
        if ChooseFunction == 1:
            crossovers = self._crossover_function1(elites)
        elif ChooseFunction == 2:
            crossovers = self._crossover_function2(elites)
        return crossovers[:] + elites

# -----------------------------Crossover Function1-------------------------------
    # 第一種交配+突變方式 擷取父親的一部份路徑(長度為變異數variant) 將母親中有包含在這個路徑的程式去掉 然後再隨機選取位置插入此路徑
    def _crossover_function1(self, elites):
        # Route is a class type
        normal_breeds = []
        mutate_ones = []
        for _ in range(int(self.cross * self.populations)):
            father, mother = rd.choices(elites[:4], k=2)
            index_start = rd.randrange(0, len(father.path) - self.variant - 1)
            # list of Location obj
            father_gene = father.path[index_start: index_start + self.variant]
            father_gene_names = [loc for loc in father_gene]
            mother_gene = [
                gene for gene in mother.path if gene not in father_gene_names]
            mother_gene_cut = rd.randrange(1, len(mother_gene))
            # create new route path
            next_route_path = mother_gene[:mother_gene_cut] + \
                father_gene + mother_gene[mother_gene_cut:]
            next_route = Route(next_route_path)
            # add Route obj to normal_breeds
            normal_breeds.append(next_route)
            MutationSeed = rd.randint(1, self.populations+1)
#----------------------------Mutation Function1----------------------------------
            if MutationSeed <= self.mutates * self.populations:
                # 突變方式：將父代路徑中隨機兩個城市調換位置
                # for mutate purpose
                copy_father = copy.deepcopy(father)
                idx = range(len(copy_father.path))
                gene1, gene2 = rd.sample(idx, 2)
                copy_father.path[gene1], copy_father.path[gene2] = copy_father.path[gene2], copy_father.path[gene1]
                mutate_ones.append(copy_father)
        mutate_breeds = rd.choices(mutate_ones, k=self.mutates)
        return normal_breeds + mutate_breeds

# -----------------------------Crossover Function1-------------------------------
    # 第二種交配方式 隨機選取父親路徑中的"變異數大小(variant)"的城市 將母親中這些城市去掉 並插入母親路徑中隨機位置
    def _crossover_function2(self, elites):
        # Route is a class type
        normal_breeds = []
        mutate_ones = []
        for _ in range(int(self.cross * self.populations)):
            father, mother = rd.choices(elites[:4], k=2)
            temp = []
            father_copy = copy.deepcopy(father)
            for _ in range(self.variant):
                if len(father_copy.path) - 1 != 0:
                    randchoice = rd.randint(0, len(father_copy.path) - 1)
                    temp.append(father_copy.path[randchoice])
                    father_copy.path.pop(randchoice)
                else:
                    temp.append(father_copy.append[0])
                    father_copy.path.pop(0)
            father_gene = copy.deepcopy(temp)
            father_gene_names = [ loc for loc in father_gene]
            mother_gene = [ gene for gene in mother.path if gene not in father_gene_names]
            insertnum = len(elites)-self.variant
            for i in range(self.variant):
                randchoice = rd.randint(insertnum, 0)
                mother_gene.insert(randchoice, father_gene[i])
                insertnum += 1
            # create new route path
            next_route_path = copy.deepcopy(mother_gene)
            next_route = Route(next_route_path)
            # add Route obj to normal_breeds
            normal_breeds.append(next_route)
            MutationSeed = rd.randint(1, self.populations + 1)
#----------------------------Mutation Function2----------------------------------
            if MutationSeed <= self.mutates * self.populations:
                # 突變方式：將父代路徑的頭尾互換
                # for mutate purpose
                copy_father = copy.deepcopy(father)
                copy_father.path.insert(0, copy_father.path[-1])
                copy_father.path.pop()
                mutate_ones.append(copy_father)
        mutate_breeds = rd.choices(mutate_ones, k=self.mutates)
        return normal_breeds + mutate_breeds

#----------------------------Evolution Process------------------------------------
    def evolution(self):
        routes = self._init_routes()
        for _ in range(self.level):
            routes = self._get_next_route(routes)
        routes.sort(key=lambda x: x.length)
        self.levelbest.append(routes[0])
        self.levelworst.append(routes[-1])
        SumRoutes = 0
        for sum_routes in routes:
            SumRoutes += sum_routes.length
        self.levelaverage.append(SumRoutes/len(routes))
        return routes[0].path, routes[0].length
    
#-------------------------------Get Best, Worst, Average-------------------------
    def GetBestCost(self):
        return self.levelbest
    def GetWorstCost(self):
        return self.levelworst
    def GetAverageCost(self):
        return self.levelaverage

#-------------------------------Load File----------------------------------------
FileOpen = open("test4.txt", "r")
Temp = FileOpen.read()
TempSplit = Temp.split()
Temp = []
for i in range(1, len(TempSplit)):
    Temp.append(int(TempSplit[i]))

Node = int(TempSplit[0])
Distance = [[] for _ in range(Node)]
Count = 0
for i in range(Node):
    for j in range(Node):
        Distance[i].append(Temp[Count])
        Count += 1

Locations = []
for i in range(Node):
    Locations.append(i)

#------------------------------User Input List-----------------------------------
ChooseFunction = 0
while ChooseFunction == 0:
    try:
        print("基因演算法說明:")
        print("第一種交配+突變方式:擷取父親的一部份路徑, 將母親中有包含在這個路徑的程式去掉, 然後再隨機選取位置插入此路徑")
        print("第二種交配+突變方式:隨機選取父親路徑中的\"變異數大小(variant)\"的城市, 將母親中這些城市去掉, 並插入母親路徑中隨機位置")
        print("請選擇想要使用的基因演算法(1 or 2):", end="")
        ChooseFunction = int(input())
        if ChooseFunction < 1 or  ChooseFunction > 2 :
            print("輸入錯誤，請重新輸入!!")
            ChooseFunction = 0
    except ValueError:
        print("輸入錯誤，請重新輸入!!")
        ChooseFunction = 0
        continue
DeBugTag = 1
while DeBugTag == 1:
    try:
        print("請輸入交配機率(介於0~1之間):", end="")
        CrossInput = float(input())
        if CrossInput > 1 or CrossInput < 0:
            print("輸入錯誤，請重新輸入!!")
        else:
            DeBugTag = 0
    except ValueError:
        print("輸入錯誤，請重新輸入!!")
        DeBugTag = 1
        continue
while DeBugTag == 0:
    try:
        print("請輸入突變機率(介於0~1之間):", end="")
        MuInput = float(input())
        if MuInput > 1 or MuInput < 0:
            print("輸入錯誤，請重新輸入!!")
        else:
            DeBugTag = 1
    except ValueError:
        print("輸入錯誤，請重新輸入!!")
        DeBugTag = 0
        continue
while DeBugTag == 1:
    try:
        print("請輸入母體群數(建議輸入>7之數字):", end="")
        PopInput = int(input())
        if PopInput < 7:
            print("輸入7以下數字會造成空list例外狀況，請重新輸入!!")
        else:
            DeBugTag = 0
    except ValueError:
        print("輸入錯誤，請重新輸入!!")
        DeBugTag = 1
print("請輸入產生代數:", end="")
LevelInput = int(input())

#------------------------------Calculate and Print Output-----------------------------------
BestCost = []
WorstCost = []
StartTime = time.time()
AvargeCost = []
GACal = GeneticAlgo(Locations, LevelInput, PopInput, CrossInput, variant=3, mutate_percent=MuInput,
                      elite_save_percent=0.15, levelbest=BestCost, levelworst=WorstCost, levelaverage=AvargeCost)
Best_Route, Best_Route_Length = GACal.evolution()
LevelBestRoute = GACal.GetBestCost()
LevelWorstRoute = GACal.GetWorstCost()
EndTime = time.time()
print("所花費時間為", (EndTime - StartTime), "秒")
for i in range(1, LevelInput + 1):
    print("第", i, "代的最佳值為:", LevelBestRoute[i].length,"，最差值為:", LevelWorstRoute[i].length, "，平均值為:", AvargeCost[i])

#------------------------------Show Generation and Cost Summary Grpah-----------------------
plt.xlabel('Generation')
plt.ylabel('Cost')
PltBestCost = []
PltWorstCost = []
PltAverageCost = []
Generation = []
for i in range(1, LevelInput + 1):
    PltBestCost.append(LevelBestRoute[i].length)
for i in range(1, LevelInput + 1):
    PltWorstCost.append(LevelWorstRoute[i].length)
for i in range(1, LevelInput + 1):
    PltAverageCost.append(AvargeCost[i])
for i in range(1, LevelInput + 1):
    Generation.append(i)
PlotBestCost = plt.plot(Generation, PltBestCost, label = "Best")
PlotWorstCost = plt.plot(Generation, PltWorstCost, label = "Worst")
PlotAverageCost = plt.plot(Generation, PltAverageCost, label = "Average")
plt.legend(loc="upper right")
plt.show()

