# Sorting algorithms
# ==================
import timing
from random import randint
from timeit import repeat

def run_sorting_algorithm(algorithm, array):
    setup_code = f"from __main__ import {algorithm}" \
        if algorithm != "sorted" else ""
    
    stmt = f"{algorithm}({array})"

    times = repeat(setup=setup_code, stmt=stmt, repeat=3, number=10)

    print(f"Algorithm: {algorithm}. Minimum execution time: {min(times)}")

def bubble_sort(array):
    n = len(array)

    for i in range(n):
        already_sorted = True

        for j in range(n-i-1):
            if array[j] > array[j+1]:
                array[j], array[j+1] = array[j+1], array[j]

                already_sorted = False
        
        if already_sorted:
            break
    
    return array

def insertion_sort(array):
    
    for i in range(1, len(array)):
        key_item = array[i]

        j = i - 1

        while j >= 0 and array[j] > key_item:
            array[j + 1] = array[j]
            j -= 1
        
        array[j + 1] = key_item
    
    return array

def merge(left, right):

    if len(left) == 0:
        return right
    
    if len(right) == 0:
        return left

    result = []
    index_left = index_right = 0

    while len(result) < len(left) + len(right):
        if left[index_left] <= right[index_right]:
            result.append(left[index_left])
            index_left += 1
        else:
            result.append(right[index_right])
            index_right += 1
        
        if index_right == len(right):
            result += left[index_left:]
            break
        
        if index_left == len(left):
            result += right[index_right:]
            break

    return result

def merge_sort(array):
    if len(array) < 2:
        return array
    
    midpoint = len(array) // 2

    return merge(left=merge_sort(array[:midpoint]), right=merge_sort(array[midpoint:]))

def quicksort(array):
    if len(array) < 2:
        return array
    
    low, same, high = [], [], []

    pivot = array[randint(0, len(array) - 1)]

    for item in array:

        if item < pivot:
            low.append(item)
        elif item == pivot:
            same.append(item)
        elif item > pivot:
            high.append(item)
    
    return quicksort(low) + same + quicksort(high)

if __name__ == "__main__":
    ARRAY_LENGTH = 1000
    rand_arr = [randint(0, 1000) for i in range(ARRAY_LENGTH)]

    

    print(timing.timer(bubble_sort, rand_arr.copy()))
    print(timing.timer(insertion_sort, rand_arr.copy()))
    print(timing.timer(merge_sort, rand_arr.copy()))
    print(timing.timer(quicksort, rand_arr.copy()))

    run_sorting_algorithm(algorithm="bubble_sort", array=rand_arr)
    run_sorting_algorithm(algorithm="insertion_sort", array=rand_arr)
    run_sorting_algorithm(algorithm="merge_sort", array=rand_arr)
    run_sorting_algorithm(algorithm="quicksort", array=rand_arr)