import random
import copy

def push_forward(cur_list, beg_index, end_index, window_size, jitter):
    pushed_index = -1

    cur_range = range(beg_index,end_index)
    tmp_list = cur_list[beg_index:end_index]
    assert len(cur_range) == len(tmp_list)

    for this_index, this_item in zip(cur_range, tmp_list):
        for cur_offset in range(1, window_size+1):
            that_index = this_index - cur_offset
            if that_index < 0 : continue

            that_item = cur_list[that_index]
            if this_item != that_item : continue

            pushed_index = this_index
            break

        if has_overlap(this_item, cur_list[this_index+1]) :
            pushed_index = -1

        if pushed_index != -1 : break

    if pushed_index == -1 : return -1

    init_list = copy.deepcopy(cur_list)

    placed_index = 1 + window_size + jitter + [
        cur_index for cur_index, cur_item in enumerate(cur_list)
        if has_overlap(cur_item, cur_list[pushed_index]) and cur_index < pushed_index
    ][-1]

    if placed_index >= len(cur_list) : return -1
    cur_list.insert(placed_index, cur_list.pop(pushed_index))

    assert init_list != cur_list
    return pushed_index

def push_backward(cur_list, beg_index, end_index, window_size, jitter):
    pushed_index = -1

    cur_range = range(beg_index+1,end_index+1)
    tmp_list = cur_list[beg_index+1:end_index+1]
    assert len(cur_range) == len(tmp_list)

    for this_index, this_item in reversed(list(zip(cur_range,tmp_list))):
        for cur_offset in range(1, window_size+1):
            that_index = this_index + cur_offset
            if that_index >= len(cur_list) : continue

            that_item = cur_list[that_index]
            if this_item != that_item : continue

            pushed_index = this_index
            break

        if has_overlap(this_item, cur_list[this_index-1]) :
            pushed_index = -1

        if pushed_index != -1 : break

    if pushed_index == -1 : return -1

    init_list = copy.deepcopy(cur_list)

    placed_index = -1 * ( 1 + window_size + jitter ) + [
        cur_index for cur_index, cur_item in enumerate(cur_list)
        if has_overlap(cur_item, cur_list[pushed_index]) and cur_index > pushed_index
    ][0]

    if placed_index <= beg_index : return -1
    cur_list.insert(placed_index, cur_list.pop(pushed_index))

    assert init_list != cur_list
    return pushed_index

def has_overlap(this_list, that_list):
    if type(this_list) == list and type(that_list) == list:
        return any(
            [ this_item in that_list for this_item in this_list ]
        )

    return this_list == that_list

def reorder_list(cur_list, locked_count=4, window_size=2):
    init_list = copy.deepcopy(cur_list)

    assert locked_count > window_size
    init_length = len(cur_list)

    max_count = 10

    cur_count = 0
    meta_did_add = True

    while meta_did_add and cur_count < max_count:
        meta_did_add = False
        cur_count += 1

        if cur_count > 20: print(cur_list)
        max_jitter = 0 if cur_count < 5 else random.randint(0,2*window_size)

        beg_index = locked_count
        end_index = len(cur_list)-1

        did_add = True
        prev_list, prev_prev_list = None, None
        while did_add:
            prev_prev_list = prev_list
            prev_list = copy.deepcopy(cur_list)

            init_beg_index = beg_index
            beg_index = push_forward(cur_list, beg_index, end_index, window_size, random.randint(0,max_jitter))

            if cur_list == prev_list or cur_list == prev_prev_list :
                did_add = False
            elif beg_index == -1 :
                if init_beg_index == locked_count-1 :
                    did_add = False
                else:
                    beg_index = locked_count-1
                    continue
            else:
                did_add = True

            meta_did_add = meta_did_add or did_add

        beg_index = locked_count-1
        end_index = len(cur_list)-1

        did_add = True
        prev_list, prev_prev_list = None, None
        while did_add:
            prev_prev_list = prev_list
            prev_list = copy.deepcopy(cur_list)

            init_end_index = end_index
            end_index = push_backward(cur_list, beg_index, end_index, window_size, random.randint(0,max_jitter))

            if cur_list == prev_list or cur_list == prev_prev_list :
                did_add = False
            elif end_index == -1 :
                if init_end_index == len(cur_list)-1 :
                    did_add = False
                else:
                    end_index = len(cur_list)-1
                    continue
            else:
                did_add = True

            meta_did_add = meta_did_add or did_add

    assert cur_count <= max_count
    assert len(cur_list) == init_length

    cur_indices = [0] * len(cur_list)

    work_list = copy.deepcopy(cur_list)

    for (this_index, this_item) in enumerate(init_list):
        for (that_index, that_item) in enumerate(work_list):
            if this_item != that_item : continue

            cur_indices[that_index] = this_index
            work_list[that_index] = None
            break

    assert not any(work_list)

    return cur_list, cur_indices

def reorder_by(main_list, sort_list, locked_count=4, window_size=2):
    _, sort_indices = reorder_list(
        sort_list, locked_count, window_size
    )

    return [
        main_list[cur_index] for cur_index in sort_indices
    ]
