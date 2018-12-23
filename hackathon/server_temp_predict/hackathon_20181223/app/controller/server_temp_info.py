import json
import os
import re


class ServerTemp:
    def __init__(self):
        self.server_temp_info = {}

    def server_temp_json(self):
        new_value_list = []
        dir_path = os.path.abspath(os.path.dirname(__file__))
        with open(os.path.join(dir_path, "sdrInfo.json"), 'r')as fp:
            x = json.load(fp)

            keys = x.keys()
            for key in keys:
                values_list = x[key]
                if "CPU0_Margin_Temp" not in key:
                    continue

                for tmp in values_list:
                    if 'degrees' in tmp['value']:
                        # tmp['time'] = re.sub(r'-|\s|:', '', tmp['time'])
                        tmp['value'] = re.search(r'\d+', tmp['value']).group()
                        tmp.pop('status')
                        new_value_list.append(tmp)

        server_temp_info = {}
        server_temp_info.update({'server_temp_info': new_value_list})
        self.server_temp_info = server_temp_info

        with open(os.path.join(dir_path, 'server_temp_info.json'), 'w')as fp:
            json.dump(server_temp_info, fp)

if __name__ == "__main__":
    print("Start predict-------")
    model = ServerTemp()
    model.server_temp_json()