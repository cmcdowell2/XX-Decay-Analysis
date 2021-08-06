#!/usr/bin/python

from ROOT import *
from sys import argv
from sys import path
import os

    
c1 = TCanvas("c1", "canvas1", 800, 800);
c2 = TCanvas("c2", "canvas2", 800, 800);
c3 = TCanvas("c3", "canvas3", 800, 800);
c4 = TCanvas("c4", "canvas4", 800, 800);
gStyle.SetOptStat(0)
gStyle.SetLegendBorderSize(0);

pad1 = TPad("pad1","pad1",0.01,0.25,0.99,0.99);
pad2 = TPad("pad2", "pad2", 0.01, 0.01, 0.99, 0.25);

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

h_XX500Pt = XX500.Get("XXMassPt");
h_XX1000Pt = XX1000.Get("XXMassPt");
h_XX1500Pt = XX1500.Get("XXMassPt");
h_XX2000Pt = XX2000.Get("XXMassPt");

h_XX500Phi.SetTitle("");
h_XX500Phi.GetXaxis().SetTitle("Mass (GeV)");
h_XX500Phi.GetXaxis().SetTitleOffset(1.2);
h_XX500Phi.GetYaxis().SetTitle("Events");
h_XX500Phi.GetYaxis().SetTitleOffset(1.3);

h_XX1000Phi.SetTitle("");
h_XX1000Phi.GetXaxis().SetTitle("Mass (GeV)");
h_XX1000Phi.GetXaxis().SetTitleOffset(1.2);
h_XX1000Phi.GetYaxis().SetTitle("Events");
h_XX1000Phi.GetYaxis().SetTitleOffset(1.3);

h_XX1500Phi.SetTitle("");
h_XX1500Phi.GetXaxis().SetTitle("Mass (GeV)");
h_XX1500Phi.GetXaxis().SetTitleOffset(1.2);
h_XX1500Phi.GetYaxis().SetTitle("Events");
h_XX1500Phi.GetYaxis().SetTitleOffset(1.3);

h_XX2000Phi.SetTitle("");
h_XX2000Phi.GetXaxis().SetTitle("Mass (GeV)");
h_XX500Phi.GetXaxis().SetTitleOffset(1.2);
h_XX2000Phi.GetYaxis().SetTitle("Events");
h_XX2000Phi.GetYaxis().SetTitleOffset(1.3);


h_XX500Phi.SetLineColor(kRed-4);
h_XX500Pt.SetLineColor(kBlack);
h_XX1000Phi.SetLineColor(kRed-4);
h_XX1000Pt.SetLineColor(kBlack);
h_XX1500Phi.SetLineColor(kRed-4);
h_XX1500Pt.SetLineColor(kBlack);
h_XX2000Phi.SetLineColor(kRed-4);
h_XX2000Pt.SetLineColor(kBlack);
#h_ZZZ.SetLineColor(kGray+2);

scaleXX500Phi = (h_XX500Phi.GetEntries()/10000) * 100000 * .0000000054493;
scaleXX1000Phi = (h_XX1000Phi.GetEntries()/10000) * 100000 * .0000000072142;
scaleXX1500Phi = (h_XX1500Phi.GetEntries()/10000) * 100000 * .0000000055507;
scaleXX2000Phi = (h_XX2000Phi.GetEntries()/10000) * 100000 * .0000000035751;

scaleXX500Pt = (h_XX500Pt.GetEntries()/10000) * 100000 * .0000000054493;
scaleXX1000Pt = (h_XX1000Pt.GetEntries()/10000) * 100000 * .0000000072142;
scaleXX1500Pt = (h_XX1500Pt.GetEntries()/10000) * 100000 * .0000000055507;
scaleXX2000Pt = (h_XX2000Pt.GetEntries()/10000) * 100000 * .0000000035751;

scaleZZZPhi = (h_ZZZPhi.GetEntries()/10000) * 100000 * .00000039569;
scaleZZZPt = (h_ZZZPt.GetEntries()/10000) * 100000 * .00000039569;

nBins = h_ZZZPhi.GetNbinsX() + 1

h_ZZZPhi.Scale(scaleZZZPhi/h_ZZZPhi.Integral(0, nBins));
h_ZZZPt.Scale(scaleZZZPt/h_ZZZPt.Integral(0, nBins));

h_XX500Phi.Scale(scaleXX500Phi/h_XX500Phi.Integral(0, nBins));
h_XX1000Phi.Scale(scaleXX1000Phi/h_XX1000Phi.Integral(0, nBins));
h_XX1500Phi.Scale(scaleXX1500Phi/h_XX1500Phi.Integral(0, nBins));
h_XX2000Phi.Scale(scaleXX2000Phi/h_XX2000Phi.Integral(0, nBins));

h_XX500Pt.Scale(scaleXX500Pt/h_XX500Pt.Integral(0, nBins));
h_XX1000Pt.Scale(scaleXX1000Pt/h_XX1000Pt.Integral(0, nBins));
h_XX1500Pt.Scale(scaleXX1500Pt/h_XX1500Pt.Integral(0, nBins));
h_XX2000Pt.Scale(scaleXX2000Pt/h_XX2000Pt.Integral(0, nBins));

