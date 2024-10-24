### Task: Clustering Daily Energy Consumption Profiles

**Dataset**: Use the [Hourly Energy Consumption dataset](https://www.kaggle.com/datasets/robikscube/hourly-energy-consumption) available on Kaggle. Use only American Electric Power (AEP) dataset

#### Steps:

1. **Data Preparation**:
   - Load the dataset and extract relevant columns (e.g., `Datetime`, `Megawatt Energy Consumption`).
   - Handle any missing data by filling or interpolating values.
   
2. **Feature Engineering**:
   - Create a pivot table where each row represents a day, and each column represents the hourly energy consumption for that day (24 hours as columns).
   
3. **Data Normalization**:
   - Scale the data to ensure that differences in magnitude (e.g., between peak and low consumption hours) do not affect clustering.

4. **Clustering with K-Means**:
   - Apply the K-means clustering algorithm to identify different energy consumption profiles.
   - Experiment with different numbers of clusters (e.g., 2–5) and use the silhouette score to evaluate the optimal number of clusters.

5. **Visualization**:
   - Plot the daily load profiles in a 2D plane using t-SNE or PCA to visualize how well the data is clustered.

6. **Analysis**:
   - Interpret the resulting clusters (e.g., cluster 1 represents weekends with high afternoon energy usage, cluster 2 represents weekdays with a peak in the morning, etc.).
   
7. **Optional Extensions**:
   - Apply different clustering algorithms to see if they perform better than K-means (e.g., DBSCAN or Agglomerative Clustering).

#### Deliverables:
- Code implementation for data preparation, clustering, and visualization.
- A summary of findings and insights from clustering energy consumption profiles.