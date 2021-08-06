#include <TFile.h>
#include <TTree.h>
#include <TH1F.h>
#include <TBranch.h>
#include <TCanvas.h>
#include <TLorentzVector.h>
#include <TMath.h>
#include <iostream>

using namespace std;
void XXZRecon(const char *filepath, const char *outputFilename) {
  float_t Ele_PT[8], Ele_Eta[8], Ele_Phi[8], Jet_PT[8], Jet_Eta[8], Jet_Phi[8], Jet_Mass[8];
  int Ele_Size = 0;
  int Jet_Size = 0;
  int Ele_Charge[8];

  TFile *file = new TFile(filepath);
  file->cd();

  TTree *tree = (TTree* )file->Get("Delphes");
  tree->SetBranchAddress("Electron.PT", &Ele_PT);
  tree->SetBranchAddress("Electron.Eta", &Ele_Eta);
  tree->SetBranchAddress("Electron.Phi", &Ele_Phi);
  tree->SetBranchAddress("Electron_size", &Ele_Size);
  tree->SetBranchAddress("Electron.Charge", &Ele_Charge);
  tree->SetBranchAddress("FatJet_size", &Jet_Size);
  tree->SetBranchAddress("FatJet.PT", &Jet_PT);
  tree->SetBranchAddress("FatJet.Eta", &Jet_Eta);
  tree->SetBranchAddress("FatJet.Phi", &Jet_Phi);
  tree->SetBranchAddress("FatJet.Mass", &Jet_Mass);
  TLorentzVector M1, M2, D1, D2;

  TFile *outputFile = new TFile(outputFilename, "RECREATE");
  outputFile->cd();


  TH1F *XXMassPhi, *XXMassPt, *Z1Mass, *Z2Mass, *Z3Mass, *XXMassEta;
  XXMassPhi = new TH1F("XXMassPhi", "XX Mass Phi", 50, 100, 2400);
  XXMassPt = new TH1F("XXMassPt", "XX Mass Pt", 50, 100, 2400);
  XXMassEta = new TH1F("XXMassEta", "XX Mass Eta", 50, 100, 2400);
  Z1Mass = new TH1F("Z1Mass", "First Z Mass", 50, 0, 200);
  Z2Mass = new TH1F("Z2Mass", "Second Z Mass", 50, 0, 200);
  Z3Mass = new TH1F("Z3Mass", "Third Z Mass", 50, 0, 200);

  TLorentzVector Z1, Z2, Z3;
  Long64_t nEntries = tree->GetEntries();
  vector<TLorentzVector> electrons, positrons;
  vector<float> deltas, jdeltas;
  vector<TLorentzVector> bosons, jets;

  for (int i = 0; i < nEntries; i++) {
	  electrons.clear();
	  positrons.clear();
	  deltas.clear();
	  jdeltas.clear();
	  bosons.clear();
	  jets.clear();


	  tree->GetEntry(i);
	  int count = 1;
	  for (int j = 0; j <  Ele_Size; j++) {
		if (Ele_Charge[j] == -1) {
			D1.SetPtEtaPhiM(fabs(Ele_PT[j]),Ele_Eta[j],Ele_Phi[j],0.0);
			electrons.push_back(D1);
		} else if (Ele_Charge[j] == 1) {
			D2.SetPtEtaPhiM(Ele_PT[j],Ele_Eta[j],Ele_Phi[j],0.0);
			positrons.push_back(D2);
		}
	  }


		if (electrons.size() >= 1 && positrons.size() >= 1 && Jet_Size >= 2) {
			for (int i = 0; i < Jet_Size; i++) { 
				M1.SetPtEtaPhiM(Jet_PT[i],Jet_Eta[i],Jet_Phi[i],Jet_Mass[i]);
				jets.push_back(M1);
			}
			
			bosons = pairLeps(electrons, positrons);

			bosons = findFinal(bosons, 1);
			jets = findFinal(jets, 2);

			Z1 = bosons.at(0);
			Z2 = jets.at(0);
			Z3 = jets.at(1);

			Z1Mass->Fill(Z1.M());
			Z2Mass->Fill(Z2.M());
			Z3Mass->Fill(Z3.M());

			bosons.push_back(jets.at(0));
			bosons.push_back(jets.at(1));

			float ptMass = findMass(bosons, "pt");
			float phiMass = findMass(bosons, "phi");
			float etaMass = findMass(bosons, "eta");

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

float findMass(vector<TLorentzVector> list, string method) {
	vector<TLorentzVector> pairs, options;
	vector<float> deltas, pairDeltas;
	TLorentzVector Z1, Z2;
	pairDeltas.clear();
	pairs.clear();

	for (int i = 0; i < list.size(); i++) {
		deltas.clear();
		options.clear();
		Z1 = list.at(i);
		for (int j = 0; j < list.size(); j++) {
			if (i != j) {
				Z2 = list.at(j);
				options.push_back(Z1 + Z2);
				if (method == "pt")
					deltas.push_back(fabs(Z1.Pt() - Z2.Pt()));
				else if (method == "eta")
					deltas.push_back(fabs(Z1.Eta() - Z2.Eta()));
				else if (method == "phi")
					deltas.push_back(fabs(Z1.Phi() - Z2.Phi()));
			}
		}

		if (deltas.size() > 0) {
			vector<float>::iterator maxit = max_element(deltas.begin(), deltas.end());
			int max = distance(deltas.begin(), maxit);
			pairDeltas.push_back(deltas.at(max));
			pairs.push_back(options.at(max));
		}
	}
	vector<float>::iterator maxit = max_element(pairDeltas.begin(), pairDeltas.end());
	int max = distance(pairDeltas.begin(), maxit);
	return (pairs.at(max)).M();
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




