

class step_time_range():
    """Class to get the time range of a step.
    """
    def __init__(self, *args, **kwargs):
    
        self.t = kwargs.get("t", "last")
        self.dt = kwargs.get("dt",0.0)
        self.min = kwargs.get("t_min", None)
        self.max = kwargs.get("t_max", None)
        
        if self.max and self.min is None:
            print("Warning: t_max is set but t_min is not set. Setting min to 0") 
            self.min = 0.0
        if self.min and self.max is None:
            print("Warning: t_min is set but t_max is not set.") 
            self.t = "last"
        if self.max is not None and self.min is not None:
            self.t = (self.max+self.min)/2.0
            self.dt = abs(self.max-self.min)
        if len(args) > 0:
            if not isinstance(args[0], list):
                datas = [args[0]]
            else:
                datas = args[0]
            if isinstance(self.t, str):
                if self.t == "end" or self.t == "last":
                    self.t = max([x.Time[-1] for x in datas])-self.dt/2.0
            self.min =  max( self.t - self.dt/2.0,0)
            self.max =  min(self.t + self.dt/2.0,datas[0].Time[-1])
            
