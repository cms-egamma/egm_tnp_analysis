import uproot
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.stats.proportion import proportion_confint


# List of LQ masses and corresponding file paths
lq_masses = [300,400,500,600,700,800,900,1000]
file_paths = [
#2018
#    "/eos/user/r/ryi/TagandProbe/TnP2018/LQToBele/ok/300.root",  #300
#    "/eos/user/r/ryi/TagandProbe/TnP2018/LQToBele/ok/400.root",  #400
#    "/eos/user/r/ryi/TagandProbe/TnP2018/LQToBele/ok/500.root",  #500
#    "/eos/user/r/ryi/TagandProbe/TnP2018/LQToBele/ok/600.root",  #600
#    "/eos/user/r/ryi/TagandProbe/TnP2018/LQToBele/ok/700.root",  #700
#    "/eos/user/r/ryi/TagandProbe/TnP2018/LQToBele/ok/800.root",  #800
#    "/eos/user/r/ryi/TagandProbe/TnP2018/LQToBele/ok/900.root",  #900
#    "/eos/user/r/ryi/TagandProbe/TnP2018/LQToBele/ok/1000.root",  #1000
#2017
    "/eos/user/r/ryi/TagandProbe/TnP2017/LQToBele/ok/300.root", #300
    "/eos/user/r/ryi/TagandProbe/TnP2017/LQToBele/ok/400.root", #400
    "/eos/user/r/ryi/TagandProbe/TnP2017/LQToBele/ok/500.root", #500
    "/eos/user/r/ryi/TagandProbe/TnP2017/LQToBele/ok/600.root", #600
    "/eos/user/r/ryi/TagandProbe/TnP2017/LQToBele/ok/700.root", #700
    "/eos/user/r/ryi/TagandProbe/TnP2017/LQToBele/ok/800.root",  #800
    "/eos/user/r/ryi/TagandProbe/TnP2017/LQToBele/ok/900.root",  #900
    "/eos/user/r/ryi/TagandProbe/TnP2017/LQToBele/ok/1000.root",  #1000
##2016post
#    "/eos/user/r/ryi/TagandProbe/TnP2016post/LQToBele/ok/300.root",  #300
#    "/eos/user/r/ryi/TagandProbe/TnP2016post/LQToBele/ok/400.root",  #400
#    "/eos/user/r/ryi/TagandProbe/TnP2016post/LQToBele/ok/500.root",  #500
#    "/eos/user/r/ryi/TagandProbe/TnP2016post/LQToBele/ok/600.root",  #600
#    "/eos/user/r/ryi/TagandProbe/TnP2016post/LQToBele/ok/700.root",  #700
#    "/eos/user/r/ryi/TagandProbe/TnP2016post/LQToBele/ok/800.root",  #800
#    "/eos/user/r/ryi/TagandProbe/TnP2016post/LQToBele/ok/900.root",  #900
#    "/eos/user/r/ryi/TagandProbe/TnP2016post/LQToBele/ok/1000.root",  #1000

##2016pre
#    "/eos/user/r/ryi/TagandProbe/TnP2016pre/LQToBele/ok/300.root",  #300
#    "/eos/user/r/ryi/TagandProbe/TnP2016pre/LQToBele/ok/400.root",  #400
#    "/eos/user/r/ryi/TagandProbe/TnP2016pre/LQToBele/ok/500.root",  #500
#    "/eos/user/r/ryi/TagandProbe/TnP2016pre/LQToBele/ok/600.root",  #600
#    "/eos/user/r/ryi/TagandProbe/TnP2016pre/LQToBele/ok/700.root",  #700
#    "/eos/user/r/ryi/TagandProbe/TnP2016pre/LQToBele/ok/800.root",  #800
#    "/eos/user/r/ryi/TagandProbe/TnP2016pre/LQToBele/ok/900.root",  #900
#    "/eos/user/r/ryi/TagandProbe/TnP2016pre/LQToBele/ok/1000.root",  #1000
]
#to download to local:
#voms-proxy-init -voms cms -valid 192:00
#xrdcp root://cms-xrd-global.cern.ch//store/test/xrootd/T2_DE_DESY/store/mc/RunIISummer20UL16NanoAODAPVv9/LQToBele_M-1000_pair_bMassZero_TuneCP2_13TeV-madgraph-pythia8/NANOAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/50000/49FA601A-4F26-F74C-99E4-A79DA21CB85B.root .
#or xrdcp root://cms-xrd-global.cern.ch//store/test/xrootd/T1_US_FNAL_Disk
#or you can check site file on DAS to figure out

