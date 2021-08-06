#include <TROOT.h>
#include <TFile.h>
#include <TTree.h>
#include <TH1F.h>
#include <TBranch.h>
#include <TCanvas.h>
#include <TLorentzVector.h>
#include "TLorentzVector.h"
#include <TMath.h>
#include <iostream>

using namespace std;
vector<TLorentzVector> findFinal(vector<TLorentzVector> list, int num);
vector<TLorentzVector> pairLeps(vector<TLorentzVector> lep, vector<TLorentzVector> antilep);
float deltaR(TLorentzVector p1, TLorentzVector p2);
TLorentzVector findMass(vector<TLorentzVector> list, string method);

void XXZRecon(const char *filepath, const char *outputFilename) {
  Float_t Ele_PT[8], Ele_Eta[8], Ele_Phi[8], Mu_PT[8], Mu_Eta[8], Mu_Phi[8], Jet_PT[8], Jet_Eta[8], Jet_Phi[8], Jet_Mass[8];
  //TLorentzVector *SoftDrop1 = new TLorentzVector[8];
  int Ele_Size = 0;
  int Jet_Size = 0;
  int Mu_Size = 0;
  int Ele_Charge[8], Mu_Charge[8];
  float dPhi12, dPhi13, dPhi23;
  float dZ12, dZ13, dZ23;
  float dEta12, dEta13, dEta23;
  int Phi, Eta;

  TFile *file = new TFile(filepath);
  file->cd();

  TTree *tree = (TTree* )file->Get("Delphes");
  tree->SetBranchAddress("Electron.PT", &Ele_PT);
  tree->SetBranchAddress("Electron.Eta", &Ele_Eta);
  tree->SetBranchAddress("Electron.Phi", &Ele_Phi);
  tree->SetBranchAddress("Electron_size", &Ele_Size);
  tree->SetBranchAddress("Electron.Charge", &Ele_Charge);
  tree->SetBranchAddress("Muon.PT", &Mu_PT);
  tree->SetBranchAddress("Muon.Eta", &Mu_Eta);
  tree->SetBranchAddress("Muon.Phi", &Mu_Phi);
  tree->SetBranchAddress("Muon_size", &Mu_Size);
  tree->SetBranchAddress("Muon.Charge", &Mu_Charge);
  tree->SetBranchAddress("FatJet_size", &Jet_Size);
  tree->SetBranchAddress("FatJet.PT", &Jet_PT);
  tree->SetBranchAddress("FatJet.Eta", &Jet_Eta);
  tree->SetBranchAddress("FatJet.Phi", &Jet_Phi);
  tree->SetBranchAddress("FatJet.Mass", &Jet_Mass);
  //tree->SetBranchAddress("FatJet.SoftDroppedSubJet1", &SoftDrop1);
  //tree->SetBranchAddress("FatJet.SoftDroppedSubJet2", &SoftDropJet2);
	
  TFile *outputFile = new TFile(outputFilename, "RECREATE");
  outputFile->cd();


  TH1F *XXMassPhi, *XXMassPt, *Z1Mass, *Z2Mass, *Z3Mass, *XXMassEta;
  XXMassPhi = new TH1F("XXMassPhi", "XX Mass Phi", 50, 100, 2400);
  XXMassPt = new TH1F("XXMassPt", "XX Mass Pt", 50, 100, 2400);
  XXMassEta = new TH1F("XXMassEta", "XX Mass Eta", 50, 100, 2400);
  Z1Mass = new TH1F("Z1Mass", "First Z Mass", 50, 0, 200);
  Z2Mass = new TH1F("Z2Mass", "First Z Mass", 50, 0, 200);
  Z3Mass = new TH1F("Z3Mass", "First Z Mass", 50, 0, 200);
  TLorentzVector Z1, Z2, Z3, D1;
  Long64_t nEntries = tree->GetEntries();
  vector<TLorentzVector> muons, antimuons, bosons, mbosons, jets;

  for (int i = 0; i < nEntries; i++) {
	muons.clear();
	antimuons.clear();
	bosons.clear();
	jets.clear();

	/*for (int j = 0; j < Mu_Size; j++) {
		if (Mu_Charge[j] == -1) {
			D1.SetPtEtaPhiM(fabs(Mu_PT[j]),Mu_Eta[j],Mu_Phi[j],0.0);
			muons.push_back(D1);
		} else if (Mu_Charge[j] == 1) {
			D1.SetPtEtaPhiM(fabs(Mu_PT[j]),Mu_Eta[j],Mu_Phi[j],0.0);
			antimuons.push_back(D1);
		}
	}
	
	for (int i = 0; i < Jet_Size; i++) {
		D1.SetPtEtaPhiM(Jet_PT[i],Jet_Eta[i],Jet_Phi[i],Jet_Mass[i]);
		jets.push_back(D1);
		
	}

	if (muons.size() >= 1 && antimuons.size() >= 1 && jets.size() >= 1) {

		bosons = pairLeps(muons, antimuons);

		bosons = findFinal(bosons, 1);

		Z1 = bosons.at(0);

		//jets = findFinal(jets, 1);
		
		Z1Mass->Fill(Z1.M());

		XXMassPt->Fill((jets.at(0).M()));
	}*/
}
  outputFile->Write();
  //XXMass->GetXaxis()->SetTitle("Mass (GeV)");
  //XXMass->GetYaxis()->SetTitle("Events");
  //XXMass->Draw();
}

