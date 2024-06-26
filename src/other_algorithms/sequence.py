class Sequence:
    def __init__(self):
        self.sequence = []
        self.tailEventSet = []
        self.PI = 1000.0
        self.firstParent = None
        self.secondParent = None
        self.children = []
        self.Cmax = []
        self.RC = []
        self.isClosed = True

    def __repr__(self):
        return f"Sequence(sequence={self.sequence}, PI={self.PI}, isClosed={self.isClosed})"

    def __str__(self):
        event_types = " -> ".join(self.sequence)
        return f"Sequence: [{event_types}] with PI: {self.PI}"