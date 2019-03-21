import operator
from itertools import groupby
from itertools import combinations


def parse(line, unique_user):
    '''
    :param line: (business_id, list[user_id])
    :param unique_user: list[user_id]
    :return: (business_id, psrsed_list[user_id])
    '''
    return line[0], [unique_user.index(i) for i in line[1]]


def hashing_generate_signature(line, parameters, num_of_bins):
    '''
    :param line: (user_id, list[index])
    :param parameters: (tuples(a, b))
    :param num_of_bins: int
    :return: (user_id, parsed_list[index])
    '''
    res = []
    cal = lambda a, b, x, length: ((a * x + b) % length)
    for parameter in parameters:
        res.append(min([cal(parameter[0], parameter[1], index, num_of_bins) for index in line[1]]))
    return line[0], res

# def hashing_generate_signature(line, parameters, num_of_bins):
#     '''
#     :param line: (user_id, list[index])
#     :param parameters: (tuples(a, b))
#     :param num_of_bins: int
#     :return: (user_id, parsed_list[index])
#     '''
#     res = []
#     cal = lambda a, b, p, x, length: (((a * x + b) % p) % length)
#     for parameter in parameters:
#         res.append(min([cal(parameter[0], parameter[1], parameter[2], index, num_of_bins) for index in line[1]]))
#     return line[0], res


def chunks(list, length):
    """
    :param list: list[signatures]
    :param length: int
    """
    for i in range(0, len(list), length):
        yield list[i: i + length]


def hashing_generate_buckets(line, row_number):
    '''
    :param line: (user_id, list[signatures])
    :param row_number: int
    :return: list[tuple(signature, [business])]
    '''
    res = []
    for index, chunk in enumerate(chunks(line[1], row_number)):
        res.append((index, [(tuple(chunk), line[0])]))
    return res


def accumulate(l):
    '''
    :param l:
    '''
    it = groupby(l, operator.itemgetter(0))
    for key, subiter in it:
        yield key, [item[1] for item in subiter]


def groupby_chunk_num(line):
    '''
    :param line: list[tuples(chunk_index, [tuples(hash, budiness_id)])]
    :return:
    '''
    res = []
    for chunk in line:
        temp = list(accumulate(sorted(chunk[1])))
        res.append(temp)
    return res


# def groupby_kvpairs_in_each_basket_and_genreate_candidates(chunks):
#     '''
#     :param chunks:
#     :return:
#     '''
#     candidates = set([])
#     for chunk in chunks:
#         dic = {}
#         for pairs in chunk[1]:
#             try:
#                 dic[pairs[0]].append(pairs[1])
#             except:
#                 dic[pairs[0]] = [pairs[1]]
#         for key, value in dic.items():
#             if len(value) > 1:
#                 for comb in combinations(value, 2):
#                     candidates.add(frozenset(comb))
#     return candidates

def groupby_kvpairs_in_each_basket_and_genreate_candidates(chunks):
    '''
    :param chunks:
    :return:
    '''
    candidates = set()
    res = set()
    for chunk in chunks:
        for key, value in groupby(sorted(chunk[1]), lambda x: x[0]):
            vs = list(value)
            if len(vs) > 1:
                candidates.add(frozenset([v[1] for v in vs]))
    for cand in candidates:
        for c in combinations(cand, 2):
            res.add(frozenset(c))
    return res


def jar(l1, l2):
    '''
    :param l1: list
    :param l2: list
    :return: float
    '''
    res = [tp[0] == tp[1] for tp in zip(l1, l2)]
    return sum(res) / len(res)


def prim(max):
    res = set()
    res.add(2)
    for i in range(2, max):
        for j in range(2, max):
            if i % j == 0:
                break
            else:
                res.add(i)
    return res
