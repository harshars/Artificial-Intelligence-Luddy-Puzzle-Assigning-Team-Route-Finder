#!/usr/local/bin/python3
#
# choose_team.py : Choose a team of maximum skill under a fixed budget
#
# Code by: [[Harsha Raja Shivakumar | Maithreyi Manur Narasimha Prabhu | Sunny Bhati]]
#

import sys


def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res


def load_people(filename):
    with open(
            filename,
            "r") as f:
        data = [line for line in f.read().split("\n")]

    # If you wanna use dictionary
    # data_final = {}
    # for i in data_temp:
    #    data_final[i.split()[0]] = [int(i.split()[1]), float(i.split()[2])]

    final_data = {}
  
    for i in data:
        # key = name, value1 = skill, value2 = cost, value3 = skill/cost
        final_data[i.split()[0]] = [float(i.split()[1]), float(i.split()[2]), float(i.split()[1])/float(i.split()[2])]

    return final_data


def upper_bound_cost(data, path, name_fringe_index, budget):
    # print(path)
    upper_bound = 0
    upper_bound1 = 0
    cost = 0
    cost1 = 0
    total_path_capacity = 0
    total_path_capacity1 = 0
    total_skill = 0
    total_skill1 = 0

    keys = [key for key, value in path.items() if value == 1]
    keys1 = [key for key, value in path.items() if value == 0]

    for i in range(len(data)):
        if list(data.items())[i][0] in keys:
            total_path_capacity = total_path_capacity + list(data.items())[i][1][1]
            total_path_capacity1 = total_path_capacity1 + list(data.items())[i][1][1]
            # total_skill = total_skill + data["skill"].iloc[i]
            # total_skill1 = total_skill1 + data["skill"].iloc[i]
            # upper_bound += data["skill"].iloc[i]
            # upper_bound1 += data["skill"].iloc[i]

    keys.append(list(data.items())[name_fringe_index][0])

    #upper_bound += data["skill"].iloc[name_fringe_index]

    path1 = path.copy()

    path2 = path.copy()

    # upper_bound, cost => Including the name_fringe_index
    # upper_bound1, cost1 => Excluding the name_fringe_index

    budget1 = budget
    i = 0

    flag1 = 0
    flag2 = 0
    while (i <= len(data)):
        # print(data["cost"].iloc[i])
        if (budget1 - list(data.items())[i][1][1] >= 0) & (list(data.items())[i][0] not in keys1):
            if (list(data.items())[i][0] in keys) & (i <= name_fringe_index) & (list(data.items())[i][0] not in keys1):
                upper_bound += list(data.items())[i][1][0]
                total_skill = total_skill + list(data.items())[i][1][0]
                flag1 = 1
            if (list(data.items())[i][0] in keys) & (i < name_fringe_index) & (list(data.items())[i][0] not in keys1):
                upper_bound1 += list(data.items())[i][1][0]
                total_skill1 = total_skill1 + list(data.items())[i][1][0]
                flag2 = 1
            if (list(data.items())[i][0] not in keys1):
                cost += list(data.items())[i][1][1]
                flag1 = 1

            if (i != name_fringe_index) & (list(data.items())[i][0] not in keys1):
                cost1 += list(data.items())[i][1][1]
                flag2 = 1
            budget1 = budget1 - list(data.items())[i][1][1]
        i += 1
        if i == len(data):
            break
        if (budget1 - list(data.items())[i][1][1] < 0) and (list(data.items())[i][0] not in keys1):
            if (budget1 - list(data.items())[i][1][1] < 0) & (i <= name_fringe_index) & (
                    list(data.items())[i][0] not in keys1):
                upper_bound = -1
                # print("_______________________________")

            if (budget1 - list(data.items())[i][1][1] < 0) & (i < name_fringe_index) & (list(data.items())[i][0] not in keys1):
                upper_bound1 = -1
                # print("---------------------------------")
            break
    if (i < len(data)) & ((budget - cost) > 0) & (flag1 == 1):
        cost = total_skill + (budget - cost) * list(data.items())[i][1][0] / list(data.items())[i][1][1]
    elif flag1 == 1:
        cost = upper_bound

    if (i < len(data)) & ((budget - cost1) > 0) & (flag2 == 1):
        cost1 = total_skill1 + (budget - cost1) * list(data.items())[i][1][0] / list(data.items())[i][1][1]
    elif flag2 == 1:
        cost1 = upper_bound1

    path2[list(data.items())[name_fringe_index][0]] = 1
    path1[list(data.items())[name_fringe_index][0]] = 0

    # print(upper_bound, cost, upper_bound1, cost1, path2, path1)
    #print(total_path_capacity, total_path_capacity1)
    return upper_bound, cost, path2, total_path_capacity + list(data.items())[name_fringe_index][1][1], upper_bound1, cost1, path1, total_path_capacity1


