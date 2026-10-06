import argparse
import sys
import time

import numpy as np
from arrviss import Arrvis
from scipy.stats import norm


def insertion(arr: Arrvis):
    for i in range(len(arr)):
        idx = i
        while idx > 0 and arr.read(idx) < arr.read(idx - 1):
            arr.swap(idx, idx - 1)
            idx -= 1


def shell(arr: Arrvis):
    n = len(arr)
    gap = n
    shrink = 2
    while gap > 1:
        gap = gap // shrink
        # arr.change_title(f"gap: {gap}")
        for start in range(n):
            consider = start
            toswap = start - gap
            while toswap >= 0:
                if arr[toswap] > arr[consider]:
                    arr.swap(toswap, consider)
                    consider -= gap
                    toswap -= gap
                else:
                    break


def selection(arr: Arrvis):
    for i in range(len(arr)):
        lowest = i
        for j in range(i + 1, len(arr)):
            if arr.read(j) < arr.read(lowest):
                lowest = j
        arr.swap(i, lowest)


def merge(arr: Arrvis, lower=0, upper=None):
    if upper == None:
        upper = len(arr) - 1
    if lower >= upper:
        return

    midpoint = (lower + upper) // 2

    merge(arr, lower, midpoint)
    merge(arr, midpoint + 1, upper)

    mergepoint = midpoint + 1
    merged = False
    # while mergepoint <= upper TODO: create an auxilliary array for mergesort
    aux = []
    right_idx = midpoint + 1
    left_idx = lower
    # print("upper ",upper)
    # print("lower ",lower)
    # print("midpoint ", midpoint)
    while right_idx <= upper and left_idx <= midpoint:
        # print("\tright ",right_idx)
        # print("\tleft ",left_idx)
        # print("\taux ",aux)
        if arr.read(right_idx) <= arr.read(left_idx):
            aux.append(arr.read(right_idx))
            right_idx += 1
        else:
            aux.append(arr.read(left_idx))
            left_idx += 1

    while right_idx <= upper:
        # print("\tright ",right_idx)
        # print("\tleft ",left_idx)
        # print("\taux ",aux)
        aux.append(arr.read(right_idx))
        right_idx += 1
    while left_idx <= midpoint:
        # print("\tright ",right_idx)
        # print("\tleft ",left_idx)
        # print("\taux ",aux)
        aux.append(arr.read(left_idx))
        left_idx += 1

    # print("aux ",aux)
    # print("arr[lower:upper]",arr.arr[lower:upper])
    for i in range(lower, upper + 1):
        arr.write(i, aux[i - lower])


def iterative_merge(arr: Arrvis):  # TODO: fix me
    width = 1
    while width < len(arr):
        placeholder = []
        first_start = 0
        second_start = width
        round = 0
        while second_start < len(arr):
            print("round", round)
            round += 1
            first = first_start
            second = second_start

            # add items to placeholder array
            while (
                first < second_start
                and second < second_start + width
                and second < len(arr)
            ):
                print(width, first, second)
                if arr[first] > arr[second]:
                    placeholder.append(arr[second])
                    second += 1
                else:
                    placeholder.append(arr[second])
                    first += 1

            while first < second_start:
                placeholder.append(arr[first])
                first += 1

            while second < second_start + width and second < len(arr):
                placeholder.append(arr[second])

            # rewrite into placeholder array
            for i in range(first_start, second_start + width):
                arr[i] = placeholder[i - first_start]

            first_start = second_start + width
            second_start = first_start + width


def cocktail(arr: Arrvis):
    done = False
    while not done:
        done = True
        for i in range(len(arr) - 1):
            if arr.read(i) > arr.read(i + 1):
                arr.swap(i, i + 1)
                done = False

        for i in range(len(arr) - 2, -1, -1):
            if arr.read(i) > arr.read(i + 1):
                arr.swap(i, i + 1)
                done = False


