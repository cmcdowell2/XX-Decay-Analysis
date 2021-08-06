import pyhf
import math


def calculate(signal, scale):
    scale_signal = [i * scale for i in signal]
    print(data_hist)
    pdf = pyhf.simplemodels.hepdata_like(signal_data=scale_signal, bkg_data=bkg_hist, bkg_uncerts=bkg_uncert_hist)
    CLs_o, CLs_e = pyhf.infer.hypotest(1.0, data_hist + pdf.config.auxdata, pdf, return_expected=True)
    return CLs_o, CLs_e


global results
results = {}

for mass in [500]:
    print("THIS IS " + str(mass))
    for x in ["Pt"]:
        print("THIS IS " + x + " METHOD")
        with open(x + "Values" + str(mass) + ".txt") as f:
            signal = f.read().splitlines()
        with open("ZZZ" + x + "Values.txt") as f:
            bkg = f.read().splitlines()

        signal_hist = [float(i) for i in signal]
        bkg_hist = [float(i) for i in bkg]

    
        while bkg_hist.count(0) > 0:
           # for all bins except for the last (b/c it causes problems)
           for i in range(len(bkg_hist) - 1):
            
               # if index passes length of background list or it reaches the end, break loop
               if (len(bkg_hist) == (i+1)) or (len(bkg_hist) == i):
                   break
            
               # if the LAST zero left is at the END of the list, break loop
               if (bkg_hist.count(0) == 1) and (bkg_hist[-1] == 0):
                   break
            
               # if current index is 0, remove background bin and merge correpsponding signal with adjacent bin
               if bkg_hist[i] == 0:
                   zero_sig = signal_hist[i]
                   bkg_hist.pop(i)
                   signal_hist.pop(i)
                   signal_hist[i] += zero_sig

        
           # Fixing case where the last bkg_range bin = 0
           if bkg_hist[-1] == 0:
               zero_sig = signal_hist[-1]
               bkg_hist.pop(-1)
               signal_hist.pop(-1)
               signal_hist[-1] += zero_sig
           # Fixing case where first bkg_range bin = 0
           if bkg_hist[0] == 0:
               zero_sig = signal_hist[0]
               bkg_hist.pop(0)
               signal_hist.pop(0)
               signal_hist[0] += zero_sig
        pass


        data_hist = [round(i) for i in bkg_hist]
        bkg_uncert_hist = [i * 0.5 for i in bkg_hist]
        
        scale0 = .85
        scale_list = []
        CLs = []
        deltas = []
        CLs_exp0 = 1
        #CLs_obs0, CLs_exp0 = calculate(signal_hist, scale0)
        count = 1
        while CLs_exp0 > 0.045:
            """if (math.fabs(CLs_exp0 - 0.05) < 0.000000005):
                results[x + str(mass)] = scale0
                break
            scale0 += scale0 * (CLs_exp0 - 0.05)
            CLs_obs0, CLs_exp0 = calculate(signal_hist, scale0)
            count += 1"""

            CLs_obs0, CLs_exp0 = calculate(signal_hist, scale0)
            if 0 <= (0.05 - CLs_exp0) <= 0.01:
                scale_list.append(scale0)
                deltas.append(abs(0.05 - CLs_exp0))
                CLs.append(CLs_exp0)
            
            scale0 += .01
            scale0 = round(scale0, 3)
            print(scale0)

        #results[x + str(mass)] = scale_list[deltas.index(min(deltas))]
        CLs_exp = CLs[deltas.index(min(deltas))]
        scale_factor = scale_list[deltas.index(min(deltas))]

        
    print("----------------------------------------")
    
print('CLs_exp: {}, scale_factor: {}'.format(CLs_exp, scale_factor))

