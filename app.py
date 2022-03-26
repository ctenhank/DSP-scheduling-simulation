#from metrics.latency_generator import LatencyGenerator, SomeAwesomeSimulator

from component.cluster import Cluster
from component.topology import Topology
from component.vertex import Vertex
from scheduler.rr_scheduler import RoundRobinScheduler
from component.grouping import *
import argparse

def initialize_environment():
    pass

def create_topology():
    pass

def scheduling():
    pass

def start_simulation():
    pass

def wordcount_main():
    global args
    cluster = Cluster(random=True, max_node=args.cluster_max_node, max_rack=args.cluster_max_rack, max_worker=args.cluster_max_worker)
    source = Vertex(args.wc_src_res, args.wc_src_hint, Vertex.TYPE[0], 'source')
    split = Vertex(args.wc_st_res, args.wc_st_hint, Vertex.TYPE[1], "split")
    count = Vertex(args.wc_cnt_res, args.wc_cnt_hint, Vertex.TYPE[1], "count")
    #print(count)
    edge_src2st = shuffle_grouping(source, split)
    edge_st2cnt = shuffle_grouping(split, count)
    edges = []
    edges.extend(edge_src2st)
    edges.extend(edge_st2cnt)
    
    #print(cluster)
    
    topology = Topology(
        name=args.tp_name,
        vertex=[source, split, count],
        edge=edges
        )
    #print(topology)
    scheduler = RoundRobinScheduler()
    scheduler.schedule(topology, cluster)    
    # start simulation

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--simulate-wordcount', action='store_true')
    parser.add_argument('--simulate-star', action='store_true')
    parser.add_argument('--simulate-dfas', action='store_true')
    parser.add_argument('--cluster-max-node', type=int, default=50)
    parser.add_argument('--cluster-max-rack', type=int, default=5)
    parser.add_argument('--cluster-max-worker', type=int, default=5)
    parser.add_argument('--tp-name', type=str, default='topology')
    parser.add_argument('--wc-src-res', type=int, default=24)
    parser.add_argument('--wc-st-res', type=int, default=16)
    parser.add_argument('--wc-cnt-res', type=int, default=10)
    parser.add_argument('--wc-src-hint', type=int, default=5)
    parser.add_argument('--wc-st-hint', type=int, default=8)
    parser.add_argument('--wc-cnt-hint', type=int, default=12)
    args = parser.parse_args()
    
    if args.simulate_wordcount:
        wordcount_main()