import pyhf
import math


def calculate(data, scale):
    data = [i * scale for i in data]
    pdf = pyhf.simplemodels.hepdata_like(signal_data=data, bkg_data=bkg_hist, bkg_uncerts=bkg_uncert_hist)
    CLs_o, CLs_e = pyhf.infer.hypotest(1.0, data_hist + pdf.config.auxdata, pdf, return_expected=True)
    return CLs_o, CLs_e


global results


results = {}
for mass in [1000]:
    print("THIS IS " + str(mass))
    for x in ["Pt"]:
        print("THIS IS " + x + " METHOD")
        with open(x + "Values" + str(mass) + ".txt") as f:
            signal = f.read().splitlines()
        with open("ZZZ" + x + "Values" + ".txt") as f:
            bkg = f.read().splitlines()

        signal_hist = [float(i) for i in signal]
        bkg_hist = [float(i) for i in bkg]

        data_hist = [round(i) for i in bkg_hist]

    
        for i in bkg_hist:
            indices = [i for i, e in enumerate(bkg_hist) if e == 0.0]

        for i in sorted(indices, reverse = True):
            del bkg_hist[i]
            del data_hist[i]
            
            if (i == 0):
                signal_hist[i+1] = signal_hist[i] + signal_hist[i+1]
            else:
                signal_hist[i-1] = signal_hist[i] + signal_hist[i-1]
            del signal_hist[i]
        
        bkg_uncert_hist = [i * 0.5 for i in bkg_hist]
        
        scale0 = 1000
        
        CLs_obs0, CLs_exp0 = calculate(signal_hist, scale0)
        count = 1
        while (count < 1000):
            if (math.fabs(CLs_exp0 - 0.05) < 0.0005):
                results[x + str(mass)] = scale0
                break
            scale0 += scale0 * (CLs_exp0 - 0.05)
            CLs_obs0, CLs_exp0 = calculate(signal_hist, scale0)
            print("Confidence Level: " + str(CLs_exp0))
            count += 1
        
    print("----------------------------------------")
    

f = open("results.txt", "w")
f.write(str(results))
f.close()

"""
# background uncertainty, per bin
bkg_hist = [1.0,1.0]

bkg_uncert_hist = [0.01, 0.01]

# signal histogram
signal_hist = [12.0, 11.0]

#bkg_hist = [1.0, 1.0]
# observed data
data_hist = [0,0]

# make the PDF
pdf = pyhf.simplemodels.hepdata_like(signal_data=signal_hist, bkg_data=bkg_hist, bkg_uncerts=bkg_uncert_hist)

# get the results
CLs_obs, CLs_exp = pyhf.infer.hypotest(1.0, data_hist + pdf.config.auxdata, pdf, return_expected=True)

# display
print('Observed: {}, Expected: {}'.format(CLs_obs, CLs_exp))

# Roughly, the expected limit  on this hypothesis is at a CL of 1-CLs_exp 
# if you want a confidence level of 95%, scale your signal up or down until CLs_exp = 0.05
"""
