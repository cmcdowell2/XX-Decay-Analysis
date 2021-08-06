import sys
sys.path.append('/Applications/root_v6.20.04/lib')
import ROOT
import array


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
            #boson_histos[1].Fill(l[1][i].M())
            #boson_histos[2].Fill(l[2][i].M())

    # Making and filling the histogram with filled xx_m_list
    if type == '4l1fatjet':
        backrnd_histo = ROOT.TH1F('XX Mass Background', ' ; m_{XX}[GeV]; events', 50, 100, 2500)
    elif type == '2l2fatjet':
        backrnd_histo = ROOT.TH1F('XX Mass Background', ' ; m_{XX}[GeV]; events', 50, 100, 2500)
    else:
        backrnd_histo = ROOT.TH1F('XX Mass Background', ' ; m_{XX}[GeV]; events', 50, 100, 2500)

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
        histos = [ROOT.TH1F('', ' ; m_{XX}[GeV]; events', 50, 100, 2500) for i in outputs]

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
            #boson_histos[1].Fill(l[1][i].M())
            #boson_histos[2].Fill(l[2][i].M())

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
