#!/bin/bash

root -l -q 'XXZRecon.C("/home/achilles12/Physics/500/2Ele2Jet500/Events/run_01/tag_1_delphes_events.root", "XX500.root")'
root -l -q 'XXZRecon.C("/home/achilles12/Physics/1000/2Ele2Jet1000/Events/run_01/tag_1_delphes_events.root", "XX1000.root")'
root -l -q 'XXZRecon.C("/home/achilles12/Physics/1500/2Ele2Jet1500/Events/run_01/tag_1_delphes_events.root", "XX1500.root")'
root -l -q 'XXZRecon.C("/home/achilles12/Physics/2000/2Ele2Jet2000/Events/run_01/tag_1_delphes_events.root", "XX2000.root")'

root -l -q 'XXZRecon.C("/home/achilles12/Physics/Background/2Ele2JetBackground/Events/run_01/tag_1_delphes_events.root", "Background.root")' 
