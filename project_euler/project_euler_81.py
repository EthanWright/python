matrix = [
[131, 673, 234, 103, 18],
[201, 96, 342, 965, 150],
[630, 803, 746, 422, 111],
[537, 699, 497, 121, 956],
[805, 732, 524, 37, 331]
]

def main():
    for x in xrange(DIM, 0, -1):
        for y in xrange(0, DIM-x, 1):
            print matrix[DIM-y-1][x+y]
            update(DIM-y-1, x+y)

    for y in xrange(DIM, 0, -1):
        for x in xrange(0, y, 1):
            print matrix[y-x-1][x]
            update(y-x-1, x)

def update(y, x):
    #print x
    #print y
    #print matrix[y][x]

    right = 0
    below = 0
    if x + 1 < DIM:
        right = matrix[y][x+1]

    if y + 1 < DIM:
        below = matrix[y+1][x]

    if right and below:
        if right < below:
            matrix[y][x] += right
        else:
            matrix[y][x] += below
    elif right:
        matrix[y][x] += right
    elif below:
        matrix[y][x] += below

matrix = [line.rstrip('\n').split(',') for line in open('project_euler_81_data.txt', 'r')]
DIM = len(matrix)
for y in xrange(DIM):
    for x in xrange(DIM):
        matrix[y][x] = int(matrix[y][x])

main()
print matrix[0][0]