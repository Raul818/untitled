import pandas as pd


rank=pd.read_csv("NewCsi.csv")
df=rank.Mentions
sat=rank.Satisfaction

# def departmentCSI(a,satisfaction, method='average'):
#     n = len(a)
#     ivec=sorted(range(len(a)), key=a.__getitem__)
#     svec=[a[rank] for rank in ivec]
#     sumranks = 0
#     dupcount = 0
#     newarray = [0]*n
#     for i in range(n):
#         sumranks += i
#         dupcount += 1
#         if i==n-1 or svec[i] != svec[i+1]:
#             for j in range(i-dupcount+1,i+1):
#                 if method=='average':
#                     averank = sumranks / float(dupcount) + 1
#                     newarray[ivec[j]] = averank
#                 elif method=='max':
#                     newarray[ivec[j]] = i+1
#                 elif method=='min':
#                     newarray[ivec[j]] = i+1 -dupcount+1
#                 else:
#                     raise NameError('Unsupported method')
#
#             sumranks = 0
#             dupcount = 0
#     Avg = (sum(newarray) / 10)  # 10 is the number of departments
#     # return Avg
#     weight = []
#     for x in newarray:
#         weight[:] = [x / Avg for x in newarray]
#     preCSI = [weight[i]*satisfaction[i] for i in range(len(weight))]
#     CSI=(sum(preCSI))/10
#     return CSI

# print(departmentCSI(df,sat))
# rank=pd.read_csv("NewCsi.csv")
# df=mentions(place=place, collection=collection, start=startdate, end=enddate)
# sat=CSI(place=place, collection=collection, start=startdate, end=enddate)


def rank_simple(vector):
    return sorted(range(len(vector)), key=vector.__getitem__)

def rankdata(a, method='average'):
    n = len(a)
    ivec=rank_simple(a)
    svec=[a[rank] for rank in ivec]
    sumranks = 0
    dupcount = 0
    newarray = [0]*n
    for i in range(n):
        sumranks += i
        dupcount += 1
        if i==n-1 or svec[i] != svec[i+1]:
            for j in range(i-dupcount+1,i+1):
                if method=='average':
                    averank = sumranks / float(dupcount) + 1
                    newarray[ivec[j]] = averank
                elif method=='max':
                    newarray[ivec[j]] = i+1
                elif method=='min':
                    newarray[ivec[j]] = i+1 -dupcount+1
                else:
                    raise NameError('Unsupported method')

            sumranks = 0
            dupcount = 0

    return newarray

print(rankdata(df))

def weightage(rank):
    Avg = (sum(rank) / 10) #10 is the number of departments
    # return Avg
    Avg_to_1=[]
    for x in rank:
        Avg_to_1[:] = [x / Avg for x in rank]

    return Avg_to_1

print(weightage(rankdata(df)))

def departmentCSI(weight,satisfaction):

    preCSI = [weight[i]*satisfaction[i] for i in range(len(weight))]
    CSI=(sum(preCSI))/10
    return CSI

print(departmentCSI(weightage(rankdata(df)),sat))
