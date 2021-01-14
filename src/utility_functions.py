import sys
import random
import io

def coords_distance( xy1, xy2 ):
    #using coords_distance for computing distance between two points
    return abs( xy1[0] - xy2[0] ) + abs( xy1[1] - xy2[1] )

class Counter(dict):

    # A counter keeps track of counts for a set of keys. The counter class is an extension of the standard python dictionary type.
    def __getitem__(self, idx):
        self.setdefault(idx, 0)
        return dict.__getitem__(self, idx)

    def totalCount(self):
        #returns the sum of all values in the dict
        return sum(self.values())

    def normalize(self):
        #edits the counter such that the total count of all keys sums to 1.
        total = float(self.totalCount())
        if total == 0: return
        for key in list(self.keys()):
            self[key] = self[key] / total

    def copy(self):
        #returns a copy of the counter
        return Counter(dict.copy(self))

class Queue:

  def __init__(self):
    self.list = []

  def push(self,item):
    self.list.insert(0,item)

  def pop(self):
    return self.list.pop()

  def isEmpty(self):
    return len(self.list) == 0

def normalize(vectorOrCounter):
    #normalize a vector or counter by dividing each value by the sum of all values
    normalizedCounter = Counter()
    if type(vectorOrCounter) == type(normalizedCounter):
        counter = vectorOrCounter
        total = float(counter.totalCount())
        if total == 0: return counter
        for key in list(counter.keys()):
            value = counter[key]
            normalizedCounter[key] = value / total
        return normalizedCounter
    else:
        vector = vectorOrCounter
        s = float(sum(vector))
        if s == 0: return vector
        return [el / s for el in vector]

def sample(distribution, values = None):
    if type(distribution) == Counter:
        items = sorted(distribution.items())
        distribution = [i[1] for i in items]
        values = [i[0] for i in items]
    if sum(distribution) != 1:
        distribution = normalize(distribution)
    choice = random.random()
    i, total= 0, distribution[0]
    while choice > total:
        i += 1
        total += distribution[i]
    return values[i]

def select_from_probability_distribution( distribution ):
    #samples a counter or list of counters
    if type(distribution) == dict or type(distribution) == Counter:
        return sample(distribution)
    r = random.random()
    base = 0.0
    for prob, element in distribution:
        base += prob
        if r <= base: return element

def nearest_cord( coord ):
    #finds the nearest grid point to the position given
    ( current_row, current_col ) = coord

    grid_row = int( current_row + 0.5 )
    grid_col = int( current_col + 0.5 )
    return ( grid_row, grid_col )

def lookup(name, namespace):

    # Get a method or class from any imported module from its name.
    # Usage: lookup(functionName, globals())

    dots = name.count('.')
    if dots > 0:
        moduleName, objName = '.'.join(name.split('.')[:-1]), name.split('.')[-1]
        module = __import__(moduleName)
        return getattr(module, objName)
    else:
        modules = [obj for obj in list(namespace.values()) if str(type(obj)) == "<type 'module'>"]
        options = [getattr(module, name) for module in modules if name in dir(module)]
        options += [obj[1] for obj in list(namespace.items()) if obj[0] == name ]
        if len(options) == 1: return options[0]
        if len(options) > 1: raise Exception('Name conflict for %s')
        raise Exception('%s not found as a method or class' % name)
