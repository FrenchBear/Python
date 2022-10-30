import yaml
import pprint

pp = pprint.PrettyPrinter(indent=4)

with open("f1.yaml", "r") as stream:
    try:
        d:dict = yaml.safe_load(stream)
        for key, value in d.items():
            print(key + " : ", end='')
            pp.pprint(value)
        
        # l = d['items']
        # breakpoint()
        # pass

    except yaml.YAMLError as exc:
        print(exc)
