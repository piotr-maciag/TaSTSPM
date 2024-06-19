from src.Sequence import *


def tastsp_algorithm(D, F, R, T, theta, stq, distance_type='Earth', verbose=0):
    if verbose > 0:
        print("Starting TaSTSP Algorithm")
        print(f"Parameters: R={R}, T={T}, theta={theta}, distance_type={distance_type}")
        print(f"Number of sequences in stq: {len(stq)}")

    TaSTSPs = set()

    # Apply the first and the third pruning strategies
    for i in range(0, len(stq)):
        s = stq[i]
        if is_subsequence_of_previously_tested_sequence(s, stq, i):
            if verbose > 0:
                print(f"Skipping sequence {i} as it is a subsequence of a previously tested sequence.")
            continue
        if verbose > 1:
            print(f"Calculating I and PI for sequence {s}, Index={i}")

        for j in range(0, len(s)):
            s.calculate_I(j, D, R, T)
            s.PI = min(s.PI, PR(s, j, D))
            if verbose > 2:
                print(f"Sequence {s}, Element {j}: PI={s.PI}")
            if s.PI < theta:
                if verbose > 0:
                    print(f"Sequence {s} pruned due to PI < theta")
                return set()  # No TaSTSPs matching stq and theta

    # Apply the second pruning strategy
    for i in range(len(stq) - 1):
        if stq[i][-1].I == set():
            if verbose > 0:
                print(f"Sequence {stq[i]} pruned due to empty I set")
            return set()  # No TaSTSPs matching stq and theta

    # Apply the fourth pruning strategy
    for i in range(len(stq)):
        for j in range(i + 1, len(stq)):
            T_min = D.get_times(stq[i][-1].event_type)[0]
            T_max = D.get_times(stq[j][0].event_type)[1]
            if T_min > T_max:
                if verbose > 0:
                    print(f"Sequences {stq[i]} and {stq[j]} pruned due to T_min > T_max")
                return set()  # No TaSTSPs matching stq and theta

    s1 = stq[0]
    S = set()
    S = extend_forward(S, s1, D, F, R, T, theta, 1, stq, verbose)

    if not S:
        if verbose > 0:
            print("No sequences found after forward extension")
        return set()
    else:
        for s in S:
            S_E = set()
            s_E = extend_backward(S_E, s, D, F, R, T, theta, verbose)
            TaSTSPs.update(s_E)

    if verbose > 0:
        print(f"TaSTSPs found: {len(TaSTSPs)}")
    return TaSTSPs

def extend_forward(S, s: Sequence, D, F, R, T, theta, index=1, stq=None, verbose=0):
    if verbose > 1:
        print(f"Extending forward: Sequence={s}, Index={index}")
    for f in F:
        s_star = s.copy()
        s_star.add_element(Element(f))
        L = len(s_star)
        s_star.calculate_I(L - 1, D, R, T)
        s_star.PI = min(s.PI, PR(s_star, L - 1, D))

        if verbose > 2:
            print(f"Extended sequence: {s_star}, PI={s_star.PI}")

        if s_star.PI >= theta:
            if stq and index < len(stq):
                s_index = stq[index]
                if s_star[-1].event_type == s_index[0].event_type:
                    s_double_star = s_star.copy()
                    for k in range(1, len(s_index)):
                        s_double_star.add_element(s_index[k])
                        L = len(s_double_star)
                        s_double_star.calculate_I(L - 1, D, R, T)
                        s_double_star.PI = min(s_double_star.PI, PR(s_double_star, L - 1, D))

                        if verbose > 2:
                            print(f"Extended sequence with stq: {s_double_star}, PI={s_double_star.PI}")

                    if s_double_star.PI >= theta:
                        S = extend_forward(S, s_double_star, D, F, R, T, theta, index + 1, stq, verbose)
            S = extend_forward(S, s_star, D, F, R, T, theta, index, stq, verbose)

    if index >= len(stq):
        S.add(s)

    return S

def extend_backward(S_E, s1, D, F, R, T, theta, verbose=0):
    if verbose > 1:
        print(f"Extending backward: Sequence={s1}")
    for f in F:
        s = s1.copy()
        s.add_element_at_beginning(Element(f))
        s.calculate_I_backward(0, D, R, T)
        s.calculate_I(1, D, R, T)
        s.PI = min(s1.PI, PR(s, 0, D), PR(s, 1, D))

        if verbose > 2:
            print(f"Extended backward sequence: {s}, PI={s.PI}")

        if s.PI >= theta:
            S_E = extend_backward(S_E, s, D, F, R, T, theta, verbose)

    S_E.add(s1)
    return S_E

def PR(sequence: Sequence, index, D: Dataset):
    if len(D[sequence[index].event_type]) == 0:
        return 0
    return len(sequence[index].I) / len(D[sequence[index].event_type])

def is_subsequence_of_previously_tested_sequence(sequence: Sequence, stq, i):
    for index in range(0, i):
        if sequence.is_subsequence_of(stq[index]):
            return True
    return False