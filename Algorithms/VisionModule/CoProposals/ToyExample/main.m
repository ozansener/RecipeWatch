addpath(genpath('ExternalCode'))

%Let's create clusters
NumVid = 10;
NumClusters = 50;

Dim = 2;
MeanClusters = rand(Dim,NumClusters)*50;

for i =1:NumVid
	ClustPerVid = round(rand(1)*5)+15;
	VidClusts = randperm(NumClusters);
	VC{i}=VidClusts(1:ClustPerVid);
end


for i =1:NumVid
	DD = [];
	for j=1:length(VC{i})
		NumSamp = round(rand(1)*30)+10;
		DD=[DD randn(Dim,NumSamp)+repmat(MeanClusters(:,VC{i}(j)),[1,NumSamp])];
	end
	Data{i}=DD;
end

CM=[59,17,255;
139,16,255;
219,16,255;
241,86,211;
243,180,152;
190,230,98;
81,234,48;
0,212,9;
0,106,4;
0,0,0];

for i =1:NumVid
	scatter(Data{i}(1,:),Data{i}(2,:),20,CM(i,:)/255);
    hold on 
end

CoCluster(Data)

%hh=rmfield(hists,'ozan')
%matlabpool('open', 2);
%[IDS] = CoCluster(hh)

