# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 21:22:16 2024

@author: Vivek
"""

"""
Perform hierarchical and K-means clustering on the dataset. 
After that, perform PCA on the dataset and extract the 
first 3 principal components and make a new dataset with these 
3 principal components as the columns. 
Now, on this new dataset, perform hierarchical and K-means clustering. 
Compare the results of clustering on the original dataset 
and clustering on the principal components dataset 
(use the scree plot technique to obtain the optimum number of clusters 
in K-means clustering and check if you’re getting similar results with and without PCA).
 
"""

import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from sklearn.cluster import KMeans

wine=pd.read_csv("C:\Data Set\wine.csv")
#EDA
wine.dtypes

wine.describe()
#show the distribution of wine contents.There is average 13 alcohal 2.33 
#malic and 746.89 is Proline

plt.hist(data = wine, x = 'Alcohal');
#This is apparently not a normal distribution.
# .
wine.Type.value_counts()
#2    71
#1    59
#3    48

#Let’s look at the malic acid:
plt.hist(data = wine, x = 'Malic');
# Aparantly normal distribution and right skewed
plt.hist(data =wine, x = 'Ash');
#This is normally distributed
plt.hist(data =wine, x = 'Alkanity');
plt.hist(data = wine, x = 'Magnesium ');
plt.hist(data = wine, x = 'Phinols ');
# we know that there is scale difference among the columns,which we have to remove
#either by using normalization or standardization
def norm_func(i):
    x=(i-i.min())/(i.max()-i.min())
    return x


# Now apply this normalization function to airlines datframe for all the rows 
#and column from 1 until end

df_norm=norm_func(wine.iloc[:,:])
TWSS=[]
k=list(range(2,14))
# The values generated by TWSS are 12 and two get x and y values 12 by 12 ,
#
#range has been changed 2:14

for i in k:
    kmeans=KMeans(n_clusters=i)
    kmeans.fit(df_norm)
    TWSS.append(kmeans.inertia_)
TWSS

plt.plot(k,TWSS,'ro-');plt.xlabel("No_of_clusters");plt.ylabel("Total_within_SS")
# from the plot it is clear that the TWSS is reducing from k=2 to 3 and 3 to 4 
#than any other change in values of k,hence k=3 is selected
model=KMeans(n_clusters=3)
model.fit(df_norm)
model.labels_
mb=pd.Series(model.labels_)
wine['clust']=mb
wine.head()
wine=wine.iloc[:,[14,0,1,2,3,4,5,6,7,8,9,10,11,12,13]]
wine.Type.value_counts()
#2    71
#1    59
#3    48

wine.clust.value_counts()
#2    69
#1    60
#0    49
# very few data items have been missclassified using k-means
#Now let us apply PCA to wine data set 

wine1 = pd.read_csv("C:\Data Set\wine.csv")

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.preprocessing import scale 

# Considering only numerical data 
wine1.data = wine1.iloc[:,1:]

# Normalizing the numerical data 
wine1_normal = scale(wine1.data)
wine1_normal

pca = PCA(n_components = 6)
pca_values = pca.fit_transform(wine1_normal)

# The amount of variance that each PCA explains is 
var = pca.explained_variance_ratio_
var

# PCA weights
pca.components_
pca.components_[0]

# Cumulative variance 
var1 = np.cumsum(np.round(var, decimals = 4) * 100)
var1

# Variance plot for PCA components obtained 
plt.plot(var1, color = "red")

# PCA scores
pca_values

pca_data = pd.DataFrame(pca_values)
pca_data.columns = "comp0", "comp1", "comp2", "comp3", "comp4", "comp5"
final = pd.concat([wine1.Type, pca_data.iloc[:, 0:3]], axis = 1)

final1=final.iloc[:,1:]
# Now let us apply K-means to PCA converted final1
TWSS=[]
k=list(range(2,14))
# The values generated by TWSS are 12 and two get x and y values 12 by 12 ,
#range has been changed 2:14


for i in k:
    kmeans=KMeans(n_clusters=i)
    kmeans.fit(final1)
    TWSS.append(kmeans.inertia_)
TWSS

plt.plot(k,TWSS,'ro-');plt.xlabel("No_of_clusters");plt.ylabel("Total_within_SS")
# from the plot it is clear that the TWSS is reducing from k=2 to 3 and 3 to 4 
#than any other change in values of k,hence k=3 is selected
model=KMeans(n_clusters=3)
model.fit(final1)
model.labels_
mb=pd.Series(model.labels_)
final['clust']=mb

final.Type.value_counts()
#2    71
#1    59
#3    48
final.clust.value_counts()
#1    51     #Equivalent to type-2 ,71 % correct clustering
#0    65     #Equivalent to type-1 ,90 % correct clustering
#2    62     #Equivalent to type-3 ,77 % correct clustering

#Aglomerative clustering
import pandas as pd
import matplotlib.pylab as plt
# Now import file from data set and create a dataframe
wine3=pd.read_csv("C:\Data Set\wine.csv")

# we know that there is scale difference among the columns,which we have to remove
#either by using normalization or standardization
def norm_func(i):
    x=(i-i.min())/(i.max()-i.min())
    return x
# Now apply this normalization function to crime datframe for all the rows and 
#column from 1 until end
    
df_norm=norm_func(wine3.iloc[:,:])
# you can check the df_norm dataframe which is scaled between values from 0 to1
# you can apply describe function to new data frame
df_norm.describe()

# Now to create dendrogram, we need to measure distance,we have to import linkage
from scipy.cluster.hierarchy import linkage
import scipy.cluster.hierarchy as sch
z=linkage(df_norm,method="complete",metric="euclidean")
plt.figure(figsize=(15,8));plt.title("Hierarchical Clustering dendrogram");plt.xlabel("Index");plt.ylabel("Distance")
sch.dendrogram(z,leaf_rotation=0,leaf_font_size=10)
plt.show()

# applying agglomerative clustering choosing 11 as clusters from dendrogram
from sklearn.cluster import AgglomerativeClustering
h_complete=AgglomerativeClustering(n_clusters=3,linkage='complete',affinity="euclidean").fit(df_norm)
# apply labels to the clusters
h_complete.labels_
cluster_labels=pd.Series(h_complete.labels_)
#Assign this series to Univ Dataframe as column and name the column as "clust"
wine3['clust']=cluster_labels
# we want to relocate the column 66 to 0 th position
wine3=wine3.iloc[:,[14,0,1,2,3,4,5,6,7,8,9,10,11,12,13]]
# let us check the value count in wine3 Type columns
wine3.Type.value_counts()
#2    71
#1    59
#3    48
#Now let us check the value counts after aglomerative clustering
wine3.clust.value_counts()
#1     34     # Equivalent to Type-2,50 % correct classification
#0    116     # Equivalent to Type-1,50 % correct classification
#2     28     # Equivalent to Type-2, around 52 % correct classification
#Aglomerative clutering has huge miss classification
# let us apply PCA to win3
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.preprocessing import scale 

# excluding type column
wine3.data = wine3.iloc[:,1:]

# Normalizing the numerical data 
wine3_normal = scale(wine3.data)
wine3_normal

pca = PCA(n_components = 6)
pca_values = pca.fit_transform(wine3_normal)

# The amount of variance that each PCA explains is 
var = pca.explained_variance_ratio_
var

# PCA weights
pca.components_
pca.components_[0]
import numpy as np
# Cumulative variance 
var1 = np.cumsum(np.round(var, decimals = 4) * 100)
var1

# Variance plot for PCA components obtained 
plt.plot(var1, color = "red")

# PCA scores
pca_values

pca_data = pd.DataFrame(pca_values)
pca_data.columns = "comp0", "comp1", "comp2", "comp3", "comp4", "comp5"
final = pd.concat([wine3.Type, pca_data.iloc[:, 0:3]], axis = 1)
#Excluding Type column
final1=final.iloc[:,1:]
# Now let us apply to agglomerative clustering
from scipy.cluster.hierarchy import linkage
import scipy.cluster.hierarchy as sch
z=linkage(final1,method="complete",metric="euclidean")
plt.figure(figsize=(15,8));plt.title("Hierarchical Clustering dendrogram");plt.xlabel("Index");plt.ylabel("Distance")
sch.dendrogram(z,leaf_rotation=0,leaf_font_size=10)
plt.show()

# applying agglomerative clustering choosing 3 as clusters from dendrogram
from sklearn.cluster import AgglomerativeClustering
h_complete=AgglomerativeClustering(n_clusters=3,linkage='complete',affinity="euclidean").fit(df_norm)
# apply labels to the clusters
h_complete.labels_
cluster_labels=pd.Series(h_complete.labels_)
#Assign this series to Univ Dataframe as column and name the column as "clust"
final['clust']=cluster_labels

final.Type.value_counts()
#2    71
#1    59
#3    48
final.clust.value_counts()
#1     34    # Equivalent to Type-2,50 % correct classification
#0    116    # Equivalent to Type-1,50 % correct classification
#2     28    # Equivalent to Type-3,50 % correct classification