def successor(data, path, budget):

    #print(list(data.items())[0])
    #print(data)
    names = list(path.keys())
    data_sub = {k: v for k, v in data.items() if k not in names}
    #print(data_sub)
    #data_sub = data[~data["name"].isin(names)]
    #print(len(data_sub))
    #print(data_sub[0])
    #print(data_sub.keys()[0])
    if len(data_sub) == 0:
        return []

    name_fringe = list(data_sub.keys())[0]
    name_fringe_index = list(data.keys()).index(name_fringe)

    #print(name_fringe)
    #print(name_fringe_index)

    upper_bound, cost, path2, total_path_capacity, upper_bound1, cost1, path1, total_path_capacity1 = upper_bound_cost(
        data, path, name_fringe_index, budget)
    #print(total_path_capacity, total_path_capacity1)
    return [(path2, upper_bound, cost, total_path_capacity), (path1, upper_bound1, cost1, total_path_capacity1)]


def check(path, max_skills, upper_bound, previous_path, total_path_capacity, total_cost):
    if upper_bound > max_skills:
        return path, upper_bound, total_path_capacity
    else:
        return previous_path, max_skills, total_cost


def solve(data, budget):
    fringe = [({'root': 0}, 0)]
    final_solution = []

    max_skills = -1
    final_people = ""
    total_cost = 0

    while (len(fringe) > 0):
        path, total_path_capacity = fringe.pop(0)
        #print(path)
        #print("after while", total_path_capacity)

        # path1, upper_bound1, cost1, total_path_capacity1 = successor(path)
        for (path1, upper_bound1, cost1, total_path_capacity1) in successor(data, path, budget):
            # print(max_skills,final_people,path)
            # print(path, path1)
            if not (((total_path_capacity1) > budget) | (upper_bound1 > cost1)):
                if Merge(path, path1) == len(data) and total_path_capacity + total_path_capacity1 != 0:
                    #print("Added1")
                    final_people, max_skills, total_cost = check(Merge(path, path1), max_skills, upper_bound1,
                                                                 final_people, total_path_capacity1, total_cost)
                    #print(max_skills, upper_bound1)
                else:
                    # print(len(list(Merge(path,path1).keys())))
                    # print(Merge(path1,path))
                    if len(list(Merge(path, path1).keys())) == len(data)+1 and total_path_capacity + total_path_capacity1 != 0:
                        final_people, max_skills, total_cost = check(Merge(path, path1), max_skills, upper_bound1,
                                                                     final_people, total_path_capacity1, total_cost)
                        #print("Added2", max_skills, upper_bound1)
                    else:
                        if upper_bound1 != -1:
                            #print("Inside if condition", total_path_capacity1)
                            fringe.append((Merge(path, path1), total_path_capacity1))

            elif total_path_capacity1 >= budget and total_path_capacity + total_path_capacity1 != 0:
                final_people, max_skills, total_cost = check(path, max_skills, upper_bound1, final_people,
                                                             total_path_capacity, total_cost)
                #print("Added3", max_skills, upper_bound1)

    return (final_people, max_skills, total_cost)


if __name__ == "__main__":

    if (len(sys.argv) != 3):
        raise Exception('Error: expected 2 command line arguments')

    budget = float(sys.argv[2])
    data = load_people(sys.argv[1])

    #print(data)
    data = dict(sorted(data.items(), key=lambda x: x[1][2], reverse=True))

    #print(data)
    #data["skill_cost"] = data["skill"] / data["cost"]

    #data = data.sort_values(by=['skill_cost'], ascending=False).reset_index(drop=True)

    final_people, max_skills, total_cost = solve(data, budget)
    # print("\n",final_people, max_skills)

    if len(final_people) > 1:
        final_people1 = [key for key, value in final_people.items() if value == 1]

        print("Found a group with %d people costing %f with total skill %f" % \
                   ( len(final_people1), total_cost , max_skills))

        for i in final_people1:
            print(i + " " + '1.000000')
    else:
        print("Inf")

