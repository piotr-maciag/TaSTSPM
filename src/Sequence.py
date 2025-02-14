import math
import difflib
import pandas as pd
from geopy.distance import geodesic
import pandas as pd
from collections import defaultdict



class Event:
    def __init__(self, instance_id, event_type, x_location, y_location, occurrence_time):
        self.event_type = event_type
        self.occurrence_time = occurrence_time
        self.x_location = x_location
        self.y_location = y_location
        self.instance_id = instance_id

    def is_within_backward_spatiotemporal_distance(self, e, R, T, distance_type ='Earth'):

        # Calculate the spatial distance
        if distance_type == 'Earth':
            spatial_distance = self.distanceEarth(e)
        elif distance_type == 'Euclidean':
            spatial_distance = self.distanceEuclidian(e)

        # Calculate the time difference
        time_difference =  self.occurrence_time - e.occurrence_time

        # Check if the spatial distance is within R and time difference is within T
        if spatial_distance <= R and self.occurrence_time > e.occurrence_time and time_difference < T:
            return True
        return False

    def is_within_spatiotemporal_distance(self, e, R, T, distance_type ='Earth'):
        # Calculate the spatial distance

        if distance_type == 'Earth':
            spatial_distance = self.distanceEarth(e)
        elif distance_type == 'Euclidean':
            spatial_distance = self.distanceEuclidian(e)

        # Calculate the time difference
        time_difference = e.occurrence_time - self.occurrence_time

        # Check if the spatial distance is within R and time difference is within T
        if spatial_distance <= R and self.occurrence_time < e.occurrence_time and time_difference < T:
            return True
        return False

    def distanceEuclidian(self, e):
        return math.sqrt((self.x_location - e.x_location) ** 2 + (self.y_location - e.y_location) ** 2)

    def distanceEarth(self, e):
        def deg2rad(deg):
            return deg * (math.pi / 180.0)

        earthRadiusKm = 6371.0  # Radius of the Earth in kilometers
        lat1r = deg2rad(self.y_location)
        lon1r = deg2rad(self.x_location)
        lat2r = deg2rad(e.y_location)
        lon2r = deg2rad(e.x_location)
        u = math.sin((lat2r - lat1r) / 2)
        v = math.sin((lon2r - lon1r) / 2)
        return 2.0 * earthRadiusKm * math.asin(math.sqrt(u * u + math.cos(lat1r) * math.cos(lat2r) * v * v)) * 1000

    def __str__(self):
        return (f"Event(ID: {self.instance_id}, Type: {self.event_type}, Time: {self.occurrence_time}, "
                f"Location: ({self.x_location}, {self.y_location}))")


class Dataset:
    def __init__(self, file_path=None):
        self.dataset_dict = defaultdict(list)
        self.times_dict = {}
        if file_path:
            self.load_data(file_path)

    def add_event(self, event):
        if isinstance(event, Event):
            # Update dataset_dict
            self.dataset_dict[event.event_type].append(event)

            # Update times_dict
            if event.event_type not in self.times_dict:
                self.times_dict[event.event_type] = (event.occurrence_time, event.occurrence_time)
            else:
                min_time, max_time = self.times_dict[event.event_type]
                self.times_dict[event.event_type] = (
                    min(min_time, event.occurrence_time), max(max_time, event.occurrence_time)
                )

    def sort_events(self):
        for event_type in self.dataset_dict:
            self.dataset_dict[event_type] = sorted(self.dataset_dict[event_type], key=lambda x: x.occurrence_time)

    def get_sorted_events(self, event_type):
        return self.dataset_dict[event_type]

    def __getitem__(self, event_type):
        return self.get_sorted_events(event_type)

    def get_times(self, event_type):
        return self.times_dict[event_type]

    def __repr__(self):
        report_lines = []
        for event_type, events in self.dataset_dict.items():
            report_lines.append(f"Event Type: {event_type}, Number of Events: {len(events)}")
        for event_type, times in self.times_dict.items():
            report_lines.append(f"Event Type: {event_type}, Time Range: ({times[0]}, {times[1]})")
        return "\n".join(report_lines)

    def load_data(self, file_path):
        print(f"Loading data from {file_path}")

        # Read the comma-separated CSV file
        try:
            df = pd.read_csv(file_path, delimiter=',')
            print(f"Data read successfully: {df.shape[0]} rows")
        except Exception as e:
            print(f"Failed to read data: {e}")
            return

        # Iterate over each row in the DataFrame and create Event instances
        for _, row in df.iterrows():
            event = Event(
                instance_id=row['Instance_ID'],
                event_type=str(row['Event_type']),
                occurrence_time=row['Occurrence_time'],
                x_location=row['Location_X'],
                y_location=row['Location_Y']
            )

            self.add_event(event)

        # Ensure events are sorted by occurrence_time for each event type
        self.sort_events()


