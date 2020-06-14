# Project Euler 22

class Tree(object):

    def __init__(self, score):
        self.score = score
        self.branches = {}
        self.terminal_branch = False

    def add_branch(self, value):
        new_branch = Tree(self.score + value)
        self.branches[value] = new_branch

    def get_branch(self, value):
        return self.branches.get(value)

    def get_branches_ordered(self):
        ordered_branches = []
        #import pdb; pdb.set_trace()
        res = sorted(self.branches.keys())
        for index in res:
            ordered_branches.append(self.branches.get(index))
        return ordered_branches

    def __repr__(self):
        return "Score {} Branches: {} Terminal: {}".format(self.score, self.branches.keys(), self.terminal_branch)
    
def to_num_arr(name):
    num_arr = []
    for letter in name:
        num = ord(letter.lower()) - 96
        num_arr.append(num)
    return num_arr

def add_name(name, tree):
    num_arr = to_num_arr(name)

    for num in num_arr:
        branch = tree.get_branch(num)
        if not branch:
            tree.add_branch(num)
            branch = tree.get_branch(num)

        tree = branch

    tree.terminal_branch = True

class Counter(object):
    def __init__(self):
        self.value = 1

    def increment(self):
        self.value += 1

    def get_value(self):
        return self.value

def sum_tree(tree, counter):
    #print(tree)
    sum = 0

    if tree.terminal_branch:
        sum = tree.score * counter.get_value()
        counter.increment()

    for branch in tree.get_branches_ordered():
        #import pdb; pdb.set_trace()
        sum += sum_tree(branch, counter)

    return sum

def clean(name):
    return name.strip().replace('"', '')

def run():
    tree_root = Tree(0)

    #add_name("colin", tree_root)
    with open("project_euler_22_data.txt") as fp:
       data = fp.read()
    names = data.split(",")

    for name in names:
       add_name(clean(name), tree_root)

    counter = Counter()
    total = sum_tree(tree_root, counter)

    print(total)
    return total

if __name__ == "__main__":
    run()

    # 871198282
