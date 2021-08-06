from ROOT import *

XX500 = TFile("XX500.root");
XX1000 = TFile("XX1000.root");
XX1500 = TFile("XX1500.root");
XX2000 = TFile("XX2000.root");
ZZZdata = TFile("Background.root");

h_XX500Phi = XX500.Get("XXMassPhi");
h_XX1000Phi = XX1000.Get("XXMassPhi");
h_XX1500Phi = XX1500.Get("XXMassPhi");
h_XX2000Phi = XX2000.Get("XXMassPhi");

h_ZZZPhi = ZZZdata.Get("XXMassPhi");
h_ZZZPt = ZZZdata.Get("XXMassPt");
h_ZZZEta = ZZZdata.Get("XXMassEta");

h_XX500Pt = XX500.Get("XXMassPt");
h_XX1000Pt = XX1000.Get("XXMassPt");
h_XX1500Pt = XX1500.Get("XXMassPt");
h_XX2000Pt = XX2000.Get("XXMassPt");

h_XX500Eta = XX500.Get("XXMassEta");
h_XX1000Eta = XX1000.Get("XXMassEta");
h_XX1500Eta = XX1500.Get("XXMassEta");
h_XX2000Eta = XX2000.Get("XXMassEta");

scaleXX500Phi = (h_XX500Phi.GetEntries()/10000) * 100000 * .0000013291;
scaleXX1000Phi = (h_XX1000Phi.GetEntries()/10000) * 100000 * .0000016211;
scaleXX1500Phi = (h_XX1500Phi.GetEntries()/10000) * 100000 * .000001233;
scaleXX2000Phi = (h_XX2000Phi.GetEntries()/10000) * 100000 * .0000007886;

scaleXX500Pt = (h_XX500Pt.GetEntries()/10000) * 100000 * .0000013291;
scaleXX1000Pt = (h_XX1000Pt.GetEntries()/10000) * 100000 * .0000016211;
scaleXX1500Pt = (h_XX1500Pt.GetEntries()/10000) * 100000 * .000001233;
scaleXX2000Pt = (h_XX2000Pt.GetEntries()/10000) * 100000 * .0000007886;

scaleXX500Eta = (h_XX500Eta.GetEntries()/10000) * 100000 * .0000013291;
scaleXX1000Eta = (h_XX1000Eta.GetEntries()/10000) * 100000 * .0000016211;
scaleXX1500Eta = (h_XX1500Eta.GetEntries()/10000) * 100000 * .000001233;
scaleXX2000Eta = (h_XX2000Eta.GetEntries()/10000) * 100000 * .0000007886;

scaleZZZPhi = (h_ZZZPhi.GetEntries()/200000) * 100000 * .64666;
scaleZZZPt = (h_ZZZPt.GetEntries()/200000) * 100000 * .64666;
scaleZZZEta = (h_ZZZEta.GetEntries()/200000) * 100000 * .64666;

nBins = h_ZZZPhi.GetNbinsX() + 1

h_ZZZPhi.Scale(scaleZZZPhi/h_ZZZPhi.Integral(0, nBins));
h_ZZZPt.Scale(scaleZZZPt/h_ZZZPt.Integral(0, nBins));
h_ZZZEta.Scale(scaleZZZEta/h_ZZZEta.Integral(0, nBins));

h_XX500Phi.Scale(scaleXX500Phi/h_XX500Phi.Integral(0, nBins));
h_XX1000Phi.Scale(scaleXX1000Phi/h_XX1000Phi.Integral(0, nBins));
h_XX1500Phi.Scale(scaleXX1500Phi/h_XX1500Phi.Integral(0, nBins));
h_XX2000Phi.Scale(scaleXX2000Phi/h_XX2000Phi.Integral(0, nBins));

h_XX500Pt.Scale(scaleXX500Pt/h_XX500Pt.Integral(0, nBins));
h_XX1000Pt.Scale(scaleXX1000Pt/h_XX1000Pt.Integral(0, nBins));
h_XX1500Pt.Scale(scaleXX1500Pt/h_XX1500Pt.Integral(0, nBins));
h_XX2000Pt.Scale(scaleXX2000Pt/h_XX2000Pt.Integral(0, nBins));

h_XX500Eta.Scale(scaleXX500Eta/h_XX500Eta.Integral(0, nBins));
h_XX1000Eta.Scale(scaleXX1000Eta/h_XX1000Eta.Integral(0, nBins));
h_XX1500Eta.Scale(scaleXX1500Eta/h_XX1500Eta.Integral(0, nBins));
h_XX2000Eta.Scale(scaleXX2000Eta/h_XX2000Eta.Integral(0, nBins));


for mass in [500, 1000, 1500, 2000]:
    if (mass == 500):
        histPhi = h_XX500Phi;
        histPt = h_XX500Pt;
        histEta = h_XX500Eta;
    elif (mass == 1000):
        histPhi = h_XX1000Phi;
        histPt = h_XX1000Pt;
        histEta = h_XX1000Eta;
    elif (mass == 1500):
        histPhi = h_XX1500Phi;
        histPt = h_XX1500Pt;
        histEta = h_XX1500Eta;
    else:
        histPhi = h_XX2000Phi;
        histPt = h_XX2000Pt;
        histEta = h_XX2000Eta;
    Zpt = open("txtFiles/ZZZPtValues"+str(mass)+".txt", "w");
    Zphi = open("txtFiles/ZZZPhiValues"+str(mass)+".txt", "w");
    Zeta = open("txtFiles/ZZZEtaValues"+str(mass)+".txt", "w");

    for ibin in range(0, h_ZZZPhi.GetNbinsX() + 2):
        bkg1content = h_ZZZPhi.GetBinContent(ibin);
        bkg2content = h_ZZZPt.GetBinContent(ibin);
        bkg3content = h_ZZZEta.GetBinContent(ibin);

        Zphi.write(str(bkg1content) + "\n");
        Zpt.write(str(bkg2content) + "\n");
        Zeta.write(str(bkg3content) + "\n");

    nbins = histPhi.GetNbinsX();

    pt = open("txtFiles/PtValues"+str(mass)+".txt", "w");
    phi = open("txtFiles/PhiValues"+str(mass)+".txt", "w");
    eta = open("txtFiles/EtaValues"+str(mass)+".txt", "w");
    for ibin in range(0, nbins + 2):
        data1content = histPhi.GetBinContent(ibin);
        data2content = histPt.GetBinContent(ibin);
        data3content = histEta.GetBinContent(ibin);

        phi.write(str(data1content) + "\n");
        pt.write(str(data2content) + "\n");
        eta.write(str(data3content) + "\n");




