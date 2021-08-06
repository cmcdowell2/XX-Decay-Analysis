# XX-Decay-Analysis

This houses all of the code I have written for the XX particle decay analysis. 
The XX particle is a theoretical particle that we are investigating to see if it is worth searching for in actual LHC data. This is a preliminary phenomological study using Madgraph+pythia8+delphes samples.


It works fairly simply, and all of the different decay chains have the same mechanism with slight differences based on which particles are desired to recreate.

Execute the run.sh file to call the commands to run the analysis code (XXZRecon.C) over the samples that Madgraph generated.
Then run PrepStats.py to scale the histograms, extract the bin values, and put them into a text file
Finally the Stats.py code is run, using the bin values of the signal and background through a pyhf function to create a scale factor for each mass value. Currently this scale factor is just being compared between the me and the other student I work with to ensure that the reconstruction methods we are using are consistent. 


For reference, the XX-Decays.PDF file shows all of the theoretical decay chains for this particle that are represented here. There are a few you won't find that haven't been completed.
