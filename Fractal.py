import random
import numpy as np

class fragment:
    """
    A class to implement the basic idea of a fragment.

    @members:
    peak - yval that the fractal ends at (default: 1)
    valley - yval that the fractal begins at (default: 0)
    num - number of points in the fractal between start and end (default: 2)

    """
    def __init__(self, peak = 1, valley = 0, num = 2):
        self.peak = peak
        self.valley = valley
        self.num = num
        self.create_hinges()
        
    def create_hinges(self):
        """
        create_hinges: A method to construct a new fragment
        @Params: None
        @Returns: None
        """
        self.hinges = list()
        self.hinges.append((0.,0.))
        for i in range(1, self.num + 1):
            self.hinges.append((random.uniform(self.hinges[i - 1][0], 1), random.uniform(self.valley, self.peak)))
            
        self.hinges.append((1.,1.))
        
    def __str__(self):
        return str(self.hinges)
    
    
    def compute_iteration(self, fragment_list=[]):
        """
        compute_iteration: A method to compute an iteration of the fractal.

        @Params: fragment_list (optional) - a list of fragments to use when constructing an iteration. If not provided a list will be generated automatically.
        @Returns: None
        """
        if (len(fragment_list) == 0):
            for i in range(self.num):
                fragment_list.append(fragment(num=self.num))
        
        for i in range(len(self.hinges) - 2, -1, -1):
            frag = random.choice(fragment_list)
            frag_x_range = frag.hinges[-1][0] - frag.hinges[0][0]
            frag_y_range = frag.hinges[-1][1] - frag.hinges[0][1]

            if (frag_x_range == 0 or frag_y_range == 0):
                print('Fragment is undefined')
                return
            
            init_x, init_y = self.hinges[i]
            
            component_x_range = self.hinges[i + 1][0] - init_x
            component_y_range = self.hinges[i + 1][1] - init_y
            
            x_scale = component_x_range / frag_x_range
            y_scale = component_y_range / frag_y_range
            
            for j in range(frag.num):
                compute_x = frag.hinges[-2-j][0] * x_scale
                compute_y = frag.hinges[-2-j][1] * y_scale
                
                self.hinges.insert(i + 1, \
                                   (init_x + compute_x, \
                                   init_y + compute_y) \
                                  )
    
    # def plot(self):
    #     x_vals = [hinge[0] for hinge in self.hinges]
    #     y_vals = [hinge[1] for hinge in self.hinges]
    #     plt.plot(x_vals, y_vals)
        
    def xy_lists(self):
        """
        xy_lists - a utility function that returns a list containing two tuples. The first is the xvals of points along the fractal and the second is the yvals. This is nice for graphing.
        
        @returns: list
        """
        return list(zip(*self.hinges))
        
    def compute_deltas(self):
        """
        compute_deltas - function that will return list of changes between points as a percent.

        @returns: list
        """
        deltas = list()
        for i in range(1, len(self.hinges)):
            if (self.hinges[i-1][1] != 0):
                deltas.append(self.hinges[i][1]/self.hinges[i-1][1])
            
        return deltas

class fragment_uniform_x(fragment):
    """
    A class that implements a fragment. For this variety the distance between points is uniform along the x direction.
    """
    def create_hinges(self):
        self.hinges = list()
        x_vals = np.linspace(0, 1, self.num + 2)
        self.hinges.append((x_vals[0], 0.))
        for i in range(1, self.num + 1):
            self.hinges.append((x_vals[i], random.uniform(self.valley, self.peak)))
            
        self.hinges.append((x_vals[-1], 1.))

class fragment_tame(fragment):
    """
    A class that implements a fragment. For this veriety the points are unifromly spaced along the x direction and are gauranteed to fall within a certain range along the y direction. This version contols volatility.
    """
    def create_hinges(self):
        self.hinges = list()
        x_vals = np.linspace(0, 1, self.num + 2)
        self.hinges.append((x_vals[0], 0.))
        for i in range(1, self.num + 1):
            self.hinges.append( \
                ( \
                 x_vals[i], \
                 random.uniform( \
                                max(self.valley, x_vals[i - 1]), \
                                min(self.peak, x_vals[i + 1]) \
                               )\
                ) \
            )
            
        self.hinges.append((x_vals[-1], 1.))