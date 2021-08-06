

def z_mass(amnt, plus=[], minus=[], neutral=[]):  # mu_plus and mu_minus might both be greater then 3
    """
    plus is a list of TLorentzVectors representing the positive particles in the selected generated events.
    minus is a list of TLorentzVectors representing the negative particles in the selected generated events.
    neutral is a list of TLorentzVectors representing neutral particles in the selected events.
    amnt is the amount of Z bosons that are desired.
    These particles will be reconstructed into 3 Z bosons.

    The use of this function uses either both plus and minus, or just neutral. amnt is not optional.
    """
    ######## PLUS & MINUS CASE ########
    if (len(plus) > 0) and (len(minus) > 0):
        # left list will have every element matched with each element of the right list,
        # so left is shorter
        if len(plus) < len(minus):
            left = plus
            right = minus
        else:
            left = minus
            right = plus

        # z_bos will contain the reconstructed Zs
        z_bos = []

        # Matching each particle in left to each particle in right and optimizing the mass to 91 GeV
        for i in left:
            # List of difference between THIS i and EACH j that is not equal to this i
            deltas = []
            for j in right:
                if i != j:
                    deltas.append(pow(abs(91.1 - (i + j).M()), 2))
            # Adding the (i+j) match with the closest mass to 91 GeV to the z_bos list
            z_bos.append((i + right[deltas.index(min(deltas))]))

        # Reducing the amount of bosons in z_bos to 3, taking out the ones with mass furthest from 91
        while len(z_bos) > amnt:
            z_bos_deltas = [pow(abs(91.1 - z.M()), 2) for z in z_bos]
            z_bos.pop(z_bos_deltas.index(max(z_bos_deltas)))

    ######## FOR UNCHARGED PARTICLES ########
    if len(neutral) > 0:
        # Create a copy of the particle list and a list of possible reconstructed Zs
        neutral_copy = neutral[:]
        possible_zs = []

        # The 2 for loops looks at possible particle combinations
        for d in neutral:
            option_list = []
            for f in neutral_copy:
                if d != f:
                    option_list.append(d + f)

            # Creating a list that tells us how close the mass of each potential Z is from 91 GeV
            option_mass_deltas = [pow(abs(91.1-k.M()), 2) for k in option_list]

            if len(option_mass_deltas) > 0:
                # Adding the particle with closest mass to 91 to the possible_zs list
                possible_zs.append(option_list[option_mass_deltas.index(min(option_mass_deltas))])

                # Removing the matched particle from the process, counting it as already matched
                neutral_copy.pop(option_mass_deltas.index(min(option_mass_deltas)))

        # z_bos will be the list of final Zs
        z_bos = []
        # List of how far each of the particles in possible_zs is from 91 GeV
        poss_z_mass_deltas = [pow(abs(91-k.M()), 2) for k in possible_zs]

        # Reducing the amount of particles to those desired, picking out those with greatest mass deviation
        while len(z_bos) < amnt:
            # Adding the particle with closest mass to 91 GeV to list of final Zs, z_bos
            z_bos.append(possible_zs[poss_z_mass_deltas.index(min(poss_z_mass_deltas))])
            # Popping the delta of the added particle and removing it from delta list and possible_zs list
            possible_zs.pop(poss_z_mass_deltas.index(min(poss_z_mass_deltas)))
            poss_z_mass_deltas.remove(min(poss_z_mass_deltas))

    return z_bos
