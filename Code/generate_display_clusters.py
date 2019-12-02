import json
import botometer
import pickle
import random
import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA,TruncatedSVD
from sklearn.manifold import TSNE
from sklearn.cluster import DBSCAN
from sklearn.mixture import GaussianMixture
import pylab as pl
import plotly.graph_objects as go
from random import randrange

def main():
	f=open('data/user_labels.pickle','rb')
	user_labels=pickle.load(f)
    
	f_vec,bot_names=get_bot_data_matrix_from_data(user_labels=user_labels)

	labels=predict_labels_from_DBSCAN(users_feature_matrix=f_vec)+1	
	num_of_labels=len(np.unique(labels))
	gmm_labels=predict_labels_from_GMM(users_feature_matrix=f_vec,num_of_labels=num_of_labels)
	km_labels=predict_labels_from_KMeans(users_feature_matrix=f_vec,num_of_labels=num_of_labels)

	gmm_user_type=get_user_type_dict(bot_names=bot_names,labels=gmm_labels)
	km_user_type=get_user_type_dict(bot_names=bot_names,labels=km_labels)

	user_fv=get_user_feature_vector_dict(bot_names=bot_names,f_vec=f_vec)

	plot_clusters_in_2D_using_PCA(users_feature_matrix=f_vec,labels=gmm_labels,algo='GMM')
	plot_clusters_in_2D_using_PCA(users_feature_matrix=f_vec,labels=km_labels,algo='KMeans')

	plot_clusters_in_2D_using_TSNE(users_feature_matrix=f_vec,labels=gmm_labels,algo='GMM')
	plot_clusters_in_2D_using_TSNE(users_feature_matrix=f_vec,labels=km_labels,algo='KMeans')
	
	display_avg_feature_vector_by_cluster_type(user_type=gmm_user_type,user_fv=user_fv,labels=np.unique(gmm_labels))
	display_tweets_by_cluster_type(user_type=gmm_user_type,labels=np.unique(gmm_labels),l_type=10)
	display_avg_feature_vector_by_cluster_type(user_type=km_user_type,user_fv=user_fv,labels=np.unique(km_labels))
	display_tweets_by_cluster_type(user_type=km_user_type,labels=np.unique(km_labels),l_type=10)

def get_user_type_dict(bot_names,labels):
	user_type={}
	i=0
	for bot in bot_names:
		user_type[bot]=labels[i]
		i=i+1

	return user_type

def get_user_feature_vector_dict(bot_names,f_vec):
	user_fv={}
	i=0
	for bot in bot_names:
		user_fv[bot]=f_vec[i]
		i=i+1

	return user_fv

def display_tweets_by_cluster_type(user_type,labels,l_type):
	label=l_type
	print(f'################# Running for label={label} ####################')
	for user in user_type.keys():
		if user_type[user] == label:
			print(f'User={user}')
			print(f'Tweet={get_tweets_for_a_user(user)}')
	print(f'################# Ending the run for label={label} ####################')		


def display_avg_feature_vector_by_cluster_type(user_type,user_fv,labels):
	"""
	Has the following format
    | len_screen_name | longevity | friends | followers | frnd-follower ratio | # tweets | # of tweets per day | total retweets received | total favorited | total favorites received
    """
	for label in labels:
		avg_vec=np.zeros((1,10))
		print(f'################# Running for label={label} ####################')
		num_of_users=0
		for user in user_fv.keys():
			if user_type[user] == label:
				avg_vec=avg_vec+user_fv[user]
				num_of_users=num_of_users+1
		avg_vec=avg_vec/num_of_users
		print(f'Number of users:={num_of_users}')
		print(f'Average feature vector==={avg_vec}')
		print(f'Length of screen_name= {avg_vec[0][0]}')
		print(f'Longevity of account= {avg_vec[0][1]}')
		print(f'Number of following= {avg_vec[0][2]}')
		print(f'Number of followers= {avg_vec[0][3]}')
		print(f'Friend Follower Ratio= {avg_vec[0][4]}')
		print(f'Number of total tweets= {avg_vec[0][5]}')
		print(f'Number of tweets per day= {avg_vec[0][6]}')
		print(f'Total Retweets received= {avg_vec[0][7]}')
		print(f'Total favorited= {avg_vec[0][8]}')	
		print(f'Total favorites received= {avg_vec[0][9]}')	
		print(f'################# Ending the run for label={label} ####################')

def get_bot_data_matrix_from_data(user_labels):
	f=open('data/user_features.pickle','rb')
	user_features=pickle.load(f)
	bot_names=[]
	matrix=[]
	for user in user_labels.keys():
		if user_labels[user] == 1:
			matrix.append(user_features[user])
			bot_names.append(user)

	return np.array(matrix),bot_names

def get_humans_data_matrix_from_data(user_labels):
	f=open('data/user_features.pickle','rb')
	user_features=pickle.load(f)
	matrix=[]
	for user in user_labels.keys():
		if user_labels[user] == 0:
			matrix.append(user_features[user])
	
	return np.array(matrix)

def predict_labels_from_GMM(users_feature_matrix,num_of_labels):
	gmm=GaussianMixture(n_components=num_of_labels)
	labels=gmm.fit_predict(X=users_feature_matrix)
	return labels

def predict_labels_from_KMeans(users_feature_matrix,num_of_labels):
	kmeans=KMeans(n_clusters=num_of_labels)
	kmeans.fit(users_feature_matrix)
	labels=kmeans.predict(users_feature_matrix)
	return labels

def predict_labels_from_DBSCAN(users_feature_matrix):
	dbscan= DBSCAN(eps=2,min_samples=2)
	labels= dbscan.fit_predict(users_feature_matrix)
	return labels

def get_tweets_for_a_user(screen_name):
	with open('data-4.json') as json_file:
		line=json_file.readline()
		
		while line: 
			data=json.loads(line)
			if getScreenName(data)==screen_name:
				return getFullText(data)

			line=json_file.readline()	

		return None	


def plot_clusters_in_2D_using_PCA(users_feature_matrix,labels,algo):
	pca_2d = PCA(n_components=2).fit_transform(users_feature_matrix)
	pl.figure(f'{algo} with {len(np.unique(labels))} clusters')
	pl.scatter(pca_2d[:, 0], pca_2d[:, 1], c=labels)
	pl.show()		
	
def plot_clusters_in_2D_using_TSNE(users_feature_matrix,labels,algo):
	tsne_2d = TSNE(n_components=2).fit_transform(users_feature_matrix)
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=tsne_2d[:,0], y=tsne_2d[:,1],
                    mode='markers',
                    name='markers',
                    marker=dict(
                	color=labels)
                    ))
	fig.show()

def get_historical_data_for_a_user(screen_name):
	pass

def getFullText(data):
	try:
		return data['retweeted_status']['full_text']

	except Exception as e:
		return data['full_text']	

def getRetweeterName(data):
    return data['user']['screen_name']

def getScreenName(data):
    try:
        return data['retweeted_status']['user']['screen_name']

    except Exception as e:
        return getRetweeterName(data)    

if __name__ == '__main__':
	main()