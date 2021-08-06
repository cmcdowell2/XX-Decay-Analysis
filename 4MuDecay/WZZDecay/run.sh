#!/bin/bash

#root -l -q 'XXZRecon.C("tag_1_delphes_events.root", "XX500.root")'
#root -l -q 'XXZRecon.C("tag_8_delphes_events.root", "Background.root")'

root -l -q 'XXZRecon.C("/home/achilles12/Physics/500/4MuonW500/Events/run_01/tag_1_delphes_events.root", "XX500.root")'
root -l -q 'XXZRecon.C("/home/achilles12/Physics/1000/4MuonW1000/Events/run_01/tag_1_delphes_events.root", "XX1000.root")'
root -l -q 'XXZRecon.C("/home/achilles12/Physics/1500/4MuonW1500/Events/run_01/tag_1_delphes_events.root", "XX1500.root")'
root -l -q 'XXZRecon.C("/home/achilles12/Physics/2000/4MuonW2000/Events/run_01/tag_1_delphes_events.root", "XX2000.root")'

root -l -q 'XXZRecon.C("/home/achilles12/Physics/Background/4MuBackground/Events/run_01/tag_1_delphes_events.root", "Background.root")' 
