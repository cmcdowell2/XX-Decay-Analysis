import sys
sys.path.append('/Applications/root_v6.20.04/lib')
import ROOT
import array
from math import sqrt


### Function for finding 3 Zs 
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
                    deltas.append(pow(abs(91 - (i + j).M()), 1))
            # Adding the (i+j) match with the closest mass to 91 GeV to the z_bos list
            z_bos.append((i + right[deltas.index(min(deltas))]))
            
        # Reducing the amount of bosons in z_bos to 3, taking out the ones with mass furthest from 91
        while len(z_bos) > amnt:
            z_bos_deltas = [pow(abs(91 - z.M()), 1) for z in z_bos]
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
            option_mass_deltas = [pow(abs(91-k.M()), 1) for k in option_list]

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


#def xx_mass(b1=ROOT.TLorentzVector(), b2=ROOT.TLorentzVector(), b3=ROOT.TLorentzVector(), type='', bosons='zzz', photons=[]):
def xx_mass(z_list=[], w_list=[], zw_list=[], dtype='', bosons='zzz', photons=[], ):
    '''
    z_list = []
    w_list = []

    del1z = pow(abs(b1.M() - 91.2), 2)
    del1w = pow(abs(b1.M() - 80.4), 2)
    if del1z < del1w:
        z_list.append(b1)
    elif del1w < del1z:
        w_list.append(b1)
    del2z = pow(abs(b2.M() - 91.2), 2)
    del2w = pow(abs(b2.M() - 80.4), 2)
    if del2z < del2w:
        z_list.append(b2)
    elif del2w < del2z:
        w_list.append(b2)
    del3z = pow(abs(b3.M() - 91.2), 2)
    del3w = pow(abs(b3.M() - 80.4), 2)
    if del3z < del3w:
        z_list.append(b3)
    elif del3w < del3z:
        w_list.append(b3)
    '''
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

    elif dtype == 'photon':
        if bosons == 'zaa':
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
                        #pt_deltas.append(pow(abs(d.Pt() - f.Pt()), 2))
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

        elif bosons == 'aza':
            pt_deltas = []

            for p in photons:
                pt_deltas.append(pow(abs(z_list[0].Pt() - p.Pt()), 2))
            xx = z_list[0] + photons[pt_deltas.index(max(pt_deltas))]


    return xx


def background_histo(outputs, crossx_list, boson_histos, type=''):
    """
    outputs is the output that the main function will give. crossx_list is the list of the cross sections of each file.
    outputs is a LIST of all disired files' outputs.
    Returns a histogram ready to draw and print.
    """
    xx_m_list1 = []  # empty list for xx masses
    eff_list1 = []  # empty list of efficiencies
    boson_list = []

    # Extracting all XX bosons from all files and adding that to xx_m_list
    for out in outputs:
        xx_m_list1 += out[0]
        eff_list1.append(out[1])
        boson_list.append(out[2])
        # FIXME: brackets around [out[2]] above only for vfatjet decays. REMOVE for others
    # Filling the boson histograms
    for l in boson_list:
        for i in range(len(l[0])):
            boson_histos[0].Fill(l[0][i].M())


    # Making and filling the histogram with filled xx_m_list
    if type == '4l1fatjet':
        backrnd_histo = ROOT.TH1F('XX Mass Background', ' ; m_{XX}[GeV]; events', 50, 100, 2500)
    elif type == '2l2fatjet':
        backrnd_histo = ROOT.TH1F('XX Mass Background', ' ; m_{XX}[GeV]; events', 50, 100, 2500)
    else:
        backrnd_histo = ROOT.TH1F('XX Mass Background', ' ; m_{XX}[GeV]; events', 50, 100, 2200)

    for i in xx_m_list1:
        backrnd_histo.Fill(i.M())

    # Calculating number of events we can expect at the LHC
    lumi = 100000   # (picobarns)
    total_events = 0
    N_list = []
    for i in range(len(outputs)):
        N_list.append(lumi * crossx_list[i] * eff_list1[i])
    N = sum(N_list) / len(N_list)

    print 'Background N:', N

    backrnd_histo.Scale(N / backrnd_histo.Integral(0, 51))

    return backrnd_histo


