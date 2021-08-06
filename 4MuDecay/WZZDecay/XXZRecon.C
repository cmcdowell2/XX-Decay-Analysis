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

  TFile *outputFile = new TFile(outputFilename, "RECREATE");
  outputFile->cd();


  TH1F *XXMassPhi, *XXMassPt, *Z1Mass, *Z2Mass, *W1Mass, *XXMassEta;
  XXMassPhi = new TH1F("XXMassPhi", "XX Mass Phi", 50, 100, 2400);
  XXMassPt = new TH1F("XXMassPt", "XX Mass Pt", 50, 100, 2400);
  XXMassEta = new TH1F("XXMassEta", "XX Mass Eta", 50, 100, 2400);
  Z1Mass = new TH1F("Z1Mass", "First Z Mass", 50, 0, 200);
  Z2Mass = new TH1F("Z2Mass", "Second Z Mass", 50, 0, 200);
  W1Mass = new TH1F("W1Mass", "First W Mass", 50, 0, 200);
  TLorentzVector Z1, Z2, W1, D1;
  Long64_t nEntries = tree->GetEntries();
  vector<TLorentzVector> muons, antimuons, bosons, mbosons, jets;

  for (int i = 0; i < nEntries; i++) {
	muons.clear();
	antimuons.clear();
	bosons.clear();
	jets.clear();

	tree->GetEntry(i);
	
	for (int j = 0; j < Mu_Size; j++) {
		if (Mu_Charge[j] == -1) {
			D1.SetPtEtaPhiM(fabs(Mu_PT[j]),Mu_Eta[j],Mu_Phi[j],0.0);
			muons.push_back(D1);
		} else if (Mu_Charge[j] == 1) {
			D1.SetPtEtaPhiM(fabs(Mu_PT[j]),Mu_Eta[j],Mu_Phi[j],0.0);
			antimuons.push_back(D1);
		}
	}

	if (muons.size() >= 2 && antimuons.size() >= 2 && Jet_Size >= 1) {
		for (int i = 0; i < Jet_Size; i++) { 
			D1.SetPtEtaPhiM(Jet_PT[i],Jet_Eta[i],Jet_Phi[i],Jet_Mass[i]);
			jets.push_back(D1);
		}

		bosons = pairLeps(muons, antimuons);

		bosons = findFinal(bosons, 2, 91.1);

		Z1 = bosons.at(0);
		Z2 = bosons.at(1);

		jets = findFinal(jets, 1, 80.4);

		W1 = jets.at(0);
		
		Z1Mass->Fill(Z1.M());
		Z2Mass->Fill(Z2.M());
		W1Mass->Fill(W1.M());

		XXMassPt->Fill((Z1 + Z2).M());
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
