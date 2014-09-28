addpath(genpath('ExternalCode'))
load 'Hs.mat'
hh=rmfield(hists,'ozan')
matlabpool('open', 8);
[IDS] = CoCluster(hh)

