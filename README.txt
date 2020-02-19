CSE-472 Project 2: Evolution of Bots

With the advent of internet there has been substantial increase in con-
tent polluters and fake bots on various popular social media platforms like
Twitter, Facebook and many others. Out of these, political bots majorly
involve in intentionally automating interactions related to political issues
and elections. Hence it becomes critical for such a platform to detect
these bots and eliminate them when found. And with increased knowl-
edge they have improved over the time to refrain from getting detected
using traditional methods. Through this study we have (1) collected a
subset of data-set comprising of accounts who were active on topics re-
lated to 2016 US Presidential elections (2) used cluster analysis to identify
dierent types of bots and their patterns (3) compared these results to
that of Lee et al.[2] to understand intentions of these bots (4) presented
an analysis on how these bots have evolved over time with knowledge.

Keywords fake bot detection, evolution of bots, cluster analysis, US election twit-
ter data, social media mining, in
uence of twitter bots on 2016 US election


Running Instructions and Information:

1) Code folder contains the source code for crawling twitter data, classifying bots and performing clustering.
2) Run setup.sh to generate a virtual environment with all the dependencies.
3) Within the virtualenv run the following command to generate the 57196x 10 feature vectors from the JSON data structure: "python generate_feature_vectors.py"
4) Run the following command to classify the twitter users as bot or human:[The userlabels.pickle file which is created by this command is already provided,so this step can be skipped: "python detect_bot.py"
5) Run the following command to perform clustering and display the clusters: "python generate_display_clusters.py"

Contributors: 
Jay Shah
Kunal Vinay Kumar Suthar
