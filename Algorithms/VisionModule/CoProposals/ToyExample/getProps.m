load r_50.mat
load sg.mat
mkdir('R_10')
for i =1:length(RES)
        IDS = RES{i};
        mkdir(['R_10/' num2str(i)])
        for j=1:length(IDS)
                d = IDS(j);
		Seg{d}.name
                I=imread([ '/expts/ozan_recipe/YoutubePipeline/' Seg{d}.name] );
                M=repmat(Seg{d}.mask,[1,1,3]);
                imwrite(uint8(double(I).*M),['R_10/' num2str(i) '/' num2str(j) '.jpg'])
   	end
end
              
