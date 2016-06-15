
class Vertex:
    counter = 0
    def __init__(self, name: str, observed_value: int=None):
        self.name = name
        self.observed_value = observed_value
        self.id = Vertex.counter
        Vertex.counter += 1

    # def __eq__(self, other):
    #     return self.id == other.id

    def __str__(self):
        return self.name

    # def __hash__(self):
    #     return self.id


