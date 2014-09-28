function cst = compCoCost(NumVid,CurSolRep,A,AC,SegSizes,lambd)

r = zeros(NumVid,NumVid);
%Compute the cost
for j=1:NumVid
	CS = CurSolRep(SegSizes(2*j+1):SegSizes(2*j+2),1);
	r(j,j)=(CS'*A{j}*CS)/(CS'*CS);
	for k= setdiff(1:NumVid,j)
	    CSK = CurSolRep(SegSizes(2*k+1):SegSizes(2*k+2),1);
	    r(j,k)=lambd*(CS'*AC{j,k}*CSK)/((CS'*ones(size(AC{j,k}))*CSK));
	end
end
cst = (-1)*sum(r(:));
