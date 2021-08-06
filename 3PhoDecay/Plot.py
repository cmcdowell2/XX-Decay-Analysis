#!/usr/bin/python

from ROOT import *
from sys import argv
from sys import path
import ast
import os

for x in ["Pt"]:
    c = TCanvas("c", "canvas", 800, 800);
    gStyle.SetOptStat(0)
    gStyle.SetLegendBorderSize(0);
    c.SetLogy();
    c.cd();

    f = open("txtFiles/results.txt", "r")
    contents = f.read()
    results = ast.literal_eval(contents)

    XX500 = TFile("XX500.root");
    XX1000 = TFile("XX1000.root");
    XX1500 = TFile("XX1500.root");
    XX2000 = TFile("XX2000.root");
    ZZZdata = TFile("Background.root");

    h_XX500 = XX500.Get("XXMass" + x);
    h_XX1000 = XX1000.Get("XXMass" + x);
    h_XX1500 = XX1500.Get("XXMass" + x);
    h_XX2000 = XX2000.Get("XXMass" + x);
    h_ZZZ = ZZZdata.Get("XXMass" + x);

    h_ZZZ.SetTitle("2 Muon Decay Reconstruction " + x);
    h_ZZZ.GetXaxis().SetTitle("Mass (GeV)");
    h_ZZZ.GetXaxis().SetTitleOffset(1.2);
    h_ZZZ.GetYaxis().SetTitle("Events");
    h_ZZZ.GetYaxis().SetTitleOffset(1.3);
    h_XX500.SetLineColor(kRed);
    h_XX1000.SetLineColor(kGreen+1);
    h_XX1500.SetLineColor(kCyan+1);
    h_XX2000.SetLineColor(kViolet);
    h_ZZZ.SetLineColor(kGray+3);

    scaleZZZ = (h_ZZZ.GetEntries()/325000) * 100000 * .10819;
    scaleXX500 = (h_XX500.GetEntries()/25000) * 100000 * .00011836 * results[x + "500"];
    scaleXX1000 = (h_XX1000.GetEntries()/10000) * 100000 * .00014448 * results[x + "1000"];
    scaleXX1500 = (h_XX1500.GetEntries()/10000) * 100000 * .00011251 * results[x + "1500"];
    scaleXX2000 = (h_XX2000.GetEntries()/10000) * 100000 * .000073972 * results[x + "2000"];

    nbins = h_XX500.GetNbinsX() + 1
    h_ZZZ.Scale(scaleZZZ/h_ZZZ.Integral(0, nbins));
    h_XX500.Scale(scaleXX500/h_XX500.Integral(0, nbins));
    h_XX1000.Scale(scaleXX1000/h_XX1000.Integral(0, nbins));
    h_XX1500.Scale(scaleXX1500/h_XX1500.Integral(0, nbins));
    h_XX2000.Scale(scaleXX2000/h_XX2000.Integral(0, nbins));

    h_ZZZ.GetXaxis().SetLabelSize(0.03);

    h_ZZZ.Draw("hist");
    h_XX500.Draw("hist same");
    h_XX1000.Draw("hist same");
    h_XX1500.Draw("hist same");
    h_XX2000.Draw("hist same");

    leg = TLegend(0.65, 0.75, 0.85, 0.9,"");
    leg.AddEntry(h_ZZZ, "ZZZ Background");
    leg.AddEntry(h_XX500, "XX Mass 500 GeV");
    leg.AddEntry(h_XX1000, "XX Mass 1000 GeV");
    leg.AddEntry(h_XX1500, "XX Mass 1500 GeV");
    leg.AddEntry(h_XX2000, "XX Mass 2000 GeV");
    leg.SetFillColor(kWhite);
    leg.SetFillStyle(0);
    leg.SetTextSize(0.025);
    leg.Draw();

    c.SaveAs("/mnt/c/Users/perse/Documents/PhysicsHistos/3PhoMass" + x + ".png");
