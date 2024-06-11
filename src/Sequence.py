import math
import difflib

class Event:
    def __init__(self, instance_id, event_type, x_location, y_location, occurrence_time):
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
    def __init__(self, dataset_dict=None, times_dict=None):
        if dataset_dict is None:
            dataset_dict = {}
        self.dataset_dict = dataset_dict
        if times_dict is None:
            times_dict = {}
        self.times_dict = times_dict

    def add_event(self, event: Event):
        if isinstance(event, Event):
            # Update dataset_dict
            if event.event_type not in self.dataset_dict:
                self.dataset_dict[event.event_type] = set()
            self.dataset_dict[event.event_type].add(event)

            # Update times_dict
            if event.event_type not in self.times_dict:
                self.times_dict[event.event_type] = (event.occurrence_time, event.occurrence_time)
            else:
                min_time, max_time = self.times_dict[event.event_type]
                self.times_dict[event.event_type] = \
                    (min(min_time, event.occurrence_time), max(max_time, event.occurrence_time))

    def __getitem__(self, event_type):
        return self.dataset_dict[event_type]

    def get_times(self, event_type):
        return self.times_dict[event_type]

    def __repr__(self):
        report_lines = []
        for event_type, events in self.dataset_dict.items():
            report_lines.append(f"Event Type: {event_type}, Number of Events: {len(events)}")
            for event in events:
                report_lines.append(f"\tEvent ID: {event.instance_id}, Time: {event.occurrence_time}, Location: ({event.x_location}, {event.y_location})")
        report_lines.append("\nTime Ranges:")
        for event_type, times in self.times_dict.items():
            report_lines.append(f"Event Type: {event_type}, Time Range: {times}")
        return "\n".join(report_lines)

class Element:
    def __init__(self, event_type, I : set = None):
        self.event_type = event_type  # Type of the event
        if I == None:
            self.I = set()  # Initial empty set for I
        self.I = I

    def __repr__(self):
        return f"Element(type={self.event_type}, I={self.I})"

    def __eq__(self, other):
        if isinstance(other, Element):
            return (self.event_type == other.event_type)
        return False

class Sequence:
    def __init__(self, elements=None):
        if elements is None:
            self.elements = list()
        self.elements=elements
        self.PI = 0  # PI value for the sequence

    def __len__(self):
        return len(self.elements)

    def __getitem__(self, index):
        return self.elements[index]

    def __eq__(self, other):
        if isinstance(other, Sequence):
            return self.elements == other.elements
        return False

    def add_element(self, element:Element):
        self.elements.append(element)

    def add_element_at_begining(self, element:Element):
        self.elements.insert(0, element)

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

    def is_supersequence_of(self, other):
        # Check if self is a subsequence of other sequence
        event_types = [el.event_type for el in self.elements]
        other_event_types = [el.event_type for el in other.elements]
        s = difflib.SequenceMatcher(None, event_types, other_event_types)
        match = s.find_longest_match(0, len(event_types), 0, len(other_event_types))
        return match.size == len(other_event_types) and match.b == 0

    def is_subsequence_of(self, other):
        # Check if self is a subsequence of other sequence
        event_types = [el.event_type for el in self.elements]
        other_event_types = [el.event_type for el in other.elements]
        s = difflib.SequenceMatcher(None, other_event_types, event_types)
        match = s.find_longest_match(0, len(other_event_types), 0, len(event_types))
        return match.size == len(event_types) and match.b == 0

    def __repr__(self):
        elements_repr = ", ".join(repr(e) for e in self.elements)
        return f"Sequence(elements=[{elements_repr}], PI={self.PI})"

    def __str__(self):
        elements_str = "\n".join(str(e) for e in self.elements)
        return f"Sequence:\n{elements_str}\nPI: {self.PI}"


#%%
