import json
def parse_json(json_file_name):
    json_content = None
    with open(json_file_name, "r") as f:
        json_content = json.load(f)
    recipe = parse_recipe(json_content['recipe'])


def parse_recipe(recipe_dict):
    pass
