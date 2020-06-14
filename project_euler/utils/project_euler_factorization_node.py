"""
Project Euler Node Helper
"""

import copy


class FactorizationNode(object):
    def __init__(self, factor, solution):
        self.factor = factor
        self.solution = solution
        self.values = []
        self.children_nodes = {}  # {factor : node}

    def add_child(self, node):
        if node.factor in self.children_nodes:
            return False
        self.children_nodes[node.factor] = node

    def has_factor(self, factor):
        return factor in self.children_nodes

    def get_factor(self, factor):
        return self.children_nodes.get(factor, None)

    def add_value(self, number):
        self.values.append(number)

    def print_self(self, past_list):
        # print(' ' * len(past_list)),
        print('{} Solution: {}'.format(past_list, self.solution, self.values))
        # print('{} Solution: {} Values: {}'.format(past_list, self.solution, self.values))

    def print_recursive(self, past_list=[]):
        if self.factor > 0:
            past_list.append(self.factor)
            self.print_self(past_list)
        for factor in self.children_nodes:
            new_list = copy.copy(past_list)
            child_node = self.children_nodes[factor]
            child_node.print_recursive(new_list)


class FactorizationTree(object):
    def __init__(self):
        self.root_node = FactorizationNode(0, 0)

    def add_value(self, number, factor_count_list, solution=None):
        if len(factor_count_list) == 0:
            return

        node = self.root_node
        for factor in reversed(sorted(factor_count_list)):
            if node.has_factor(factor):
                new_node = node.get_factor(factor)
            elif solution:
                new_node = FactorizationNode(factor, solution)
                node.add_child(new_node)
            else:
                return 1
            node = new_node

        if solution:
            if node.solution != solution:
                exit('noooo {} {}'.format(solution, node.solution))

        node.add_value(number)

    def print_tree(self):
        self.root_node.print_recursive()
