%addpath(genpath('/expts/ozan_recipe/VisionProcesser/Keysegments/code/'))
LBinSize = 100 / 22;
abBinSize = 256 / 22;
LBinEdges = [0:LBinSize:100];
abBinEdges = [-128:abBinSize:128];


load HIS_LIS.mat

segCnt = 1;
hists.ozan = 0
for i =1:length(MAT)
	imn = strtrim( Image(i,:))
	mn=strtrim(MAT(i,:));
	fN = strtrim(Fols(i,:));
	disp(mn)
	load(mn);
	im = imread(imn);
	disp([num2str(length(masks(1,1,:))),' _ ',mn])
	if length(masks(1,1,:)) < 5
		continue;
	else
		NN = min(30,length(masks(1,1,:)));
	end
	disp(NN)
	for j=1:NN
		% Compute The Histogram
		Seg{segCnt}.name=imn;
		Seg{segCnt}.mask=masks(:,:,j);
		Seg{segCnt}.score=scores(j);
		segCnt = segCnt + 1;

	        [L,a,b] = RGB2Lab(double(im(:,:,1)), double(im(:,:,2)), double(im(:,:,3)));
	        if(max(L(:)) > 100 | min(L(:)) < 0)
	            fprintf('error in L range\n');
        	    keyboard;
       		end
    	        if(max(a(:)) > 128 | min(a(:)) < -128)
        	    fprintf('error in a range\n');
    	       	    keyboard;
    	       end
       	       if(max(b(:)) > 128 | min(b(:)) < -128)
        	    fprintf('error in b range\n');
            	    keyboard;
               end  
               color_hists = [histc(L(masks(:,:,j)), LBinEdges); histc(a(masks(:,:,j)), abBinEdges); histc(b(masks(:,:,j)), abBinEdges)];

		H.hist = color_hists;
		H.score = scores(j);
		H.cnt = segCnt;
		
		
		vN_C  = strrep(fN,'-','_');
		if ~isfield(hists,vN_C)
			hists.(vN_C)=H;
		else
			hists.(vN_C)=[hists.(vN_C),H];
		end
	end
end

save('Hs.mat','hists')
save('S.mat','Seg')