#--------------------------------------------------------
xmin = h_XX500Phi.GetXaxis().GetXmin();
xmax = h_XX500Phi.GetXaxis().GetXmax();
yaxis = TGaxis(xmin, 0, xmin, 2.2, 0, 2.2, 6, "");     
yaxis.SetLabelFont(42);
yaxis.SetLabelSize(0.10);

xaxis = TGaxis(xmin, 0, xmax, 0, xmin, xmax, 510);
xaxis.SetLabelFont(42);
xaxis.SetLabelSize(0.10);
#--------------------------------------------------------

for mass in [500, 1000, 1500, 2000]:
    Zpt = open("ZZZPtValues"+str(mass)+".txt", "w");
    Zphi = open("ZZZPhiValues"+str(mass)+".txt", "w");
    
    for ibin in range(1, h_ZZZPhi.GetNbinsX() + 1):
        bkg1content = h_ZZZPhi.GetBinContent(ibin);
        bkg2content = h_ZZZPt.GetBinContent(ibin);

        Zphi.write(str(bkg1content) + "\n");
        Zpt.write(str(bkg2content) + "\n");


for mass in [500, 1000, 1500, 2000]:
    if (mass == 500):
        c = c1;
        histPhi = h_XX500Phi;
        histPt = h_XX500Pt;
    elif (mass == 1000):
        c = c2;
        histPhi = h_XX1000Phi;
        histPt = h_XX1000Pt;
    elif (mass == 1500):
        c = c3;
        histPhi = h_XX1500Phi;
        histPt = h_XX1500Pt;
    else:
        c = c4;
        histPhi = h_XX2000Phi;
        histPt = h_XX2000Pt;
    
    c.cd();
    pad1.Draw();
    pad1.cd();
    pad1.SetLogy();
    pad1.SetFillColor(0); pad1.SetFrameBorderMode(0); pad1.SetBorderMode(0);
    pad1.SetBottomMargin(0.);
    histPhi.Draw("hist");
    histPt.Draw("hist same");
    if (mass != 2000):
        leg = TLegend(0.65, 0.7, 0.85, 0.85,"");
        leg.AddEntry(histPhi, "XX Mass From Phi");
        leg.AddEntry(histPt, "XX Mass From Pt");
        leg.SetFillColor(kWhite);
        leg.SetFillStyle(0);
        leg.SetTextSize(0.025);
        leg.Draw();
    else:
        leg = TLegend(0.1, 0.7, 0.3, 0.85,"");
        leg.AddEntry(histPhi, "XX Mass From Phi");
        leg.AddEntry(histPt, "XX Mass From Pt");
        leg.SetFillColor(kWhite);
        leg.SetFillStyle(0);
        leg.SetTextSize(0.025);
        leg.Draw();

    c.cd();
    pad2.Draw();
    pad2.cd();
    pad2.SetFillColor(0); pad2.SetFrameBorderMode(0); pad2.SetBorderMode(0);
    pad2.SetTopMargin(0);
    pad2.SetBottomMargin(0.35);
    
    nbins = histPhi.GetNbinsX();
    Ratio = histPhi.Clone("Ratio");
    
    pt = open("PtValues"+str(mass)+".txt", "w");
    phi = open("PhiValues"+str(mass)+".txt", "w");
    for ibin in range(1, nbins + 1):
        data1content = histPhi.GetBinContent(ibin);
        data2content = histPt.GetBinContent(ibin);

        phi.write(str(data1content) + "\n");
        pt.write(str(data2content) + "\n");

        ratiocontent = 0;
        if (data1content != 0 and data2content != 0):
            ratiocontent = (data2content)/(data1content);
        Ratio.SetBinContent(ibin,  ratiocontent);
    
    Ratio.GetYaxis().SetRangeUser(0.0, 2.2);
    Ratio.SetStats(0);
    Ratio.GetYaxis().CenterTitle();
    Ratio.SetMarkerStyle(20);
    Ratio.SetMarkerSize(0.7);

    line = TLine(histPhi.GetXaxis().GetXmin(), 1., histPhi.GetXaxis().GetXmax(), 1.);
    line.SetLineStyle(8);

    Ratio.Draw("p");
    line.SetLineColor(kBlack);
    line.Draw("same");
    yaxis.Draw("same");
    xaxis.Draw("same");

    Ratio.GetYaxis().SetTitle("PtData/PhiData");
    Ratio.GetYaxis().SetLabelSize(0.14);
    Ratio.GetYaxis().SetTitleSize(0.10);
    Ratio.GetYaxis().SetLabelFont(42);
    Ratio.GetYaxis().SetTitleFont(42);
    Ratio.GetYaxis().SetTitleOffset(0.3);
    Ratio.GetYaxis().SetNdivisions(100);
    Ratio.GetYaxis().SetTickLength(0.05);

    Ratio.GetXaxis().SetLabelSize(0.1);
    Ratio.GetXaxis().SetTitleSize(0.12);
    Ratio.GetXaxis().SetLabelFont(42);
    Ratio.GetXaxis().SetTitleFont(42);
    Ratio.GetXaxis().SetTitleOffset(0.9);
    Ratio.GetXaxis().SetTickLength(0.05);

    c.Update();
    #c.SaveAs("/mnt/c/Users/Cameron/Pictures/Screenshots/XXMassComparison" + str(mass) + ".png");
    
