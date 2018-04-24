# import matplotlib.pyplot as plt
from Init_population import init, init_binary
from Cross import SBXcross_2c, SBXcross_1c, c_binary
from Mutation import ploy_mutation,m_binary
from Selection import selection,sel_binart


"""
:parameter setting
"""
pop_size = 100
max_gen = 100
precision = 100000
dec_num = 2
obj_num = 1
dec_min_val = (-3, 4.1)
dec_max_val = (12.1, 5.8)
population = []     #[var1,var2，..],[],[]..[]]
popobj = []
Pc = 0.9
Pm = 0.01
Dc = 20
Dm = 20


if __name__ == '__main__':
    init_binary(population, pop_size, dec_num, dec_min_val, dec_max_val)
    for i in range(max_gen):
        offspring = c_binary(population, Pc, dec_num, dec_min_val, dec_max_val, Dc)
        m_binary(offspring, Pm, dec_num, dec_min_val, dec_max_val, Dm)
        merge = population+offspring
        # score = selection(merge, popobj, pop_size, population)
        score = sel_binart(merge, popobj, pop_size, population, dec_min_val, dec_max_val, precision)
        print(score)



