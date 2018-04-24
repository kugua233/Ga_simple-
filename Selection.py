import math

def selection(merge, popobj, popsize,population):
    del popobj[:]
    del population[:]
    for i in merge:
        popobj.append(object_fun(i))
    index = sorted(range(len(popobj)), key=lambda k: popobj[k], reverse=True) #从小到大的索引值
    for i in range(popsize):
        population.append(merge[index[i]])
    score = popobj[index[0]]
    return score


def sel_binart(merge, popobj, popsize,population, min, max):
    del popobj[:]
    del population[:]
    for i in merge:
        popobj.append(binary_fun(i, min, max))
    index = sorted(range(len(popobj)), key=lambda k: popobj[k], reverse=True)  # 从小到大的索引值
    for i in range(popsize):
        population.append(merge[index[i]])
    score = popobj[index[0]]
    return score


def object_fun(p):
    x1 = p[0]
    x2 = p[1]
    y = 21.5 + x1 * math.sin(4 * math.pi * x1) + x2 * math.sin(20 * math.pi * x2)
    return y


def binary_fun(p, min, max):
    x1 = min[0]+int(p[0], 2)*(max[0]-min[0])*1.0/(2**len(p[0])-1)
    x2 = min[1]+int(p[1], 2)*(max[1]-min[1])*1.0/(2**len(p[1])-1)
    y = 21.5 + x1 * math.sin(4 * math.pi * x1) + x2 * math.sin(20 * math.pi * x2)
    return y