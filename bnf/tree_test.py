import re, random


class Tree:
    def __init__(self):
        self.parent = {}
        self.child = []


    def set_parent(self, parent_name):
        self.parent[parent_name] = []


    def set_child(self, parent_name, child_str):
        my_child = str(child_str).replace(" ", "").split("|")
        self.child = my_child
        self.parent[parent_name] = my_child


    def print_all_parent(self):
        parent = self.parent

        for parent_name, my_all_child in parent.items():
            print(parent_name, my_all_child)


    def parent_activate(self):
        all_parent = self.parent
        have_parent = False
        print("\n----------------", random.randint(1, 100), "----------------")

        for parent_name, my_all_child in all_parent.items():
            for child in my_all_child:
                pattern = r"(<(\w*-*)*>)"
                master_pat = re.compile(pattern)

                ele_find = re.findall(master_pat, child)
                for ele in ele_find:
                    if ele[0] in all_parent.keys():
                        text = str(child).replace(ele[0], " "+ " ".join(all_parent[ele[0]]) + " ")
                        my_all_child[my_all_child.index(child)] = text
                        have_parent = True

        Tree.print_all_parent(self)

        if have_parent:
            Tree.parent_activate(self)



bnf_tree = Tree()
bnf_tree.set_parent("<translation-unit>")
bnf_tree.set_child("<translation-unit>", "{ <external-declaration> }*")

bnf_tree.set_parent("<external-declaration>")
bnf_tree.set_child("<external-declaration>", "<function-definition>  |  <declaration>")

bnf_tree.set_parent("<function-definition>")
bnf_tree.set_child("<function-definition>", "{ <declaration-specifier> }* <declarator> { <declaration> }* <compound-statement>")

# bnf_tree.find_all_parent()
bnf_tree.parent_activate()



