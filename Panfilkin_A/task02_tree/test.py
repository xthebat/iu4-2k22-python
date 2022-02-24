import tree

TREE_LISTS = [
    ['test', ['dir1_1', ['dir2_1', 'dir3_1']], ['dir1_2', '123']],
    ["level1", ["level11", "level111", ["level112", "level1121", "level1122"]], "level12",
     ["level13", "level131", "level132"]]
]


def main():
    print("----Test Case 1: PreGen list 1----\n")
    print(TREE_LISTS[0])
    tree.print_tree_list(TREE_LISTS[0])
    print('\n\n')

    print("----Test Case 2: PreGen list 2----\n")
    print(TREE_LISTS[1])
    tree.print_tree_list(TREE_LISTS[1])
    print('\n\n')

    print("----Test Case 3: Current Directory----\n")
    tree_list = tree.generate_tree_list('.')
    print(tree_list)
    tree.print_tree_list(tree_list)
    print('\n\n')


if __name__ == "__main__":
    main()
