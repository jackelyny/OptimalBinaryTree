import math
import sys


class Node:
    def __init__(self, key):
        self.parent = None
        self.left = None
        self.right = None
        self.key = key


# Performs a post-order, recursive traversal
def traversal(root, nodes):
    if root.left is not None:
        nodes = traversal(root.left, nodes)

    if root.right is not None:
        nodes = traversal(root.right, nodes)

    nodes.append(root)

    return nodes


dictionary = {}
with open(sys.argv[1]) as f:
    n = int(f.readline().strip())
    for line in f:
        current = line.split()
        key = current[0]
        probability = float(current[1])
        dictionary[key] = probability
key_set = sorted(list(dictionary.keys()))
# Insert an element at the beginning to pad out the keys
key_set.insert(0, 0)

tableau = [[0 for a in range(0, n+1)] for b in range(0, n+2)]
root = [[None for a in range(0, n+1)] for b in range(0, n+2)]
for i in range(1, n+1):
    tableau[i][i] = dictionary[key_set[i]]
    root[i][i] = i

tableau[n+1][n] = 0
for d in range(1, n):
    for i in range(1, n-d+1):
        j = i + d
        minimum = math.inf
        for k in range(i, j+1):
            q = tableau[i][k-1] + tableau[k+1][j]
            if q < minimum:
                minimum = q
                root[i][j] = k
        sum = 0
        for a in range(i, j+1):
            sum = sum + dictionary[key_set[a]]
        tableau[i][j] = minimum + sum


key = key_set[root[1][n]]
tree_root = Node(key)
stack = [(tree_root, 1, n)]
while len(stack) > 0:
    (x, i, j) = stack.pop()
    l = root[i][j]
    if l < j:
        v = root[l+1][j]
        r_child = Node(key_set[v])
        r_child.parent = x
        x.right = r_child
        stack.append((r_child, l+1, j))
    if l > i:
        v = root[i][l-1]
        l_child = Node(key_set[v])
        l_child.parent = x
        x.left = l_child
        stack.append((l_child, i, l-1))
nodes = []
nodes = traversal(tree_root, nodes)
while len(nodes) > 0:
    current_node = nodes.pop()
    parent = current_node.parent
    if parent is not None:
        parent = parent.key
    left = current_node.left
    if left is not None:
        left = left.key
    right = current_node.right
    if right is not None:
        right = right.key
    print("Node:")
    print("\tKey: %s" % current_node.key)
    print("\tProbability: %.2f%%" % (dictionary[current_node.key] * 100))
    print("\tParent: %s" % parent)
    print("\tLeft Child: %s" % left)
    print("\tRight Child: %s\n" % right)