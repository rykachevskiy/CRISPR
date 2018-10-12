
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm_notebook

import pickle


# In[2]:


class Component:
    def __init__(self):
        self.chain = []
    
    def add_edge(self, edge):
        if len(self.chain) == 0:
            self.chain.append(edge[0])
            self.chain.append(edge[1])
            return True
        elif edge[0] == self.chain[-1]:
            self.chain.append(edge[1])
            return True
        elif edge[1] == self.chain[0]:
            self.chain.insert(0, edge[0])
            return True
        else:
            return False
        
        
    def allow_edge(self, edge):
        if len(self.chain) == 0:
            return True
        elif not edge[0] in self.chain[:-1] and not edge[1] in self.chain[1:]             and not (edge[0] == self.chain[-1] and edge[1] == self.chain[0]):
            return True
        else:
            return False
    
    def require_edge(self, edge):
        if not self.allow_edge(edge):
            return False
        if edge[0] == self.chain[-1]:
            return True
        if edge[1] == self.chain[0]:
            return True
        
    def merge(self, component):
        if component.chain[0] == self.chain[-1]:
            self.chain.extend(component.chain[1:])
            return True
        elif component.chain[-1] == self.chain[0]:
            new_chain = component.chain
            new_chain.extend(self.chain[1:])
            self.chain = new_chain
            return True
        else:
            return False
        
    def __str__(self):
        return str(self.chain)
    
    def __repr__(self):
        return str(self.chain)



def next_edge(graph, components, name = 0):
    #name = 0
    #done = False
    for argmax in graph.flatten().argsort()[::-1]:
        edge = (argmax // graph.shape[0], argmax % graph.shape[0])
        
        #print(edge, len(components))
        if len(components) == 0:
            c = Component()
            c.add_edge(edge)
            components[name] = c
            name += 1
            #break
        else:
            if all([comp.allow_edge(edge) for comp in components.values()]):
                require_names = [name for name in components if components[name].require_edge(edge)]
                #print("rn", require_names)
                if len(require_names) == 0:
                    c = Component()
                    c.add_edge(edge)
                    components[name] = c
                    name += 1
                    #break
                elif len(require_names) == 1:
                    components[require_names[0]].add_edge(edge)
                    #break
                elif len(require_names) == 2:
                    components[require_names[0]].add_edge(edge)
                    components[require_names[0]].merge(components[require_names[1]])
                    components.pop(require_names[1])
                    #break
    return name


