from ROOT import *

XX500 = TFile("XX500.root");
XX1000 = TFile("XX1000.root");
XX1500 = TFile("XX1500.root");
XX2000 = TFile("XX2000.root");
ZZZdata = TFile("Background.root");

h_ZZZPt = ZZZdata.Get("XXMassPt");

h_XX500Pt = XX500.Get("XXMassPt");
h_XX1000Pt = XX1000.Get("XXMassPt");
h_XX1500Pt = XX1500.Get("XXMassPt");
h_XX2000Pt = XX2000.Get("XXMassPt");

scaleXX500Pt = (h_XX500Pt.GetEntries()/10000) * 100000 * .00000071753;
scaleXX1000Pt = (h_XX1000Pt.GetEntries()/10000) * 100000 * .0000010304;
scaleXX1500Pt = (h_XX1500Pt.GetEntries()/10000) * 100000 * .00000083477;
scaleXX2000Pt = (h_XX2000Pt.GetEntries()/10000) * 100000 * .00000055165;

scaleZZZPt = (h_ZZZPt.GetEntries()/100000) * 100000 * .0066496;

nBins = h_ZZZPt.GetNbinsX() + 1

h_ZZZPt.Scale(scaleZZZPt/h_ZZZPt.Integral(0, nBins));

h_XX500Pt.Scale(scaleXX500Pt/h_XX500Pt.Integral(0, nBins));
h_XX1000Pt.Scale(scaleXX1000Pt/h_XX1000Pt.Integral(0, nBins));
h_XX1500Pt.Scale(scaleXX1500Pt/h_XX1500Pt.Integral(0, nBins));
h_XX2000Pt.Scale(scaleXX2000Pt/h_XX2000Pt.Integral(0, nBins));

for mass in [500, 1000, 1500, 2000]:
    if (mass == 500):
        histPt = h_XX500Pt;
    elif (mass == 1000):
        #histPhi = h_XX1000Phi;
        histPt = h_XX1000Pt;
        #histEta = h_XX1000Eta;
    elif (mass == 1500):
        #histPhi = h_XX1500Phi;
        histPt = h_XX1500Pt;
        #histEta = h_XX1500Eta;
    else:
        #histPhi = h_XX2000Phi;
        histPt = h_XX2000Pt;
        #histEta = h_XX2000Eta;
    Zpt = open("txtFiles/ZZZPtValues"+str(mass)+".txt", "w");
    #Zphi = open("txtFiles/ZZZPhiValues"+str(mass)+".txt", "w");
    #Zeta = open("txtFiles/ZZZEtaValues"+str(mass)+".txt", "w");

    for ibin in range(0, h_ZZZPt.GetNbinsX() + 2):
        #bkg1content = h_ZZZPhi.GetBinContent(ibin);
        bkg2content = h_ZZZPt.GetBinContent(ibin);
        #bkg3content = h_ZZZEta.GetBinContent(ibin);

        #Zphi.write(str(bkg1content) + "\n");
        Zpt.write(str(bkg2content) + "\n");
        #Zeta.write(str(bkg3content) + "\n"); 
    nbins = histPt.GetNbinsX();

    pt = open("txtFiles/PtValues"+str(mass)+".txt", "w");
    #phi = open("txtFiles/PhiValues"+str(mass)+".txt", "w");
    #eta = open("txtFiles/EtaValues"+str(mass)+".txt", "w");
    for ibin in range(0, nbins + 2):
        #data1content = histPhi.GetBinContent(ibin);
        data2content = histPt.GetBinContent(ibin);
        #data3content = histEta.GetBinContent(ibin);

        #phi.write(str(data1content) + "\n");
        pt.write(str(data2content) + "\n");
        #eta.write(str(data3content) + "\n");




