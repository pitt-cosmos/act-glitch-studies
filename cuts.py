import numpy as np
import moby2

def merge_cuts(cut1, cut2):
    '''Merge two cutvectors
    input cuts have to be CutVector type
    '''
    if len(cut1) == 0:
        return cut2
    if len(cut2) == 0:
        return cut1

    nsamps = max(cut1[-1][1], cut2[-1][1])
    c1m = cut1.get_mask(nsamps=nsamps)
    c2m = cut2.get_mask(nsamps=nsamps)
    cm = np.logical_or(c1m, c2m)
    merged = moby2.tod.CutsVector.from_mask(mask=cm)
    return merged

def common_cuts(cut1, cut2):
    '''Find common cuts from two cuts
    Input cuts must be of CutVectors type
    '''
    if len(cut1) == 0:
        return cut1
    if len(cut2) == 0:
        return cut2
    nsamps = max(cut1[-1][1], cut2[-1][1])
    c1m = cut1.get_mask(nsamps=nsamps)
    c2m = cut2.get_mask(nsamps=nsamps)
    cm = np.logical_and(c1m, c2m)
    common = moby2.tod.CutsVector.from_mask(mask=cm)
    return common
