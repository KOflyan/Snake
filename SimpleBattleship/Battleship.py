"""Lets play Battleship!"""


import random


from graphics import *


def main():
    """Putting it all together."""
    x = 200
    y = 340
    hello()
    draw_field_etc(x, y)


def hello():
    """Hello."""
    print("Let the game begin!" + '\n')


def field(x, y, graph):
    """Drawing a field."""

    f = Rectangle(Point(x, y), Point(x + 240, y - 240))
    f.draw(graph)


def lines(x, y, graph):
    """Drawing lines"""
    dif = 48

    for i in range(1, 5):
        Line(Point(x, y - dif), Point(x + 240, y - dif)).draw(graph)
        Line(Point(x + dif, y), Point(x + dif, y - 240)).draw(graph)
        dif += 48


def adding_some_txt(x, y, graph):
    """Adding markers."""
    nums = 1
    abc = "ABCDE"
    dist = 24
    for i in range(1, 6):
        Text(Point(x - 15, y - dist), nums).draw(graph)
        Text(Point(x + dist, y - 255), abc[i-1]).draw(graph)
        nums += 1
        dist += 48


def coordinates_1(x, y):
    """Appending coordinates for size 1 ships."""
    list_of_x = []  # x
    list_of_y = []  # y

    step_v = 24
    for i in range(1, 6):  # appending all possible x and y to lists
        step_h = 24
        for j in range(1, 6):
            list_of_x.append(x + step_h)
            list_of_y.append(y - 240 + step_v)
            step_h += 48
        step_v += 48

    return list_of_x, list_of_y


def generating_rows_and_columns(list_of_x, list_of_y):
    """Linking A-E columns and 1-5 rows with points."""
    x_sort = []  # Excluding repeating x and y
    for i in list_of_x:
        if i not in x_sort:
            x_sort.append(i)

    y_sort = []
    for i in list_of_y:
        if i not in y_sort:
            y_sort.append(i)

    dict_abc = {}
    dict_num = {}
    st = "ABCDE"
    ind = 0  # Creating dictionaries for columns and rows
    ind2 = 5
    for i in range(1, 6):
        dict_abc[st[i-1]] = x_sort[ind]
        dict_num[str(ind2)] = y_sort[ind]
        ind += 1
        ind2 -= 1

    return dict_abc, dict_num


def ship_size_1(x, y):
    """Constructing ships of size 1."""
    list_of_x = coordinates_1(x, y)[0]  # Drawing 1 ship of size 1
    list_of_y = coordinates_1(x, y)[1]

    point1 = list([random.choice(list_of_x), random.choice(list_of_y)])

    return point1


def ship_size_2(x, y):
    """Constructing ships of size 2."""
    list_of_x = coordinates_1(x, y)[0]  # Same for 2-sized ship
    list_of_y = coordinates_1(x, y)[1]

    point1 = list([random.choice(list_of_x), random.choice(list_of_y)])
    point2 = []
    for i in list_of_x:
        for j in list_of_y:
            if i == point1[0] and (j == point1[1] - 48 or j == point1[1] + 48) or j == point1[1] \
                    and (i == point1[0] - 48 or i == point1[0] + 48):
                point2 = list([i, j])
                break
    return point1, point2


def draw_field_etc(x, y):
    """Drawing field and all."""
    g = GraphWin("Battleship", 600, 400)
    k = ship_size_1(x, y)
    while True:
        second = ship_size_1(x, y)
        if second[0] == k[0] and second[1] == k[1]:
            continue
        break

    points = []

    for i in range(2):
        while True:
            f = ship_size_2(x, y)
            if f[0] == k or f[1] == k or f[0] == second or f[1] == second:
                continue

            if f[0][0] not in points \
                    and f[0][1] not in points and f[1][0] not in points and f[1][1] not in points:

                for j in f:
                    for l in j:
                        points.append(l)
                break
            continue

    sunk = 0
    count = 0
    while True:

        for i in range(10):

            lines(x, y, g)
            adding_some_txt(x, y, g)
            field(x, y, g)
            sh = collect_input(x, y, g)

            if count == 6:
                break

            if sh[0] in k and sh[1] in k:
                sunk += 1
                count += 1
                ship1 = Circle(Point(k[0], k[1]), 20)
                ship1.setOutline("Red")
                ship1.draw(g)

            if sh[0] in second and sh[1] in second:
                sunk += 1
                count += 1
                ship2 = Circle(Point(second[0], second[1]), 20)
                ship2.setOutline("Red")
                ship2.draw(g)

            for j in range(len(points)-1):

                if sh[0] == points[j] and sh[1] == points[j + 1]:
                    count += 1
                    Circle(Point(points[j], points[j + 1]), 20).draw(g)

        Circle(Point(second[0], second[1]), 20).draw(g)
        Circle(Point(k[0], k[1]), 20).draw(g)

        Circle(Point(points[0], points[1]), 20).draw(g)
        Circle(Point(points[2], points[3]), 20).draw(g)
        Circle(Point(points[4], points[5]), 20).draw(g)
        Circle(Point(points[6], points[7]), 20).draw(g)

        print("Game over! Gratz bro!")
        while True:
            input_quest = input("Would you like to play again? (y/n): ")
            if input_quest != "y" and input_quest != "n":
                print("Type n or y!")
                continue
            break
        if input_quest is "y":
            g.close()
            g = GraphWin("Battleship", 600, 400)
            continue
        print('\n' + "Goodbye")
        break
    g.getMouse()


def collect_input(x, y, g):
    """Collecting and controlling user input."""

    while True:
        input_string = input("Please input column letter and number: ")

        if input_string == "end":
            print('\n' + "Goodbye")
            raise SystemExit
        if len(input_string) == 2:
            if input_string[0].isdigit() or input_string[1].isalpha():
                print("You\'re doing it all wrong!")
                continue
        if len(input_string) != 2:
            print("Entered value is incorrect!")
            continue
        if input_string[0] not in "abcdeABCDE":
            print("Only letters from A to E are allowed!")
            continue
        if int(input_string[1]) not in range(1, 6):
            print("Only numbers from 1 to 5 are allowed!")
            continue
        break

    letter = input_string[0].upper()
    number = input_string[1]

    list_abc = generating_rows_and_columns(coordinates_1(x, y)[0], coordinates_1(x, y)[1])[0]
    list_nums = generating_rows_and_columns(coordinates_1(x, y)[0], coordinates_1(x, y)[1])[1]

    circ = Circle(Point(list_abc[letter], list_nums[number]), 5)
    circ.setFill("Red")
    circ.setOutline("Red")
    circ.draw(g)

    list_of_points = (list([list_abc[letter], list_nums[number]]))
    return list_of_points

main()
