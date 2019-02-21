def create_candidates(candidates_list, length):
    '''
    :param candidates_list: list[set]
    :return: list[set]
    '''
    res = []
    for item_1 in candidates_list:
        for item_2 in candidates_list:
            temp = frozenset(item_1 | item_2)
            # print(temp)
            if temp not in res and len(temp) == length:
                res.append(temp)
    return res


def frequent_items(partition, candidates, support):
    '''
    :param partition: iterator
    :param candidates: list[set]
    :param support: int
    :return: list[set]
    '''
    res = []
    count = {}
    for line in partition:
        for candidate in candidates:
            if candidate.issubset(line[1]):
                if tuple(candidate) not in count:
                    count[tuple(candidate)] = 1
                else:
                    count[tuple(candidate)] += 1
    for key, value in count.items():
        if value >= support:
            if set(key) not in res:
                res.append(frozenset(key))
    return res


def Apriori(partition, support):
    '''
    :param partition: iterator
    :param support: int
    :return: tuple(tuple(int, tuple))
    '''
    frequent = {}
    cand_1 = {}
    temp_partition = list(partition)
    for line in temp_partition:
        for item in line[1]:
            if item not in cand_1:
                cand_1[(item)] = 1
            else:
                cand_1[(item)] += 1
    frequent[1] = [frozenset([key]) for key, value in cand_1.items() if value >= support]
    k = 2
    while 1:
        # print(k)
        temp_candidate = create_candidates(frequent[k - 1], k)
        # print('temp_candidate completed')
        temp_frequent = frequent_items(temp_partition, temp_candidate, support)
        # print('temp_frequent completed')
        if len(temp_frequent) == 0:
            break
        else:
            frequent[k] = temp_frequent
            k += 1
    res = [(key, value) for key, value in frequent.items()]
    # print(res)
    return res


# def find_global_frequent(set, line, support):
#     length_set = set[0]
#     items = list(set[1])
#     counter = {}
#     for item in items:
#         if item.issubset(line):
#             if tuple(item) not in counter:
#                 counter[tuple(item)] = 1
#             else:
#                 counter[tuple(item)] += 1
#     res = [key for key, value in counter.items() if value > support]
#     return length_set, res


def global_frequent(line, candidates, support):
    res = []
    # print(line)
    # print(candidates)
    for candidate in candidates:
        # print(candidate)
        length_set = candidate[0]
        items = list(candidate[1])
        # print(items)
        counter = {}
        for item in items:
            if item.issubset(line):
                if tuple(item) not in counter:
                    counter[tuple(item)] = 1
                else:
                    counter[tuple(item)] += 1
        # print(counter)
        # res_local = [key for key, value in counter.items() if value > support]
        res.append((length_set, counter))
    # print(res)
    return res
