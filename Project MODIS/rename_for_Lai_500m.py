import os
path = "Data_for_analysis/mcd15a2h_Lai_500m/"
for filename in os.listdir(path):
	dst = filename[:41]+filename[55:]
	src = path + filename
	dst = path + dst
	os.rename(src, dst)
