#!/bin/bash

root -l -q 'XXZRecon.C("/home/achilles12/Physics/500/2Pho1JetW500/Events/run_01/tag_1_delphes_events.root", "XX500.root")'
root -l -q 'XXZRecon.C("/home/achilles12/Physics/1000/2Pho1JetW1000/Events/run_01/tag_1_delphes_events.root", "XX1000.root")'
root -l -q 'XXZRecon.C("/home/achilles12/Physics/1500/2Pho1JetW1500/Events/run_01/tag_1_delphes_events.root", "XX1500.root")'
root -l -q 'XXZRecon.C("/home/achilles12/Physics/2000/2Pho1JetW2000/Events/run_01/tag_1_delphes_events.root", "XX2000.root")'

root -l -q 'XXZRecon.C("/home/achilles12/Physics/Background/2Pho1JetBackground/Events/run_01/tag_1_delphes_events.root", "Background.root")' 
