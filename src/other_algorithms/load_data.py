import pandas as pd
from src.other_algorithms.st_point import STPoint

class Dataset:
    def __init__(self, path):
        self.data, self.event_type_counts = self.load_dataset(path)
        self.sortedDataset = self.transform_data()

    def load_dataset(self, path):
        df = pd.read_csv(path)
        dataset = []
        event_type_counts = {}

        for _, row in df.iterrows():
            event = STPoint(
                eventID=row['Instance_ID'],
                eventType=row['Event_type'],
                spatialX=row['Location_X'],
                spatialY=row['Location_Y'],
                temporal=row['Occurrence_time']
            )
            if row['Event_type'] not in event_type_counts:
                event_type_counts[row['Event_type']] = 0
            event_type_counts[row['Event_type']] += 1

            dataset.append(event)

        return dataset, event_type_counts

    def transform_data(self):
        event_dict = {}
        for event in self.data:
            if event.eventType not in event_dict:
                event_dict[event.eventType] = []
            event_dict[event.eventType].append(event)

        sortedDataset = [sorted(events, key=lambda x: x.temporal) for events in event_dict.values()]
        return sortedDataset