#include <TFile.h>
#include <TTree.h>
#include <TH1F.h>
#include <TBranch.h>
#include <TCanvas.h>
#include <TLorentzVector.h>
#include <TMath.h>
#include <iostream>

using namespace std;
vector<TLorentzVector> findFinal(vector<TLorentzVector> list, int num, float mass);
vector<TLorentzVector> pairLeps(vector<TLorentzVector> lep, vector<TLorentzVector> antilep);

void XXZRecon(const char *filepath, const char *outputFilename) {
  float_t Ele_PT[8], Ele_Eta[8], Ele_Phi[8], Mu_PT[8], Mu_Eta[8], Mu_Phi[8], Jet_PT[8], Jet_Eta[8], Jet_Phi[8], Jet_Mass[8];
  int Ele_Size = 0;
  int Jet_Size = 0;
  int Mu_Size = 0;
  int Ele_Charge[8], Mu_Charge[8];

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

  TFile *outputFile = new TFile(outputFilename, "RECREATE");
  outputFile->cd();


  TH1F *XXMassPt, *Z1Mass, *W1Mass, *W2Mass;
  XXMassPt = new TH1F("XXMassPt", "XX Mass", 50, 100, 2400);
  Z1Mass = new TH1F("Z1Mass", "First Z Mass", 50, 0, 200);
  W1Mass = new TH1F("W1Mass", "First W Mass", 50, 0, 200);
  W2Mass = new TH1F("W2Mass", "Second W Mass", 50, 0, 200);
  TLorentzVector Z1, W1, W2, D1;
  Long64_t nEntries = tree->GetEntries();
  vector<TLorentzVector> electrons, positrons, bosons, jets;

  for (int i = 0; i < nEntries; i++) {
	electrons.clear();
	positrons.clear();
	bosons.clear();
	jets.clear();

	tree->GetEntry(i);
	
	for (int j = 0; j < Ele_Size; j++) {
		if (Ele_Charge[j] == -1) {
			D1.SetPtEtaPhiM(fabs(Ele_PT[j]),Ele_Eta[j],Ele_Phi[j],0.0);
			electrons.push_back(D1);
		} else if (Ele_Charge[j] == 1) {
			D1.SetPtEtaPhiM(fabs(Ele_PT[j]),Ele_Eta[j],Ele_Phi[j],0.0);
			positrons.push_back(D1);
		}
	}

	if (electrons.size() >= 1 && positrons.size() >= 1 && Jet_Size >= 2) {
		for (int i = 0; i < Jet_Size; i++) { 
			D1.SetPtEtaPhiM(Jet_PT[i],Jet_Eta[i],Jet_Phi[i],Jet_Mass[i]);
			jets.push_back(D1);
		}

		bosons = pairLeps(electrons, positrons);

		bosons = findFinal(bosons, 1, 91.1);

		Z1 = bosons.at(0);

		jets = findFinal(jets, 2, 80.4);

		W1 = jets.at(0);
		W2 = jets.at(1);

		Z1Mass->Fill(Z1.M());
		W1Mass->Fill(W1.M());
		W2Mass->Fill(W2.M());

		XXMassPt->Fill((W1 + W2).M());
	}
}
  outputFile->Write();
  //XXMass->GetXaxis()->SetTitle("Mass (GeV)");
  //XXMass->GetYaxis()->SetTitle("Events");
  //XXMass->Draw();
}

vector<TLorentzVector> findFinal(vector<TLorentzVector> list, int num, float mass) {
	vector<float> deltas;
	while (list.size() > num) {
		deltas.clear();
		for (int i = 0; i < list.size(); i++) {
			deltas.push_back(fabs(mass - list[i].M()));
		}
		vector<float>::iterator maxit = max_element(deltas.begin(), deltas.end());
		int max = distance(deltas.begin(), maxit);
		list.erase(list.begin() + max);
	}

	return list;
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