class Element:
    def __init__(self, event_type, I : set = None):
        self.event_type = event_type  # Type of the event
        if I == None:
            self.I = set()  # Initial empty set for I
        self.I = I

    def __repr__(self):
        return (f"Element(type={self.event_type}, len(I)={len(self.I)})"
                #f"I_ids={[e.instance_id for e in self.I]})"
                )

    def __eq__(self, other):
        if isinstance(other, Element):
            return (self.event_type == other.event_type)
        return False

    def __hash__(self):
        return hash(self.event_type)




import concurrent.futures

class Sequence:
    def __init__(self, elements=None, event_types=None):
        if elements is not None:
            self.elements = elements
        elif event_types is not None:
            self.elements = [Element(event_type) for event_type in event_types]
        else:
            self.elements = []

        self.PI = 1  # PI value for the sequence

    def __len__(self):
        return len(self.elements)

    def __getitem__(self, index):
        return self.elements[index]

    def __eq__(self, other):
        if isinstance(other, Sequence):
            return self.elements == other.elements
        return False

    def __hash__(self):
        return hash(tuple(self.elements))

    def add_element(self, element: Element):
        self.elements.append(element)

    def add_element_at_beginning(self, element: Element):
        self.elements.insert(0, element)

    def forward_sweep(self, tailEventSet, instancesSet, T, R):
        joinResult = []
        tailEventSet = sorted(tailEventSet, key=lambda x: x.occurrence_time)
        instancesSet = sorted(instancesSet, key=lambda x: x.occurrence_time)

        while tailEventSet and instancesSet:
            p = tailEventSet[0]
            q = instancesSet[0]

            if p.occurrence_time < q.occurrence_time:
                tailEventSet.pop(0)
                for q in instancesSet:
                    if p.occurrence_time + T > q.occurrence_time:
                        dist = geodesic((p.y_location, p.x_location), (q.y_location, q.x_location)).meters
                        if dist <= R:
                            joinResult.append(q)
            else:
                instancesSet.pop(0)

        # Remove duplicates by eventID, maintaining order
        seen = set()
        unique_joinResult = []
        for event in joinResult:
            if event.instance_id not in seen:
                unique_joinResult.append(event)
                seen.add(event.instance_id)

        return unique_joinResult

    def forward_sweep_D(self, tailEventSet, instancesSet, T, R):
        joinResult = []
        tailEventSet = sorted(tailEventSet, key=lambda x: x.occurrence_time)

        while tailEventSet and instancesSet:
            p = tailEventSet[0]
            q = instancesSet[0]

            if p.occurrence_time < q.occurrence_time:
                tailEventSet.pop(0)
                for q in instancesSet:
                    if p.occurrence_time + T > q.occurrence_time:
                        dist = geodesic((p.y_location, p.x_location), (q.y_location, q.x_location)).meters
                        if dist <= R:
                            joinResult.append(q)
                else:
                    instancesSet.pop(0)

        # Remove duplicates by eventID, maintaining order
        seen = set()
        unique_joinResult = []
        for event in joinResult:
            if event.instance_id not in seen:
                unique_joinResult.append(event)
                seen.add(event.instance_id)

        return unique_joinResult

    def calculate_I_sweep(self, index, D, R, T):
        self.elements[index].I = set()
        if index == 0:
            self.elements[index].I = set(D[self.elements[index].event_type])
        else:
            previous_events = list(self.elements[index - 1].I)
            current_events = D[self.elements[index].event_type]
            self.elements[index].I = self.forward_sweep_D(previous_events, current_events, T, R)

    def calculate_PI_sweep(self, PR_func, D, R, T):
        self.PI = 1
        for i in range(len(self.elements)):
            self.calculate_I_sweep(i, D, R, T)
            self.PI = min(self.PI, PR_func(self, i, D))

    def recalculate_I_and_PI_sweep(self, PR_func, index, D, R, T):
        if index == 0:
            self.elements[index].I = D[self.elements[index].event_type]
        else:
            previous_events = list(self.elements[index - 1].I)
            current_events = list(self.elements[index].I)
            self.elements[index].I = self.forward_sweep(previous_events, current_events, T, R)

        self.calculate_PI(PR_func, D, R, T)

    def calculate_I(self, index, D, R, T):
        self.elements[index].I = set()
        if index == 0:
            self.elements[index].I = D[self.elements[index].event_type]
        else:
            neighborhoods = [self.calculate_neighborhood(event, index, D, R, T) for event in self.elements[index - 1].I]
            merged_neighborhood = set().union(*neighborhoods)
            self.elements[index].I = merged_neighborhood

    def calculate_I_backward(self, index, D, R, T):
        self.elements[index].I = set()
        neighborhoods = [self.calculate_neighborhood_backward(event, index, D, R, T) for event in self.elements[index + 1].I]
        merged_neighborhood = set().union(*neighborhoods)
        self.elements[index].I = merged_neighborhood

    def calculate_neighborhood(self, event, index, D, R, T):
        return {e for e in D[self.elements[index].event_type] if event.is_within_spatiotemporal_distance(e, R, T)}

    def calculate_neighborhood_I(self, event, index, R, T):
        return {e for e in self.elements[index].I if event.is_within_spatiotemporal_distance(e, R, T)}

    def calculate_neighborhood_backward(self, event, index, D, R, T):
        return {e for e in D[self.elements[index].event_type] if event.is_within_backward_spatiotemporal_distance(e, R, T)}

    def recalculate_I_and_PI(self, PR, index, D, R, T):
        if index == 0:
            self.elements[index].I = D[self.elements[index].event_type]
        else:
            neighborhoods = [self.calculate_neighborhood_I(event, index, R, T) for event in self.elements[index - 1].I]
            merged_neighborhood = set().union(*neighborhoods)
            self.elements[index].I = merged_neighborhood

        self.calculate_PI(PR, D, R, T)

    def calculate_PI(self, PR_func, D, R, T):
        self.PI = 1
        for i in range(0, len(self.elements)):
            # self.calculate_I(i, D, R, T)
            self.PI = min(self.PI, PR_func(self, i, D))
        pass

    def copy(self):
        s = Sequence(elements=[Element(e.event_type, e.I.copy()) for e in self.elements])
        s.PI = self.PI
        return s

    def is_subsequence_of(self, other):
        # Check if self is a subsequence of other sequence
        event_types = [el.event_type for el in self.elements]
        other_event_types = [el.event_type for el in other.elements]
        s = difflib.SequenceMatcher(None, other_event_types, event_types)
        match = s.find_longest_match(0, len(other_event_types), 0, len(event_types))
        return match.size == len(event_types) and match.b == 0

    def is_supersequence_of(self, other):
        # Check if self is a supersequence of another sequence
        event_types = [el.event_type for el in self.elements]
        other_event_types = [el.event_type for el in other.elements]
        s = difflib.SequenceMatcher(None, event_types, other_event_types)
        match = s.find_longest_match(0, len(event_types), 0, len(other_event_types))
        return match.size == len(other_event_types) and match.b == 0

    def __repr__(self):
        return f"Sequence(elements=[{', '.join(repr(e) for e in self.elements)}], PI={self.PI})"

    def __str__(self):
        str = (' -> '.join(e.event_type for e in self.elements))
        return f"{str}, PI: {self.PI}"

        #%%
