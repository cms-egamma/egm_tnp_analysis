import uproot
import matplotlib.pyplot as plt
import numpy as np

# List of LQ masses and corresponding file paths
lq_masses = [300,400,500,600,700,800,900,1000]
file_paths = [
    "root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL16NanoAODAPVv9/LQToDEle_M-300_pair_bMassZero_TuneCP2_13TeV-madgraph-pythia8/NANOAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/50000/E35CA8EE-657A-DE4A-87C3-963172EEF315.root",
    "root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL16NanoAODAPVv9/LQToDEle_M-400_pair_bMassZero_TuneCP2_13TeV-madgraph-pythia8/NANOAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/30000/9F005757-07D5-6B4E-8F8B-F0647AFA2097.root",
    "root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL16NanoAODAPVv9/LQToDEle_M-500_pair_bMassZero_TuneCP2_13TeV-madgraph-pythia8/NANOAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/40000/990823AF-0DA0-B141-9964-BF18C10461C7.root",
    "root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL16NanoAODAPVv9/LQToDEle_M-600_pair_bMassZero_TuneCP2_13TeV-madgraph-pythia8/NANOAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/2530000/7E66302D-6516-814D-B99F-3789922B8BE9.root",
    "root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL16NanoAODAPVv9/LQToDEle_M-700_pair_bMassZero_TuneCP2_13TeV-madgraph-pythia8/NANOAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/2520000/54C0D80F-8012-5C41-9F7A-2FC91F702D1E.root",
    "root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL16NanoAODAPVv9/LQToDEle_M-800_pair_bMassZero_TuneCP2_13TeV-madgraph-pythia8/NANOAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/40000/9A3F0F9E-9B20-9C47-9044-C89688948BEA.root",
    "root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL16NanoAODAPVv9/LQToDEle_M-900_pair_bMassZero_TuneCP2_13TeV-madgraph-pythia8/NANOAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/40000/E706B63C-13DC-BF45-8B16-A87F642836A7.root",
    "root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL16NanoAODAPVv9/LQToDEle_M-1000_pair_bMassZero_TuneCP2_13TeV-madgraph-pythia8/NANOAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/50000/49FA601A-4F26-F74C-99E4-A79DA21CB85B.root",
]

# Function to calculate trigger efficiencies
def calculate_trigger_efficiencies(trigger_paths):
    trigger_efficiencies = []

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

    return trigger_efficiencies


# List of combined trigger paths to plot
combined_trigger_paths = [
    ["HLT_Ele27_WPTight_Gsf", "HLT_Photon175"],
    ["HLT_Ele27_WPTight_Gsf", "HLT_Photon175", "HLT_Ele115_CaloIdVT_GsfTrkIdT"],
    ["HLT_Ele27_WPTight_Gsf"],
]

# Calculate trigger efficiencies
trigger_efficiencies_1 = calculate_trigger_efficiencies(combined_trigger_paths[0])
trigger_efficiencies_2 = calculate_trigger_efficiencies(combined_trigger_paths[1])
trigger_efficiencies_3 = calculate_trigger_efficiencies(combined_trigger_paths[2])

average_efficiency_1 = sum(trigger_efficiencies_1) / len(trigger_efficiencies_1)
average_efficiency_2 = sum(trigger_efficiencies_2) / len(trigger_efficiencies_2)
average_efficiency_3 = sum(trigger_efficiencies_3) / len(trigger_efficiencies_3)

print("Average Trigger Efficiencies:")
print("Average Trigger Efficiencies 1:", average_efficiency_1)
print("Average Trigger Efficiencies 2:", average_efficiency_2)
print("Average Trigger Efficiencies 3:", average_efficiency_3)

# Calculate the ratio of trigger efficiencies
trigger_efficiency_ratios = np.array(trigger_efficiencies_1) / np.array(trigger_efficiencies_2)

# Create a two-panel plot
print("Trigger Efficiencies 1:", trigger_efficiencies_1)
print("Trigger Efficiencies 2:", trigger_efficiencies_2)
print("Trigger Efficiencies 3:", trigger_efficiencies_3)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8), sharex=True, gridspec_kw={'height_ratios': [3, 1], 'hspace': 0.1})

# Plot trigger efficiencies on the upper panel
ax1.plot(lq_masses, trigger_efficiencies_1, marker="o", label=" || ".join(combined_trigger_paths[0]))
ax1.plot(lq_masses, trigger_efficiencies_2, marker="o", label=" || ".join(combined_trigger_paths[1]))
ax1.plot(lq_masses, trigger_efficiencies_3, marker="o", label=" || ".join(combined_trigger_paths[2]))
ax1.set_ylim(0.8, 1.2)
ax1.set_ylabel("Trigger Efficiency")
ax1.set_title("Trigger Efficiency as a function of LQ Mass")
ax1.legend()
ax1.grid()

# Plot the ratio of trigger efficiencies on the lower panel
ax2.plot(lq_masses, trigger_efficiency_ratios, marker="o", label="Efficiency Ratio")
ax2.set_xlabel("LQ Mass (GeV)")
ax2.set_ylabel("TE Ratio：without/with Ele115")
ax2.set_ylim(0.8, 1.2)
ax2.legend()
ax2.grid()

plt.show()
