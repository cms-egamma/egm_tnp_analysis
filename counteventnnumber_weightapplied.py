import ROOT

# Open the input file and get the tree
file = ROOT.TFile.Open("/eos/user/r/ryi/TagandProbe/TnP2018/DY_NLO_inclusive_allptrange_reweight.root")
tree = file.Get("tnpEleTrig/fitter_tree")
#/eos/user/r/ryi/TagandProbe/TnP2018/DY_NLO_inclusive_allptrange_reweight.root
#/eos/user/r/ryi/TagandProbe/TnP2018/UL2018_DY_NLO_ptbinned_heep.root

num_entries = tree.GetEntries()
# Define the pt and eta bin you are interested in
pt_min = 350.0
pt_max = 500.0
eta_min = 1.566
eta_max = 2.5

# Initialize the event count
event_count = 0

# Initialize a dictionary to store the event count for each bin
bin_counts = {}

# Loop over all events and count the number of events in the specified bin
for i in range(num_entries):
    # Load the ith entry in the tree
    tree.GetEntry(i)

    # Get the values of pt and eta for the current event
    pt = tree.el_pt
    eta = tree.el_eta
    totWeight = tree.totWeight

    # Apply totWeight to the event count
    event_count += totWeight

    # Check if the event falls within the specified bin
    if pt >= pt_min and pt < pt_max and eta >= eta_min and eta < eta_max:
        # Create a unique key for the pt and eta bin
        bin_key = (round(pt, 1), round(eta, 1))

        # Increment the bin count
        if bin_key in bin_counts:
            bin_counts[bin_key] += totWeight
        else:
            bin_counts[bin_key] = totWeight

# Write the event count to a text file
with open("count_withweight.txt", "w") as f:
    f.write("Total events in sample: {}\n".format(event_count))
    f.write("\n")
    f.write("Event count for each bin:\n")
    for bin_key, count in bin_counts.items():
        f.write("Pt: [{:.1f}, {:.1f}], Eta: [{:.1f}, {:.1f}]: {}\n".format(
            bin_key[0], bin_key[0]+10.0, bin_key[1], bin_key[1]+0.5, count))
