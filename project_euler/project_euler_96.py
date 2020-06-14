"""
Project Euler Problem 96
Ethan Wright
"""
from pprint import pprint

"""
This is the one this program can't solve without some help, or guess and check:
 0 | 1 4 3 9 8 7 2 5 6
 9 | 6     4 2 5
18 | 2     7 3 1   9 4_
27 | 9     3   4   7
36 | 3     6   8
45 | 4 1   2   9     3_
54 | 8 2 1 5 7 3     9
63 | 7     1 4 2     5
72 | 5 3 4 8 9 6 7 1 2


 0 |   4 3 9 8 6 2 5
 9 | 6     4 2 5
18 | 2         1   9 4
27 | 9         4   7
36 | 3     6   8
45 | 4 1   2   9     3
54 | 8 2   5
63 |             8 2 5
72 | 5 3 4 8 9 2 7 1 6
"""


class Group(object):

    def __init__(self, index, size, type):
        self.cells = []
        self.size = size
        self.index = index
        self.hypo_cells = {}
        self.type = type

    def add_cell(self, cell):
        self.cells.append(cell)

    def get_cells(self):
        return self.cells

    @property
    def hypothetical_values(self):
        result = []
        for values in self.hypo_cells.values():
            result.extend(values)
        return set(result)

    def add_hypo_values(self, index, value_list):
        updated_a_cell = False

        if index in self.hypo_cells:
            len_before = len(self.hypo_cells[index])
            for value in value_list:
                self.hypo_cells[index].add(value)
            if len(self.hypo_cells[index]) > len_before:
                updated_a_cell = True
        else:
            self.hypo_cells[index] = set(value_list)
            updated_a_cell = True

        #print("Adding {} to hypo list for Cell {} in {} Group {}".format(value_list, index, self.type, self.index))

        return updated_a_cell 


class Cell(object):
    def __init__(self, index):
        self.value = 0
        self.index = index
        self.invalid_values = set()
        self.has_to_be = []

        self.horizontal_group_index = index / 9
        self.vertical_group_index = index % 9
        self.box_group_index = (3 * (self.horizontal_group_index / 3)) + (self.vertical_group_index / 3)
        #print(self.index, self.horizontal_group, self.vertical_group, self.box_group)

    def set_value(self, value):
        self.value = value
        #print("Updating cell {} to be {}").format(self.index, value)
        # TODO Should I pass in the GroupsList and validate here?

    def __repr__(self):
        return "Cell Index: {} Value: {}".format(self.index, self.value)


class GroupsList(object):

    def __init__(self, size):
        self.size = size
        self.horizontal_groups = { x: Group(x, self.size, "horizontal") for x in range(self.size) }
        self.vertical_groups = { x: Group(x, self.size, "vertical") for x in range(self.size) }
        self.box_groups = { x: Group(x, self.size, "box") for x in range(self.size) }

    def add_cell_to_groups(self, cell):
        self.horizontal_groups[cell.horizontal_group_index].add_cell(cell)
        self.vertical_groups[cell.vertical_group_index].add_cell(cell)
        self.box_groups[cell.box_group_index].add_cell(cell)

    def get_groups_for_cell(self, cell):

        horizontal_group = self.horizontal_groups.get(cell.horizontal_group_index)
        vertical_group = self.vertical_groups.get(cell.vertical_group_index)
        box_group = self.box_groups.get(cell.box_group_index)

        return [horizontal_group, vertical_group, box_group]

    def get_all_affecting_cells(self, cell):
        cell_list = []
        groups = self.get_groups_for_cell(cell)
        for group in groups:
            cell_list.extend(group.get_cells())

        return cell_list

    def get_invalid_values(self, cell):
        return set([c.value for c in self.get_all_affecting_cells(cell)])

    def get_invalid_hypothetical_values(self, cell):

        invalid_hypothetical_values = set()
        groups = self.get_groups_for_cell(cell)
        for group in groups:
            invalid_hypothetical_values = invalid_hypothetical_values.union(set(group.hypothetical_values) - set(group.hypo_cells.get(cell.index, [])))

        return invalid_hypothetical_values

    def get_valid_values(self, cell):
        diff_set = set([x for x in range(1, self.size + 1)])
        return diff_set - self.get_invalid_values(cell)

    @property
    def groups(self):
        return self.horizontal_groups.values() + self.vertical_groups.values() + self.box_groups.values()


