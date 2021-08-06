from ROOT import *
import ast

f = open("txtFiles/results.txt", "r")
contents = f.read()
results = ast.literal_eval(contents)

XX500 = TFile("XX500.root");
XX1000 = TFile("XX1000.root");
XX1500 = TFile("XX1500.root");
XX2000 = TFile("XX2000.root");

h_XX500Pt = XX500.Get("XXMassPt");
h_XX1000Pt = XX1000.Get("XXMassPt");
h_XX1500Pt = XX1500.Get("XXMassPt");
h_XX2000Pt = XX2000.Get("XXMassPt");

#for x, y in results.items():
   # print("Scale Factor " + x + ": " + str(y))

print("Scale Factor 500Pt: " + str(results["Pt500"]))
print("Scale Factor 1000Pt: " + str(results["Pt1000"]))
print("Scale Factor 1500Pt: " + str(results["Pt1500"]))
print("Scale Factor 2000Pt: " + str(results["Pt2000"]))

print("500 Pt Scaled Expected Value: " + str(h_XX500Pt.GetEntries()/10000 * 100000 * .0000041181 * results["Pt500"]))
print("1000 Pt Scaled Expected Value: " + str(h_XX1000Pt.GetEntries()/25000 * 100000 * .000005245 * results["Pt1000"]))
print("1500 Pt Scaled Expected Value: " + str(h_XX1500Pt.GetEntries()/10000 * 100000 * .0000040391 * results["Pt1500"]))
print("2000 Pt Scaled Expected Value: " + str(h_XX2000Pt.GetEntries()/10000 * 100000 * .0000025785 * results["Pt2000"]))
