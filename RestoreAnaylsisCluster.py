import os
import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist
import networkx as nx

# Load your DataFrame
original_csv_path = '/Users/seggewa/Desktop/2024-02-04_16-04-36_SV5.tracks.csv'
df = pd.read_csv(original_csv_path)

# Prepare a DataFrame to hold all cluster information across frames
all_frames_clusters = pd.DataFrame()

for frame in df['frame'].unique():
    # Filter data for the current frame
    frame_data = df[df['frame'] == frame]

    # Total tracks in the frame
    total_tracks = frame_data['track_id'].nunique()

    # Create graph for the current frame
    G = nx.Graph()

    # Calculate distances and filter within 100 pixels
    body_coordinates = frame_data[['x_spiracle', 'y_spiracle']].to_numpy()
    distance_matrix = cdist(body_coordinates, body_coordinates, 'euclidean')
    np.fill_diagonal(distance_matrix, np.nan)

    # Add edges if distance is 100 pixels or less
    for i in range(distance_matrix.shape[0]):
        for j in range(i + 1, distance_matrix.shape[1]):
            if not np.isnan(distance_matrix[i, j]) and distance_matrix[i, j] <= 30:
                G.add_edge(frame_data.iloc[i]['track_id'], frame_data.iloc[j]['track_id'])

    # Identify clusters
    clusters = [c for c in nx.connected_components(G) if len(c) >= 3]

    if clusters:
        clustered_tracks = len(set.union(*[set(cluster) for cluster in clusters]))
        cluster_percentage = (clustered_tracks / total_tracks) * 100
    else:
        cluster_percentage = 0

    # Create a DataFrame for the current frame's clusters
    frame_clusters = pd.DataFrame({
        'Frame': frame,
        'Cluster': list(range(1, len(clusters) + 1)),
        'Tracks': [', '.join(map(str, cluster)) for cluster in clusters],
        'Percentage of Tracks in Clusters': [cluster_percentage] * len(clusters)
    })

    # Append the current frame's clusters to the all_frames_clusters DataFrame
    all_frames_clusters = pd.concat([all_frames_clusters, frame_clusters], ignore_index=True)

# Construct the output file path
base_name = os.path.basename(original_csv_path)  # Extract basename of the original file
name, ext = os.path.splitext(base_name)  # Split the extension from the basename
output_path = os.path.join(os.path.dirname(original_csv_path), f"{name}_CLUSTERANALYSIS{ext}")

# Save the clusters DataFrame to the new CSV file
all_frames_clusters.to_csv(output_path, index=False)

print(f"Clusters saved to CSV: {output_path}")