class Board(object):

    def __init__(self, size):
        self.groups_list = GroupsList(size)
        self.cells = []
        self.size = size

        for x in range(0, self.size * self.size):
            new_cell = Cell(x)
            self.cells.append(new_cell)
            self.groups_list.add_cell_to_groups(new_cell)

    def initialize_game(self, starting_array):
        index = 0

        for line in starting_array:
            for number in line:
                cell=self.cells[index]
                cell.set_value(int(number))
                index += 1

    @property
    def is_solved(self):
        for cell in self.cells:
            if cell.value == 0:
                return False
        return True

    def print_board(self, new=None):
        for cell in self.cells:
            if cell.index % self.size == 0:
                if cell.index > 0:
                    print ("\n"),
                print("{}{} |".format(" " if cell.index < 10 else "",  cell.index)),
            if cell.value == 0:
                print(" "),
            else:
                if cell.index == new:
                    print("_"),
                else:
                    print(cell.value),
        print "\n"

    def solve(self):
        #self.print_board()
        updated_a_cell = True

        while updated_a_cell:
            updated_a_cell = False
            #self.print_board()
            #import pdb; pdb.set_trace()
            for group in self.groups_list.groups:
                #import pdb; pdb.set_trace()
                if self.solve_by_group(group):
                    updated_a_cell = True
                #self.print_board()

        #for group in self.groups_list.groups:
        #    print(group.hypo_cells)

        return self.is_solved

    def solve_by_group(self, group):

        updated_a_cell = False
        value_dict = { x: [] for x in range(1, self.size + 1) }

        for cell in group.get_cells():
            #import pdb; pdb.set_trace()
            if cell.value == 0:

                valid_values = self.groups_list.get_valid_values(cell)

                if len(cell.has_to_be):
                    valid_values = valid_values.intersection(cell.has_to_be)

                valid_values_minus_hypo = valid_values - self.groups_list.get_invalid_hypothetical_values(cell)

                #print("Cell: {} Valid Values: {} Invalid Hypothetical Values: {} Leaving {}".format(
                #    cell.index, valid_values, self.groups_list.get_invalid_hypothetical_values(cell), sorted(valid_values_minus_hypo)
                #))

                if len(valid_values_minus_hypo) == 1:
                    value = valid_values_minus_hypo.pop()
                    cell.set_value(value)
                    #print("Cell {} can only be one value, {}".format(cell.index, value))
                    #self.print_board(new=cell.index)
                    value_dict[value] = []
                    updated_a_cell = True
                    self.clear_hypo_values_for_cell(cell)

                else:
                    for value in valid_values_minus_hypo:
                        value_dict[value].append(cell)

        #print("Hypo Cells "),;pprint(group.hypo_cells)
        #print("Value Dict "),;pprint(value_dict)
        values_to_remove = []
        for value in value_dict:

            if len(value_dict[value]) == 1:  # Only 1 cell in the group can be this value
                new_cell = next(iter(value_dict[value]))
                new_cell.set_value(value)
                #print("The {} group {} needs a {} and Cell {} is the only viable cell".format(group.type, group.index, value, new_cell.index))
                #self.print_board(new=new_cell.index)
                updated_a_cell = True
                self.clear_hypo_values_for_cell(new_cell)
                value_dict[value] = []
                values_to_remove.append(value)

        for value in value_dict:
            value_dict[value] = list(set(value_dict[value]) - set(values_to_remove))

        for value in value_dict:

            if len(value_dict[value]) == 2 or len(value_dict[value]) == 3:

                other_group = self.check_if_cell_list_resides_in_another_group(value_dict[value], group.type)
                if other_group:
                    for hypo_cell in value_dict[value]:
                        if other_group.add_hypo_values(hypo_cell.index, [value]):
                            updated_a_cell = True

            if len(value_dict[value]) == 2:
                for hypo_cell in value_dict[value]:
                    if group.add_hypo_values(hypo_cell.index, [value]):
                         updated_a_cell = True

        # TODO Are any hypo cells a triplet?

        # Are any hypo cells a pair?
        """
        for x in group.hypo_cells:
            if len(group.hypo_cells[x]) == 2:
                for y in group.hypo_cells:
                    if group.hypo_cells[x] == group.hypo_cells[y] and x != y:
                        hypo_values = group.hypo_cells[x]

                        for hypo_cell_index in [x, y]:
                           hypo_cell = self.cells[hypo_cell_index]
                           if not len(hypo_cell.has_to_be):
                               hypo_cell.has_to_be = hypo_values
                               updated_a_cell = True

        """

        # Are any hypo cells a pair? Attempt 2
        value_to_cell = {}      
        for x in group.hypo_cells:
            for y in group.hypo_cells[x]:
                if y in value_to_cell:
                    value_to_cell[y].append(x)
                else:
                    value_to_cell[y] = [x]
        #pprint(value_to_cell)

        for x in value_to_cell:
            if len(value_to_cell[x]) == 2:
                for y in value_to_cell:
                    if value_to_cell[x] == value_to_cell[y] and x != y:
                        hypo_values = [x, y]

                        for hypo_cell_index in value_to_cell[x]:
                           hypo_cell = self.cells[hypo_cell_index]
                           if not len(hypo_cell.has_to_be):
                               hypo_cell.has_to_be = hypo_values
                               updated_a_cell = True

        return updated_a_cell

    def clear_hypo_values_for_cell(self, cell):
        #print("Removing {} and value {}".format(cell.index, cell.value))
        for group in self.groups_list.get_groups_for_cell(cell):
            if cell.index in group.hypo_cells:
                #import pdb;pdb.set_trace()
                del group.hypo_cells[cell.index]
            for index in group.hypo_cells:
                group.hypo_cells[index] = set(group.hypo_cells[index]) - set([cell.value])

    def check_if_cell_list_resides_in_another_group(self, cell_list, group_type):
        other_group = None
        if group_type != 'box':
            # Check if it intersects with a box group
            if self.has_all_the_same_box_groups(cell_list):
                other_group = self.groups_list.box_groups.get(cell_list[0].box_group_index)

        else:
            # Check if it intersects with either a horizontal or vertical group
            if self.has_all_the_same_vertical_groups(cell_list):
                other_group = self.groups_list.vertical_groups.get(cell_list[0].vertical_group_index)

            elif self.has_all_the_same_horizontal_groups(cell_list):
                other_group = self.groups_list.horizontal_groups.get(cell_list[0].horizontal_group_index)

        return other_group

    def has_all_the_same_box_groups(self, cell_list):
        return self.has_all_the_same_group_index([cell.box_group_index for cell in cell_list])

    def has_all_the_same_vertical_groups(self, cell_list):
        return self.has_all_the_same_group_index([cell.vertical_group_index for cell in cell_list])

    def has_all_the_same_horizontal_groups(self, cell_list):
        return self.has_all_the_same_group_index([cell.horizontal_group_index for cell in cell_list])

    def has_all_the_same_group_index(self, index_list):
        for index in index_list:
            if index != index_list[0]:
                return False
        return True


class SudokuPuzzleSolver(object):

    def run(self):
        file_name = 'data/project_euler_96_data_5.txt'
        starting_array = []
        total = 0

        with open(file_name) as sudoku_file:
            line = sudoku_file.readline().rstrip()
            while line:

                if 'Grid' in line:  # We hit the end of a grid
                    if starting_array:
                        total += self.solve_sudoku_puzzle(starting_array)
                        starting_array = []

                else:
                    starting_array.append([x for x in line])

                line = sudoku_file.readline().rstrip()

            if starting_array:
                total += self.solve_sudoku_puzzle(starting_array)
                starting_array = []
        print(total)
        return total

    def solve_sudoku_puzzle(self, starting_array):
        total = 0
        board = Board(len(starting_array))
        board.initialize_game(starting_array)
        #board.print_board()  # Print before solving
        if board.solve():
            print("DONE!")
            total = board.cells[0].value * 100 + board.cells[1].value * 10 + board.cells[2].value
        else:
            print("Well shit")
        #board.print_board()  # Print after solving

        return total

if __name__ == "__main__":
    puzzle = SudokuPuzzleSolver()
    puzzle.run()
