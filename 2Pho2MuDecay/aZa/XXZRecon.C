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
float findMass(vector<TLorentzVector> list, TLorentzVector z, string method);

void XXZRecon(const char *filepath, const char *outputFilename) {
  float_t Ele_PT[8], Ele_Eta[8], Ele_Phi[8], Mu_PT[8], Mu_Eta[8], Mu_Phi[8], Jet_PT[8], Jet_Eta[8], Jet_Phi[8], Jet_Mass[8], Pho_PT[8], Pho_Eta[8], Pho_Phi[8];
  int Ele_Size = 0;
  int Mu_Size = 0;
  int Pho_Size = 0;
  int Ele_Charge[8], Mu_Charge[8];
  float dPhi11, dPhi12;
  float dZ11, dZ12;
  float dEta11, dEta12;
  int Phi, Eta;

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

  TFile *outputFile = new TFile(outputFilename, "RECREATE");
  outputFile->cd();


  TH1F *XXMassPhi, *XXMassEta, *XXMassPt, *Z1Mass;
  XXMassPhi = new TH1F("XXMassPhi", "XX Mass Phi", 50, 100, 2400);
  XXMassPt = new TH1F("XXMassPt", "XX Mass Pt", 50, 100, 2400);
  XXMassEta = new TH1F("XXMassEta", "XX Mass Eta", 50, 100, 2400);
  Z1Mass = new TH1F("Z1Mass", "First Z Mass", 50, 0, 200);
  TLorentzVector Z1, P1, P2, D1;
  Long64_t nEntries = tree->GetEntries();
  vector<TLorentzVector> muons, antimuons, bosons, photons;

  for (int i = 0; i < nEntries; i++) {
	muons.clear();
	antimuons.clear();
	bosons.clear();
	photons.clear();

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

	if (muons.size() >= 1 && antimuons.size() >= 1 && Pho_Size >= 2) {
		for (int j = 0; j < Pho_Size; j++) { 
			D1.SetPtEtaPhiM(Pho_PT[j],Pho_Eta[j],Pho_Phi[j],0.0);
			photons.push_back(D1);
		}

		bosons = pairLeps(muons, antimuons);

		bosons = findFinal(bosons, 1);

		Z1 = bosons.at(0);
		Z1Mass->Fill(Z1.M());
		
		float ptMass = findMass(photons, Z1, "pt");
		float phiMass = findMass(photons, Z1, "phi");
		float etaMass = findMass(photons, Z1, "eta");

		XXMassPt->Fill(ptMass);
		XXMassPhi->Fill(phiMass);
		XXMassEta->Fill(etaMass);
	}
}
  outputFile->Write();
  //XXMass->GetXaxis()->SetTitle("Mass (GeV)");
  //XXMass->GetYaxis()->SetTitle("Events");
  //XXMass->Draw();
}

float findMass(vector<TLorentzVector> list, TLorentzVector Z, string method) {
	vector<TLorentzVector> pairs;
	vector<float> deltas;
	TLorentzVector p1;
	deltas.clear();
	pairs.clear();
	
	for (int i = 0; i < list.size(); i++) {
		p1 = list.at(i);
		pairs.push_back(p1 + Z);
		if (method == "pt") 
			deltas.push_back(fabs(Z.Pt() - p1.Pt()));
		else if (method == "eta")
			deltas.push_back(fabs(Z.Eta() - p1.Eta()));
		else if (method == "phi")
			deltas.push_back(fabs(Z.Phi() - p1.Phi()));
	}
	
	vector<float>::iterator minit = max_element(deltas.begin(), deltas.end());
	int min = distance(deltas.begin(), minit);
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
