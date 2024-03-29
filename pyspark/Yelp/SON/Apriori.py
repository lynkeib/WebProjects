def create_candidates(item_set, length):
    '''
    :param item_set: list[set()]
    :param length: int
    :return: list[set()]
    '''
    return_list = []
    for item_1 in item_set:
        for item_2 in item_set:
            temp = item_1.union(item_2)
            if temp not in return_list and len(temp) == length:
                return_list.append(temp)
    return return_list

# print(create_candidates(A, A, 2))
def frequent_items(items, data, support):
    '''
    :param items: list[set()]
    :param data: list[list]
    :param support: int
    :return: list[set()]
    '''
    return_ = []
    count = {}
    for line in data:
        for item in items:
            if item.issubset(line[1]):
                if tuple(item) not in count:
                    count[tuple(item)] = 1
                else:
                    count[tuple(item)] += 1
    for key, value in count.items():
        if value >= support:
            if set(key) not in return_:
                return_.append(set(key))
    return return_

def makedic(data):
    '''
    :param data: iterator
    :return: list[tuple]
    '''
    return_key = []
    return_value = []
    for line in data:
        for item in line[1]:
            if item not in return_key:
                return_key.append(item)
                return_value.append(1)
            else:
                index = return_key.index(item)
                return_value[index] += 1
    return_list = list(zip(return_key, return_value))
    return return_list
