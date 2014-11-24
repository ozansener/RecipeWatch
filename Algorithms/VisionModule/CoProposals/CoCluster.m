function [RES] = CoCluster(structIn)

vidNames = fieldnames(structIn);


for i=1:length(vidNames)
    viN=vidNames(i);
    vidN = viN{1};
    DD=zeros(length(structIn.(vidN)(1).hist),length(structIn.(vidN)));
    CC=zeros(length(structIn.(vidN)),1);
    CN=zeros(length(structIn.(vidN)),1);
    parfor j=1:length(structIn.(vidN))
        DD(:,j) = structIn.(vidN)(j).hist;
        CC(j)=structIn.(vidN)(j).score;
        CN(j)=structIn.(vidN)(j).cnt;
    end
    DATA{i}=DD;
    Cost{i}=CC;
    CNT{i}=CN;
end

knn = 5;
lambd = 100;
NumVid = length(vidNames);


% 50 is maximum number of clusters
for m = 1:50
    disp(['Call to L-BFGS' num2str(m)])
    RES{m} = [];
    
    if m<2
	    [CurSave,A,AC] = getCoClusters_lbfgs(DATA,NumVid,knn,lambd);
    else
	    [CurSave,~,~] = getCoClusters_lbfgs(DATA,NumVid,knn,lambd,A,AC);
    end

    exit

    save(['CS' num2str(m) '.mat'],'CurSave')
    A_S = A;
    AC_S = AC;

    for i=1:NumVid
        cEig = CurSave{i};
        [temp_eigvec tempind] = sort(cEig,'descend');

        %Discritize it
        indic_vec = zeros(length(cEig),1);
        f_vec = indic_vec; 
        indic_vec(1)=1;
        %Get at most 100 segments from each video
        sc = -1;
        for k = 1:min(length(cEig),100)
            indic_vec(k) = 1;
	    temp_f = zeros(length(cEig),1);
	    temp_f(tempind)=indic_vec;
            cur_sc = (temp_f' * A_S{i} * temp_f)/(temp_f'*temp_f);
            for l=setdiff(1:NumVid,i)
                cur_sc = cur_sc + lambd*(temp_f' * AC_S{i,l}*CurSave{l})/(temp_f' *ones(size(AC_S{i,l}))*CurSave{l});
            end
            if cur_sc > sc
                sc = cur_sc;
                f_vec = indic_vec;
            end
        end
        
        final_i = zeros(length(cEig),1);
        final_i(tempind) = f_vec;    
        
        CurSave{i} = final_i;
        
        selind = find(final_i==1);
        %final_i is the discritized one
        DATA{i}(:,selind)=[];
        RES{m}=[RES{m} CNT{i}(selind)]
        CNT{i}(selind)=[];
        
        A{i}(selind,:)=[];
        A{i}(:,selind)=[];
        for l=setdiff(1:NumVid,i)
            AC{i,l}(selind,:)=[];
	    AC{l,i}(:,selind)=[];
        end
	disp(['A and AC are deleted'])
    end
    save(['CS' num2str(m) '_d.mat'],'CurSave')
    save('current_res.mat','RES')
end

