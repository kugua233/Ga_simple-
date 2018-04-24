#ploy_mutation  对实数的多项式变异
import random
def ploy_mutation(offspring, Pm, dec_num, dec_min_val, dec_max_val, Dm):
    for i in range(len(offspring)):
        for j in range(dec_num):
            r = random.random()
            #对个体某变量进行变异
            if r <= Pm:
                y = offspring[i][j]     #第i个个体的第j个变量
                low = dec_min_val[j]
                up = dec_max_val[j]
                delta1 = 1.0*(y-low)/(up-low)   #1.0保证精度不为整数
                delta2 = 1.0*(up-y)/(up-low)
                r = random.random()
                mut_pow = 1.0/(Dm+1.0)  #最外层因子
                if r <= 0.5:
                    var = 1.0-delta1
                    lambda_ = 2.0*r+(1.0-2.0*r)*(var**(Dm+1.0))
                    deltaq = lambda_**mut_pow-1.0
                else:
                    var = 1.0-delta2
                    lambda_ = 2.0*(1.0-r)+2.0*(r-0.5)*(var**(Dm+1.0))
                    deltaq = 1.0-lambda_**mut_pow
                y = y+deltaq*(up-low)
                y = min(up, max(y, low))
                offspring[i][j] = y

def m_binary(offspring, Pm, dec_num, dec_min_val, dec_max_val, Dm):
    for i in range(len(offspring)):
        if Pm > random.random():
            pop = offspring[i]
            for j in range(dec_num):
                index = random.randint(0, len(pop[j])-1)
                str = pop[j]
                k = str[index]
                k = inverse(k)
                newstr = str[:index] + k + str[index:]
                pop[j] = newstr


def inverse(k):
    r = '1'
    if k == '1':
        r = '0'
    return r