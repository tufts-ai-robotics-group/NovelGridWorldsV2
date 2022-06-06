class SimpleItemEncoder:
    class TooManyItemTypes(Exception):
        pass

    def __init__(self, item_list=None, initial_id=1, id_limit=0):
        self.curr_id = initial_id - 1
        self.item_list = {}
        self.reverse_look_up_table = {}
        self.id_limit = id_limit
        if item_list is not None:
            self.load_item_list(item_list)
    

    def load_item_list(self, item_list):
        """
        Load the item_list from a pre-set dictionary.
        """
        for key, value in item_list.items():
            self.curr_id = max(value, self.curr_id)
            self.reverse_look_up_table[value] = key
        self.item_list = item_list


    def load_json(self, file_name: str):
        """
        Loads the json file from a previous run
        """
        with open(file_name, 'r') as f:
            item_list = json.load(f)
            self.load_item_list(item_list)
    
    def get_id(self, key: str):
        """
        Takes in a key, returns a list. Not thread-safe.
        """
        if key in self.item_list:
            return self.item_list[key]
        elif self.id_limit > 0 and self.curr_id + 1 >= self.id_limit:
            raise self.TooManyItemTypes(
                "Cannot add item \"" + key + "\" to the encoder because there are " +
                "too many types of items. Consider increasing the number of allowed item types."
            )
        else:
            self.curr_id += 1
            self.item_list[key] = self.curr_id
            self.reverse_look_up_table[self.curr_id] = key
            return self.curr_id
    
    def reverse_look_up(self, id: int):
        return self.reverse_look_up_table[id]
    
    def create_alias(self, alias_dict):
        """
        alias_dict: {"alias": "key"}
        """
        for alias, key in alias_dict.items():
            if key in self.item_list and alias not in self.item_list:
                self.item_list[alias] = self.item_list[key]

    def save_json(self, file_name: str):
        """
        Saves the encoding to a json file for future run
        """
        with open(file_name, 'w') as f:
            serialized = json.dumps(self.item_list)
            f.write(serialized)
