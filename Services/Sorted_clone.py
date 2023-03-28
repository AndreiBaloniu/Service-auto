def sorted_clone(random_list: list, key, reverse: bool):
    """

    :param random_list:
    :param key:
    :param reverse:
    :return:
    """

    for i in range(len(random_list)):
        for j in range(i + 1, len(random_list)):
            if key(random_list[i]) > key(random_list[j]):
                random_list[i], random_list[j] = random_list[j], random_list[i]

    if reverse is True:
        return random_list[::-1]
    else:
        return random_list
