# Module for XX reconstruction

def xx_mass(z_list=[], w_list=[], zw_list=[], dtype='', bosons='zzz', photons=[]):

    if (dtype == 'pt') and (bosons == 'zzz'):
        pt_deltas = []
        pt_deltas.append(abs(z_list[0].Pt() - z_list[1].Pt()))
        pt_deltas.append(abs(z_list[0].Pt() - z_list[2].Pt()))
        pt_deltas.append(abs(z_list[1].Pt() - z_list[2].Pt()))

        if pt_deltas.index(max(pt_deltas)) == 0:
            xx = z_list[0] + z_list[1]
        elif pt_deltas.index(max(pt_deltas)) == 1:
            xx = z_list[0] + z_list[2]
        elif pt_deltas.index(max(pt_deltas)) == 2:
            xx = z_list[1] + z_list[2]
    elif (dtype == 'pt') and (bosons == 'zzw'):
        # If uncertain boson zw_list is NOT used
        if len(zw_list) == 0:
            xx = z_list[0] + z_list[1]
        # If uncertain boson zw_list IS used
        else:
            '''
            # Send all 3 bosons to this function again under 'zzz' to treat them equally
            xx = xx_mass(z_list=(z_list+zw_list), dtype='pt', bosons='zzz')
            '''
            pt_deltas = []
            pt_deltas.append(abs(z_list[0].Pt() - zw_list[0].Pt()))
            pt_deltas.append(abs(z_list[0].Pt() - zw_list[1].Pt()))
            if pt_deltas[0] < pt_deltas[1]:
                xx = z_list[0] + zw_list[1]
            else:
                xx = z_list[0] + zw_list[0]

            # Rearrange zw_list to z-first, w-last to identify the bosons
            if (z_list[0].M() + zw_list[1].M()) == xx.M():
                zw_list.reverse()

    elif (dtype == 'pt') and (bosons == 'zww'):
        xx = w_list[0] + w_list[1]

    elif (dtype == 'pt') and (bosons == 'azz'):
        xx = z_list[0] + z_list[1]

        # Finding photon candidate, greatest delta PT
        pt_deltas = []
        for p in photons:
            pt_deltas.append(abs(xx.Pt() - p.Pt()))

        p_index = pt_deltas.index(max(pt_deltas))

        photons[0], photons[p_index] = photons[p_index], photons[0]

    elif dtype == 'photon':
        if (bosons == 'zaa') or (bosons == 'waa'):
            xx = zaa_waa(photons)

        elif bosons == 'aza':
            xx = aza(photons, z_list)

        elif bosons == 'zza':
            xx = zza(photons, z_list)

        elif bosons == 'aaa':
            xx = aaa(photons)

    return xx


def zaa_waa(photons):
    # Create a copy of the photon list and a list of possible reconstructed XXs
    photons_copy = photons[:]
    possible_xxs = []
    pair_list = []

    # The 2 for loops looks at possible photon combinations
    # The loop will try every combination and record the Pt difference between the combined particles
    for d in photons:
        option_list = []
        pt_deltas = []
        pair = []
        for f in photons_copy:
            if d != f:
                option_list.append(d + f)
                pair.append([d, f])
                # pt_deltas.append(pow(abs(d.Pt() - f.Pt()), 2))
                pt_deltas.append(pow(abs(d.M() + f.M()), 2))

        if len(pt_deltas) > 0:
            # Adding the particle with closest mass to 91 to the possible_xxs list
            possible_xxs.append(option_list[pt_deltas.index(min(pt_deltas))])
            pair_list.append(pair[pt_deltas.index(min(pt_deltas))])

            # Removing the matched particle from the process, counting it as already matched
            photons_copy.pop(pt_deltas.index(min(pt_deltas)))

    masses = [p.M() for p in possible_xxs]
    xx = possible_xxs[masses.index(min(masses))]
    final_pair = pair_list[masses.index(min(masses))]

    p_copy = photons[:]
    for p in p_copy:
        if p not in final_pair:
            photons.remove(p)

    return xx


def aza(photons, z_list):
    pt_deltas = []

    for p in photons:
        pt_deltas.append(pow(abs(z_list[0].Pt() - p.Pt()), 2))
    xx = z_list[0] + photons[pt_deltas.index(max(pt_deltas))]

    # Rearrage photons list to make the first photon the XX one
    if (z_list[0] + photons[1]).M() == xx.M():
        photons.reverse()

    return xx


def aaa(photons):
    pt_deltas = []
    pt_deltas.append(abs(photons[0].Pt() - photons[1].Pt()))
    pt_deltas.append(abs(photons[0].Pt() - photons[2].Pt()))
    pt_deltas.append(abs(photons[1].Pt() - photons[2].Pt()))

    if pt_deltas.index(max(pt_deltas)) == 0:
        xx = photons[0] + photons[1]
    elif pt_deltas.index(max(pt_deltas)) == 1:
        photons[1], photons[2] = photons[2], photons[1]
        xx = photons[0] + photons[1]
        # xx = photons[0] + photons[2]
        # photons[1], photons[2] = photons[2], photons[1]
    elif pt_deltas.index(max(pt_deltas)) == 2:
        photons[0], photons[2] = photons[2], photons[0]
        xx = photons[0] + photons[1]
        # xx = photons[1] + photons[2]

    return xx


def zza(photons, z_list):
    pt_deltas1, pt_deltas2 = [], []

    for p in photons:
        pt_deltas1.append(abs(p.Pt() - z_list[0].Pt()))
        pt_deltas2.append(abs(p.Pt() - z_list[1].Pt()))

    p1_max, p1_max_in = max(pt_deltas1), pt_deltas1.index(max(pt_deltas1))
    p2_max, p2_max_in = max(pt_deltas2), pt_deltas2.index(max(pt_deltas2))

    if p1_max > p2_max:
        xx = z_list[0] + photons[p1_max_in]
    elif p1_max < p2_max:
        xx = z_list[1] + photons[p2_max_in]

    # Emptying photon list and adding only used photon
    photons_copy = photons[:]
    photons = []
    for p in photons_copy:
        if (p + z_list[0] == xx) or (p + z_list[1] == xx):
            photons.append(p)
            if p + z_list[1] == xx:
                z_list.reverse()
    return xx