from typing import List
import uuid

from dsp_simulation.topology.task_graph import SubTaskGraph
#from dsp_simulation.topology.subtopology import SubTopology

#from dsp_simulation.topology.task import Task
class Worker:
    CNT = 0
    """This class is a process to execute and handle a subtopology of a topology in physical machine.
    It can process only one subtopology per worker.
    """
    def __init__(self, capability):
        #self._id = 'worker-' + str(uuid.uuid1())        
        self._id = 'worker-' + str(Worker.CNT)
        self._cap = capability
        self.assigned = False
        self._graph: SubTaskGraph = None
        Worker.CNT += 1
            
    @property
    def capability(self):
        return self._cap
        
    @property
    def id(self):
       return self._id
    
    @property
    def graph(self):
        return self._graph
        
    def assign(self, graph: SubTaskGraph):
       self.assigned = True
       self._graph = graph
    
    def deassign(self):
        self.assigned = False
        self._graph = None