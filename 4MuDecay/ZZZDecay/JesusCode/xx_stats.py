import pyhf


def remove_zeros(background, signal):
    """
    Removes zeros in the background.
    Background bins with 0 will be merged into adjecent bins as well as signals,
    this removes the invalid zero-background but keeps signal strength.
    """
    # While there are still bins with zero background
    while background.count(0) > 0:
        # for all bins except for the last (b/c it causes problems)
        for i in range(len(background) - 1):
            
            # if index passes length of background list or it reaches the end, break loop
            if (len(background) == (i+1)) or (len(background) == i):
                break
            
            # if the LAST zero left is at the END of the list, break loop
            if (background.count(0) == 1) and (background[-1] == 0):
                break
            
            # if current index is 0, remove background bin and merge correpsponding signal with adjacent bin
            if background[i] == 0:
                zero_sig = signal[i]
                background.pop(i)
                signal.pop(i)
                signal[i] += zero_sig

        
        # Fixing case where the last bkg_range bin = 0
        if background[-1] == 0:
            zero_sig = signal[-1]
            background.pop(-1)
            signal.pop(-1)
            signal[-1] += zero_sig
        # Fixing case where first bkg_range bin = 0
        if background[0] == 0:
            zero_sig = signal[0]
            background.pop(0)
            signal.pop(0)
            signal[0] += zero_sig
    pass
    

def scale_signal(background, uncertainty, signal, data):
    """
    Scales signal histogram list bins by a constant scale factor until
    confidence level (CL) is about 95% (typically slightly higher).

    Returns expected confidence level (CLs_exp) and the scale factor that the signal
    was scaled to in order to achieve the CL.
    """
    
    # Starting with scale factor of 0 and CLs_exp at 1 (0% condfidence level [I think])
    scale_factor = 750
    CLs_exp = 1

    # Lists that will hold potential scale factors, deltas, and confidence levels
    scale_list = []
    deltas = []
    CLs = []

    # While loop will stop when CLs_exp drops below 0.03, then will choose CLs_exp closest to 0.05
    while CLs_exp > 0.045:
        # scale signal bins
        scaled_signal = [i*scale_factor for i in signal]

        #print('Scaled Signal:', scaled_signal)
        #print('Background:', background)
        # Create PDF that helps evaluate: prob ( data | background only) & prob (data | background+signal)
        pdf = pyhf.simplemodels.hepdata_like(signal_data=scaled_signal, bkg_data=background, bkg_uncerts=uncertainty)
        
        # Get CLs_obs (not relevant) and CLs_exp
        CLs_obs, CLs_exp = pyhf.infer.hypotest(1.0, data + pdf.config.auxdata, pdf, return_expected=True)

        #print('Scale Factor: {}, Expected: {}'.format(scale_factor, CLs_exp))
        
        #if abs(0.05 - CLs_exp) < 0.01:
        # If CLs_exp is in the range [0.05, 0.06] add scale factor, delta, and CLs_exp to a list of potentials
        if 0 <= (0.05 - CLs_exp) <= 0.01:
            scale_list.append(scale_factor)
            deltas.append(abs(0.05 - CLs_exp))
            CLs.append(CLs_exp)
            
        # Increase scale factor
        scale_factor += 1
        scale_factor = round(scale_factor, 3)
        print(scale_factor)

    # Returns the CLs with the smallest delta from 0.05 and the corresponding scale factor
    return CLs[deltas.index(min(deltas))], scale_list[deltas.index(min(deltas))]   


if __name__ == "__main__":    
    # Opening file in which cross section limits will be listed
    crossx_file = open('crossx_limits.txt', 'w')

    # List of cross sections corresponding to the signal bin files
    crossx_list = [0.000006132, 0.000006884, 0.000005183, 0.000003301]
    
    #signal_hists = ['sig_content1.txt', 'sig_content2.txt', 'sig_content3.txt', 'sig_content4.txt']
    signal_hists = ['PtValues500.txt']
    
    # Background histogram as list
    back_data = []
    background_file = open('ZZZPtValues.txt', 'r')
    
    """for event in background_file.read().split('\n'):
        line = event.replace('\n', '')
        if len(line) > 1:
            back_data.append(float(line))
    background_file.close()"""
    
    with open("ZZZPtValues.txt") as f:
        back_data = f.read().splitlines()
    with open("PtValues500.txt") as f:
        sig_data = f.read().splitlines()
    
    sig_data = [float(i) for i in sig_data]
    back_data = [float(i) for i in back_data]
    # Signal histograms as list, looping over them
    for j in range(len(signal_hists)):
        """sig_data = []
        sig_file = open(signal_hists[j], 'r')

        for event in sig_file.read().split('\n'):
            line = event.replace('\n', '')
            if len(line) > 1:
                sig_data.append(float(line))
        sig_file.close()"""

        # Using all bins for calculations (50 max) by making copies of data bins
        bkg_range, sig_range = back_data[:], sig_data[:]

        # Removing zero-background bins and merging corresponding signal to adjacent bins
        remove_zeros(bkg_range, sig_range)
        
        # Printing: the lengths of bkg_range and sig_range, just to eyeball that they're the same 
        print('bkg_range length:', len(bkg_range))
        print('sig_range length:', len(sig_range))
        print()
        
        # background uncertainty, per bin
        bkg_uncert_hist = [0.5*bkg_range[l] for l in range(len(bkg_range))]

        # observed data
        data = []
        for k in range(len(bkg_range)):
            data.append(round(bkg_range[k]))
        print(data) 
        # Scale sig_range
        #pdf = pyhf.simplemodels.hepdata_like(signal_data=sig_range, bkg_data=bkg_range, bkg_uncerts=bkg_uncert_hist)
        #CLs_obs, CLs_exp = pyhf.infer.hypotest(1.0, data + pdf.config.auxdata, pdf, return_expected=True)
        #print('No Scale CLs_exp:', CLs_exp)
        
        CLs_exp, scale_factor = scale_signal(bkg_range, bkg_uncert_hist, sig_range, data)
        print('CLs_exp: {}, scale_factor: {}'.format(CLs_exp, scale_factor))
        crossx_file.write(str(crossx_list[j] * scale_factor) + '\n')
        
        print()

    crossx_file.close()    


### BINNING FUNCTION ###
'''
def bins(background, signal):
    """
    Selects range of bins to analyze from both the signal and background histograms.
    All signal bins are included and any zero-background bins are later merged with remove_zeros function.

    Returns range of bins including full signal and at least 1 non-zero background bin.
    """
    # Creating lists of all non-zero indices for signal and bacgkround histograms
    sig_nonzero_inds = [i for i in range(len(signal)) if signal[i] != 0]
    bkg_nonzero_inds = [j for j in range(len(background)) if background[j] != 0]
    
    # Selecting bin range
    if background.count(0) != len(background):
        # If there is at least 1 non-zero background bin in the signal range,
        # the range is from the first non-zero to the last non-zero bins of the signal
        bkg_range = background[sig_nonzero_inds[0]:sig_nonzero_inds[-1]]
        sig_range = signal[sig_nonzero_inds[0]:sig_nonzero_inds[-1]]
    else:
        # If all background bins in the signal range are zero,
        # the range is from the last non-zero <<background>> bin to the last non-zero <<signal>> bin
        bkg_range = background[bkg_nonzero_inds[-1]:sig_nonzero_inds[-1]]
        sig_range = signal[bkg_nonzero_inds[-1]:sig_nonzero_inds[-1]]
    

    return bkg_range, sig_range 
'''


