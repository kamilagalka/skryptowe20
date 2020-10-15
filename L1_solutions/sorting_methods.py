SHRINK_FACTOR = 1.3


def comb_sort(numbers: list) -> list:
    """
    Sorts list of numbers using comb sort algorithm.
    Note: comb sort is not a stable sort, meaning that the relative order of equal sort items is not preserved.
    :param numbers: list of numbers to sort
    :return: list sorted in ascending order
    """
    numbers_len = len(numbers)
    gap = numbers_len
    is_sorted = False

    while not is_sorted:
        gap = max(1, int(gap / SHRINK_FACTOR))

        for i in range(numbers_len - gap):
            j = gap + i

            if numbers[i] > numbers[j]:
                numbers[i], numbers[j] = numbers[j], numbers[i]
                is_sorted = False

        if gap == 1:
            return numbers

    return numbers


def merge_sort(numbers: list) -> list:
    """
    Sorts list of numbers using merge sort algorithm.
    Note: this implementation is not stable, meaning that the relative order of equal sort items is not preserved.
    :param numbers: list of numbers to sort
    :return: list sorted in ascending order
    """

    if len(numbers) > 1:
        mid_id = len(numbers) // 2

        left = merge_sort(numbers[:mid_id])
        right = merge_sort(numbers[mid_id:])
        numbers = []

        while len(left) and len(right):
            if left[0] < right[0]:
                numbers.append(left[0])
                left.pop(0)
            else:
                numbers.append(right[0])
                right.pop(0)

        numbers.extend(left)
        numbers.extend(right)

    return numbers


if __name__ == '__main__':
    numbers_to_sort = [0, -12.4323, 23, 0.0, -543.2, 65, 1023, 5.65, 0.00003]
    print(f"List to sort: {numbers_to_sort}\n")

    comb_sort_result = comb_sort(numbers_to_sort)
    print(f"Comb sort result: {comb_sort_result}")

    merge_sort_result = merge_sort(numbers_to_sort)
    print(f"Merge sort result: {merge_sort_result}")

    print("\n\nEmpty list test:")
    comb_sort_empty_list_result = comb_sort([])
    print(f"Comb sort empty list result: {comb_sort_empty_list_result}")

    merge_sort_empty_list_result = merge_sort([])
    print(f"Merge sort empty list result: {merge_sort_empty_list_result}")
