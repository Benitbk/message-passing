from TransmissionNetwork.Graph import Graph
from TransmissionNetwork.Edge import Edge
from TransmissionNetwork.Vertex import Vertex

def get_transmission_distribution(flip_probability):
    return {0 : flip_probability}


def main():
    vertices = []
    for i in range(0, 10):
        vertices.append(Vertex("X" + str(i + 1)))


    # vertices = [Vertex("X1"), Vertex("X2"), Vertex("X3"), Vertex("X4"), Vertex("X5"),
    #             Vertex("X6"), Vertex("X7"), Vertex("X8"), Vertex("X9"), Vertex("X10")]

    edges = [Edge(vertices[0], vertices[1], 0.1),
             Edge(vertices[1], vertices[2], 0.1),
             Edge(vertices[1], vertices[3], 0.2),
             Edge(vertices[0], vertices[4], 0.1),
             Edge(vertices[4], vertices[5], 0.1),
             Edge(vertices[4], vertices[6], 0.4),
             Edge(vertices[0], vertices[7], 0.1),
             Edge(vertices[7], vertices[8], 0.5),
             Edge(vertices[7], vertices[9], 0.3)]
    graph = Graph(vertices, edges)
    # for v in graph.vertices:
    #     print("Vertex: %s is a leaf: %s" % (v.name, graph.is_leaf(v)))

    # for v in graph.vertices:
    #     edges = graph.get_neighbour_edges(v)
    #     print("Vertex: %s has edges: %s" % (v.name, ','.join([str(e) for e in edges])))

    for v in graph.vertices:
        vertices = graph.get_neighbour_vertices(v)
        print("Vertex: %s has edges: %s" % (v.name, ','.join([str(e) for e in vertices])))
main()

