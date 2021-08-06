#include <TFile.h>
#include <TTree.h>
#include <TH1F.h>
#include <TBranch.h>
#include <TCanvas.h>
#include <TLorentzVector.h>
#include <TMath.h>
#include <iostream>

using namespace std;
vector<TLorentzVector> findFinal(vector<TLorentzVector> list, int num);
vector<TLorentzVector> pairLeps(vector<TLorentzVector> lep, vector<TLorentzVector> antilep);
float findMass(vector<TLorentzVector> list, string method);

void XXZRecon(const char *filepath, const char *outputFilename) {
  float_t Ele_PT[8], Ele_Eta[8], Ele_Phi[8], Mu_PT[8], Mu_Eta[8], Mu_Phi[8], Jet_PT[8], Jet_Eta[8], Jet_Phi[8], Jet_Mass[8], Pho_PT[8], Pho_Eta[8], Pho_Phi[8];
  int Ele_Size = 0;
  int Jet_Size = 0;
  int Mu_Size = 0;
  int Pho_Size = 0;
  int Ele_Charge[8], Mu_Charge[8];

  TFile *file = new TFile(filepath);
  file->cd();

  TTree *tree = (TTree* )file->Get("Delphes");
  tree->SetBranchAddress("Photon.PT", &Pho_PT);
  tree->SetBranchAddress("Photon.Eta", &Pho_Eta);
  tree->SetBranchAddress("Photon.Phi", &Pho_Phi);
  tree->SetBranchAddress("Photon_size", &Pho_Size);
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

  TFile *outputFile = new TFile(outputFilename, "RECREATE");
  outputFile->cd();
  	
  TH1F *XXMassPhi, *XXMassEta, *XXMassPt, *Z1Mass, *Z2Mass;
  XXMassPhi = new TH1F("XXMassPhi", "XX Mass Phi", 50, 100, 2400);
  XXMassPt = new TH1F("XXMassPt", "XX Mass Pt", 50, 100, 2400);
  XXMassEta = new TH1F("XXMassEta", "XX Mass Eta", 50, 100, 2400);
  Z1Mass = new TH1F("Z1Mass", "First Z Mass", 50, 0, 200);
  Z2Mass = new TH1F("Z2Mass", "Second Z Mass", 50, 0, 200);
  TLorentzVector Z1, Z2, Z3, D1;
  Long64_t nEntries = tree->GetEntries();
  vector<TLorentzVector> jets, photons;

  for (int i = 0; i < nEntries; i++) {
	jets.clear();
	photons.clear();

	tree->GetEntry(i);
	
	for (int j = 0; j < Jet_Size; j++) {
		D1.SetPtEtaPhiM(fabs(Jet_PT[j]),Jet_Eta[j],Jet_Phi[j],Jet_Mass[j]);
		jets.push_back(D1);
	}

	if (jets.size() >= 2 && Pho_Size >= 1) {
		for (int i = 0; i < Pho_Size; i++) { 
			D1.SetPtEtaPhiM(Pho_PT[i],Pho_Eta[i],Pho_Phi[i],0.0);
			photons.push_back(D1);
		}

		jets = findFinal(jets, 2);

		Z1 = jets.at(0);
		Z2 = jets.at(1);

		XXMassPt->Fill((Z1 + Z2).M());
		Z1Mass->Fill(Z1.M());
		Z2Mass->Fill(Z2.M());
	}
}
  outputFile->Write();
}

float findMass(vector<TLorentzVector> list, string method) {
	vector<TLorentzVector> pairs, options;
	vector<float> deltas, pairDeltas;
	TLorentzVector p1;
	pairDeltas.clear();
	pairs.clear();
	
	for (int i = 0; i < list.size(); i++) {
		deltas.clear();
		options.clear();
		p1 = list.at(i);
		for (int j = 0; j < list.size(); j++) {
			options.push_back(p1);
			if (method == "pt") 
				deltas.push_back(fabs(p1.Pt()));
			else if (method == "eta")
				deltas.push_back(fabs(p1.Eta()));
			else if (method == "phi")
				deltas.push_back(fabs(p1.Phi()));
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
	return (pairs.at(min)).M();
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