# Function to calculate trigger efficiencies
def calculate_trigger_efficiencies(trigger_paths):
    trigger_efficiencies = []
    trigger_efficiency_errors = []
    for index, file_path in enumerate(file_paths):
        # Read the NanoAOD file
        file = uproot.open(file_path)
        tree = file["Events"]

        # Count events with at least one gen electron within ECAL fiducial acceptance
        gen_electron_mask = (abs(tree["GenPart_pdgId"].array()) == 11) & (tree["GenPart_status"].array() == 1)
        gen_electrons_within_acceptance = tree["GenPart_eta"].array()[gen_electron_mask].count() > 0
        denominator = gen_electrons_within_acceptance.sum()

        print("File {} (LQ mass {} GeV):".format(index + 1, lq_masses[index]))
        print("Denominator: {}".format(denominator))

        # Count events that pass the combined triggers
        trigger_mask = None
        for trigger_path in trigger_paths:
            if trigger_mask is None:
                trigger_mask = tree[trigger_path].array()
            else:
                trigger_mask = trigger_mask | tree[trigger_path].array()

        numerator = (gen_electrons_within_acceptance & trigger_mask).sum()

        print("Numerator: {}".format(numerator))

        # Calculate trigger efficiency
        trigger_efficiency = float(numerator) / denominator if denominator != 0 else 0
    #    trigger_efficiency = numerator / denominator if denominator != 0 else 0
        trigger_efficiencies.append(trigger_efficiency)
        # Calculate the lower and upper confidence intervals for each efficiency
        lower, upper = proportion_confint(numerator, denominator, alpha=0.05, method='beta')
        trigger_efficiency_errors.append((trigger_efficiency - lower, upper - trigger_efficiency))


    return trigger_efficiencies, trigger_efficiency_errors


# List of combined trigger paths to plot
combined_trigger_paths = [
    ["HLT_Ele27_WPTight_Gsf", "HLT_Photon175"],
    ["HLT_Ele27_WPTight_Gsf", "HLT_Photon175", "HLT_Ele115_CaloIdVT_GsfTrkIdT"],
    ["HLT_Ele27_WPTight_Gsf"],
]

# Calculate trigger efficiencies
trigger_efficiencies_1, trigger_efficiency_errors_1 = calculate_trigger_efficiencies(combined_trigger_paths[0])
trigger_efficiencies_2, trigger_efficiency_errors_2 = calculate_trigger_efficiencies(combined_trigger_paths[1])
trigger_efficiencies_3, trigger_efficiency_errors_3 = calculate_trigger_efficiencies(combined_trigger_paths[2])


# Calculate the ratio of trigger efficiencies
trigger_efficiency_ratios = np.array(trigger_efficiencies_1) / np.array(trigger_efficiencies_2)

# Create a two-panel plot

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8), sharex=True, gridspec_kw={'height_ratios': [3, 1], 'hspace': 0.1})

# Plot trigger efficiencies on the upper panel
ax1.plot(lq_masses, trigger_efficiencies_1, marker="o", label=" || ".join(combined_trigger_paths[0]))
ax1.plot(lq_masses, trigger_efficiencies_2, marker="o", label=" || ".join(combined_trigger_paths[1]))
ax1.plot(lq_masses, trigger_efficiencies_3, marker="o", label=" || ".join(combined_trigger_paths[2]))

ax1.errorbar(lq_masses, trigger_efficiencies_1, yerr=np.array(trigger_efficiency_errors_1).T, fmt='o', capsize=4, label=" || ".join(combined_trigger_paths[0]))
ax1.errorbar(lq_masses, trigger_efficiencies_2, yerr=np.array(trigger_efficiency_errors_2).T, fmt='o', capsize=4, label=" || ".join(combined_trigger_paths[1]))
ax1.errorbar(lq_masses, trigger_efficiencies_3, yerr=np.array(trigger_efficiency_errors_3).T, fmt='o', capsize=4, label=" || ".join(combined_trigger_paths[2]))

#plt.errorbar(lq_masses, trigger_efficiencies_1, yerr=np.array(trigger_efficiency_errors_1).T, fmt='o', capsize=4, label=" || ".join(combined_trigger_paths[0]))
#plt.errorbar(lq_masses, trigger_efficiencies_2, yerr=np.array(trigger_efficiency_errors_2).T, fmt='o', capsize=4, label=" || ".join(combined_trigger_paths[1]))
#plt.errorbar(lq_masses, trigger_efficiencies_3, yerr=np.array(trigger_efficiency_errors_3).T, fmt='o', capsize=4, label=" || ".join(combined_trigger_paths[2]))

ax1.set_ylim(0.8, 1.2)
ax1.set_ylabel("Trigger Efficiency")
ax1.set_title("Trigger Efficiency as a function of LQ Mass")
ax1.legend()
ax1.grid()

# Plot the ratio of trigger efficiencies on the lower panel
ax2.plot(lq_masses, trigger_efficiency_ratios, marker="o", label="Efficiency Ratio")
ax2.errorbar(lq_masses, trigger_efficiency_ratios, yerr=np.array(trigger_efficiency_errors_3).T, fmt='o', capsize=4, label=" || ".join(combined_trigger_paths[2]))

ax2.set_xlabel("LQ Mass (GeV)")
ax2.set_ylabel("TE Ratio without/with Ele115")
ax2.set_ylim(0.95, 1.05)
ax2.legend()
ax2.grid()

plt.show()
