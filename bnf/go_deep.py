import copy

ary = [
    {"1":[
        {"1-a":[{"1-a-1":[1,2,3,4, "1-a-1"]}]},
        {"1-b":[{"1-b-1":[{
                    "1-b-1-a":[5,6,7,8],
                    "1-b-1-b":[55,66,77,88]
                }]},
                {"1-b-2": [{
                    "1-b-2-a": [25, 26, 27, 28],
                    "1-b-2-b": [255, 266, 277, 288]
                }]}
        ]},
        {"1-c":[]},
        {"1-d":[11]}
            ],
    "2":[22,33,4,4]
}]


class TestGoDeep:
    def __init__(self):
        self.end_message = "This tree is empty."

    def go_deep(self, parent_ary):
        if parent_ary is None or len(parent_ary) == 0:
            print(self.end_message)
            print(parent_ary)

        if len(parent_ary) > 0:
            for child_ary in parent_ary:
                if isinstance(child_ary, dict):
                    for child_ary_key, child_ary_value in child_ary.items():
                        for value in child_ary_value:

                            if child_ary_key in child_ary_value:
                                print("go back")
                                print(child_ary_key, child_ary_value, "\n")
                                break


                            if isinstance(value, dict):
                                copy_class = copy.deepcopy(TestGoDeep)
                                temp_go_deep = copy_class().go_deep
                                # print("function Id --- {0}".format(id(temp_go_deep)))
                                temp_go_deep(child_ary_value)

                            else:
                                print(child_ary_key, child_ary_value)

                            break

a = TestGoDeep()
a.go_deep(ary)
