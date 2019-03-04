from itertools import combinations
import itertools
import operator
from functools import reduce


def create_candidates(candidates_list, length):
    '''
    :param candidates_list: list[list]
    :param length: int
    :return:
    '''
    for comb in combinations(candidates_list, 2):
        temp = set(comb[0]) | set(comb[1])
        if len(temp) == length:
            yield tuple(temp)


def frequent_items(dict, k, candidates, support):
    '''
    :param dict: {business_id: set(user_id)}
    :param k: int
    :param candidates: list[list]
    :param support: int
    :return: list[list]
    '''
    res = []
    for comb in create_candidates(candidates, k):
        if set(comb) not in res:
            temp = reduce(lambda a, b: a & b, (dict[x] for x in comb))
            if len(temp) >= support:
                res.append(set(comb))
    res = [list(comb) for comb in res]
    return res


def convert(line):
    '''
    :param line: (key, (values))
    :return: list[tuple(key, value)]
    '''
    res = []
    for business in line[1]:
        res.append((business, line[0]))
    return res


def accumulate(l):
    '''
    :param l: list[tuple((key, value))]
    :return:
    '''
    it = itertools.groupby(sorted(l), operator.itemgetter(0))
    res = {}
    for key, subiter in it:
        res[key] = {item[1] for item in subiter}
    return res


def Apriori(partition, support):
    '''
    :param partition: iterator
    :param support: int
    :return: tuple(tuple(int, tuple))
    '''

    temp_partition = list(partition)
    cand_1 = {}
    frequent = {}

    business = []

    for line in temp_partition:
        temp = convert(line)
        business.extend(temp)

    own_business_list = accumulate(business)

    for line in temp_partition:
        for item in line[1]:
            if item not in cand_1:
                cand_1[(item)] = 1
            else:
                cand_1[(item)] += 1

    frequent[1] = [[key] for key, value in cand_1.items() if value >= support]

    k = 2
    while 1:
        print("Creating Candidates and Frequent", k)
        temp_frequent = frequent_items(own_business_list, k, frequent[k - 1], support)
        if len(temp_frequent) == 0:
            break
        frequent[k] = temp_frequent
        k += 1
    res = [(key, {frozenset(pair) for pair in value}) for key, value in frequent.items()]

    return res

# def global_frequent(line, candidates):
#     '''
#     :param line: list
#     :param candidates: list[tuple]
#     :return: list[tuple]
#     '''
#     res = []
#     for candidate in candidates:
#         length_set = candidate[0]
#         items = list(candidate[1])
#         counter = {}
#         for item in items:
#             if set(item).issubset(line):
#                 if item not in counter:
#                     counter[item] = 1
#                 else:
#                     counter[item] += 1
#         res.append((length_set, counter))
#     return res
