from .sequence import Sequence
from .utils import forward_sweep

def calculate_PI(instSet, event_type_counts):
    if not instSet:
        return 0.0
    event_type = instSet[0].eventType
    totalNumber = event_type_counts[event_type]
    return len(instSet) / totalNumber if totalNumber > 0 else 0.0

def CST_SPMiner(dataset, theta, T, R, verbose=0):
    SequencesSetSPTree = []
    Length1Seq = []
    Length2Seq = []

    if verbose > 0:
        print("Starting CST_SPMiner Algorithm")

    for data in dataset.sortedDataset:
        seq = Sequence()
        seq.sequence.append(data[0].eventType)
        seq.tailEventSet.append(data)
        seq.PI = 1.0
        Length1Seq.append(seq)

    SequencesSetSPTree.append(Length1Seq)

    if verbose > 1:
        print("Created 1-length sequences")

    for i in range(len(Length1Seq)):
        for j in range(len(Length1Seq)):
            seq = Sequence()
            seq.sequence.append(Length1Seq[i].sequence[0])
            seq.sequence.append(Length1Seq[j].sequence[0])
            I2 = forward_sweep(Length1Seq[i].tailEventSet[0], Length1Seq[j].tailEventSet[0], T, R)

            if I2:
                seq.tailEventSet.append(I2)
                seq.PI = calculate_PI(seq.tailEventSet[-1], dataset.event_type_counts)

                if seq.PI > theta:
                    seq.firstParent = Length1Seq[i]
                    seq.secondParent = Length1Seq[j]
                    seq.firstParent.children.append(seq)
                    Length2Seq.append(seq)

    SequencesSetSPTree.append(Length2Seq)

    if verbose > 1:
        print(f"Created 2-length sequences")

    k = 1
    while SequencesSetSPTree[k]:
        k += 1
        LengthKSeq = gen_and_verify(SequencesSetSPTree[k - 1], dataset, theta, T, R)
        SequencesSetSPTree.append(LengthKSeq)

        if verbose > 1:
            print(f"Created {k+1}-length sequences")

    if verbose > 0:
        print("CST_SPMiner Algorithm Completed")

    return SequencesSetSPTree

def gen_and_verify(SeqVec, dataset, theta, T, R):
    newSeqs = []

    for i in range(len(SeqVec)):
        sl = SeqVec[i].secondParent
        for j in range(len(sl.children)):
            seq = Sequence()

            for l in range(len(SeqVec[i].sequence)):
                seq.sequence.append(SeqVec[i].sequence[l])
            seq.sequence.append(sl.children[j].sequence[-1])

            seq.tailEventSet.append(forward_sweep(SeqVec[i].tailEventSet[-1], sl.children[j].tailEventSet[-1], T, R))

            seq.firstParent = SeqVec[i]
            seq.secondParent = sl.children[j]

            PI = calculate_PI(seq.tailEventSet[-1], dataset.event_type_counts)
            seq.PI = min(PI, SeqVec[i].PI)

            if seq.PI > theta:
                seq.firstParent.children.append(seq)
                if seq.PI == seq.firstParent.PI: seq.firstParent.isClosed = False
                if seq.PI == seq.secondParent.PI: seq.secondParent.isClosed = False
                newSeqs.append(seq)

    return newSeqs

def STBFM(dataset, theta, T, R, verbose=0):
    SequencesSetSPTree = []
    Length1Seq = []
    Length2Seq = []

    if verbose > 0:
        print("Starting STBFM Algorithm")

    for data in dataset.sortedDataset:
        seq = Sequence()
        seq.sequence.append(data[0].eventType)
        seq.tailEventSet.append(data)
        seq.PI = 1.0
        Length1Seq.append(seq)

    SequencesSetSPTree.append(Length1Seq)

    if verbose > 1:
        print("Created 1-length sequences")

    for i in range(len(Length1Seq)):
        for j in range(len(Length1Seq)):
            seq = Sequence()
            seq.sequence.append(Length1Seq[i].sequence[0])
            seq.sequence.append(Length1Seq[j].sequence[0])
            I2 = forward_sweep(Length1Seq[i].tailEventSet[0], Length1Seq[j].tailEventSet[0], T, R)

            if I2:
                seq.tailEventSet.append(I2)
                seq.PI = calculate_PI(seq.tailEventSet[-1], dataset.event_type_counts)

                if seq.PI > theta:
                    seq.firstParent = Length1Seq[i]
                    seq.secondParent = Length1Seq[j]
                    seq.firstParent.children.append(seq)
                    Length2Seq.append(seq)

    SequencesSetSPTree.append(Length2Seq)

    if verbose > 1:
        print(f"Created 2-length sequences")

    k = 1
    while SequencesSetSPTree[k]:
        k += 1
        LengthKSeq = gen_and_verify(SequencesSetSPTree[k - 1], dataset, theta, T, R)
        SequencesSetSPTree.append(LengthKSeq)

        if verbose > 1:
            print(f"Created {k+1}-length sequences")

    if verbose > 0:
        print("STBFM Algorithm Completed")

    return SequencesSetSPTree