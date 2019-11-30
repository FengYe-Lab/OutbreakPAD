import math
import random
import time
import numpy as np
import matplotlib.pylab  as plt
import pandas as pd
#
# define C(t,+) computation module
def compute_Ctplus(sample, miu0, k):
    # obtain length of the 'method-wrapper' object: sample (for usage in the iteration)
    l = sample.__len__()
    # define vector container
    Ctplus = [0] * l
    # define C(0,+)=0
    Ctplus[0] = 0
    # define a iterator to compute C(t,+), t>=1
    iterator = tuple(range(1, l))
    for i in iterator:
        # define C(t,+)=max(0,C(t-1,+)+Xt-empirical_mean-allowance constant)
        Ctplus[i] = max(Ctplus[i - 1] + (sample[i] - miu0) - k, 0)
    # this is a vector function which return CUSUM vector:Ctplus
    return Ctplus


# define bootstrapping resampling module
def resampling(ICdata):
    # obtain length of the 'method-wrapper' object: ICdata (for usage in the iteration)
    l = ICdata.__len__()
    # define vector container
    resample = [0] * l
    # initialize random seed for the following montecarlo resampling with the iteration
    random.seed()
    # define a iterator for collecting resample points
    iterator = tuple(range(l))
    for i in iterator:
        # cout<<"i="<<i<<endl;
        # uniform(1,sample_size) distributed montecarlo resampling
        resample[i] = ICdata[random.randrange(0, l - 1)]
        # cout<<"sample size and random# are: "<<sample.size()<<"\t"<<rand()%sample.size()<<endl;
    # this is a vector function which return resample vector
    return resample


