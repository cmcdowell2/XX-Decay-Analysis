import sys
sys.path.append('/Applications/root_v6.20.04/lib')
import ROOT
from xx_func_1 import reconstruct
from histo_mod import background_histo, signal_histo


if __name__ == '__main__':

    pdf_tex = input('pdf or tex:')

    ###### FOUR MUONS, TWO JETS ######

    ###----------------Background----------------###

    directory_bkg = ['/mnt/e/Users/Cameron/AppData/Local/Packages/CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc/LocalState/rootfs/home/achilles12/Physics/Background/2Pho1JetBackground/Events/run_01/tag_1_delphes_events.root']
    
    # Cross-section corresponding to each file
    xs_list = [112.43]

    # dictionaries with histograms to count particles
    count_histos_bkg = {'photon': ROOT.TH1F('Bkg Muon Count', ' ; amount; events', 6, 0, 6),
                        'fatjet': ROOT.TH1F('Bkg Photon Count', ' ; amount; events', 6, 0, 6)}

    # creating list output_bkg with reconstruct() output of each file in directory_bkg
    output_bkg = [reconstruct(p, xx_products = {'photon' : 1}, z_products = {'fatjet' : 1}, extra_ps={'photon': 1}, count_histos=count_histos_bkg) for p in directory_bkg]

    # Mass Histograms for the 3 bosons
    bkg_boson_hists = [ROOT.TH1F('Bkg Muon-Z1', ' ; mass [GeV]; events', 50, 0, 200), ROOT.TH1F('Bkg Muon-Z2', ' ; mass [GeV]; events', 50, 0, 200), ROOT.TH1F('Bkg Muon-Z3', ' ; mass [GeV]; events', 50, 0, 200)]

    # Giving list background_outputs to backround_histo to return a histogram
    bkg_canvas = ROOT.TCanvas()
    bkg_histo = background_histo(output_bkg, xs_list, boson_histos=bkg_boson_hists, type='2l2a')
    bkg_histo_root = ROOT.TFile('2mu2a_bkg_file.root', 'recreate')
    bkg_histo.Draw("HIST")
    bkg_histo.Write()
    bkg_canvas.Print('2mu2a_bkg_histo.' + pdf_tex)
    bkg_histo_root.Close()

    # Printing out counting histograms
    count_canv1 = ROOT.TCanvas()
    count_histos_bkg['photon'].Draw()
    count_canv1.Print('bkg_muon_count.' + pdf_tex)
    count_canv2 = ROOT.TCanvas()
    count_histos_bkg['fatjet'].Draw()
    count_canv2.Print('bkg_fatjet_count.' + pdf_tex)

    bc_1 = ROOT.TCanvas(); bkg_boson_hists[0].Draw(); bc_1.Print('bkg_boson1.' + pdf_tex)
    bc_2 = ROOT.TCanvas(); bkg_boson_hists[1].Draw(); bc_2.Print('bkg_boson2.' + pdf_tex)
    bc_3 = ROOT.TCanvas(); bkg_boson_hists[2].Draw(); bc_3.Print('bkg_boson3.' + pdf_tex)
    
    bkg_boson_file = ROOT.TFile('bkg_boson_file.root', 'recreate')
    bkg_boson_hists[0].Write(); bkg_boson_file.Close()
    
    # Getting bin content and writing them to txt file
    bin_content_file = open('ZZZPtValues.txt', 'w')
    for bi in range(0, 52):
        bin_content_file.write(str(bkg_histo.GetBinContent(bi)) + '\n')
    bin_content_file.close()

    ###----------------Signal----------------###
    directory = ['/mnt/e/Users/Cameron/AppData/Local/Packages/CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc/LocalState/rootfs/home/achilles12/Physics/500/2Pho1JetA500/Events/run_01/tag_1_delphes_events.root']   # 500 GeV]   

    # dictionaries with histograms to count particles
    count_histos_sig = {'photon': ROOT.TH1F('Signal Muon Count', ' ; amount; events', 6, 0, 6),
                        'fatjet': ROOT.TH1F('Signal Photon Count', ' ; amount; events', 6, 0, 6)}

    # list of outputs from reconstruct() function for each file
    output = [reconstruct(d, xx_products={'photon' : 1}, z_products={'fatjet' : 1}, extra_ps={'photon': 1}, count_histos=count_histos_sig) for d in directory]

    # Masses and xs lists correpsonding to each file
    xs_list = [.000052893]
    mass_list = [500]

    # Mass Histograms for the 3 bosons
    sig_boson_hists = [ROOT.TH1F('Signal Muon-Z1', ' ; mass [GeV]; events', 50, 0, 200), ROOT.TH1F('Signal Muon-Z2', ' ; mass [GeV]; events', 50, 0, 200), ROOT.TH1F('Signal Muon-Z3', ' ; mass [GeV]; events', 50, 0, 200)]

    # Run the reconstruct() output through the signal function, and extract the outputted histogram, legend, and graph
    sig_histo_eff_graph = signal_histo(output, mass_list, xs_list, boson_histos=sig_boson_hists, type='2l2a')
    sig_histos, sig_legend, efficiency_plot = sig_histo_eff_graph[0], sig_histo_eff_graph[1], sig_histo_eff_graph[2]

    # Printing out coutning histograms
    count_canv1 = ROOT.TCanvas()
    count_histos_sig['photon'].Draw()
    count_canv1.Print('sig_muon_count.' + pdf_tex)
    count_canv2 = ROOT.TCanvas()
    count_histos_sig['fatjet'].Draw()
    count_canv2.Print('sig_fatjet_count.' + pdf_tex)

    bc_1 = ROOT.TCanvas(); sig_boson_hists[0].Draw(); bc_1.Print('sig_boson1.' + pdf_tex)
    bc_2 = ROOT.TCanvas(); sig_boson_hists[1].Draw(); bc_2.Print('sig_boson2.' + pdf_tex)
    bc_3 = ROOT.TCanvas(); sig_boson_hists[2].Draw(); bc_3.Print('sig_boson3.' + pdf_tex)
    
    sig_boson_file = ROOT.TFile('sig_boson_file.root', 'recreate')
    sig_boson_hists[0].Write(); sig_boson_file.Close()

    # Creating signal canvas and root file, drawing and writing histograms and legend
    sig_histo_canvas = ROOT.TCanvas()
    #sig_histo_canvas.SetLogy();
    sig_histo_canvas.cd();
    sig_histo_file = ROOT.TFile('4mu1fatjet_signals_histo_file.root', 'recreate')

    #sig_histos[1].Draw("HISTO")
    #sig_histos[1].Write()
    for h in sig_histos:
        #if h != sig_histos[1]:
            h.Draw("HISTO SAME")
            h.Write()
    sig_legend.Draw()
    sig_histo = signal_histo(output, mass_list, xs_list, boson_histos=sig_boson_hists, type='2l2a')
    sig_histo[0][0].Draw("HIST")
    sig_histo[0][0].Write()
    sig_histo_canvas.Print('4mu1fatjet_signals_histo.' + pdf_tex)
    sig_histo_file.Close()
    
    # Creating eff plot canvas and root file, drawing and writing eff plot
    eff_canvas = ROOT.TCanvas()
    eff_plot_file = ROOT.TFile('4mu1fatjet_signal_efficiency.root', 'recreate')
    efficiency_plot.SetMinimum(0)
    efficiency_plot.SetMaximum(1.0)
    efficiency_plot.Draw()
    efficiency_plot.Write()
    eff_canvas.Print('signal_eff.' + pdf_tex)
    eff_plot_file.Close()
    
    # Writing all signal bin contents to txt files
    sig_file1 = open('PtValues500.txt', 'w')
    #sig_file3, sig_file4 = open('sig_content3.txt', 'w'), open('sig_content4.txt', 'w')
    sig_files = [sig_file1]
    for j in range(len(sig_histos)):
        for bi in range(0, 52):
            sig_files[j].write(str(sig_histos[j].GetBinContent(bi)) + '\n')
    sig_file1.close()

    print 'Done'
