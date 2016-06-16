from enum import Enum

from HW3.TransmissionNetwork.Graph import Graph
from HW3.TransmissionNetwork.Vertex import Vertex
from HW3.TransmissionNetwork.Edge import Edge
from HW3.Utils import VectorUtils


class MessagePassingAlgorithm:
    def __init__(self, graph: Graph, root: Vertex, root_probability):
        self.graph = graph
        self.root = root
        self.root_probability = root_probability
        self.took_care_of_root_probability = False
        self.phi = {vertex: self.compute_phi(vertex) for vertex in self.graph.vertices}
        self.phi_matrix = {edge: self.compute_phi_matrix(edge) for edge in self.graph.edges}
        self.collect_messages = {edge: [0, 0] for edge in self.graph.edges}
        self.distribute_messages = {edge: [0, 0] for edge in self.graph.edges}
        self.vertex_status = {vertex: VertexStatus.new for vertex in self.graph.vertices}
        self.marginals = {vertex: [1, 1] for vertex in self.graph.vertices}

    @staticmethod
    def compute_phi(vertex: Vertex):
        return [1, 1] if vertex.observed_value is None else ([1, 0] if vertex.observed_value is 0 else [0, 1])

    def compute_marginals(self):
        self.collect(self.root)
        self.vertex_status = {vertex: VertexStatus.new for vertex in self.graph.vertices}
        self.distribute(self.root)

    def collect(self, vertex: Vertex) -> float:
        self.vertex_status[vertex] = VertexStatus.in_progress
        if not self.is_vertex_leaf(vertex):
            for child_vertex in self.get_vertex_children(vertex):
                child_edge = self.graph.get_edge(child_vertex, vertex)
                self.collect_messages[child_edge] = self.collect(child_vertex)
                self.phi[vertex] = VectorUtils.multiply_vectors(self.phi[vertex],
                                                                self.collect_messages[child_edge])
        self.vertex_status[vertex] = VertexStatus.finished
        if vertex is self.root:
            return
        else:
            return self.generate_collect_message(vertex)

    def generate_collect_message(self, vertex: Vertex):
        parent_vertex = self.get_vertex_parent(vertex)
        parent_edge = self.graph.get_edge(vertex, parent_vertex)
        result = [0, 0]
        for i in [0, 1]:
            result[i] = self.phi_matrix[parent_edge][i][0] * self.phi[vertex][0] + \
                        self.phi_matrix[parent_edge][i][1] * self.phi[vertex][1]
        return result

    def distribute(self, vertex: Vertex):
        self.vertex_status[vertex] = VertexStatus.in_progress
        if vertex is self.root:
            self.marginals[vertex] = self.phi[vertex]
        else:
            vertex_parent = self.get_vertex_parent(vertex)
            edge_parent = self.graph.get_edge(vertex, vertex_parent)
            for i in [0, 1]:
                self.marginals[vertex][i] = self.phi[vertex][i] * self.distribute_messages[edge_parent][i]
        if not self.is_vertex_leaf(vertex):
            for child_vertex in self.get_vertex_children(vertex):
                child_edge = self.graph.get_edge(child_vertex, vertex)
                self.calculate_distribute_message(vertex, child_edge)
                # recursion on children
                self.distribute(child_vertex)
        self.vertex_status[vertex] = VertexStatus.finished

    def get_vertex_children(self, vertex: Vertex):
        return [neighbour_vertex for neighbour_vertex in self.graph.get_neighbour_vertices(vertex)
                if not self.vertex_status[neighbour_vertex] is VertexStatus.in_progress]

    def get_vertex_parent(self, vertex: Vertex) -> Vertex:
        neighbours = self.graph.get_neighbour_vertices(vertex)
        for neighbour in neighbours:
            if self.vertex_status[neighbour] is VertexStatus.in_progress:
                return neighbour

    def is_vertex_leaf(self, vertex: Vertex):
        return self.graph.is_leaf(vertex) and len(self.get_vertex_children(vertex)) is 0

    # sum of multiplication between the phi and the marginal of father
    def calculate_distribute_message(self, vertex: Vertex, edge: Edge):
        for i in [0, 1]:
            self.distribute_messages[edge][i] = 0
            if self.collect_messages[edge][0] != 0:
                self.distribute_messages[edge][i] += (self.phi_matrix[edge][0][i] * self.marginals[vertex][0]) / self.collect_messages[edge][0]
            if self.collect_messages[edge][1] != 0:
                self.distribute_messages[edge][i] += (self.phi_matrix[edge][1][i] * self.marginals[vertex][1])/self.collect_messages[edge][1]

    @staticmethod
    def generate_transmission_distribution_matrix(edge: Edge):
        return [[1 - edge.flip_probability, edge.flip_probability],
                [edge.flip_probability, 1 - edge.flip_probability]]

    def compute_phi_matrix(self, edge):
        # for one of the edges that interacts with the root, multiply by root probability
        if (edge.source is self.root or edge.destination is self.root) and not self.took_care_of_root_probability:
            self.took_care_of_root_probability = True
            return [[(1 - edge.flip_probability) * self.root_probability[0],
                     edge.flip_probability * self.root_probability[1]],
                    [edge.flip_probability * self.root_probability[0],
                     (1 - edge.flip_probability) * self.root_probability[1]]]
        else:
            return self.generate_transmission_distribution_matrix(edge)

    def print_result(self):
        for vertex in self.graph.vertices:
            if vertex.observed_value is None:
                normalized_marginal = [self.marginals[vertex][0] / sum(self.marginals[vertex]),
                                       self.marginals[vertex][1] / sum(self.marginals[vertex])]
                print("P(%s) = %s. (Normalized: %s)" % (vertex, self.marginals[vertex], normalized_marginal))
        print("P(XA) = %s" % sum(self.marginals[self.root]))

    def get_likelihood(self):
        return sum(self.marginals[self.root])
class VertexStatus(Enum):
    new = 1
    in_progress = 2
    finished = 3
