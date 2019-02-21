def create_candidates(candidates_list, length):
    '''
    :param candidates_list: list[set]
    :return: list[set]
    '''
    res = []
    for item_1 in candidates_list:
        for item_2 in candidates_list:
            temp = frozenset(item_1 | item_2)
            if temp not in res and len(temp) == length:
                res.append(temp)
    print(res)
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

def Apriori(partition, support, threshold=0):
    '''
    :param partition: iterator
    :param support: int
    :return: tuple(tuple(int, tuple))
    '''
    frequent = {}
    cand_1 = {}
    temp_partition = list(partition)
    print('temp_partition')
    for line in temp_partition:
        for item in line[1]:
            if item not in cand_1:
                cand_1[(item)] = 1
            else:
                cand_1[(item)] += 1
    cand_1 = {key: value for key, value in cand_1.items() if value >= threshold}
    print('cand_1')
    frequent[1] = [frozenset([key]) for key, value in cand_1.items() if value >= support]
    k = 2
    print(k)
    while 1:
        temp_candidate = create_candidates(frequent[k - 1], k)
        temp_frequent = frequent_items(temp_partition, temp_candidate, support)
        if len(temp_frequent) == 0:
            break
        else:
            frequent[k] = temp_frequent
            k += 1
    res = [(key, value) for key, value in frequent.items()]
    return res


def global_frequent(line, candidates):
    '''
    :param line: list
    :param candidates: list[set]
    :return: list[tuple]
    '''
    res = []
    for candidate in candidates:
        length_set = candidate[0]
        items = list(candidate[1])
        counter = {}
        for item in items:
            if item.issubset(line):
                if tuple(item) not in counter:
                    counter[tuple(item)] = 1
                else:
                    counter[tuple(item)] += 1
        res.append((length_set, counter))
    return res
