from ROOT import *
import ast

f = open("txtFiles/results.txt", "r")
contents = f.read()
results = ast.literal_eval(contents)

XX500 = TFile("XX500.root");
XX1000 = TFile("XX1000.root");
XX1500 = TFile("XX1500.root");
XX2000 = TFile("XX2000.root");

h_XX500Phi = XX500.Get("XXMassPhi");
h_XX1000Phi = XX1000.Get("XXMassPhi");
h_XX1500Phi = XX1500.Get("XXMassPhi");
h_XX2000Phi = XX2000.Get("XXMassPhi");

h_XX500Pt = XX500.Get("XXMassPt");
h_XX1000Pt = XX1000.Get("XXMassPt");
h_XX1500Pt = XX1500.Get("XXMassPt");
h_XX2000Pt = XX2000.Get("XXMassPt");

h_XX500Eta = XX500.Get("XXMassEta");
h_XX1000Eta = XX1000.Get("XXMassEta");
h_XX1500Eta = XX1500.Get("XXMassEta");
h_XX2000Eta = XX2000.Get("XXMassEta");

#for x, y in results.items():
   # print("Scale Factor " + x + ": " + str(y))

print("Scale Factor 500Phi: " + str(results["Phi500"]))
print("Scale Factor 1000Phi: " + str(results["Phi1000"]))
print("Scale Factor 1500Phi: " + str(results["Phi1500"]))
print("Scale Factor 2000Phi: " + str(results["Phi2000"]))

print("Scale Factor 500Pt: " + str(results["Pt500"]))
print("Scale Factor 1000Pt: " + str(results["Pt1000"]))
print("Scale Factor 1500Pt: " + str(results["Pt1500"]))
print("Scale Factor 2000Pt: " + str(results["Pt2000"]))

print("Scale Factor 500Eta: " + str(results["Eta500"]))
print("Scale Factor 1000Eta: " + str(results["Eta1000"]))
print("Scale Factor 1500Eta: " + str(results["Eta1500"]))
print("Scale Factor 2000Eta: " + str(results["Eta2000"]))

print("500 Phi Scaled Expected Value: " + str(h_XX500Phi.GetEntries()/10000 * 100000 * .0000039979 * results["Phi500"]))
print("1000 Phi Scaled Expected Value: " + str(h_XX1000Phi.GetEntries()/10000 * 100000 * .0000052399 * results["Phi1000"]))
print("1500 Phi Scaled Expected Value: " + str(h_XX1500Phi.GetEntries()/10000 * 100000 * .000004031 * results["Phi1500"]))
print("2000 Phi Scaled Expected Value: " + str(h_XX2000Phi.GetEntries()/10000 * 100000 * .0000025888 * results["Phi2000"]))

print("500 Pt Scaled Expected Value: " + str(h_XX500Pt.GetEntries()/10000 * 100000 * .0000039979 * results["Pt500"]))
print("1000 Pt Scaled Expected Value: " + str(h_XX1000Pt.GetEntries()/10000 * 100000 * .0000052399 * results["Pt1000"]))
print("1500 Pt Scaled Expected Value: " + str(h_XX1500Pt.GetEntries()/10000 * 100000 * .000004031 * results["Pt1500"]))
print("2000 Pt Scaled Expected Value: " + str(h_XX2000Pt.GetEntries()/10000 * 100000 * .0000025888 * results["Pt2000"]))

print("500 Eta Scaled Expected Value: " + str(h_XX500Eta.GetEntries()/10000 * 100000 * .0000039979 * results["Eta500"]))
print("1000 Eta Scaled Expected Value: " + str(h_XX1000Eta.GetEntries()/10000 * 100000 * .0000052399 * results["Eta1000"]))
print("1500 Eta Scaled Expected Value: " + str(h_XX1500Eta.GetEntries()/10000 * 100000 * .000004031 * results["Eta1500"]))
print("2000 Eta Scaled Expected Value: " + str(h_XX2000Eta.GetEntries()/10000 * 100000 * .0000025888 * results["Eta2000"]))
#
