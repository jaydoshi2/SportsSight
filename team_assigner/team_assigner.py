from sklearn.cluster import KMeans


class TeamAssigner:

    def __init__(self):
        self.team_colors = {}
        self.player_team_dict = {}

    def get_clustering_model(self, image):
        # Reshape the image to 2D array
        image_2d = image.reshape(-1, 3)

        # Preform K-means with 2 clusters
        kmeans = KMeans(n_clusters=2, init="k-means++", n_init=1)
        """
        n_clusters=2: We are clustering into 2 groups, assuming one group represents the player and the other the background.
        init="k-means++": This initializes the cluster centroids in a smart way to speed up convergence.
        n_init=1: The algorithm runs only once to initialize centroids.
        
        LOGIC: This part identifies two distinct regions in the top half of the image by clustering similar pixel colors. 
        This is important because we expect that one cluster will represent the background (usually less important), 
        and the other will represent the player’s uniform color.
        """

        kmeans.fit(image_2d)

        return kmeans

    def get_player_color(self, frame, bbox):
        """
        Crop the Image: Using the provided bounding box (bbox), we crop out the player's portion from the frame. 
        The bounding box is in the format (x1, y1, x2, y2), where (x1, y1) represents the top-left corner and (x2, y2) the bottom-right corner.
        
        """
        image = frame[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2])]
        """
        frame[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2])]: This is slicing the image to extract the player's bounding box. 
        bbox[1]:bbox[3] extracts the height (rows), and bbox[0]:bbox[2] extracts the width (columns).
        """

        top_half_image = image[0:int(image.shape[0] / 2), :]

        # Get Clustering model
        kmeans = self.get_clustering_model(top_half_image)

        # Get the cluster labels forr each pixel
        labels = kmeans.labels_

        # Reshape the labels to the image shape
        clustered_image = labels.reshape(top_half_image.shape[0],
                                         top_half_image.shape[1])

        # Get the player cluster
        corner_clusters = [
            clustered_image[0, 0], clustered_image[0, -1],
            clustered_image[-1, 0], clustered_image[-1, -1]
        ]
        non_player_cluster = max(set(corner_clusters),
                                 key=corner_clusters.count)
        player_cluster = 1 - non_player_cluster

        player_color = kmeans.cluster_centers_[player_cluster]

        return player_color

    def assign_team_color(self, frame, player_detections):
        """
        frame: This is the current frame/image containing players (e.g., from a video feed).
        player_detections: A dictionary containing detected players, 
        where each entry has a bounding box (bbox) specifying the area where the player is locat
        """

        player_colors = []
        """
        player_detection dictionary. The bbox is expected to be in the format (x1, y1, x2, y2), which defines the rectangle that encloses the player in the frame.
        Get Player Color: The get_player_color method is called, passing the entire frame and the bounding box of the player. 
        This method processes the cropped image of the player to determine the dominant color of their uniform. The returned color (in RGB format) is stored in player_color.
        Store Player Color: The determined player_color is appended to the player_colors list.
        After this loop, player_colors will contain the dominant colors for all detected players.
        
        """
        for _, player_detection in player_detections.items():
            bbox = player_detection["bbox"]
            player_color = self.get_player_color(frame, bbox)
            player_colors.append(player_color)
        """
        Create KMeans Instance: A KMeans clustering object is created with the following parameters:

        n_clusters=2: This means we want to group the players into two distinct teams based on their colors.
        init="k-means++": This initializes the cluster centers using the k-means++ algorithm, which helps to ensure that the initial centers are selected more intelligently, often leading to better convergence.
        n_init=10: This means the algorithm will run 10 times with different centroid seeds and return the best output based on inertia (the sum of squared distances from each point to its assigned cluster center).
        Fit the Model: The fit method is called with player_colors. This method will compute the KMeans clustering based on the player colors. It effectively partitions the players' colors into two clusters (teams).
        """

        kmeans = KMeans(n_clusters=2, init="k-means++", n_init=10)
        kmeans.fit(player_colors)

        self.kmeans = kmeans
        """
        Assign Team Colors: The cluster centers returned by KMeans represent the average color of each cluster. These colors are assigned to the team_colors dictionary:
        self.team_colors[1] = kmeans.cluster_centers_[0]: The color of team 1 is set to the first cluster center.
        self.team_colors[2] = kmeans.cluster_centers_[1]: The color of team 2 is set to the second cluster center.
        After this step, self.team_colors will have two entries, with each team assigned a dominant color based on the clustering results.
        """
        self.team_colors[1] = kmeans.cluster_centers_[0]
        self.team_colors[2] = kmeans.cluster_centers_[1]



    def get_player_team(self, frame, player_bbox, player_id):
        if player_id in self.player_team_dict:
            return self.player_team_dict[player_id]

        player_color = self.get_player_color(frame, player_bbox)

        team_id = self.kmeans.predict(player_color.reshape(1, -1))[0]
        team_id += 1

        if player_id == 91:
            team_id = 1

        self.player_team_dict[player_id] = team_id

        return team_id