vector<TLorentzVector> findFinal(vector<TLorentzVector> list, int num) {
	vector<float> deltas;
	while (list.size() > num) {
		deltas.clear();
		for (int i = 0; i < list.size(); i++) {
			deltas.push_back(fabs(91.1 - list[i].M()));
		}
		vector<float>::iterator maxit = max_element(deltas.begin(), deltas.end());
		int max = distance(deltas.begin(), maxit);
		list.erase(list.begin() + max);
	}

	return list;
}


TLorentzVector findMass(vector<TLorentzVector> list, string method) {
	vector<TLorentzVector> pairs, options;
	vector<float> deltas, pairDeltas;
	TLorentzVector p1, p2;
	pairDeltas.clear();
	pairs.clear();
	
	for (int i = 0; i < list.size(); i++) {
		deltas.clear();
		options.clear();
		p1 = list.at(i);
		for (int j = 0; j < list.size(); j++) {
			if (i != j) {
				p2 = list.at(j);
				options.push_back(p1 + p2);
				deltas.push_back(deltaR(p1, p2));
			}
		}
		if (deltas.size() > 0) {
			vector<float>::iterator minit = min_element(deltas.begin(), deltas.end());
			int min = distance(deltas.begin(), minit);
			pairDeltas.push_back(deltas.at(min));
			pairs.push_back(options.at(min));
		}
	}
	vector<float>::iterator minit = min_element(pairDeltas.begin(), pairDeltas.end());
	int min = distance(pairDeltas.begin(), minit);
	return pairs.at(min);
}

float deltaR(TLorentzVector p1, TLorentzVector p2) {
	float etas = pow((p1.Eta() - p2.Eta()), 2);
	float phis = pow((p1.Phi() - p2.Phi()), 2);
	return pow((etas + phis), .5);
}

vector<TLorentzVector> pairLeps(vector<TLorentzVector> lep, vector<TLorentzVector> antilep) {
	vector<TLorentzVector> pairs;
	vector<float> deltas;
	for (int i = 0; i < lep.size(); i++) {
		deltas.clear();
		for (int j = 0; j < antilep.size(); j++) {
			deltas.push_back(fabs(91.1 - (lep.at(i) + antilep.at(j)).M()));
		}

		vector<float>::iterator minit = min_element(deltas.begin(), deltas.end());
		int min = distance(deltas.begin(), minit);
		pairs.push_back(lep.at(i) + antilep.at(min));
	}

	return pairs;
}
