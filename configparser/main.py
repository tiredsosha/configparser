from configparser.entities.park import Park
import yaml


with open('configs/park.yaml') as park:
    fruits_list = Park(**yaml.safe_load(park))