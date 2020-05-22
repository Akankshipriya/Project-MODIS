import pandas as pd
import numpy as np
import rasterio

df=pd.read_csv("DOY_for_data_extraction.csv",sep=";")
df["DAY"]=pd.to_datetime(df["DAY"])
df["year"]=pd.DatetimeIndex(df["DAY"]).year
a=df.groupby(["year","IDGRID","DOY"])
b=a.size().reset_index()
b[["year","IDGRID","DOY"]].to_csv("final.csv",index=False)


df=pd.read_csv("final.csv")
df["period"] = df["year"].astype(str) + df["DOY"].astype(str)
df.drop(['year','DOY'],axis=1)
c=0
def file_in_dir_or_previous(data):
	while int(data)>=2002185:
		try:
			src ='Data_for_analysis/mcd15a2h_Lai_500m/HDF4_EOS_EOS_GRID__MCD15A2H_A' + str(data) + '_006_hdf__MOD_Grid_MOD15A2H_Lai_500m.tif'
			s=rasterio.open(src)
			return src
		except IOError:
			pass
		data=str(int(data)-1)
def file_in_dir_or_next(data):
	while int(data)<=2019201:
		try:
			src ='Data_for_analysis/mcd15a2h_Lai_500m/HDF4_EOS_EOS_GRID__MCD15A2H_A' + str(data) + '_006_hdf__MOD_Grid_MOD15A2H_Lai_500m.tif'
			s=rasterio.open(src)
			return src
		except IOError:
			pass
		data=str(int(data)+1)

def avg(array):
	array = np.array(array)
	array=np.where(array>=255, 0, array) 
	s=0
	c=0
	for i in range(135,235):
		for j in range(0,80):
			s=s+array[i][j]
			if array[i][j]!=0:
				c=c+1
	return s/c

for i in range(0,df.shape[0]):
	data=df["period"][i]
	if len(data)!=7:
		data=data[:4]+"0"+data[4:]
	src1=file_in_dir_or_previous(data)
	s1=rasterio.open(src1)
	array1 = s1.read(1)
	avg1=avg(array1)
	
	
	src2=file_in_dir_or_next(data)
	s2=rasterio.open(src2)
	array2 = s2.read(1)
	avg2=avg(array2)
	print(round((avg1+avg2)/2,2))