# -----------------------------------------------------------------------------
# main model
# time counting begins
def Pvalue_CUSUM(data, k):
    #     t0=time.perf_counter()

    # request input of allowance constant and sample size
    #     k=float(input("Enter the allowance constant: "))
    #     s=int(input("Enter the size of your sample: "))
    s = len(data)
    ##divide sample size into two equal pieces of capacity m, with the former piece used as In-control data, and the latter used as the testing data
    m = math.ceil(s / 2)
    # initialize ICdata vector
    ICdata = [0] * m
    # initialize sum of ICdata vector, for later calculation of ICdata mean
    IC_sum = 0
    # open text file from the path your file (which better be a single column data) is stored at
    # with open('/home/zoushengmei/script/origin_values.txt') as file1:
    #     #read data line by line
    #     lines1=file1.readlines()
    lines1 = data
    # see above
    iterator1 = tuple(range(m))
    for i in iterator1:
        # store every line of numerical ICdata read from the file
        ICdata[i] = float(lines1[i])
        # cumulate thqe sum of ICdata vector
        IC_sum += ICdata[i]
        # cout<<"ICdata no."<<i+1<<" is: \t"<<ICdata[i]<<endl;
    # compute the mean of ICdata vector
    IC_mean = IC_sum / m
    # cout<<"ICdata_mean is:\t"<<IC_mean<<endl;

    # request input of the number of times of montecarlo resampling
    #     M=int(input("Enter the number of times of resampling: "))
    M = 2000
    # initialize m vectors of empirical Ctplus distribution simulated by M times of montecarlo resampling
    Ctplus_empirical_distribution = [0] * m
    for i in iterator1:
        # initialize each of the m empirical distribution vectors, each with a capacity of M
        Ctplus_empirical_distribution[i] = [0] * M  # maximum significance level adopted is 1/10
        # cout<<"size of em_dist. is:\t"<<Ctplus_empirical_distribution[i].size()<<endl;

    # initialize resample vector for later calling on resampling module we previously defined
    resample = [0] * m
    # initialize resample's Ctplus vector for later calling on resampling module we previously defined
    resample_Ctplus = [0] * m
    # see above
    iterator2 = tuple(range(M))
    for i in iterator2:
        # calling resampling module
        resample = resampling(ICdata)
        # cout<<"count resample times: time "<<i+1<<endl;
        # calling C(t,+) computation module
        resample_Ctplus = compute_Ctplus(resample, IC_mean, k)
        # cout<<endl;
        for j in iterator1:
            # store the resample's Ctplus to the empirical Ctplus distribution vector, at every time t (t=1,...,m)
            Ctplus_empirical_distribution[j][i] = resample_Ctplus[j];
            # cout<<"resample\t"<<resample[j]<<endl;
            # cout<<"resample_Ctplus\t"<<resample_Ctplus[j]<<endl;

    # initialize the testing sample vector
    Testdata = [0] * m
    for i in iterator1:
        #   store every line of numerical testing data read from the file
        Testdata[i] = float(lines1[i + m - 1])
        # cout<<"Testdata no."<<m+i+1<<" is: \t"<<Testdata[i]<<endl;

    # calling on C(t,+) computation module to compute the Ctplus of the testing data
    Testdata_Ctplus = compute_Ctplus(Testdata, IC_mean, k)

    # compute Ctplus critical values at various significance level: alpha1=0.1, alpha2=0.05,alpha3=0.01
    # compute the pvalue of the Ctplus of the testing data
 #   print("The computed Ctplus Testdata value and the simulated Ctplus critical value at alpha=0.1,0.05,0.01 are:")
    rank_Testdata_Ctplus = [0] * m
    pvalue_Testdata_Ctplus = [0] * m
    Ctplus_alpha1 = [0] * m
    Ctplus_alpha2 = [0] * m
    Ctplus_alpha3 = [0] * m
    Ctplus = []
    for i in iterator1[1:]:
        Ctplus_empirical_distribution[i].sort()
        rank_Testdata_Ctplus[i] = min(range(M),
                                      key=lambda j: abs(Ctplus_empirical_distribution[i][j] - Testdata_Ctplus[i]))
        # cout<<rank_Testdata_Ctplus[i]<<endl;
        pvalue_Testdata_Ctplus[i] = (M - rank_Testdata_Ctplus[i]) / (M);
        # cout<<pvalue_Testdata_Ctplus[i]<<endl;
        Ctplus_alpha1[i] = Ctplus_empirical_distribution[i][int(M - M / 10 - 1)];
        Ctplus_alpha2[i] = Ctplus_empirical_distribution[i][int(M - M / 20 - 1)];
        Ctplus_alpha3[i] = Ctplus_empirical_distribution[i][int(M - M / 100 - 1)];
        #         print("C(",m+i,",+) of Testdata/pvalue/alpha0.1/0.05/0.01\t",Testdata_Ctplus[i],("\t\t","   \t")[Testdata_Ctplus[i]<1e-10 or Testdata_Ctplus[i]>(1-1e-10)],pvalue_Testdata_Ctplus[i],("\t\t","   \t")[pvalue_Testdata_Ctplus[i]<1e-10 or pvalue_Testdata_Ctplus[i]>(1-1e-10)],Ctplus_alpha1[i],("\t\t","   \t")[Ctplus_alpha1[i]<1e-10 or Ctplus_alpha1[i]>(1-1e-10)],Ctplus_alpha2[i],("\t\t","   \t")[Ctplus_alpha2[i]<1e-10 or Ctplus_alpha2[i]>(1-1e-10)],Ctplus_alpha3[i])
        #         PvalueCUSUM.append(pd.DataFrame("C(",m+i,",+)",Testdata_Ctplus[i],[Testdata_Ctplus[i]<1e-10 or Testdata_Ctplus[i]>(1-1e-10)],pvalue_Testdata_Ctplus[i],[pvalue_Testdata_Ctplus[i]<1e-10 or pvalue_Testdata_Ctplus[i]>(1-1e-10)],Ctplus_alpha1[i],[Ctplus_alpha1[i]<1e-10 or Ctplus_alpha1[i]>(1-1e-10)],Ctplus_alpha2[i],[Ctplus_alpha2[i]<1e-10 or Ctplus_alpha2[i]>(1-1e-10)],Ctplus_alpha3[i]))
        #         if pvalue_Testdata_Ctplus>0.05:
        #             print(m+i)
        Ctplus.append(m + i)
    # print("\nA total of ",time.perf_counter()-t0," seconds are used")
    limit_pvalue = []
    for i in range(0, m):
        a = 0.05
        limit_pvalue.append(a)

#    plt.plot(pvalue_Testdata_Ctplus, "b")
#    plt.plot(limit_pvalue, "r--")
    #     plt.savefig("./Dectection/{}_Pvalue_CUSUM.png".format(name))
#    plt.show()
    #     Ctplus.append((len(Ctplus)+1)*2)
    Pvalue_CUSUM = pd.DataFrame(index=list(Ctplus))
    # Pvalue_CUSUM["Testdata_Ctplus"]=Testdata_Ctplus
    del (pvalue_Testdata_Ctplus[0])
    Pvalue_CUSUM["pvalue_Testdata_Ctplus"] = list(pvalue_Testdata_Ctplus)
    #     print("Pvalue_CUSUM:",Pvalue_CUSUM[Pvalue_CUSUM["pvalue_Testdata_Ctplus"]<0.05].index)
    #     return Ctplus,Testdata_Ctplus,pvalue_Testdata_Ctplus
    K = Pvalue_CUSUM[Pvalue_CUSUM["pvalue_Testdata_Ctplus"] < 0.05].index
    return K
