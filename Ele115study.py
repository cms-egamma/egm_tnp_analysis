import uproot
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.stats.proportion import proportion_confint


# List of LQ masses and corresponding file paths
lq_masses = [300,400,500,600,700,800,900,1000]
file_paths = [
#2018
#    "/eos/user/r/ryi/TagandProbe/TnP2018/LQToDele/6AD97ED0-A43C-1A42-BBF1-7992785001D8.root",
#    "/eos/user/r/ryi/TagandProbe/TnP2018/LQToDele/46E92EB7-4720-E94D-9212-0687FAACA519.root",
#    "/eos/user/r/ryi/TagandProbe/TnP2018/LQToDele/D98F99A2-5DCF-4D48-B244-5FF709435B7C.root",
#    "/eos/user/r/ryi/TagandProbe/TnP2018/LQToDele/C8BE3437-8092-D848-9E37-397D1B381AF2.root",
#    "/eos/user/r/ryi/TagandProbe/TnP2018/LQToDele/85C2C8B6-18CE-7B4A-B8D6-F73A20D5DDEC.root",
#    "/eos/user/r/ryi/TagandProbe/TnP2018/LQToDele/38B78932-1C59-974B-A6F5-6FB16079A726.root",
#    "/eos/user/r/ryi/TagandProbe/TnP2018/LQToDele/786F206C-2151-E745-96DC-EB1CB1A76587.root",
#    "/eos/user/r/ryi/TagandProbe/TnP2018/LQToDele/2039CF0C-B7DB-2944-AC81-FEE2811C84C0.root",
#2017
#    "/eos/user/r/ryi/TagandProbe/TnP2017/LQToDele/C11F1D64-88F9-9643-BFC2-55440632567C.root",
#    "/eos/user/r/ryi/TagandProbe/TnP2017/LQToDele/EBD1DEDF-6CE0-434B-85A5-1BB4D3B8A57A.root",
#    "/eos/user/r/ryi/TagandProbe/TnP2017/LQToDele/633136EC-BA51-3F41-9E09-60F96F16FE18.root",
#    "/eos/user/r/ryi/TagandProbe/TnP2017/LQToDele/0EB7984F-640F-7B45-B675-05EC85BD3918.root",
#    "/eos/user/r/ryi/TagandProbe/TnP2017/LQToDele/78C35BA8-44BB-5E4B-9A43-42A6EEDB5050.root",
#    "/eos/user/r/ryi/TagandProbe/TnP2017/LQToDele/787C3B71-2C63-A142-ACFE-317DF138D848.root",
#    "/eos/user/r/ryi/TagandProbe/TnP2017/LQToDele/88BF7591-0D6E-394C-A50F-B0F417FBA93F.root",
#    "/eos/user/r/ryi/TagandProbe/TnP2017/LQToDele/3A379BE6-1304-E34E-911A-F54820310E60.root",
#2016post
    "/eos/user/r/ryi/TagandProbe/TnP2016post/LQToDele/7208357C-2A06-FD4D-8757-332060540A1B.root",
    "/eos/user/r/ryi/TagandProbe/TnP2016post/LQToDele/9659C839-17E5-4142-A1AC-E85617D4976A.root",
    "/eos/user/r/ryi/TagandProbe/TnP2016post/LQToDele/F6D661BC-25AA-674B-98F1-122072DBF1A4.root",
    "/eos/user/r/ryi/TagandProbe/TnP2016post/LQToDele/BEB068B6-F7CC-9D48-B153-2517684BDBC3.root",
    "/eos/user/r/ryi/TagandProbe/TnP2016post/LQToDele/49150006-AAC0-C94B-81A9-4D22B9CBD58A.root",
    "/eos/user/r/ryi/TagandProbe/TnP2016post/LQToDele/8E2FCEE7-CA19-C943-980D-CC31E4579E3B.root",
    "/eos/user/r/ryi/TagandProbe/TnP2016post/LQToDele/0154061C-663F-DF49-8153-DC1969B7E571.root",
    "/eos/user/r/ryi/TagandProbe/TnP2016post/LQToDele/E8BE0CF8-AA01-DA43-818D-CB32B3D86246.root",

#2016pre
#    "/eos/user/r/ryi/TagandProbe/TnP2016pre/LQToDele/E35CA8EE-657A-DE4A-87C3-963172EEF315.root",
#    "/eos/user/r/ryi/TagandProbe/TnP2016pre/LQToDele/9F005757-07D5-6B4E-8F8B-F0647AFA2097.root",
#    "/eos/user/r/ryi/TagandProbe/TnP2016pre/LQToDele/990823AF-0DA0-B141-9964-BF18C10461C7.root",
#    "/eos/user/r/ryi/TagandProbe/TnP2016pre/LQToDele/7E66302D-6516-814D-B99F-3789922B8BE9.root",
#    "/eos/user/r/ryi/TagandProbe/TnP2016pre/LQToDele/54C0D80F-8012-5C41-9F7A-2FC91F702D1E.root",
#    "/eos/user/r/ryi/TagandProbe/TnP2016pre/LQToDele/9A3F0F9E-9B20-9C47-9044-C89688948BEA.root",
#    "/eos/user/r/ryi/TagandProbe/TnP2016pre/LQToDele/E706B63C-13DC-BF45-8B16-A87F642836A7.root",
#    "/eos/user/r/ryi/TagandProbe/TnP2016pre/LQToDele/49FA601A-4F26-F74C-99E4-A79DA21CB85B.root",
]
#to download to local:
#voms-proxy-init -voms cms -valid 192:00
#xrdcp root://cms-xrd-global.cern.ch//store/test/xrootd/T2_DE_DESY/store/mc/RunIISummer20UL16NanoAODAPVv9/LQToDEle_M-1000_pair_bMassZero_TuneCP2_13TeV-madgraph-pythia8/NANOAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/50000/49FA601A-4F26-F74C-99E4-A79DA21CB85B.root .
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
