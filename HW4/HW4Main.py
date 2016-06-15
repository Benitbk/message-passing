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
    initial_parameters = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.4, 0.4 ]
    initial_parameters = [0.6] * len(graph.vertices)

    algorithm = ExpectationMaximizationAlgorithm(graph, graph.vertices[0],
                                                     parser.data, parser.variables)
    algorithm.start(initial_parameters)

print("finished")
