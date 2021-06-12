
def process_data(data):
    numbers = [int(i) for i in data.split()]
    return numbers

# Works for small trees but hits max recursion depth error for large trees
# def recurse(tree, nodes, metadata, total=0):
#     if nodes == 0:
#         tree_length = len(tree)
#         total_metadata = sum(metadata)
#         if tree_length != total_metadata:
#             m = metadata.pop()
#             total += sum(tree[0: m])
#             return tree[m:], metadata, total
#         else:
#             total += sum(tree)
#             return tree, metadata, total

#     for n in range(nodes):
#         nodes -= 1
#         metadata.append(tree[1])
#         tree, metadata, total = recurse(
#             tree[2:], tree[0], metadata, total)

#     return tree, metadata, total


class Node():
    def __init__(self, child_nodes, metadata_entries, parent=None, value=0) -> None:
        self.child_nodes = child_nodes
        self.metadata_entries = metadata_entries
        self.nodes = []
        self.data = []
        self.value = value
        self.parent = parent

    def __str__(self) -> str:
        return f"{self.data} - {self.value} - {self.child_nodes} - {self.metadata_entries}"


def part1(data):
    tree_data = process_data(data)
    root_node_children = tree_data.pop(0)
    root_node_metadata_entries = tree_data.pop(0)
    tree = Node(root_node_children, root_node_metadata_entries)
    current_node = tree
    total = 0
    while tree_data:
        node_children = tree_data.pop(0)
        node_metadata_entries = tree_data.pop(0)
        node = Node(node_children, node_metadata_entries, current_node)
        current_node.nodes.append(node)
        current_node = node
        if node_children > 0:
            continue

        while current_node.child_nodes == len(current_node.nodes):
            for i in range(current_node.metadata_entries):
                current_node.data.append(tree_data.pop(0))
            sum_of_data = sum(current_node.data)

            # Part 1 - total of all metadata
            total += sum_of_data

            # Part 2 - add value
            if current_node.child_nodes == 0:
                current_node.value = sum_of_data
            else:
                temp_value = 0
                for d in current_node.data:
                    index = d - 1
                    if index == -1:
                        continue
                    try:
                        temp_value += current_node.nodes[index].value
                    except IndexError:
                        temp_value += 0
                current_node.value = temp_value

            if current_node.parent == None:
                break
            current_node = current_node.parent

    return total, current_node.value

    # tree, metadata, total = recurse(tree[2:], tree[0], [tree[1]])
    # return total
