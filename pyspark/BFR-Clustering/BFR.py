from pyspark.sql import SparkSession
import os
import numpy as np
from sklearn.cluster import KMeans
from math import sqrt
from itertools import combinations

# import sklearn

np.random.seed(1)

path = 'Data/hw5_clustering.txt'

ss = SparkSession.builder.getOrCreate()

sc = ss.sparkContext

clusterRDD = sc.textFile(path)

clusterRDD = clusterRDD.map(lambda line: line.split(',')) \
    .map(lambda line: [int(line[0]), int(line[1]), float(line[2]), float(line[3])])

all_points = np.array(clusterRDD.map(lambda line: (line[2], line[3])).collect())


# -------------------------- initialization Started --------------------------


# print('DS:')
# for k, v in DS.items():
#     print('Cluster {}: {}'.format(k, v))
# print('RS:')
# print(RS)


# -------------------------- initialization Finished --------------------------

# Step 6

class BRF(object):

    def __init__(self, init_data):
        self.init_data = init_data
        self.DS = None
        self.CS = None
        self.RS = None

    def init(self):
        # Step 1

        # sample_index = np.random.randint(low=0, high=len(all_points), size=round(len(init_data) * 0.2))

        # sample_points = all_points[sample_index, 2:]

        # Step 2

        kmeans = KMeans(n_clusters=100, random_state=0).fit(self.init_data)

        clusters = {}

        for i in range(len(kmeans.labels_)):
            try:
                clusters[kmeans.labels_[i]].append(tuple(self.init_data[i]))
            except:
                clusters[kmeans.labels_[i]] = [tuple(self.init_data[i])]

        DS_points = []
        RS = []

        # Step 3

        for cluster_num, points in clusters.items():
            if len(points) == 1:
                RS.append(list(points[0]))
            else:
                DS_points.extend(points)

        # Step 4

        kmeans = KMeans(n_clusters=100, random_state=0).fit(np.array(DS_points))

        # Step 5

        DS = []

        centers = kmeans.cluster_centers_

        clusters = {}

        for i in range(len(kmeans.labels_)):
            try:
                clusters[kmeans.labels_[i]].append(tuple(DS_points[i]))
            except:
                clusters[kmeans.labels_[i]] = [tuple(DS_points[i])]

        for cluster_num, points in clusters.items():
            # print(points)
            DS.append({'N': len(points),
                       'SUM': [sum(j for j in i) for i in zip(*points)],
                       'SUMSQ': [sum(j ** 2 for j in i) for i in zip(*points)]})

        # Step 6
        if len(RS) < 100:
            CS = []
        else:
            kmeans = KMeans(n_clusters=100, random_state=0).fit(np.array(RS))
            clusters = {}
            for i in range(len(kmeans.labels_)):
                try:
                    clusters[kmeans.labels_[i]].append(tuple(RS[i]))
                except:
                    clusters[kmeans.labels_[i]] = [tuple(RS[i])]
            CS = []
            RS = []
            for cluster_num, points in clusters.items():
                if len(points) == 1:
                    RS.append(list(points[0]))
                else:
                    CS.append({'N': len(points),
                               'SUM': [sum(j for j in i) for i in zip(*points)],
                               'SUMSQ': [sum(j ** 2 for j in i) for i in zip(*points)]})
        self.DS = DS
        self.CS = CS
        self.RS = RS

    def Mahalanobis(self, point, cluster_dict):
        N = cluster_dict['N']
        SUM_list = cluster_dict['SUM']
        SUMSQ_list = cluster_dict['SUMSQ']
        mean_list = [SUM / N for SUM in SUM_list]
        variance_list = [(SUMSQ / N) - ((SUM / N) ** 2) for SUM, SUMSQ in zip(SUM_list, SUMSQ_list)]
        return sum([(X - C) ** 2 / V for X, C, V in zip(point, mean_list, variance_list)]) ** 0.5

    def bfr_main(self, new_data):

        # Step 7
        for data in new_data:
            # Step 8
            dist = float('inf')
            cluster = -1
            for key, value in enumerate(self.DS):
                temp_dist = self.Mahalanobis(data, value)
                if temp_dist < dist:
                    dist = temp_dist
                    cluster = key

            if dist < 2 * (2 ** (1 / 2)):
                self.DS[cluster]['N'] += 1
                self.DS[cluster]['SUM'] = [self.DS[cluster]['SUM'][0] + data[0],
                                           self.DS[cluster]['SUM'][1] + data[1]]
                self.DS[cluster]['SUMSQ'] = [self.DS[cluster]['SUMSQ'][0] + data[0] ** 2,
                                             self.DS[cluster]['SUMSQ'][1] + data[1] ** 2]

            # Step 9
            else:
                dist = float('inf')
                cluster = -1
                for key, value in enumerate(self.CS):
                    temp_dist = self.Mahalanobis(data, value)
                    if temp_dist < dist:
                        dist = temp_dist
                        cluster = key

                if dist < 2 * (2 ** (1 / 2)):
                    self.CS[cluster]['N'] += 1
                    self.CS[cluster]['SUM'] = [self.CS[cluster]['SUM'][0] + data[0],
                                               self.CS[cluster]['SUM'][1] + data[1]]
                    self.CS[cluster]['SUMSQ'] = [self.CS[cluster]['SUMSQ'][0] + data[0] ** 2,
                                                 self.CS[cluster]['SUMSQ'][1] + data[1] ** 2]

                # Step 10
                else:
                    self.RS.append(data)

        # Step 11
        if len(self.RS) > 100:
            kmeans = KMeans(n_clusters=100, random_state=0).fit(np.array(self.RS))
            centers = kmeans.cluster_centers_

            clusters = {}

            CS = []
            RS = []

            for i in range(len(kmeans.labels_)):
                try:
                    clusters[kmeans.labels_[i]].append(tuple(self.RS[i]))
                except:
                    clusters[kmeans.labels_[i]] = [tuple(self.RS[i])]

            for cluster_num, points in clusters.items():
                if len(points) == 1:
                    RS.append(list(points[0]))
                else:
                    CS.append({'N': len(points),
                               'SUM': [sum(j for j in i) for i in zip(*points)],
                               'SUMSQ': [sum(j ** 2 for j in i) for i in zip(*points)]})

            self.CS.extend(CS)
            self.RS = RS

        # Step 12
        self.mergeCS()

    def mergeCS(self):
        l = []
        for comb in combinations(self.CS, 2):
            A = comb[0]
            B = comb[1]
            A_centroid = [i / A['N'] for i in A['SUM']]
            d = self.Mahalanobis(A_centroid, B)
            if d < 2 * (2 ** 0.5):
                l.append([d, self.CS.index(A), self.CS.index(B)])
        if l:
            D_list = min(l, key=lambda x: x[0])
            if D_list[1] > D_list[2]:
                A = self.CS.pop(D_list[1])
                B = self.CS.pop(D_list[2])
            else:
                B = self.CS.pop(D_list[2])
                A = self.CS.pop(D_list[1])
            C = {'N': A['N'] + B['N'],
                 'SUM': [i + j for i, j in zip(A['SUM'], B['SUM'])],
                 'SUMSQ': [i + j for i, j in zip(A['SUMSQ'], B['SUMSQ'])]}
            self.CS.append(C)
            return True
        else:
            return False

    def finish(self):
        for A in self.CS:
            l = []
            centroid = [SUM / A['N'] for SUM in A['SUM']]
            for B in self.DS:
                l.append([self.Mahalanobis(centroid, B), self.DS.index(B)])
            D_list = min(l, key=lambda x: x[0])
            B = self.DS[D_list[1]]
            self.DS[D_list[1]] = {'N': A['N'] + B['N'],
                                  'SUM': [i + j for i, j in zip(A['SUM'], B['SUM'])],
                                  'SUMSQ': [i + j for i, j in zip(A['SUMSQ'], B['SUMSQ'])]}
        for P in self.RS:
            l = []
            for C in self.DS:
                l.append([self.Mahalanobis(P, C), self.DS.index(C)])
            D_list = min(l, key=lambda x: x[0])
            C = self.DS[D_list[1]]
            self.DS[D_list[1]] = {'N': 1 + C['N'],
                                  'SUM': [i + j for i, j in zip(P, C['SUM'])],
                                  'SUMSQ': [i ** 2 + j for i, j in zip(P, C['SUMSQ'])]}


percentage = 0.2

n = len(all_points)
print(n)
init_data = all_points[:int(percentage * n)]

brf = BRF(init_data)
brf.init()
round = 1
print(f'Round {round}: {sum(cluster["N"] for cluster in brf.DS)}, {len(brf.CS)}, {sum(cluster["N"] for cluster in brf.CS)}, {len(brf.RS)}')

start = int(n * percentage)
end = start + int(n * percentage)
i = 0
while start < n:
    # print(i)
    i += 1
    # print(start, end)
    if i == 4:
        brf.bfr_main(all_points[start:])
    else:
        brf.bfr_main(all_points[start:end])
    start = end
    end = start + int(n * percentage)
    round += 1
    print(f'Round {round}: {sum(cluster["N"] for cluster in brf.DS)}, {len(brf.CS)}, {sum(cluster["N"] for cluster in brf.CS)}, {len(brf.RS)}')
    if i == 4:
        brf.finish()
        break

# next_data = all_points[int(percentage * n) + 1: int(n * 0.4) + 1]
# brf.init()
#
# brf.bfr_main(next_data)

# print(brf.DS)
print(sum([item['N'] for item in brf.DS]))
# print(brf.RS)
# print(brf.CS)
