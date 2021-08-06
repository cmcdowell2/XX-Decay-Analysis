#!/bin/bash

root -l -q 'XXZRecon.C("/home/achilles12/Physics/500/4EleW500/Events/run_01/tag_1_delphes_events.root", "XX500.root")'
root -l -q 'XXZRecon.C("/home/achilles12/Physics/1000/4EleW1000/Events/run_01/tag_1_delphes_events.root", "XX1000.root")'
root -l -q 'XXZRecon.C("/home/achilles12/Physics/1500/4EleW1500/Events/run_01/tag_1_delphes_events.root", "XX1500.root")'
root -l -q 'XXZRecon.C("/home/achilles12/Physics/2000/4EleW2000/Events/run_01/tag_1_delphes_events.root", "XX2000.root")'

root -l -q 'XXZRecon.C("/home/achilles12/Physics/Background/4EleBackground/Events/run_01/tag_1_delphes_events.root", "Background.root")' 
