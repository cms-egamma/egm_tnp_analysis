import ROOT
# Open the input file and get the tree
file = ROOT.TFile.Open("/eos/user/r/ryi/TagandProbe/TnP2018/UL2018_DY_NLO_ptbinned_heep.root")
tree = file.Get("tnpEleTrig/fitter_tree")
#/eos/user/r/ryi/TagandProbe/TnP2018/DY_NLO_inclusive_allptrange.root  inclusive
#/eos/user/r/ryi/TagandProbe/TnP2018/UL2018_DY_NLO_ptbinned_heep.root  ptbinned


num_entries = tree.GetEntries()
# Define the pt and eta bin you are interested in
pt_min = 250.0
pt_max = 400.0
eta_min = 1.566
eta_max = 2.5

# Initialize the event count
event_count = 0

# Loop over all events and count the number of events in the specified bin
for i in range(num_entries):
    # Load the current event
    tree.GetEntry(i)

    # Get the values of pt and eta for the current event
    pt = tree.el_pt
    eta = tree.el_eta

    # Check if the event falls within the specified bin
    if pt >= pt_min and pt < pt_max and eta >= eta_min and eta < eta_max:
        event_count += 1

# Write the event count to a text file
with open("count.txt", "w") as f:
    f.write(str(event_count))
