import json


class FileHandler():
    def __init__(self):
        super().__init__() 
        
    # def read_file(self, path: str):
    #     try:
    #         list_to_return = []
    #         with open(path, 'r') as f:
    #             list_of_lines = [line for line in f.read().split('\n') if line]
    #         for line in list_of_lines:
    #             numbers = [float(x) for x in line.split()]
    #             list_to_return.append(numbers)
    #         print(*list_to_return, '\n')
    #         return list_to_return
    #     except:
    #         print("Error: cannot read the data from the file with this path:\n")
    #         print("Path: " + str(path))
    #     return None
    
    def write_json_file(self, path: str, data: dict):
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)
            
    def read_json_file(self, path: str):
        with open(path) as f:
            data = json.load(f)
            for attr, v in data.items():
                print('{}: {}'.format(attr, v))
        return data
             
class OptimizedSchedule():
    def __init__(self, data: dict):
                #   list_of_lists_of_times: list, deadline: int, 
                #  list_of_important_indexes: list, time_of_the_start: int):
        super().__init__() 
        self._list_of_lists_of_times = data['T'] # list_of_lists_of_times
        self._deadline = data['V'] # deadline
        self._list_of_important_indexes = data['Indexes'] # list_of_important_indexes
        self._time_of_the_start = data['U'] # time_of_the_start
        self._valid_length_of_list = data['N'] # valid_length_of_list
        
        self.list_of_valid_lists_of_times = \
            self._validate_each_list_of_times(self._list_of_lists_of_times)
        self.the_best_list = self._find_the_best_list(self.list_of_valid_lists_of_times)
        
    def print_the_best_list(self):
        if not self.the_best_list:
            print("there are no any valid lists")
        else:
            print(self.the_best_list) # print(*self.the_best_list, sep='\n')
        
    def _find_the_best_list(self, list_of_valid_lists_of_times: list):
        if list_of_valid_lists_of_times:
            list_of_sum = []
            for i, v in enumerate(list_of_valid_lists_of_times):
                list_of_sum.append(sum(range(len(v))))
                
            index_of_the_best_list = list_of_sum.index(min(list_of_sum))
            return list_of_valid_lists_of_times[index_of_the_best_list]
        return None
        
    def _validate_each_list_of_times(self, list_of_lists_of_times: list):
        raw_list_of_valid_lists_of_times = []
        for i, list_of_times in enumerate(list_of_lists_of_times):
            raw_list_of_valid_lists_of_times.append(self._check_validation(list_of_times))
        list_of_valid_lists_of_times = [i for i in raw_list_of_valid_lists_of_times if i]
        return list_of_valid_lists_of_times
        
    def _check_validation(self, list_of_times: list):
        _sum = self._time_of_the_start
        try:
            if self._list_of_important_indexes:  
                for i in range(0, max(self._list_of_important_indexes)):
                    _sum += list_of_times[i]
            else:  # if _list_of_important_indexes is empty then we compare sum of all elements with the deadline 
                for i in range(0, len(list_of_times)):
                    _sum += list_of_times[i]
            if self._deadline > _sum:
                return list_of_times
        except:
            invalid_input = True
        return None
        
        
if __name__ == "__main__":
    
    # given values
    N = 5 # N is number of items, just the length of the list
    V = 4 # V is deadline, items with important indexes must be processed by this value of time
    K, L = 2, 4 # K and L are two important indexes
    U = 0 # the time of the start
    
    # lists down below are the lists of time of processing each item
    # (each element is the time of processing current item with that index)
    T = [  # list_of_lists_with_times
        [2, 2, 1, 1, 1],
        [1, 1, .5, .5, .5], # this one is the best out of all given samples
        [2, 2, 4, 4, 4],
        [1, 1, 1, .5, .5],
        [1, 2, 2, 2, 2]    
    ]
    
    
    # Main issue: if the sum of elements(until the last important index) more than a deadline value
    #  and there is missing one or more of important elements with indexes K, L (etc)
    #  then the current list is not valid
    
    # Main task: find the shortest time to process all the elements
    #  so there is one list to find: valid list with the minimum sum of all elements
    
    data = {
        'N': N,
        'V': V,
        'Indexes': tuple([K, L]),
        'U': U,
        'T': tuple(T)
    }
    
    # hardcoded input
    # optimized_schedule = OptimizedSchedule([list_1, list_2, list_3, list_4, list_5], V, [K, L], U)
    
    # input from the file
    file_handler = FileHandler()
    
    # T = file_handler.read_file('in.txt')
    # T_1 = file_handler.write_json_file('in.json.txt', [V, [K, L], U, T])
    
    # T = file_handler.write_json_file('in.json.txt',
    #                                     {
    #                                      'N': N,
    #                                      'V': V,
    #                                      'Indexes': tuple([K, L]),
    #                                      'U': U,
    #                                      'T': tuple(T)})
    
    # data = file_handler.read_json_file('in.json.txt')
    
    # optimized_schedule = OptimizedSchedule(T, V, [K, L], U)
    
    optimized_schedule = OptimizedSchedule(data)
    
    # init schedule class to process the given list of lists to get the best valid list of times
    optimized_schedule.print_the_best_list()
    # the best list of times out of all given samples is [1, 1, .5, .5, .5]