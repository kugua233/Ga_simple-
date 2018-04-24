import random
import math

def init(population, pop_size, dec_num, dec_min_val, dec_max_val):
    rangeRealVal = [dec_max_val[i]-dec_min_val[i] for i in range(dec_num)]
    for i in range(pop_size):
        tempIndividual=[]
        for j in range(dec_num):
            temp = random.uniform(0, 1)*rangeRealVal[j]+dec_min_val[j]
            tempIndividual.append(temp)
        population.append(tempIndividual)   #population为[[由多个变量组成的个体一],[],[]..[]]


def init_binary(population, pop_size, dec_num, dec_min_val, dec_max_val):
    precision = 10**4
    length = []
    # length = [math.ceil(math.log((dec_max_val[i]-dec_min_val[i])*precision, 2)) for i in range(dec_num)]
    for i in range(dec_num):
        temp = (dec_max_val[i] - dec_min_val[i]) * precision
        length.append(math.ceil(math.log(temp,2)))
    for i in range(pop_size):
        tempIndividual = []
        for j in range(dec_num):
            temp = ''
            for k in range(length[j]):
                temp += str(random.randint(0, 1))
            tempIndividual.append(temp)
        population.append(tempIndividual)   #单变量转为了字符串存储



def init_unifor():
    pass


#测试代码
# if __name__=="__main__":
#     population=[]
#     N=200
#     V=2
#     minRealVal=(-5, -5)
#     maxRealVal=(5, 5)
#     population_init(population, N, V, minRealVal, maxRealVal)
#     print population