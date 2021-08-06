import sys
sys.path.append('/Applications/root_v6.20.04/lib')
import ROOT
from xx_func_2_final import z_mass, xx_mass


def reconstruct(directory, z_products='', w_products='', xx_products='', count_histos=''):
    """
    directory is a string of the path of the root file that will be opened.
    reconstruct() opens the file and reconstructs the particles in different ways, depending on the decay process.
    Then the X boson is reconstructed.

    Returns: a list (xx_list) of TLorentzVectors, representing the XX bosons; the efficiency of the events in this file.
    """

    # Open file, get tree, get number of events
    delph_file = ROOT.TFile.Open(directory)
    tree = delph_file.Get('Delphes')

    # amount of events generated in MadGraph
    generated_events = tree.GetEntries()

    # list index corresponds to event number. Contains TLorentzVectors.
    z1_list, z2_list, z3_list = [], [], []      # z1_list, z2_list, z3_list are for Z bosons used in tri-boson production events
    w1_list, w2_list, w3_list = [], [], []      # w1_list, w2_list, w3_list are for W bosons used in tri-boson production events
    zw1_list, zw2_list, zw3_list = [], [], []   # for situation where fatjets cannot be yet identified as Zs or Ws until XX reconstruction

    phots = []
    phot1, phot2, phot3 = [], [], []      # phots contains photons that decay from the X

    xx_list = []    # xx_list will contain the reconstructed X bosons

    # Amount of Zs wanted per event
    zs_wanted = 0
    for e in z_products:
        if (e == 'muon') or (e == 'electron'):
            zs_wanted += z_products[e]/2
        elif e == 'fatjet':
            zs_wanted += z_products[e]
    # Amount of Ws wanted per event
    ws_wanted = 0
    for v in w_products:
        if (v == 'muon') or (v == 'electron'):
            ws_wanted += w_products[v]/2
        elif v == 'fatjet':
            ws_wanted += w_products[v]
    # Amount of photons wanted per event
    ps_wanted = 0
    for p in xx_products:
        if p == 'photon':
            ps_wanted += xx_products[p]

    for i in range(generated_events):
        entry = tree.GetEntry(i)

        # When count is True, the event passes all event selection requirements
        count = True

        # HERE BEGIN RECONSTRUCTIONS
        if 'muon' in z_products:

            muon_amount = tree.Muon.GetEntries()

            # Filling the muon count histogram
            #count_histos['muon'].Fill(muon_amount)

            muons = [ROOT.TLorentzVector() for k in range(muon_amount)]

            # Separate the muons by charge
            muons_plus, muons_minus = [], []

            # Setting Pt, Eta, Phi, M
            for j in range(muon_amount):
                muons[j].SetPtEtaPhiM(tree.GetLeaf('Muon.PT').GetValue(j),
                                      tree.GetLeaf('Muon.Eta').GetValue(j),
                                      tree.GetLeaf('Muon.Phi').GetValue(j),
                                      0.0)
                if tree.GetLeaf('Muon.Charge').GetValue(j) == -1:
                    muons_minus.append(muons[j])
                elif tree.GetLeaf('Muon.Charge').GetValue(j) == 1:
                    muons_plus.append(muons[j])

            # Reconstructing the muons into desired amount of Zs
            if (len(muons_plus) >= (z_products['muon']//2)) and (len(muons_minus) >= (z_products['muon']//2)):
                z_muon_list = z_mass(plus=muons_plus, minus=muons_minus, amnt=z_products['muon']//2)

            else:
                z_muon_list = []
                count = False
        else:
            z_muon_list = []

        if 'electron' in z_products:         # If decay products include electrons
            electron_amount = tree.Electron.GetEntries()

            # Filling the electron count histogram
            #count_histos['electron'].Fill(electron_amount)

            electrons = [ROOT.TLorentzVector() for k in range(electron_amount)]

            # Separate the muons by charge
            elec_plus, elec_minus = [], []

            # Setting Pt, Eta, Phi, M
            for j in range(electron_amount):
                electrons[j].SetPtEtaPhiM(tree.GetLeaf('Electron.PT').GetValue(j),
                                          tree.GetLeaf('Electron.Eta').GetValue(j),
                                          tree.GetLeaf('Electron.Phi').GetValue(j),
                                          0.0005)
                if tree.GetLeaf('Electron.Charge').GetValue(j) == -1:
                    elec_minus.append(electrons[j])
                elif tree.GetLeaf('Electron.Charge').GetValue(j) == 1:
                    elec_plus.append(electrons[j])

            # Reconstructing electrons into desired amount of Zs
            if (len(elec_plus) >= (z_products['electron']//2)) and (len(elec_minus) >= (z_products['electron']//2)):
                z_electron_list = z_mass(plus=elec_plus, minus=elec_minus, amnt=z_products['electron']//2)

            else:
                z_electron_list = []
                count = False
        else:
            z_electron_list = []

        if ('fatjet' in z_products) and ('fatjet' not in w_products):
            fatjet_amount = tree.FatJet.GetEntries()

            # Filling the fat jet count histogram
            #count_histos['fatjet'].Fill(fatjet_amount)

            fatjets = [ROOT.TLorentzVector() for fj in range(fatjet_amount)]

            # Setting Pt, Eta, Phi, M
            for f in range(fatjet_amount):
                fatjets[f].SetPtEtaPhiM(tree.GetLeaf('FatJet.PT').GetValue(f),
                                        tree.GetLeaf('FatJet.Eta').GetValue(f),
                                        tree.GetLeaf('FatJet.Phi').GetValue(f),
                                        tree.GetLeaf('FatJet.Mass').GetValue(f))

            if fatjet_amount >= z_products['fatjet']:
                z_fatjet_list = fatjets[:]

                while len(z_fatjet_list) > z_products['fatjet']:
                    z_bos_deltas = [pow(abs(91.2 - z.M()), 1) for z in z_fatjet_list]
                    z_fatjet_list.pop(z_bos_deltas.index(max(z_bos_deltas)))
            else:
                z_fatjet_list = []
                count = False
        else:
            z_fatjet_list = []

        #### W BOSON -> FAT JETS ####
        if ('fatjet' in w_products) and ('fatjet' not in z_products):
            fatjet_amount = tree.FatJet.GetEntries()

            # Filling the fat jet count histogram
            #count_histos['fatjet'].Fill(fatjet_amount)

            fatjets = [ROOT.TLorentzVector() for fj in range(fatjet_amount)]

            # Setting Pt, Eta, Phi, M
            for f in range(fatjet_amount):
                fatjets[f].SetPtEtaPhiM(tree.GetLeaf('FatJet.PT').GetValue(f),
                                        tree.GetLeaf('FatJet.Eta').GetValue(f),
                                        tree.GetLeaf('FatJet.Phi').GetValue(f),
                                        tree.GetLeaf('FatJet.Mass').GetValue(f))

            if fatjet_amount >= w_products['fatjet']:
                w_fatjet_list = fatjets[:]

                while len(w_fatjet_list) > w_products['fatjet']:
                    w_bos_deltas = [pow(abs(80.4 - w.M()), 2) for w in w_fatjet_list]
                    w_fatjet_list.pop(w_bos_deltas.index(max(w_bos_deltas)))
            else:
                w_fatjet_list = []
                count = False

        else:
            w_fatjet_list = []

        #### Z, W BOSONS -> FAT JETS ####
        if ('fatjet' in z_products) and ('fatjet' in w_products):
            fatjet_amount = tree.FatJet.GetEntries()

            # Filling the fat jet count histogram
            #count_histos['fatjet'].Fill(fatjet_amount)

            fatjets = [ROOT.TLorentzVector() for fj in range(fatjet_amount)]

            # Setting Pt, Eta, Phi, M
            for f in range(fatjet_amount):
                fatjets[f].SetPtEtaPhiM(tree.GetLeaf('FatJet.PT').GetValue(f),
                                        tree.GetLeaf('FatJet.Eta').GetValue(f),
                                        tree.GetLeaf('FatJet.Phi').GetValue(f),
                                        tree.GetLeaf('FatJet.Mass').GetValue(f))

            if fatjet_amount >= (z_products['fatjet']+w_products['fatjet']):
                # Reduce number of fat jets to the exact total that we want
                while len(fatjets) > (z_products['fatjet'] + w_products['fatjet']):
                    boson_deltas = [pow(abs(85 - b.M()), 2) for b in fatjets]
                    fatjets.pop(boson_deltas.index(max(boson_deltas)))

                # This list will contain both fat jets since we cannot yet determine which came from z, w.
                # This will be determined after xx reconstruction. We will know based on which is used.
                fj_bosons = fatjets[:]

            else:
                fj_bosons = []
                count = False

        else:
            fj_bosons = []

        if 'photon' in xx_products:
            photon_amount = tree.Photon.GetEntries()

            # Filling the photon count histogram
            #count_histos['photon'].Fill(photon_amount)

            photons = [ROOT.TLorentzVector() for p in range(photon_amount)]

            # Setting Pt, Eta, Phi, M
            for p in range(photon_amount):
                photons[p].SetPtEtaPhiM(tree.GetLeaf('Photon.PT').GetValue(p),
                                        tree.GetLeaf('Photon.Eta').GetValue(p),
                                        tree.GetLeaf('Photon.Phi').GetValue(p),
                                        0)
            if (photon_amount >= 2) and (count is True):
                phots.append(photons)
            else:
                count = False
        else:
            photons = []

        # Here the 3 bosons in the event are appended in to their appropriate lists to be used later to reconstruct XXs
        if (count is True) and (zs_wanted == 3):
            z_list = z_muon_list + z_electron_list + z_fatjet_list
            # Append Zs to z1_list-z3_list if the event meets counting requirements
            if len(z_list) == 3:
                z1_list.append(z_list[0])
                z2_list.append(z_list[1])
                z3_list.append(z_list[2])

        if (count is True) and (zs_wanted == 2) and (ws_wanted == 1):
            if len(fj_bosons) == 0:
                z_list = z_muon_list + z_electron_list + z_fatjet_list
                w_list = w_fatjet_list
                if (len(z_list) == 2) and (len(w_list) == 1):
                    z1_list.append(z_list[0])
                    z2_list.append(z_list[1])
                    w1_list.append(w_list[0])
            else:
                z_list = z_muon_list + z_electron_list

                z1_list.append(z_list[0])
                zw1_list.append(fj_bosons[0])
                zw2_list.append(fj_bosons[1])

        if (count is True) and (zs_wanted == 1) and (ws_wanted == 2):
            z_list = z_muon_list + z_electron_list + z_fatjet_list
            w_list = w_fatjet_list
            if (len(z_list) == 1) and (len(w_list) == 2):
                z1_list.append(z_list[0])
                w1_list.append(w_list[0])
                w2_list.append(w_list[1])

        if (count is True) and (zs_wanted == 1) and (ps_wanted == 2 or ps_wanted == 1):
            z_list = z_muon_list + z_electron_list + z_fatjet_list
            z1_list.append(z_list[0])
            # FIXME: May need fixing due to ignoring other bosons


    if zs_wanted == 3:
        for l in range(len(z3_list)):
            xx_list.append(xx_mass(z_list=[z1_list[l], z2_list[l], z3_list[l]], dtype='pt', bosons='zzz'))
        # amount of events that made it through the selection process
        numb_events = len(xx_list)
        boson_list = [z1_list, z2_list, z3_list]

    elif (zs_wanted == 2) and (ws_wanted == 1):
        # If uncertain boson list is NOT used (z or w)
        if len(zw1_list) == 0:
            for l in range(len(w1_list)):
                #xx_list.append(xx_mass(z1_list[l], z2_list[l], w1_list[l], type='pt', bosons='zzw'))
                xx_list.append(xx_mass(z_list=[z1_list[l], z2_list[l]], w_list=[w1_list[l]], dtype='pt', bosons='zzw'))
            numb_events = len(xx_list)
            boson_list = [z1_list, z2_list, w1_list]

        # IF uncertain boson list IS used
        elif len(zw1_list) != 0:
            for l in range(len(z1_list)):
                # This list contains the two fat jets that we cannot yet identify as Z or W. It will be sent to xx_mass
                # via zw_list optional input under 'zzw' bosons, will then be recursively sent again as 'zzz' bosons for
                # pt selection. The z_or_w_list will then be arranged in a z-first, w-last order so we can then add the
                # zs to the z2_list and ws to w1_list.
                z_or_w_list = [zw1_list[l], zw2_list[l]]
                xx_list.append(xx_mass(z_list=[z1_list[l]], zw_list=z_or_w_list, dtype='pt', bosons='zzw'))
                z2_list.append(z_or_w_list[0])
                w1_list.append(z_or_w_list[1])
            numb_events = len(xx_list)
            boson_list = [z1_list, z2_list, w1_list]

    elif (zs_wanted == 1) and (ws_wanted == 2):
        for l in range(len(w1_list)):
            xx_list.append(xx_mass(z_list=[z1_list[l]], w_list=[w1_list[l], w2_list[l]], dtype='pt', bosons='zww'))
        numb_events = len(xx_list)
        boson_list = [z1_list, w1_list, w2_list]

    elif (zs_wanted == 1) and ((ps_wanted == 2) or (ps_wanted == 1)):
        for k in range(len(phots)):
            if xx_products['photon'] == 2:
                xx_list.append(xx_mass(z_list=[z1_list[k]], photons=phots[k], dtype='photon', bosons='zaa'))
            elif xx_products['photon'] == 1:
                xx_list.append(xx_mass(z_list=[z1_list[k]], photons=phots[k], dtype='photon', bosons='aza'))
            phot1.append(phots[k][0])
            phot2.append(phots[k][1])
        # amount of events that made it through the selection process
        numb_events = len(xx_list)
        boson_list = [z1_list, phot1]

    efficiency = float(numb_events)/float(generated_events)
    print 'Generated Events:', generated_events
    print 'Nmb of events:', numb_events
    print 'Efficiency:', efficiency
    print ''
    delph_file.Close()

    return xx_list, efficiency, boson_list


if __name__ == '__main__':
    reconstruction("/home/achilles12/Physics/Code/4MuDecay/tag_1_delphes_events.root", {'muon': 4, 'fatjet': 1})
    print 'Done'