def signal_histo(outputs, mass_list, crossx_list, boson_histos, type=''):
    """
    outputs is a LIST of the desired files' output.
    mass_list is the list of masses corresponding to the signals.
    Signal histogram will be created.
    Efficiency plot will be created.

    Returns list of histograms to be drawn on same canvas. Largest histogram must be drawn first.
    Returns legend to draw.
    Returns efficiency plot to be drawn on separate canvas.
    """
    # Creating empty list of efficiency for each output
    efficiency_list = []

    # List of boson histograms
    boson_list = []

    # Making a histogram for each output and giving each a different color
    if (type == '4l1fatjet') or (type == '6mu'):
        histos = [ROOT.TH1F('', ' ; m_{XX}[GeV]; events', 50, 100, 2500) for i in outputs]
    elif type == '2l2fatjet':
        histos = [ROOT.TH1F('', ' ; m_{XX}[GeV]; events', 50, 100, 2500) for i in outputs]
    else:
        histos = [ROOT.TH1F('', ' ; m_{XX}[GeV]; events', 50, 100, 2200) for i in outputs]

    for k in range(len(histos)):
        histos[k].SetLineColor(k+1)
    '''
    # Filling the histograms with corresponding output
    for j in range(len(outputs)):
        for i in range(len(outputs[j])):
            xx_m_list2 = outputs[j][i][0]
            efficiency_list.append(outputs[j][i][1])
            boson_list.append(outputs[j][i][2])
            for xx in xx_m_list2:
                print xx
                histos[j].Fill(xx.M())
    '''
    # Filling the histograms with corresponding output
    for j in range(len(outputs)):
        xx_m_list2 = outputs[j][0]
        efficiency_list.append(outputs[j][1])
        boson_list.append(outputs[j][2])
        for xx in xx_m_list2:
            histos[j].Fill(xx.M())

    #FIXME: Uncomment for more bosons
    # Plotting the bosons
    bos_histo1 = ROOT.TH1F('Boson 1', ' ; mass [GeV]; events', 50, 0, 200)
    bos_histo2 = ROOT.TH1F('Boson 2', ' ; mass [GeV]; events', 50, 0, 200)
    bos_histo3 = ROOT.TH1F('Boson 3', ' ; mass [GeV]; events', 50, 0, 200)
    bos_histo_list = [bos_histo1, bos_histo2, bos_histo3]

    for l in boson_list:
        for i in range(len(l[0])):
            boson_histos[0].Fill(l[0][i].M())

    # Normalizing histograms
    lumi = 100000  # (picobarns)
    for hi in range(len(histos)):
        N = crossx_list[hi] * lumi * efficiency_list[hi]
        histos[hi].Scale(N / histos[hi].Integral(0, 51))

        print 'Signal N:', N

    # Making legend for histogram
    legend = ROOT.TLegend(0.65, 0.7, 0.99, 0.95)
    for p in range(len(histos)):
        legend.AddEntry(histos[p], 'm_{XX} = '+'{} GeV'.format(mass_list[p]))
    legend.SetBorderSize(0)

    # List of efficiency: divided events/gen_events
    eff_list = [efficiency_list[0]]
    # Making efficiency and masses arrays to use in efficiency TGraph
    eff_array = array.array('d', eff_list)
    mass_array = array.array('d', mass_list)

    # Making eff_graph, titling it, and customizing it. Ready to be drawn.
    eff_graph = ROOT.TGraph(len(mass_list), mass_array, eff_array)
    eff_graph.SetMarkerStyle(4)
    eff_graph.SetTitle('')
    eff_graph.GetXaxis().SetTitle('m_{XX}[GeV]')
    eff_graph.GetYaxis().SetTitle('Efficiency')

    # Printing efficiency list
    print 'Efficiency List:', eff_list

    return histos, legend, eff_graph
