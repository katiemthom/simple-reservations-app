# Write a function that takes an iterable 
# (something you can loop through, ie: string, 
# list, or tuple) and produces a dictionary 
# with all distinct elements as the keys, and
# the number of each element as the value
def count_unique(some_iterable):
    count = {}
    for val in some_iterable: 
        count[val] = count.get(val, 0) + 1
    return count

# Given two lists, (without using the keyword 'in' 
# or the method 'index') return a list of all common 
# items shared between both lists
def common_items(list1, list2):
    list3 = []
    list1_count = count_unique(list1)
    list2_count = count_unique(list2)
    for key in list1_count.keys(): 
        value = list2_count.get(key, 0)
        if value != 0: 
            list3.append(key)
    return list3

# Given two lists, (without using the keyword 'in' or 
# the method 'index') return a list of all common 
# items shared between both lists. This time, use 
# a dictionary as part of your solution.
def common_items2(list1, list2):
    list1_dict = {}
    for val in list1:
        list1_dict[val] = 1
    for val in list2: 
        list1_dict[val] = list1_dict.get(val, 0) + 1
    common = []
    for key in list1_dict.keys(): 
        if list1_dict[key] > 1: 
            common.append(key)
    return common

string = "banana"
a_list = ["a", "1", "apple", "apple", "a", "0", "dog"]
another_list = ["a", 2, "apple", "apple","orange", "a", "3", "dog", "dog"]
a_tuple = (1, 1)
print common_items(a_list, another_list)