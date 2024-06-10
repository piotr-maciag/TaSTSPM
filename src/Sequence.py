import math

class Event:
    def __init__(self, event_type, occurrence_time, x_location, y_location, instance_id):
        self.event_type = event_type
        self.occurrence_time = occurrence_time
        self.x_location = x_location
        self.y_location = y_location
        self.instance_id = instance_id

    def is_within_spatiotemporal_distance(self, e, R, T):
        # Calculate the spatial distance
        spatial_distance = math.sqrt((self.x_location - e.x_location) ** 2 + (self.y_location - e.y_location) ** 2)

        # Calculate the time difference
        time_difference = e.occurrence_time - self.occurrence_time

        # Check if the spatial distance is within R and time difference is within T
        if spatial_distance <= R and time_difference <= T:
            return True
        return False

class Dataset:
    def __int__(self):
        self.dataset_dict = dict()

    def __init__(self, dataset_dict):
        self.dataset_dict = dataset_dict

    def add_event(self, event):
        if isinstance(event, Event):
            if not event.event_type in self.dataset_dict:
                self.dataset_dict[event.event_type] = set()
            self.dataset_dict[event.event_type].add(event)

    def get_istances(self,event_type):
        return self.dataset_dict[event_type]

class Element:
    def __init__(self, event_type, T_min = 0, T_max = 0):
        self.event_type = event_type  # Type of the event
        self.T_min = T_min  # Minimum time of the event type
        self.T_max = T_max  # Maximum time of the event type
        self.I = set()  # Initial empty set for I

    def __repr__(self):
        return f"Event(type={self.event_type}, T_min={self.T_min}, T_max={self.T_max}, I={self.I})"

    def __eq__(self, other):
        if isinstance(other, Element):
            return (self.event_type == other.event_type and
                    self.T_min == other.T_min and
                    self.T_max == other.T_max)
        return False

class Sequence:
    def __init__(self, elements):
        self.elements = elements
        self.PI = 0  # PI value for the sequence

    def __len__(self):
        return len(self.elements)

    def __getitem__(self, index):
        return self.elements[index]

    def __eq__(self, other):
        if isinstance(other, Sequence):
            return self.elements == other.elements
        return False

    def calculate_PI(self, PR_func, R, T):
        self.PI = 0
        for i in range(1, len(self.elements)):
            self.elements[i].I = self.calculate_I(self.elements[i], i, R, T)
            self.PI = min(self.PI, PR_func(self, i))
        pass

    def calculate_I(self, index, D, R, T):
        if index == 0:
            self.elements[index].I = D.get_instances(self.elements[index].event_type)
        else:
            neighborhoods = [self.calculate_neighborhood(event, index, D, R, T) for event in self.events[index-1]]
            merged_neighborhood = set().union(*neighborhoods)
            self.elements[index].I = merged_neighborhood
        pass

    def calculate_neighborhood(self, event, index, D, R, T):
        return {e for e in D.get_instances(self.elements[index].event_type)
                if event.is_within_spatiotemporal_distance(e, R, T)}

    def is_subsequence_of(self, other):
        # Check if self is a subsequence of other sequence
        return all()

    def __repr__(self):
        return f"Sequence(event_types={self.elements.event_types}, PI={self.PI})"

