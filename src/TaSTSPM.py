from Sequence import *

def tastsp_algorithm(D, F, R, T, theta, stq):
    TaSTSPs = set()

    # Apply the first and the third pruning strategies
    for s in stq:
        if is_subsequence_of_previously_tested_sequence(s, stq):
            continue
        s_PI = 0
        for i in range(0, len(s)):
            s.calculate_I(i, D, R, T)
            s_PI = min(s_PI, PR(s, i, D))
            if s_PI < theta:
                return set()  # No TaSTSPs matching stq and theta
        s.PI = s_PI

    # Apply the second pruning strategy
    for i in range(len(stq) - 1):
        if stq[i][-1].I == set():
            return set()  # No TaSTSPs matching stq and theta

    # Apply the fourth pruning strategy
    for i in range(len(stq)):
        for j in range(i + 1, len(stq)):
            T_min = D.get_times(stq[i][-1].event_type)[0]
            T_max = D.get_times(stq[j][0].event_type)[1]
            if T_min > T_max:
                return set()  # No TaSTSPs matching stq and theta

    s1 = stq[0]
    S = set()
    S = extend_forward(S, s1, D, F, R, T, theta, 1, stq)

    if not S:
        return set()
    else:
        for s in S:
            S_E = set()
            s_E = extend_backward(S_E, s, D, F, R, T, theta)
            TaSTSPs.update(s_E)

    return TaSTSPs


def extend_forward(S, s: Sequence, D, F, R, T, theta, index=1, stq=None):
    for f in F:
        s_star = s.add_element(Element(f))
        L = len(s_star)
        s_star.calculate_I(L - 1, D, R, T)
        s_star.PI = min(s.PI, PR(s_star, L - 1, D))

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

                    if s_double_star.PI >= theta:
                        S = extend_forward(S, s_double_star, D, F, R, T, theta, index + 1, stq)
            S = extend_forward(S, s_star, D, F, R, T, theta, index, stq)

    if index >= len(stq):
        S.add(s)

    return S


def extend_backward(S_E, s1, D, F, R, T, theta):
    for f in F:
        s = s1.add_element_at_beginning(Element(f))
        s.calculate_I(0, D, R, T)
        s.PI = min(s1.PI, PR(s, 0))

        if s.PI >= theta:
            S_E = extend_backward(S_E, s, D, F, R, T, theta)

    S_E.add(s1)

    return S_E


def PR(sequence: Sequence, index, D: Dataset):
    return len(sequence[index].I) / len(D[sequence[index].event_type])


def is_subsequence_of_previously_tested_sequence(sequence: Sequence, stq):
    for s in stq:
        while sequence != s:
            if sequence.is_subsequence_of(s):
                return True
    return False
    pass
