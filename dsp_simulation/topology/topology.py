import uuid

from typing import Dict, List, Tuple
from dsp_simulation.simulator.workload import *
from dsp_simulation.topology.task_graph import TaskGraph
from dsp_simulation.topology.vertex import OperatorVertex, SinkVertex, SourceVertex, Vertex

    
class Topology:
    """Acyclic graph consisting of logical operators
    TODO:
        1. Topology가 Subgraph로 분리됐지만 다른 Worker에 할당된 Subgrpah의 Task와 통신해야 하는 경우
    
    """

    CONNECTION = ['shuffle', 'all', 'global']
    PREDEFINED = ['wc']
    WORKLOAD_DISTRIBUTION = ['binomial', 'normal', 'uniform', 'constant']

    def __init__(self, name, input_rate_dist:str='twostep', step=900):
        f"""_summary_

        Args:
            name (_type_): Topology name
            predefined (_type_, optional): predefined topology, {Topology.PREDEFINED}.
            conf_distribution (_type_, optional): the path of distributions for each operators
        """
        if name == None:
            self._id  = 'topology-' + str(uuid.uuid1())
        else:
            self._id = name
            
        self._source: List[SourceVertex] = []
        self._sink: List[SinkVertex] = []
        self._operator: List[OperatorVertex] = []
        self._edge: Dict[Tuple[str, str], str] = {}
        self._taskgraph: TaskGraph = []
        self._graph = { 'root': [] }
        self._workload_dist_type = input_rate_dist
        self._workload_dist = self._update_workload(self._workload_dist_type, step)
        self.order = None
        
    def _update_workload(self, dist, step):
        ret = []
        if dist == 'binomial':
            ret = binomal_distribution(step)
        elif dist == 'normal':
            ret = normal_distribution(step)
        elif dist == 'uniform':
            ret = uniform_distribution(step)      
        elif dist == 'constant':
            ret = [1 for _ in range(step+1)]
        elif dist == 'twostep':
            for i in range(step+1):
                if (i < step / 2):
                    ret.append(0.2)
                else:
                    ret.append(1)
                
        return ret 
        
    @property
    def id(self):
        return self._id
    
    @property
    def source(self):
        return self._source

    @property
    def sink(self):
        return self._sink
    
    @property
    def operator(self):
        return self._operator
    
    @property
    def edge(self):
        return self._edge

    @property
    def taskgraph(self):
        return self._taskgraph
    
    @property
    def graph(self):
        return self._graph
    
    @property
    def profiler(self):
        return self._profiler
    
    def __str__(self):
        ret = '=' * 25 + 'Topology Info' + '='* 25 + '\n'
        #ret += 'Vertex Info: id, capability, type, parallelism\n'
        for vertex in self._source:
           ret += str(vertex) + '\n'
        for vertex in self._operator:
           ret += str(vertex) + '\n'
        for vertex in self._sink:
           ret += str(vertex) + '\n'
        #ret += f'Edge from vertex to vertex:\n {self.__edge}\n'

        for edge in self._edge:
            ret += f'({edge[0]}, {edge[1]}): {self._edge[edge]}'
        ret += '=' * 50 + '\n'
        return ret
        
            
    def _include_this_vertex(self, vertex: Vertex):
        for v in self._source:
            if v.id == vertex.id:
                return True
            
        for v in self._operator:
            if v.id == vertex.id:
                return True

        for v in self._sink:
            if v.id == vertex.id:
                return True
        
        return False
    
    def is_source(self, vertex_id: str):
        for v in self._source:
            if v.id == vertex_id:
                return True
        return False
    
    def is_sink(self, vertex_id: str):
        for v in self._sink:
            if v.id == vertex_id:
                return True
        return False
    
    def is_operator(self, vertex_id: str):
        for v in self._operator:
            if v.id == vertex_id:
                return True
        return False
        
            
    def add_source(self, source: SourceVertex):
        if self._include_this_vertex(source):
            print(f'Warn: Already existed vertex: {source}: Ignored this method call')
            return

        if type(source) is not SourceVertex:
            print(f'Error: You should add {source.__class__}, not {source.__class__}')
            exit(1)
            
        source.update_rate_distribution(self._workload_dist)
        self._source.append(source)
        
        self._graph['root'].append(source.id)
        self._graph[source.id] = []

    def add_sink(self, sink: SinkVertex):
        if self._include_this_vertex(sink):
            print(f'Warn: Already existed vertex: {sink}: Ignored this method call')
            return

        if type(sink) is not SinkVertex:
            print(f'Error: You should add {sink.__class__}, not {sink.__class__}')
            exit(1)
        
        self._sink.append(sink)
    
    def add_operator(self, operator: OperatorVertex):
        if self._include_this_vertex(operator):
            print(f'Warn: Already existed vertex: {operator}: Ignored this method call')
            return

        if type(operator) is not OperatorVertex:
            print(f'Error: You should add {operator.__class__}, not {operator.__class__}')
            exit(1)
        
        self._operator.append(operator)
        
    def connect(self, source:Vertex, target:Vertex, connect_type: str):
        f"""_summary_

        Args:
            source (Vertex): _description_
            target (OperatorVertex): _description_
            connect_type (str): {Topology.CONNECTION}
        """
        if type(target) is SourceVertex:
            print(f'{target.__class__} cannot be set as target')
            exit(1)

        if type(source) is SinkVertex:
            print(f'{target.__class__} cannot be set as source')
            exit(1)
            
        if connect_type not in Topology.CONNECTION:
            print(f'No such connection type: type one of {Topology.CONNECTION}')
            exit(1)

        if type(source) is SourceVertex:
            print('If the class of source is SourceVertex, the connect type is automatically set as ShuffleGrouping')
            connect_type = 'shuffle'
        
        if type(target) is SinkVertex:
            print('If the class of target is SinkVertex, the connect type is automatically set as GlobalGrouping')            
            connect_type = 'global'
        
        if source.id not in self._graph:
            self._graph[source.id] = []
            
        if target.id not in self._graph:
            self._graph[target.id] = []
        
        self._graph[source.id].append(target.id)
        source.add_outdegree(target)
        if type(target) is not SourceVertex:
            target.add_indegree(source)
            
        #if type(target) is not SinkVertex:
        #    target.add_indegree(source)
        
        edge = (source.id, target.id)
        if edge in self._edge:
            print(f'Already existed {edge}')
            return
        self._edge[edge] = connect_type
        
        
    def get_vertex(self, vertex_id: str):
        for v in self._source:
            if v.id == vertex_id:
                return v
            
        for v in self._operator:
            if v.id == vertex_id:
                return v
            
        return None
    
    def get_target(self, vertex_id: str):
        ret = []
        for edge in self._edge:
            u, v = edge[0], edge[1]
            if u == vertex_id and self.is_operator(v):
                ret.append(v)
        return ret
    
    def _get_vertex_order(self):
        ret = []
        for edge in self._edge:
            ret.append(edge)
        return ret
    
    def get_vertex_order(self):
        pass

    def instantiate(self, max_num_operators):
        self._taskgraph = TaskGraph(self._id, self._source, self._operator, self._sink, self._edge, max_num_operators)
