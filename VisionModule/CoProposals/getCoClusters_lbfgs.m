function [CurSave,A,AC] = getCoClusters_lbfgs(color_hist,NumVid,knn,lambd,A,AC)
% NumVid: Number of Videos
% color_hist: Array of cells (NxM histogram, N:HistSize, M:#Segments)
% knn: k for the k-nn graph
% lamb: tradeoff between within video distance and with video distance

%knn = 5;lambd = 10^5;NumVid = 2;alph = 0.3;

% Use the default parameters
if nargin < 2
    error('At least color_hist and NumVid should be supplied');
elseif nargin  < 3
    knn = 5;
    lambd = 5;
end
tic
if nargin < 5
    %Compute A and AC
    %Compute the initial color dissimilarity matrix for each video
    tic
    parfor i=1:NumVid
        color_dist = slmetric_pw(color_hist{i}, color_hist{i}, 'chisq');
        color_mean{i} = mean(mean(color_dist));
        color_K = exp(-1/color_mean{i}*color_dist);

        % construct k-nn graph
        newA = zeros(size(color_K));
        for k=1:size(color_K,1)
            [val,ind] = sort(color_K(k,:),'descend');
            newA(k,ind(1:knn)) = val(1:knn);
        end
        A{i} = (newA+newA')/2;
    end
    toc

    %Compute the color dissimilarity co-matrices
    forSp = [NumVid,NumVid];
    numSp  = prod(forSp);
    parfor idx = 1:numSp
       [i,j]=ind2sub(idx,forSp)
       if i>=j
            color_dist = slmetric_pw(color_hist{i}, color_hist{j}, 'chisq');
            color_mean = mean(mean(color_dist));
            color_K = exp(-1/color_mean*color_dist);


            % construct k-nn graph
            newA = zeros(size(color_K));
            for k=1:size(color_K,1)
                [val,ind] = sort(color_K(k,:),'descend');
                newA(k,ind(1:knn)) = val(1:knn);
            end
            ACD{idx}=newA;

            newA = zeros(size(color_K));
            for k=1:size(color_K,2)
                [val,ind] = sort(color_K(:,k),'descend');
                newA(ind(1:knn),k) = val(1:knn);
            end
            ACDI{idx} = newA';                
        end
    end
    tic
    for idx=1:numSp
        [i,j]=ind2sub(idx,forSp)
        if i>=j
            AC{i,j} = ACD{idx};
            AC{j,i} = ACDI{idx}
        end
    end
    disp(['Data transfer'])
    toc

end
toc

vecnum = 1
% Initial solution
SegSizes=zeros(2*NumVid+2,1);
InitSol = []
for i=1:NumVid
    [V,D] = eigs(A{i}); %Replace this with power method at some point
    %eigval = diag(D);
    %[eigval,ind] = sort(eigval,'descend');
    CurSol{i}= V(:,1);
    InitSol=[InitSol;CurSol{i}];
    SegSizes(i*2+1)=SegSizes(i*2)+1;
    SegSizes(i*2+2)=length(CurSol{i})+SegSizes(i*2);
end

if nargin<5
	save('InitSol.mat','CurSol');
end
N = length(InitSol);

fcn_F     = @(x) compCoCost(NumVid,x,A,AC,SegSizes,lambd);
fcn_G     = @(x) compGrad(NumVid,x,A,AC,SegSizes,lambd);


l  = zeros(SegSizes(2*NumVid+2),1);    % lower bound
u  = ones(SegSizes(2*NumVid+2),1);      % there is no upper bound
fun     = @(x)fminunc_wrapper( x, fcn_F, fcn_G); 
% Request very high accuracy for this test:
opts    = struct( 'factr', 1e4, 'pgtol', 1e-8, 'm', 10);
if N > 10000
    opts.m  = 50;
end
opts.x0 = InitSol;

% Run the algorithm:
[xk, ~, info] = lbfgsb(fun, l, u, opts );

for i=1:NumVid            
    CurSave{i}=xk(SegSizes(i*2+1):SegSizes(i*2+2));
end
