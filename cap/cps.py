def check_cps(data,
              max_cps: float = 15,
              diviation: float = 1.5):
    """
    Checks if the caption group follows the rule of around 15 characters per
    second.

    Args:
        data: Caption group according to our custom Caption-list datastructure.
        max_cps: Indicates the optimal characters per second, which is 15.
        diviation: Indicates how much it can diviate from the optimal 15
            characters per second.

    Returns:
        1 if the characters per second is too high.
        0 if the characters per second is just right.
        -1 if the characters per second is too low.
    """
    tot_time = data[-1].end - data[0].start
    characters = len(' '.join([word.text for word in data]))
    cps = characters / tot_time
    print(cps)

    if cps > max_cps + diviation:
        return 1

    elif cps < max_cps - diviation:
        return -1

    else:
        return 0


def cps(data):
    """
    Adjusts the time of the caption group so the subtitles stay shorter or
    longer on the screen. It adjusts it according to the 15 characters per
    second limit.

    Args:
        data: Caption group according to our custom Caption-list datastructure.

    Returns:
        The data with changed a changed start time for the first word of the
        caption group and a changed end time for the last word of the caption
        group
    """
    check = check_cps(data)
    while check != 0:
        if check == -1:
            data[-1].end -= 0.04
            data[0].start += 0.01
        elif check == 1:
            pass
        check = check_cps(data)
    return data


def check_wps(data,
              min_wps: float = 0.33,
              max_wps: float = 0.375):
    """
    Checks if the caption group follows the rule of one word every 0.33 to
    0.375 seconds.

    Args:
        data: Caption group according to our custom Caption-list datastructure.
        min_wps: Indicates the minum seconds per word, which is every 0.33
            seconds.
        max_wps: Indicates the maximum seconds per word, which is every 0.375
            seconds.

    Returns:
        1 if the words per second is too high.
        0 if the words per second is just right.
        -1 if the words per second is too low.
    """
    tot_time = data[-1].end - data[0].start
    words = len(data)
    spw = tot_time / words
    print(spw)
    if spw > max_wps:
        return 1

    elif spw < min_wps:
        return -1

    else:
        return 0


def wps(data):
    """
    Adjusts the time of the caption group so the subtitles stay shorter or
    longer on the screen. It adjusts it according to the rule of one word every
    0.33 to 0.375 seconds.

    Args:
        data: Caption group according to our custom Caption-list datastructure.

    Returns:
        The data with changed a changed start time for the first word of the
        caption group and a changed end time for the last word of the caption
        group
    """
    check = check_wps(data)
    while check != 0:
        if check == -1:
            data[-1].end -= 0.04
            data[0].start += 0.01
        check = check_wps(data)
    return data
