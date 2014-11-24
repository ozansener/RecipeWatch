addpath(genpath('ExternalCode'))
load 'Hs.mat'
hh=rmfield(hists,'ozan')
matlabpool('open', 2);
[IDS] = CoCluster(hh)

