简单的遗传算法
=======


导言
---

研究生研究的领域就是用启发算法来解决超多目标优化问题，所谓的超多目标就是要同时优化目标维数超过3维且目标之间具有一定矛盾性的问题。例如从深圳到北京的交通路线，我们若只考虑时间与价格这两个目标问题（二维多目标问题），会存在时长最短但是价格昂贵的路线选择（例如航班直达），也会存在价格最便宜但是很花时间的路线（例如辗转火车公交），不会存在时长最短价格最便宜的最优路线。解决多目标问题的启发算法里，遗传算法和粒子群算法的论文较多，今天讲一下简单的遗传算法。

算法思想
-----
遗传算法主要是用达尔文进化论的观点，优胜劣汰适者生存，能更好地适应环境的个体将会保留下来，这些拥有较好适应度的个体基因会传给下一代，让好基因广为流传，活埋不好的基因。遗传算法主要包括种群初始化，交叉，变异和环境选择四个主要操作。遗传算法属于随机性算法，不能找到最优解，只能找到近优解，除非是非常简单的问题。

算法过程
----
比如我们要解决一个简单的单目标问题，求解目标f的最大值，x1、x2变量有约束范围

```
max f (x1, x2) = 21.5 + x1·sin(4 pi x1) + x2·sin(20 pi x2)
s. t. -3.0 <= x1 <= 12.1
        4.1 <= x2 <= 5.8

```
对于这类连续问题，其实可以不采用网上最基础的二进制编码来进行单点交叉和单点变异的操作了。实数也可以，只要把交叉和变异操作采用模拟二进制交叉simulated binary crossover（SBX）和多项式变异Polynomial mutation就好了。所以这里的种群个体可以采用[x1,x2]的数值来代表一个个体。

首先进行种群初始化，返回一个大小为100的种群列表，每个元素代表一个由两个变量构成的个体

```
pop_size = 100    #种群规模
population = []
dec_num = 2    #变量个数
dec_min_val = (-3, 4.1)
dec_max_val = (12.1, 5.8)

def init(population, pop_size, dec_num, dec_min_val, dec_max_val):
    rangeRealVal = [dec_max_val[i]-dec_min_val[i] for i in range(dec_num)]    #范围长度
    for i in range(pop_size):
        tempIndividual=[]
        for j in range(dec_num):
            temp = random.uniform(0, 1)*rangeRealVal[j]+dec_min_val[j]  #确保变量在范围类内 
            tempIndividual.append(temp)
        population.append(tempIndividual)   #population为[[dec1,dec2],[],[]..[]]   
```

初始化种群后开始选择种群个体交配产生下一代，这里采用SBX，是通过二进制单点交叉改进的。例如现在有个体A的x1=9，个体B的x1变量为18，根据变量x1的约束范围可以算出x1的二进制编码长度，假设长度为6，则个体A的x1=001001,个体B有X1=010010,根据二进制单点交叉，选定随机一个index，例如index=3，则将两个个体的前三位互换，得到new_x1=010001和new_x2=001010。



~x1和~x2是根据父代x1和x2进行SBX后的子代，代码如下，随机挑选两个父代并产生两个子代。

```
Pc = 0.9     #交叉概率 小于这个概率的个体才进行交叉操作
Dc = 1    #交叉步长，步长越大，产生子代离父代越远的概率越大
def SBXcross_2c(population, Pc, dec_num, dec_min_val, dec_max_val, Dc):
    offspring = copy.deepcopy(population)
    for i in range(0, len(population), 2):     #随机选两个产生两个
        if random.random() > Pc:
            continue
        index1 = 0
        index2 = 0
        while index1 == index2:    #保证选到的两个父代不相同
            index1 = random.randint(0, len(population) - 1)
            index2 = random.randint(0, len(population) - 1)
        #对两个个体执行SBX交叉操作
        for j in range(dec_num):    #个体的第j个变量
            lower = dec_min_val[j]
            uper = dec_max_val[j]
            parent1 = population[index1][j]
            parent2 = population[index2][j]
            r = random.random()
            if r <= 0.5:    #betaq是采用了概率模型计算出来的，可以不用管，照着套就好了
                betaq = (2*r)**(1.0/(Dc+1.0))
            else:
                betaq = (0.5/(1.0-r))**(1.0/(Dc+1.0))

            child1 = 0.5*((1+betaq)*parent1+(1-betaq)*parent2)    #
            child2 = 0.5*((1-betaq)*parent1+(1+betaq)*parent2)
            child1 = min(max(child1, lower), uper)  #边界保护，以防超出
            child2 = min(max(child2, lower), uper)

            offspring[index1][j] = child1
            offspring[index2][j] = child2
    return offspring    #返回新生成种群
```



产生的子代需要进行变异操作，这可以有一定几率让解跳出局部最优，去寻找全局最优。

变异过程的代码如下

```
Pm = 0.1    #变异概率，小于这个概率的个体进行变异
Dm = 1    #变异步长
def ploy_mutation(offspring, Pm, dec_num, dec_min_val, dec_max_val, Dm):
    for i in range(len(offspring)):
        for j in range(dec_num):    
            r = random.random()
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
```
这样进行交叉和变异操作后，我们就得到了父代种群population和子代群众offspring.接下来的就是优胜劣汰的环境选择。环境选择的一部分太多不同的策略，基础本采用轮盘赌的那种策略是交叉过程中子代完全取代父代，然后根据适应值大小来决定轮盘概率的大小。自己很少采用这种方式，采用的是稳态进化的方式。主流的有N+1,N+q,和N+N模式，N+1模式是N个父代产生一个个体的时候，就要N+1种群里淘汰一个最差的个体。N+N采用的是N个父代产生N个子代，然后从2N个种群里选择最好的N个个体进入下一代，上面population+offspring就是N+N的模式了。

N+N环境选择的代码如下

```
popobj =[] #存储个体的适应值，这里为目标函数y的大小，适应值越高越需要留下
merge = population + offspring

def selection(merge, popobj, popsize,population):
    del popobj[:]
    del population[:]    #用来存储被保留的种群进入下一代
    for i in merge:    #计算每个个体的适应值大小
        popobj.append(object_fun(i))
    #根据适应值大小排序，取前N个拥有高适应值的个体存留下来
    index = sorted(range(len(popobj)), key=lambda k: popobj[k], reverse=True) #从小到大的索引值
    for i in range(popsize):
        population.append(merge[index[i]])
    score = popobj[index[0]]    #计算当前拥有最高适应值的个体的目标函数值y
    return score
   
def object_fun(p):
    x1 = p[0]
    x2 = p[1]
    y = 21.5 + x1 * math.sin(4 * math.pi * x1) + x2 * math.sin(20 * math.pi * x2)
    return y
```
这篇文章的代码放在github页面上：
代码也写了二进制单点模拟交叉，父代每次只产生一个子代的方式的交叉方式，差分进化的方式以后再补吧。代码量比较少，没有去优化，想用为一个遗传算法小框架的话，还是要组织代码结构，可以进行不同的初始化，交叉，变异和环境选择操作。