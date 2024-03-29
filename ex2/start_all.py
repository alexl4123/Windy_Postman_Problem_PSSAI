from src.graph_data_structs import * 
from src.parse_input_file import parse_input_file

from src.metasearch_init_procedure import *
from src.metasearch_common_procedures import *
from src.load_solution import loadAndParseSolution

from start_hill_climber import hill_climber
from start_random_init_hill_climber import randomized_hill_climber
from start_vdns import vdns
from start_evolutionary_algorithm import evolutionary_algorithm
from start_tabu_search import tabu_search   
from start_simmulated_annealing import simmulated_annealing

traceMode = True
maxTime = 60
verbose = False

# Parse input file (file from args) - only needs to be done once
graph = parse_input_file()
inits = generalInitialization(graph)

#hill_climber(graph, inits, maxTime = maxTime, traceMode = traceMode, verbose = verbose)
#randomized_hill_climber(graph, inits, maxTime = maxTime, traceMode = traceMode, verbose = verbose)
#vdns(graph, inits, maxTime = maxTime, traceMode = traceMode, verbose = verbose)
#evolutionary_algorithm(graph, inits, maxTime = maxTime, traceMode = traceMode, verbose = verbose)
#tabu_search(graph, inits, maxTime = maxTime, traceMode = traceMode, verbose = verbose)
simmulated_annealing(graph, inits, maxTime = maxTime, traceMode = traceMode, verbose = verbose)
