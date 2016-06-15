from decimal import *
from copy import deepcopy
from math import log
from HW4.TransmissionNetwork.Graph import Graph
from HW4.TransmissionNetwork.Vertex import Vertex
from HW4.Algorithms.CompleteInferringAlgorithm import CompleteInferringAlgorithm
from HW3.Algorithm.MostProbableAssignmentAlgorithm import MostProbableAssignmentAlgorithm
from HW3.Algorithm.MessagePassingAlgorithm import MessagePassingAlgorithm


class MaximumProbabilityInferenceAlgorithm:
    def __init__(self, graph: Graph, root: Vertex, data, observed_variables):
        self.graph = graph
        self.data = data
        self.root = root
        self.observed_variables = observed_variables
        self.hidden_vertices = [vertex for vertex in self.graph.vertices if vertex.name not in self.observed_variables]
        self.observed_vertices = [vertex for vertex in self.graph.vertices if vertex.name in self.observed_variables]
        self.x1 = self.graph.get_vertex_by_id(0)
        self.x2 = self.graph.get_vertex_by_id(1)
        self.x3 = self.graph.get_vertex_by_id(2)
        self.x4 = self.graph.get_vertex_by_id(3)
        self.x5 = self.graph.get_vertex_by_id(4)
        self.x6 = self.graph.get_vertex_by_id(5)
        self.x7 = self.graph.get_vertex_by_id(6)
        self.x8 = self.graph.get_vertex_by_id(7)
        self.x9 = self.graph.get_vertex_by_id(8)
        self.x10 = self.graph.get_vertex_by_id(9)

    def start(self, initial_parameters):
        current_parameters = initial_parameters
        previous_log_prob = 0
        getcontext().prec = 1000
        while True:
            complete_data = []
            s = ""
            self.update_graph_parameters(current_parameters)
            log_probability = 0
            log_likelihood = 0
            for data_instance in self.data:
                self.reset_hidden_variables()
                self.update_graph_observed_variables(data_instance)
                m_algorithm = MessagePassingAlgorithm(self.graph, self.root, [0.5, 0.5])
                m_algorithm.compute_marginals()
                log_likelihood += log(m_algorithm.get_likelihood())
                mpa_algorithm = MostProbableAssignmentAlgorithm(self.graph, self.root, [0.5, 0.5])
                mpa_algorithm.compute_most_probable_assignment()

                self.update_graph_hidden_variables(mpa_algorithm.most_probable_assignment)
                log_probability += log(mpa_algorithm.get_likelihood())
                complete_data.append([vertex.observed_value for vertex in self.graph.vertices])

            ci_algorithm = CompleteInferringAlgorithm(self.graph, self.root, complete_data)
            ci_algorithm.generate_sufficient_statistics()
            s += '\t'.join([str(edge.flip_probability) for edge in self.get_ordered_edges()])
            s += '\t%s' % float(log_probability)
            s += '\t%s' % float(log_likelihood)

            print(s)
            if abs(log_probability - previous_log_prob) < 0.001:
                break
            previous_log_prob = log_probability
            ci_algorithm.update_graph_flip_probabilities()
            current_parameters = []
            for edge in self.get_ordered_edges():
                current_parameters.append(edge.flip_probability)

    def update_graph_observed_variables(self, data):
        for index, observed_vertex in enumerate(self.observed_vertices):
            observed_vertex.observed_value = int(data[index])

    def update_graph_hidden_variables(self, most_probable_assignment):
        for hidden_vertex in self.hidden_vertices:
            hidden_vertex.observed_value = int(most_probable_assignment[hidden_vertex][0])

    def reset_hidden_variables(self):
        for hidden_vertex in self.hidden_vertices:
            hidden_vertex.observed_value = None

    def update_graph_parameters(self, parameters):
        for i, edge in enumerate(self.get_ordered_edges()):
            edge.flip_probability = parameters[i]

    def get_ordered_edges(self):
        return [self.graph.get_edge(self.x1, self.x2),
                self.graph.get_edge(self.x2, self.x3),
                self.graph.get_edge(self.x2, self.x4),
                self.graph.get_edge(self.x1, self.x5),
                self.graph.get_edge(self.x5, self.x6),
                self.graph.get_edge(self.x5, self.x7),
                self.graph.get_edge(self.x1, self.x8),
                self.graph.get_edge(self.x8, self.x9),
                self.graph.get_edge(self.x8, self.x10)]