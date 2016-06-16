from sys import argv
from HW4.Parser.FileParser import FileParser
from HW4.Tests.GraphGenerator import TransmissionNetwork
from HW4.Algorithms.CompleteInferringAlgorithm import CompleteInferringAlgorithm
from HW4.Algorithms.MaximumProbabilityInferenceAlgorithm import MaximumProbabilityInferenceAlgorithm
from HW4.Algorithms.ExpectationMaximizationAlgorithm import ExpectationMaximizationAlgorithm

if len(argv) != 3:
    raise Exception("Invalid args")
option = argv[1]
parser = FileParser(argv[2])
parser.parse()
graph = TransmissionNetwork().graph
if option is 'C':
    algorithm = CompleteInferringAlgorithm(graph, graph.vertices[0], parser.data)
    algorithm.generate_sufficient_statistics()
    algorithm.update_graph_flip_probabilities()
    algorithm.print_result()

elif option is 'M':
    initial_parameters = [0.6] * len(graph.vertices)
    algorithm = MaximumProbabilityInferenceAlgorithm(graph, graph.vertices[0],
                                                     parser.data, parser.variables)
    algorithm.start(initial_parameters)
elif option is 'E':
    initial_parameters = [0.999, 0.444, 0.527, 0.121, 0.151, 0.507, 0.448, 0.2, 0.2]
    #initial_parameters = [0.6] * len(graph.vertices)
    #initial_parameters = [0.2] * len(graph.vertices)

    algorithm = ExpectationMaximizationAlgorithm(graph, graph.vertices[0],
                                                     parser.data, parser.variables)
    algorithm.start(initial_parameters)

print("finished")
