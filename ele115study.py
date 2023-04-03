import uproot
import matplotlib.pyplot as plt

# List of LQ masses and corresponding file paths
lq_masses = [500, 1000]
file_paths = [
    "root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL16NanoAODAPVv9/LQToDEle_M-500_pair_bMassZero_TuneCP2_13TeV-madgraph-pythia8/NANOAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/40000/990823AF-0DA0-B141-9964-BF18C10461C7.root",
    "root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL16NanoAODAPVv9/LQToDEle_M-1000_pair_bMassZero_TuneCP2_13TeV-madgraph-pythia8/NANOAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/50000/49FA601A-4F26-F74C-99E4-A79DA21CB85B.root",
]

# Function to calculate trigger efficiencies
def calculate_trigger_efficiencies(trigger_paths):
    trigger_efficiencies = []

    for file_path in file_paths:
        # Read the NanoAOD file
        file = uproot.open(file_path)
        tree = file["Events"]

        # Count events with at least one gen electron within ECAL fiducial acceptance
        gen_electron_mask = (abs(tree["GenPart_pdgId"].array()) == 11) & (tree["GenPart_status"].array() == 1)
        gen_electrons_within_acceptance = tree["GenPart_eta"].array()[gen_electron_mask].count() > 0
        denominator = gen_electrons_within_acceptance.sum()

        # Count events that pass the combined triggers
        trigger_mask = None
        for trigger_path in trigger_paths:
            if trigger_mask is None:
                trigger_mask = tree[trigger_path].array()
            else:
                trigger_mask = trigger_mask | tree[trigger_path].array()

        numerator = (gen_electrons_within_acceptance & trigger_mask).sum()

        # Calculate trigger efficiency
        trigger_efficiency = numerator / denominator
        trigger_efficiencies.append(trigger_efficiency)

    return trigger_efficiencies

# List of combined trigger paths to plot
combined_trigger_paths = [
    ["HLT_Ele27_WPTight_Gsf"],
    ["HLT_Ele27_WPTight_Gsf", "HLT_Photon175"],
    ["HLT_Ele27_WPTight_Gsf", "HLT_Photon175", "HLT_Ele115_CaloIdVT_GsfTrkIdT"],
]

# Plot trigger efficiency as a function of LQ mass for different combined trigger paths
for trigger_paths in combined_trigger_paths:
    trigger_efficiencies = calculate_trigger_efficiencies(trigger_paths)
    plt.plot(lq_masses, trigger_efficiencies, marker="o", label=" || ".join(trigger_paths))

plt.xlabel("LQ Mass (GeV)")
plt.ylabel("Trigger Efficiency")
plt.title("Trigger Efficiency as a function of LQ Mass")
plt.legend()
plt.grid()
plt.show()
