#!/bin/bash

root -l -q 'XXZRecon.C("/mnt/e/Users/Cameron/AppData/Local/Packages/CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc/LocalState/rootfs/home/achilles12/Physics/500/1Pho2Ele2MuZZ500/Events/run_01/tag_1_delphes_events.root", "XX500.root")'
root -l -q 'XXZRecon.C("/mnt/e/Users/Cameron/AppData/Local/Packages/CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc/LocalState/rootfs/home/achilles12/Physics/1000/1Pho2Ele2MuZZ1000/Events/run_01/tag_1_delphes_events.root", "XX1000.root")'
root -l -q 'XXZRecon.C("/mnt/e/Users/Cameron/AppData/Local/Packages/CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc/LocalState/rootfs/home/achilles12/Physics/1500/1Pho2Ele2MuZZ1500/Events/run_01/tag_1_delphes_events.root", "XX1500.root")'
root -l -q 'XXZRecon.C("/mnt/e/Users/Cameron/AppData/Local/Packages/CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc/LocalState/rootfs/home/achilles12/Physics/2000/1Pho2Ele2MuZZ2000/Events/run_01/tag_1_delphes_events.root", "XX2000.root")'

root -l -q 'XXZRecon.C("/mnt/e/Users/Cameron/AppData/Local/Packages/CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc/LocalState/rootfs/home/achilles12/Physics/Background/1Pho2Ele2MuBackground/Events/run_01/tag_1_delphes_events.root", "Background.root")' 
