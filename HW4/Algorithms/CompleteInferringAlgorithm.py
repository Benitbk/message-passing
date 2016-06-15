from HW4.TransmissionNetwork.Graph import Graph
from HW4.TransmissionNetwork.Vertex import Vertex
from HW4.GraphTraversal.GraphTraversal import GraphTraversal
from decimal import *


class CompleteInferringAlgorithm:
    def __init__(self, graph: Graph, root: Vertex, data):
        self.graph = graph
        self.data = data
        self.root = root
        self.sufficient_statistics = {edge: [0, 0] for edge in self.graph.edges}
        # self.mle = {edge: [0, 0] for edge in self.graph.edges}
        self.graphTraversal = GraphTraversal(graph, root)
        self.graphTraversal.traverse(None)

    def generate_sufficient_statistics(self):
        for data_instance in self.data:
            self.add_data_instance(data_instance)

    def add_data_instance(self, data_instance):
        for vertex in self.graph.vertices:
            if vertex is self.root:
                continue
            parent = self.graphTraversal.parents[vertex]
            edge = self.graph.get_edge(parent, vertex)
            if self.get_data_for_vertex(data_instance, vertex) == self.get_data_for_vertex(data_instance, parent):
                self.sufficient_statistics[edge][0] += 1
            else:
                self.sufficient_statistics[edge][1] += 1

    @staticmethod
    def get_data_for_vertex(data_instance, vertex: Vertex):
        return data_instance[vertex.id]

    def update_graph_flip_probabilities(self):
        for edge in self.sufficient_statistics:
            statistic = self.sufficient_statistics[edge]
            edge.flip_probability = float(statistic[1]) / sum(statistic)

    def calculate_log_likelihood(self):
        getcontext().prec = 1000
        likelihood = Decimal(1)
        for data_instance in self.data:
            likelihood *= Decimal(self.calculate_data_instance_likelihood(data_instance))
            # print(likelihood)
            # print(likelihood.ln())
        return float(likelihood.ln())

    def calculate_data_instance_likelihood(self, data_instance):
        data_instance_likelihood = 0.5
        for vertex in self.graph.vertices:
            if vertex is self.root:
                continue
            parent = self.graphTraversal.parents[vertex]
            edge = self.graph.get_edge(parent, vertex)
            if self.get_data_for_vertex(data_instance, vertex) == self.get_data_for_vertex(data_instance, parent):
                data_instance_likelihood *= 1 - edge.flip_probability
            else:
                data_instance_likelihood *= edge.flip_probability
        return data_instance_likelihood
    #
    # def calculate_likelihood(self):
    #     getcontext().prec = 1000
    #     likelihood = Decimal(1)
    #     for edge in self.sufficient_statistics:
    #         statistic = self.sufficient_statistics[edge]
    #         likelihood *= Decimal(Decimal(1 - edge.flip_probability) ** Decimal(statistic[0]))
    #         likelihood *= Decimal(Decimal(edge.flip_probability) ** Decimal(statistic[1]))
    #     return float(likelihood.ln())

    def print_result(self):
        s = ""
        s += ('\t'.join(["{0:.3f}".format(edge.flip_probability) for edge in self.graph.edges]))
        s += "\t%s" % self.calculate_log_likelihood()
        print(s)


