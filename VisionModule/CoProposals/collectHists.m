%addpath(genpath('/expts/ozan_recipe/VisionProcesser/Keysegments/code/'))
LBinSize = 100 / 22;
abBinSize = 256 / 22;
LBinEdges = [0:LBinSize:100];
abBinEdges = [-128:abBinSize:128];


expDir = '/expts/ozan_recipe/Data/CPMC/MS/'

matS = dir([expDir '*.mat'])
segCnt = 1;
hists.ozan = 0
for i =1:length(matS)
	fN=matS(i).name;
	vN = fN(1:end-11);
	frN = str2num(fN(end-10:end-6));
	load([expDir fN])
	im = imread(['/expts/ozan_recipe/Data/CPMC/Frames_R/' vN '/JPEGImages/' fN(1:end-3) 'jpg']);
	disp([num2str(length(masks(1,1,:))),' _ ',fN])
	if length(masks(1,1,:)) < 5
		continue;
	else
		NN = min(40,length(masks(1,1,:)));
	end
	disp(NN)
	for j=1:NN
		% Compute The Histogram
		Seg{segCnt}.name=['/expts/ozan_recipe/Data/CPMC/Frames_R/' vN '/JPEGImages/' fN(1:end-3) 'jpg'];
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
		
		
		vN_C  = ['f' strrep(vN, '-', '_')];
		if ~isfield(hists,vN_C)
			hists.(vN_C)=H;
		else
			hists.(vN_C)=[hists.(vN_C),H];
		end
	end
end

save('Hs.mat','hists')
save('S.mat','Seg')

