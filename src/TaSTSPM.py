from Sequence import *

def tastsp_algorithm(D, F, R, T, theta, stq):
    TaSTSPs = set()

    # Apply the first and the third pruning strategies
    for s in stq:
        if is_subsequence_of_previously_tested_sequence(s, stq):
            continue
        s_PI = 0
        for i in range(1, len(s)):
            s[i].I = calculate_I(s[i])
            s_PI = min(s_PI, PR(s, i))
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
            if stq[i][-1].T_min > stq[j][0].T_max:
                return set()  # No TaSTSPs matching stq and theta

    s1 = stq[0]
    S = set()
    S = extend_forward(S, s1, D, F, R, T, theta)

    if not S:
        return set()
    else:
        for s in S:
            S_E = set()
            s_E = extend_backward(S_E, s, D, F, R, T, theta)
            TaSTSPs.update(s_E)

    return TaSTSPs


def extend_forward(S, s, D, F, R, T, theta, index=1, stq=None):
    for f in F:
        s_star = s + [f]
        L = len(s_star)
        s_star[-1].I = calculate_I(s_star[-1])
        s_star_PI = min(s.PI, PR(s_star, L))

        if s_star_PI >= theta:
            if stq and index <= len(stq):
                s_index = stq[index - 1]
                if s_star[-1] == s_index[0]:
                    s_double_star = s_star.copy()
                    s_double_star_PI = s_star_PI
                    for k in range(1, len(s_index)):
                        s_double_star.append(s_index[k])
                        L = len(s_double_star)
                        s_double_star[-1].I = calculate_I(s_double_star[-1])
                        s_double_star_PI = min(s_double_star_PI, PR(s_double_star, L))
                        if s_double_star_PI < theta:
                            break
                    else:
                        S = extend_forward(S, s_double_star, D, F, R, T, theta, index + 1, stq)

            S = extend_forward(S, s_star, D, F, R, T, theta, index, stq)

    if index > len(stq):
        S.add(tuple(s))

    return S


def extend_backward(S_E, s1, D, F, R, T, theta):
    for f in F:
        s = [f] + s1
        s[0].I = calculate_I(s[0])
        s_PI = min(s1.PI, PR(s, 1))

        if s_PI >= theta:
            S_E = extend_backward(S_E, s, D, F, R, T, theta)

    S_E.add(tuple(s1))

    return S_E


def calculate_I(event_instance):
    # Placeholder function for calculating I
    pass


def PR(sequence, index):
    # Placeholder function for calculating PR
    pass


def is_subsequence_of_previously_tested_sequence(seq, stq):

    for s in stq:
        while seq != s:
            if seq in s:
                return True

    pass