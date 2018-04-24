#SBX
import random
import copy


#父代随机选两个，产生两个子代
def SBXcross_2c(population, Pc, dec_num, dec_min_val, dec_max_val, Dc):
    offspring = copy.deepcopy(population)
    for i in range(0, len(population), 2):     #随机选两个产生两个
        if random.random() > Pc:
            continue
        index1 = 0
        index2 = 0
        while index1 == index2:
            index1 = random.randint(0, len(population) - 1)
            index2 = random.randint(0, len(population) - 1)
        #对两个个体执行SBX交叉操作
        for j in range(dec_num):    #个体的第j个变量
            #对某自变量交叉
            lower = dec_min_val[j]
            uper = dec_max_val[j]
            parent1 = population[index1][j]
            parent2 = population[index2][j]
            r = random.random()
            if r <= 0.5:
                betaq = (2*r)**(1.0/(Dc+1.0))
            else:
                betaq = (0.5/(1.0-r))**(1.0/(Dc+1.0))

            child1 = 0.5*((1+betaq)*parent1+(1-betaq)*parent2)
            child2 = 0.5*((1-betaq)*parent1+(1+betaq)*parent2)
            child1 = min(max(child1, lower), uper)  #边界保护
            child2 = min(max(child2, lower), uper)

            offspring[index1][j] = child1
            offspring[index2][j] = child2
    return offspring


#为每个父代选配偶，每次产生一个子代
def SBXcross_1c(population, Pc, dec_num, dec_min_val, dec_max_val, Dc):
    offspring = []
    i = 0
    while i < len(population)-1:
        # 对两个个体执行SBX交叉操作
        i = len(offspring)
        temp = []
        index = random.randint(0, len(population) - 1)
        while index == i:
            index = random.randint(0, len(population) - 1)
        for j in range(dec_num):  # 个体的第j个变量
            lower = dec_min_val[j]
            uper = dec_max_val[j]
            parent1 = population[i][j]
            parent2 = population[index][j]
            r = random.random()
            if r <= 0.5:
                betaq = (2 * r) ** (1.0 / (Dc + 1.0))
            else:
                betaq = (0.5 / (1.0 - r)) ** (1.0 / (Dc + 1.0))
            child1 = 0.5 * ((1 + betaq) * parent1 + (1 - betaq) * parent2)
            child2 = 0.5 * ((1 - betaq) * parent1 + (1 + betaq) * parent2)
            child1 = min(max(child1, lower), uper)  # 边界保护
            child2 = min(max(child2, lower), uper)
            r = random.random()
            if r <= 0.5:
                child = child1
            else:
                child = child2
            temp.append(child)
        offspring.append(temp)
    return offspring


def c_binary(population, Pc, dec_num, dec_min_val, dec_max_val, Dc):
    offspring = []
    for i in range(0, len(population), 2):
        if random.random() > Pc:
            continue
        index1 = 0
        index2 = 0
        temp = []
        while index1 == index2:  # 保证选到两个不同的个体
            index1 = random.randint(0, len(population) - 1)
            index2 = random.randint(0, len(population) - 1)
        for j in range(dec_num):
            parent1_str = population[index1][j]
            parent2_str = population[index2][j]
            index_str = random.randint(0, len(parent1_str) - 1)  # pop_i在两个片段中各选一个分割点，然后分别进行单点交换，得到交换后的两个新个体
            temp.append(parent1_str[:index_str]+parent2_str[index_str:])
        offspring.append(temp)
    return offspring


def de():
    pass