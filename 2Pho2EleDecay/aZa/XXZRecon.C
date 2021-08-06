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
  int Pho_Size = 0;
  int Ele_Charge[8], Mu_Charge[8];

  TFile *file = new TFile(filepath);
  file->cd();

  TTree *tree = (TTree* )file->Get("Delphes");
  tree->SetBranchAddress("Electron.PT", &Ele_PT);
  tree->SetBranchAddress("Electron.Eta", &Ele_Eta);
  tree->SetBranchAddress("Electron.Phi", &Ele_Phi);
  tree->SetBranchAddress("Electron_size", &Ele_Size);
  tree->SetBranchAddress("Electron.Charge", &Ele_Charge);
  tree->SetBranchAddress("Photon.PT", &Pho_PT);
  tree->SetBranchAddress("Photon.Eta", &Pho_Eta);
  tree->SetBranchAddress("Photon.Phi", &Pho_Phi);
  tree->SetBranchAddress("Photon_size", &Pho_Size);

  TFile *outputFile = new TFile(outputFilename, "RECREATE");
  outputFile->cd();


  TH1F *XXMassPhi, *XXMassEta, *XXMassPt, *Z1Mass;
  XXMassPhi = new TH1F("XXMassPhi", "XX Mass Phi", 50, 100, 2400);
  XXMassPt = new TH1F("XXMassPt", "XX Mass Pt", 50, 100, 2400);
  XXMassEta = new TH1F("XXMassEta", "XX Mass Eta", 50, 100, 2400);
  Z1Mass = new TH1F("Z1Mass", "First Z Mass", 50, 0, 200);
  TLorentzVector Z1, P1, P2, D1;
  Long64_t nEntries = tree->GetEntries();
  vector<TLorentzVector> electrons, positrons, bosons, photons;

  for (int i = 0; i < nEntries; i++) {
	electrons.clear();
	positrons.clear();
	bosons.clear();
	photons.clear();

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

	if (electrons.size() >= 1 && positrons.size() >= 1 && Pho_Size >= 2) {
		for (int i = 0; i < Pho_Size; i++) { 
			D1.SetPtEtaPhiM(Pho_PT[i],Pho_Eta[i],Pho_Phi[i],0.0);
			photons.push_back(D1);
		}

		bosons = pairLeps(electrons, positrons);

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
