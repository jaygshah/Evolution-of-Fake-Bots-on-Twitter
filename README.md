# CSE-472 Project 2: Evolution of Bots

With the advent of internet there has been substantial increase in content polluters and fake bots on various popular social media platforms like Twitter, Facebook and many others. Out of these, political bots majorly involve in intentionally automating interactions related to political issues and elections. Hence it becomes critical for such a platform to detect
these bots and eliminate them when found. And with increased knowledge they have improved over the time to refrain from getting detected using traditional methods. Through this study we have 
- Collected a subset of data-set comprising of accounts who were active on topics related to 2016 US Presidential elections
- Used cluster analysis to identify different types of bots and their patterns 
- Compared these results to that of Lee et al.[2] to understand intentions of these bots 
- Presented an analysis on how these bots have evolved over time with knowledge.

Keywords fake bot detection, evolution of bots, cluster analysis, US election twitter data, social media mining, influence of twitter bots on 2016 US election


Running Instructions and Information:

1) Code folder contains the source code for crawling twitter data, classifying bots and performing clustering.
2) Run setup.sh to generate a virtual environment with all the dependencies.
3) Within the virtualenv run the following command to generate the 57196x 10 feature vectors from the JSON data structure: "python generate_feature_vectors.py"
4) Run the following command to classify the twitter users as bot or human:[The userlabels.pickle file which is created by this command is already provided,so this step can be skipped: "python detect_bot.py"
5) Run the following command to perform clustering and display the clusters: "python generate_display_clusters.py"

Lee et. al[1] showed an analysis of different types of content polluters based on their activity and account characteristics on 2011 US election data. We use a subset of those features to analyse how these bots have evolved in their methodologies based on 2016 US election data and provide insights for robust classification.

Features we use: [screen-name length, account longevity, clusters in 2D using t-SNE on K-means
followers/#following, #tweets, #tweets per day, retweets received, #favorites received]

Dataset: [9,016 / 57,196] bot accounts extracted from 1,85,000 tweets scraped using Twitter API.

Results: We used DBSCAN, K-Means and GMM using DBSCAN we are able to find 11 differentiable clusters and 4 categories
- Duplicate + Duplicate @Spammers: 143
- Sophisticated Active: 5988
- Sophisticated Influential: 2885

![clusters in 2D using t-SNE on K-means](/clusters_in_2D_using_tSNE_on_Kmeans.png)

