from geopy.distance import geodesic

def forward_sweep(tailEventSet, instancesSet, T, R):
    joinResult = []
    tailEventSet = sorted(tailEventSet, key=lambda x: x.temporal)
    instancesSet = sorted(instancesSet, key=lambda x: x.temporal)

    while tailEventSet and instancesSet:
        p = tailEventSet[0]
        q = instancesSet[0]

        if p.temporal < q.temporal:
            tailEventSet.pop(0)
            for q in instancesSet:
                if p.temporal + T > q.temporal:
                    dist = geodesic((p.spatialY, p.spatialX), (q.spatialY, q.spatialX)).meters
                    if dist <= R:
                        joinResult.append(q)
        else:
            instancesSet.pop(0)

    # Remove duplicates by eventID, maintaining order
    seen = set()
    unique_joinResult = []
    for event in joinResult:
        if event.eventID not in seen:
            unique_joinResult.append(event)
            seen.add(event.eventID)

    return unique_joinResult

def calculate_PI(instSet, event_type_counts):
    if not instSet:
        return 0.0
    event_type = instSet[0].eventType
    totalNumber = event_type_counts.get(event_type, 0)
    return len(instSet) / totalNumber if totalNumber > 0 else 0.0