#!/usr/bin/env bash

comm=https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/2020-03-13/comm_use_subset.tar.gz
noncomm=https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/2020-03-13/noncomm_use_subset.tar.gz
pmc=https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/2020-03-13/pmc_custom_license.tar.gz
rxiv=https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/2020-03-13/biorxiv_medrxiv.tar.gz

wget $comm -O comm_use_subset.tar.gz
wget $noncomm -O noncomm_use_subset.tar.gz
wget $pmc -O pmc_custom_license.tar.gz
wget $rxiv -O biorxiv_medrxiv.tar.gz

mkdir comm_use_subset
tar -xvzf comm_use_subset.tar.gz  -C comm_use_subset
mkdir noncomm_use_subset
tar -xvzf noncomm_use_subset.tar.gz  -C noncomm_use_subset
mkdir pmc_custom_license
tar -xvzf pmc_custom_license.tar.gz  -C pmc_custom_license
mkdir biorxiv_medrxiv
tar -xvzf biorxiv_medrxiv.tar.gz  -C biorxiv_medrxiv

rm ./*.tar.gz
