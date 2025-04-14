
import types




class EC_Datas_base:
    """ Reads data from a TDMS file in the format of EC4 DAQ.

    When creating an opject the file path must be given.
     
    """
    def __init__(self,*args, **kwargs):
        
        self.datas = []
        
        #############################################################################
    
    def __setitem__(self, item_index:int, new_data):
        if not isinstance(item_index, int):
            raise TypeError("key must be an integer")
        self.datas[item_index] = new_data
    
    def __getitem__(self, item_index:slice | int): 

        if isinstance(item_index, slice):
            step = 1
            start = 0
            stop = len(self.datas)
            if item_index.step:
                step =  item_index.step
            if item_index.start:
                start = item_index.start
            if item_index.stop:
                stop = item_index.stop    
            return [self.datas[i] for i in range(start, stop, step)  ]
        else:
            return self.datas[item_index] 
    
    def __len__(self):
        """Return the number of items in the list."""
        return len(self.datas)
    
    #### basic functions.
    
    def pop(self,index):
        """Remove and return item at index (default last).

        Raises IndexError if list is empty or index is out of range."""
        self.datas.pop(index)
        
    def append(self,other):
        """Append object to the end of the list.
        """
        self.datas.append(other)
        
        
    def _check_paths(self,paths):
        if paths is not None:
            # paths = args[0]
            
            if isinstance(paths,types.GeneratorType):
                #generates a pathlist from a generator object.
                path_list = [p for p in paths]
            elif not isinstance(paths,list ):
                path_list = [paths]
            else:
                path_list = paths
            
        return path_list
            #print(index)
    
    
def check_paths(paths):
    if paths is not None:
        # paths = args[0]
        
        if isinstance(paths,types.GeneratorType):
            #generates a pathlist from a generator object.
            path_list = [p for p in paths]
        elif not isinstance(paths,list ):
            path_list = [paths]
        else:
            path_list = paths
        
    return path_list
        #print(index)