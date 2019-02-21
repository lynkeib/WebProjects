def create_candidates(candidates_list, length):
    '''
    :param candidates_list: list[set]
    :return: list[set]
    '''
    res = []
    for item_1 in candidates_list:
        for item_2 in candidates_list:
            temp = item_1 | item_2
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
                res.append(set(key))
    return res


def Apriori(partition, support):
    '''
    :param partition: iterator
    :param support: int
    :return: tuple(tuple(int, tuple))
    '''
    res = []
    candidate = {}
    frequent = {}
    cand_1 = {}
    temp_partition = list(partition)
    for line in partition:
        for item in line[1]:
            if item not in cand_1:
                cand_1[(item)] = 1
            else:
                cand_1[(item)] += 1

    candidate[1] = [{key} for key, value in cand_1.items()]
    frequent[1] = [{key} for key, value in cand_1.items() if value > support]

    k = 2
    while 1:
        temp_candidate = create_candidates(frequent[k - 1], k)
        # print(temp_candidate)
        temp_frequent = frequent_items(temp_partition, temp_candidate, support)
        # print(temp_frequent)
        if len(temp_frequent) == 0:
            break
        else:
            candidate[k] = temp_candidate
            frequent[k] = temp_frequent
            k += 1
    print(candidate)
    print(frequent)
    return res
