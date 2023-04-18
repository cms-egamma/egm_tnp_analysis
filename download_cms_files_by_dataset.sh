#!/bin/bash

# Set the dataset name here
dataset="/LQToBEle_M-1000_pair_TuneCP2_13TeV-madgraph-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM"


# Set the target directory here
target_dir="/eos/user/r/ryi/TagandProbe/TnP2017/LQToBele/"
# Create the target directory if it doesn't exist
mkdir -p "${target_dir}"

# Query the dataset for the list of root files
files=$(dasgoclient --query="file dataset=${dataset}")

xrdcp_opts="--force --nopbar --silent"

# Download the files using xrdcp
for file in $files; do
    echo "Downloading ${file} to ${target_dir}..."
    xrdcp $xrdcp_opts root://cms-xrd-global.cern.ch/${file} "${target_dir}/"
done

# Merge the downloaded ROOT files
output_file="${target_dir}/1000.root"
echo "Merging ROOT files into ${output_file}..."
hadd -f "${output_file}" "${target_dir}"/*.root
mv "${output_file}" "/eos/user/r/ryi/TagandProbe/TnP2017/LQToBele/ok/"
rm /eos/user/r/ryi/TagandProbe/TnP2017/LQToBele/*.root
