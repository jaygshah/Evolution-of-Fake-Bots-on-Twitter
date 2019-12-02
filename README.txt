CSE-472 Project 2: Evolution of Bots

Student Names: 
Kunal Vinay Kumar Suthar
Jay Shah


Running Instructions and Information:

1) Code folder contains the source code for crawling twitter data, classifying bots and performing clustering.
2) Run setup.sh to generate a virtual environment with all the dependencies.
3) Within the virtualenv run the following command to generate the 57196x 10 feature vectors from the JSON data structure: "python generate_feature_vectors.py"
4) Run the following command to classify the twitter users as bot or human:[The userlabels.pickle file which is created by this command is already provided,so this step can be skipped: "python detect_bot.py"
5) Run the following command to perform clustering and display the clusters: "python generate_display_clusters.py"

