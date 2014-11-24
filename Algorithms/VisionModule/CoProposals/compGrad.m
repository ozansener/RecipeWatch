function GradG = compGrad(NumVid,CurSolRep,A,AC,SegSizes,lambd)

r = zeros(NumVid,NumVid);
GradG = zeros(SegSizes(2*NumVid+2),1);
for j = 1:NumVid
	CS = CurSolRep(SegSizes(2*j+1):SegSizes(2*j+2),1);
	r(j,j)=(CS'*A{j}*CS)/(CS'*CS);
	Gradd = (2*A{j}*CS-2*CS*r(j,j))/(CS'*CS);
	for k=setdiff(1:NumVid,[j])
		CSK = CurSolRep(SegSizes(2*k+1):SegSizes(2*k+2),1);
		r(j,k)=(CS'*AC{j,k}*CSK)/((CS'*ones(size(AC{j,k}))*CSK));
	   	Gradd =Gradd + lambd*(1/(CS'*ones(size(AC{j,k}))*CSK))*(AC{j,k}*CSK-ones(size(AC{j,k}))*CSK*r(j,k));
        
		r(j,k)=(CSK'*AC{k,j}*CS)/((CSK'*ones(size(AC{k,j}))*CS));
	   	Gradd =Gradd + lambd*(1/(CSK'*ones(size(AC{k,j}))*CS))*(AC{k,j}'*CSK-ones(size(AC{k,j}'))*CSK*r(j,k));
    end
	GradG(SegSizes(2*j+1):SegSizes(2*j+2),1) = Gradd;
end

GradG = (-1)*GradG;