def optimized_cocktail(arr: Arrvis):
    done = False
    iter = 0
    while not done:
        done = True
        for i in range(iter, len(arr) - 1 - iter):
            if arr.read(i) > arr.read(i + 1):
                arr.swap(i, i + 1)
                done = False

        if done:
            break

        for i in range(len(arr) - 2 - iter, iter - 1, -1):
            if arr.read(i) > arr.read(i + 1):
                arr.swap(i, i + 1)
                done = False
        iter += 1


def bubble(arr: Arrvis):
    done = False
    while not done:
        done = True
        for i in range(len(arr) - 1):
            if arr.read(i) > arr.read(i + 1):
                arr.swap(i, i + 1)
                done = False


def optimized_bubble(arr: Arrvis):
    done = False
    iter = 1
    while not done:
        done = True
        for i in range(len(arr) - iter):
            if arr.read(i) > arr.read(i + 1):
                arr.swap(i, i + 1)
                done = False
        iter += 1


def comb(arr: Arrvis):
    done = False
    gap = len(arr)
    shrink = 1.3
    while not done:
        gap = int(gap // shrink)
        if gap < 1:
            gap = 1
            done = True

        for i in range(len(arr) - gap):
            if arr.read(i) > arr.read(i + gap):
                arr.swap(i, i + gap)
                done = False


def comb_shaker(arr: Arrvis):
    done = False
    gap = len(arr)
    shrink = 1.3
    while not done:
        gap = int(gap // shrink)
        if gap < 1:
            gap = 1
            done = True

        for i in range(len(arr) - gap):
            if arr.read(i) > arr.read(i + gap):
                arr.swap(i, i + gap)
                done = False

        for i in range(len(arr) - 1, gap, -1):
            if arr.read(i - gap) > arr.read(i):
                arr.swap(i, i - gap)
                done = False


def max_heap(arr: Arrvis):
    # heapify the list
    start = len(arr) // 2
    end = len(arr)
    while end > 1:
        if start > 0:
            start -= 1
        else:
            end -= 1
            arr.swap(end, 0)

        root = start
        while 2 * root + 1 < end:
            child = 2 * root + 1
            if child + 1 < end and arr.read(child) < arr.read(child + 1):
                child += 1
            if arr.read(root) < arr.read(child):
                arr.swap(root, child)
                root = child
            else:
                break


def pigeonhole(arr: Arrvis):
    """assumes inputs are integers"""
    maximum = -np.inf
    minimum = np.inf
    for i in range(len(arr)):
        if arr[i] > maximum:
            maximum = arr[i]
        if arr[i] < minimum:
            minimum = arr[i]
    rng = maximum - minimum
    holes = [None] * (rng + 1)
    counts = [0] * (rng + 1)
    for i in range(len(arr)):
        holes[arr[i] - minimum] = arr[i]
        counts[arr[i] - minimum] += 1

    idx = 0
    for i in range(len(holes)):
        if holes[i] is None:
            continue
        arr[idx] = holes[i]
        idx += 1


def count(arr: Arrvis, place, base):
    # if upper is None:
    # 	upper = len(arr) - 1
    out = [0] * len(arr)
    count = [0] * base

    for i in range(len(arr)):
        index = arr[i] // place
        count[index % base] += 1

    for i in range(1, base):
        count[i] += count[i - 1]

    i = len(arr) - 1
    for i in range(len(arr) - 1, -1, -1):
        index = arr[i] // place
        out[count[index % base] - 1] = arr[i]
        count[index % base] -= 1

    for i in range(len(arr)):
        arr[i] = out[i]


def radix_LSD(arr: Arrvis, base=2):
    # find maximum
    maximum = -np.inf
    for i in range(len(arr)):
        if arr[i] > maximum:
            maximum = arr[i]

    place = 1
    while maximum / place >= 1:
        count(arr, place, base)
        place *= base


def partition(arr: Arrvis, lower, upper):
    median = lower + (upper - lower) // 2
    if arr.read(upper) < arr.read(median):
        arr.swap(upper, median)
    if arr.read(median) < arr.read(lower):
        arr.swap(median, lower)
    if arr.read(upper) < arr.read(median):
        arr.swap(upper, median)

    value = arr.read(median)
    inc = lower
    dec = upper
    done = False
    while not done:
        while arr.read(inc) < value:
            inc += 1
        while arr.read(dec) > value:
            dec -= 1

        if inc >= dec:
            done = True
        else:
            arr.swap(inc, dec)
            inc += 1
            dec -= 1
    return dec


def quick(arr: Arrvis, lower=0, upper=None):
    if upper == None:
        upper = len(arr) - 1
    if lower >= upper:
        return

    part = partition(arr, lower, upper)
    quick(arr, lower, part)
    quick(arr, part + 1, upper)


def stooge(arr: Arrvis, lower=0, upper=None):
    if upper == None:
        upper = len(arr) - 1
    if arr[lower] > arr[upper]:
        arr.swap(lower, upper)
    if upper - lower + 1 > 2:
        t = int((upper - lower + 1) / 3)
        stooge(arr, lower, upper - t)
        stooge(arr, lower + t, upper)
        stooge(arr, lower, upper - t)


def odd_even(arr: Arrvis):
    done = False
    while not done:
        done = True
        for i in range(1, len(arr) - 1, 2):
            if arr[i] > arr[i + 1]:
                arr.swap(i, i + 1)
                done = False
        for i in range(0, len(arr) - 1, 2):
            if arr[i] > arr[i + 1]:
                arr.swap(i, i + 1)
                done = False


def swaplastsort(arr: Arrvis):
    lidx = len(arr) - 1
    while lidx > 0:
        for i in range(0, lidx):
            if arr[i] > arr[lidx]:
                arr.swap(i, lidx)
                # arr[i], arr[lidx] = arr[lidx], arr[i]
        lidx -= 1
    return arr


def swapfirstsort(arr: Arrvis):
    fidx = 0
    while fidx < len(arr) - 1:
        for i in range(fidx + 1, len(arr)):
            if arr[i] < arr[fidx]:
                arr.swap(i, fidx)
                # arr[i], arr[fidx] = arr[fidx], arr[i]
        fidx += 1
    return arr


def identity_crisis(arr: Arrvis, merge_first=True):
    def mod_quick(left=0, right=None):
        if right is None:
            right = len(arr) - 1
        if left >= right:
            return
        part = partition(arr, left, right)
        mod_merge(left, part)
        mod_merge(part + 1, right)

    def mod_merge(left=0, right=None):
        if right is None:
            right = len(arr) - 1
        if left >= right:
            return

        mid = (left + right) // 2
        mod_quick(left, mid)
        mod_quick(mid + 1, right)
        aux = []
        right_idx = mid + 1
        left_idx = left
        while right_idx <= right and left_idx <= mid:
            if arr[right_idx] < arr[left_idx]:
                aux.append(arr[right_idx])
                right_idx += 1
            else:
                aux.append(arr[left_idx])
                left_idx += 1

        while right_idx <= right:
            aux.append(arr[right_idx])
            right_idx += 1

        while left_idx <= mid:
            aux.append(arr[left_idx])
            left_idx += 1

        for i in range(left, right + 1):
            arr[i] = aux[i - left]

    if merge_first:
        mod_merge()
    else:
        mod_quick()

    return arr


def insert_select(arr: Arrvis):
    for i in range(len(arr) // 2):
        idx = i
        while idx > 0 and arr[idx] < arr[idx - 1]:
            arr.swap(idx, idx - 1)
            idx -= 1
    for i in range(len(arr) // 2, len(arr)):
        lowest = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[lowest]:
                lowest = j
        arr.swap(i, lowest)

    # need to combine the two halves
    aux = []
    lower = 0
    upper = len(arr) - 1
    midpoint = (lower + upper) // 2
    right_idx = midpoint + 1
    left_idx = lower
    # print("upper ",upper)
    # print("lower ",lower)
    # print("midpoint ", midpoint)
    while right_idx <= upper and left_idx <= midpoint:
        # print("\tright ",right_idx)
        # print("\tleft ",left_idx)
        # print("\taux ",aux)
        if arr.read(right_idx) <= arr.read(left_idx):
            aux.append(arr.read(right_idx))
            right_idx += 1
        else:
            aux.append(arr.read(left_idx))
            left_idx += 1

    while right_idx <= upper:
        # print("\tright ",right_idx)
        # print("\tleft ",left_idx)
        # print("\taux ",aux)
        aux.append(arr.read(right_idx))
        right_idx += 1
    while left_idx <= midpoint:
        # print("\tright ",right_idx)
        # print("\tleft ",left_idx)
        # print("\taux ",aux)
        aux.append(arr.read(left_idx))
        left_idx += 1

    # print("aux ",aux)
    # print("arr[lower:upper]",arr.arr[lower:upper])
    for i in range(lower, upper + 1):
        arr.write(i, aux[i - lower])


def shuffle(arr: Arrvis):
    n = len(arr)
    for i in range(n):
        swap_idx = np.random.randint(i, n)
        arr.swap(i, swap_idx)


def gaussian(arr: Arrvis):
    num = len(arr)
    dom = np.linspace(-3, 3, num)
    gauss = norm.pdf(dom)
    gauss /= np.min(gauss)
    gauss = num * gauss / np.max(gauss) + 1
    gauss = gauss.astype(int)
    for i in range(len(arr)):
        arr[i] = gauss[i]


def reverse(arr: Arrvis):
    n = len(arr)
    lzt = list(np.arange(n) + 1)
    for i in range(len(arr)):
        arr[i] = lzt[i]
    for i in range(n // 2):
        arr.swap(i, n - i - 1)


def sorted(arr: Arrvis):
    n = len(arr)
    lzt = list(np.arange(n) + 1)
    for i in range(len(arr)):
        arr[i] = lzt[i]


def test_verify(n):
    lzt = list(np.arange(n) + 1)
    arr = Arrvis(lzt, plot=True)
    arr.change_title("shuffling...")
    shuffle(arr)
    arr.verify()
    arr.change_title("first half quicksort...")
    quick(arr, lower=0, upper=len(arr) // 2)
    arr.verify()
    arr.change_title("full merge sort...")
    merge(arr)
    arr.verify()


def main():
    start = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("--algors", default=["quick"], nargs="*")
    parser.add_argument("-n", default="64")
    parser.add_argument("--inputs", default=["shuffle"], nargs="*")
    parser.add_argument("--ms", default="auto")
    parser.add_argument("--vl", default="auto")
    parser.add_argument("--rt", default=False, action="store_true")
    parser.add_argument("--test-verify", default=False, action="store_true")
    parser.add_argument("--vtauto", default=20)
    args = parser.parse_args()
    n = int(args.n)
    if args.test_verify:
        test_verify(n)
        return

    if args.ms == "auto":
        ms_frame = None
    else:
        ms_frame = int(args.ms)

    algors = [
        bubble,
        optimized_bubble,
        cocktail,
        optimized_cocktail,
        comb,
        odd_even,
        swapfirstsort,
        swaplastsort,
        insert_select,
        selection,
        max_heap,
        insertion,
        shell,
        quick,
        merge,
        radix_LSD,
        pigeonhole,
        identity_crisis,
    ]
    algors = [
        optimized_bubble,
        optimized_cocktail,
        comb,
        odd_even,
        swapfirstsort,
        swaplastsort,
        selection,
        max_heap,
        insert_select,
        insertion,
        shell,
        quick,
        merge,
        radix_LSD,
        pigeonhole,
        identity_crisis,
    ]
    stralgors = [
        "bubble",
        "optbubble",
        "cocktail",
        "optcocktail",
        "comb",
        "oddeven",
        "swapfirstsort",
        "swaplastsort",
        "insert_select",
        "selection",
        "maxheap",
        "insertion",
        "shell",
        "quick",
        "merge",
        "LSD",
        "pigeonhole",
        "idc",
    ]
    stralgors = [
        "optbubble",
        "optcocktail",
        "comb",
        "oddeven",
        "swapfirstsort",
        "swaplastsort",
        "selection",
        "maxheap",
        "insert_select",
        "insertion",
        "shell",
        "quick",
        "merge",
        "LSD",
        "pigeonhole",
        "idc",
    ]
    if "all" in args.algors:
        algors_to_do = [a for a in algors]
    else:
        algors_to_do = []
        for a in args.algors:
            if a in stralgors:
                algors_to_do.append(algors[stralgors.index(a)])
            else:
                print(a, "not recognized. skipping")

    inputs = [shuffle, gaussian, reverse, sorted]
    strinputs = ["shuffle", "gaussian", "reversed", "sorted"]
    if "all" in args.inputs:
        inputs_to_do = [i for i in inputs]
    else:
        inputs_to_do = []
        for i in args.inputs:
            if i in strinputs:
                inputs_to_do.append(inputs[strinputs.index(i)])
            else:
                print(i, "not recognized. skipping")

    # create the list
    lzt = np.arange(n) + 1
    lzt = list(lzt)
    arr = Arrvis(lzt, plot=args.rt)

    num_sorts = len(inputs_to_do) * len(algors_to_do)
    count = 0
    for i in inputs_to_do:
        for a in algors_to_do:
            count += 1
            arr.change_title(
                f"algorithm: {a.__name__}; input: {i.__name__} (sort {count}/{num_sorts})"
            )
            i(arr)
            a(arr)
            arr.verify()
    if not args.rt:
        if args.vl == "auto":
            time_per_sort = float(args.vtauto)
            video_length = time_per_sort * num_sorts
        else:
            video_length = float(args.vl)
        if "all" in args.inputs and "all" in args.algors:
            filename = "all_sorts__all_inputs"
        elif "all" in args.algors and len(inputs_to_do) == 1:
            filename = f"all_sorts__{inputs_to_do[0].__name__}_inputs"
        elif "all" in args.algors:
            filename = "all_sorts"
        elif len(algors_to_do) == 1 and "all" in args.inputs:
            filename = f"{algors_to_do[0].__name__}__all_inputs"
        elif len(algors_to_do) == 1 and len(inputs_to_do) == 1:
            filename = f"{algors_to_do[0].__name__}__{inputs_to_do[0].__name__}_input"
        elif len(algors_to_do) == 1:
            filename = f"{algors_to_do[0].__name__}"
        else:
            filename = "multisort"
        print(filename)
        arr.animate_frames(
            filename=filename, ms_frame=ms_frame, video_length=video_length
        )

    # if len(sys.argv) < 2:
    # 	print("sorting algorithm required")
    # 	return
    # algor = sys.argv[1]
    # num=64
    # if len(sys.argv) >= 3:
    # 	num = int(sys.argv[2])
    # if len(sys.argv) >= 4:
    # 	arr_type = sys.argv[3]
    # else:
    # 	arr_type = "random"

    # if arr_type == "random":
    # 	lzt = np.arange(num)+1
    # 	lzt = list(lzt)
    # 	arr=Arrvis(lzt)
    # 	shuffle(arr)
    # elif arr_type == "gaussian":
    # 	dom = np.linspace(-3,3,num)
    # 	gauss = norm.pdf(dom)
    # 	gauss /= np.min(gauss)
    # 	gauss = gauss.astype(int)
    # 	arr = Arrvis(np.sort(gauss))
    # 	for i in range(len(arr)):
    # 		arr[i] = gauss[i]
    # elif arr_type == "reversed":
    # 	lzt = np.arange(num) + 1
    # 	arr=Arrvis(lzt)
    # 	reverse(arr)

    # print("sorting")
    # start=time.time()
    # if algor == "insertion":
    # 	insertion(arr)
    # 	arr.animate_frames(algor,arr_type,ms_frame=ms_frame)
    # elif algor == "selection":
    # 	selection(arr)
    # 	arr.animate_frames(algor,arr_type,ms_frame=ms_frame)
    # elif algor == "cocktail":
    # 	cocktail(arr)
    # 	arr.animate_frames(algor,arr_type,ms_frame=ms_frame)
    # elif algor=="bubble":
    # 	bubble(arr)
    # 	arr.animate_frames(algor,arr_type,ms_frame=ms_frame)
    # elif algor == "quick":
    # 	quick(arr)
    # 	arr.animate_frames(algor,arr_type,ms_frame=ms_frame)
    # elif algor == "merge":
    # 	merge(arr)
    # 	arr.animate_frames(algor,arr_type,ms_frame=ms_frame)
    # elif algor == "optcocktail":
    # 	optimized_cocktail(arr)
    # 	arr.animate_frames(algor,arr_type,ms_frame=ms_frame)
    # elif algor == "itermerge":
    # 	iterative_merge(arr)
    # 	arr.animate_frames(algor,arr_type,ms_frame=ms_frame)
    # elif algor == "comb":
    # 	comb(arr)
    # 	arr.animate_frames(algor,arr_type,ms_frame=ms_frame)
    # elif algor == "combshaker":
    # 	comb_shaker(arr)
    # 	arr.animate_frames(algor,arr_type,ms_frame=ms_frame)
    # elif algor == "maxheap":
    # 	max_heap(arr)
    # 	arr.animate_frames(algor,arr_type,ms_frame=ms_frame)
    # elif algor == "radixLSD":
    # 	radix_LSD(arr,4)
    # 	arr.animate_frames(algor,arr_type,ms_frame=ms_frame)
    # elif algor == "pigeonhole":
    # 	pigeonhole(arr)
    # 	arr.animate_frames(algor,arr_type,ms_frame=ms_frame)
    # elif algor == "stooge":
    # 	stooge(arr)
    # 	arr.animate_frames(algor,arr_type,ms_frame=ms_frame)
    # elif algor == "oddeven":
    # 	odd_even(arr)
    # 	arr.animate_frames(algor,arr_type,ms_frame=ms_frame)
    # elif algor == "optbubble":
    # 	optimized_bubble(arr)
    # 	arr.animate_frames(algor,arr_type,ms_frame=ms_frame)
    # elif algor == "swaplast":
    # 	swaplastsort(arr)
    # 	arr.animate_frames(algor,arr_type,ms_frame=ms_frame)
    # elif algor == "swapfirst":
    # 	swapfirstsort(arr)
    # 	arr.animate_frames(algor,arr_type,ms_frame=ms_frame)
    # elif algor == "idc":
    # 	idc_sort(arr,merge_first=False)
    # 	arr.animate_frames(algor,arr_type,ms_frame=ms_frame)
    # elif algor == "all":
    # 	# does not support non random input
    # 	lzt = np.arange(num)+1
    # 	arr = Arrvis(lzt)
    # 	algors = [bubble, cocktail, odd_even, optimized_cocktail, comb, swapfirstsort, swaplastsort, selection, insertion, max_heap, quick, merge, radix_LSD, pigeonhole]
    # 	# algors = [insertion,selection,cocktail,bubble,quick,merge,optimized_cocktail,comb,comb_shaker,max_heap,radix_LSD,pigeonhole]
    # 	for a in algors:
    # 		shuffle(arr)
    # 		a(arr)
    # 	arr.animate_frames(sort_type=algor, input_type="random",ms_frame=ms_frame)
    # else:
    # 	print("algoritm not recognized")
    print(f"finished in {int(time.time()-start)} seconds")


if __name__ == "__main__":

    main()
