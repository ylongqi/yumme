import sys
import numpy as np
import pickle
import random
import sklearn.preprocessing as preprocessing
import math
import json
import scipy.sparse as sparse

DEBUG=False

import logging
logger = logging.getLogger(__name__)

if (DEBUG):
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.ERROR)

logFormatter = logging.Formatter("%(asctime)s [%(filename)s:%(lineno)s] [%(levelname)-5.5s]  %(message)s")

fileHandler = logging.FileHandler("{0}/{1}.log".format('.', 'server'))
fileHandler.setFormatter(logFormatter)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)

logger.addHandler(consoleHandler)
logger.addHandler(fileHandler)
logger.propagate = False

if DEBUG:
    from inspect import getargspec, getmembers, ismethod
    logger.info('DEBUG is opening. Please turn it off before deployment!')

    def overrides(interface):
        def overrider(method):
            try:
                synonyms = filter(lambda (_,m): m.__name__ == method.__name__, getmembers(interface, ismethod))
                assert len(synonyms)
                assert len(filter(lambda (_,m): getargspec(m.__func__) == getargspec(method), synonyms))
            except AssertionError:
                print('method %s is not overriding, please check signiture' % method.__name__)
                sys.exit(-1)
            return method
        return overrider
else:
    # if not DEBUG, return null decorator to avoid overhead
    def overrides(inf):
        def overrider(method):
            return method
        return overrider


class ServerHandler():

    def __init__(self):
        # Define global common variables for users
        self.user_dict = dict()
        self.Propagate_matrix = {}

        with open("plateclick_data/MainDishes_prop.pickle", "r") as f_handle:
            self.Propagate_matrix["normal"] = pickle.load(f_handle)
        with open("plateclick_data/vegetarian_prop.pickle", "r") as f_handle:
            self.Propagate_matrix["vegetarian"] = pickle.load(f_handle)
        with open("plateclick_data/vegan_prop.pickle", "r") as f_handle:
            self.Propagate_matrix["vegan"] = pickle.load(f_handle)
        with open("plateclick_data/kosher_prop.pickle", "r") as f_handle:
            self.Propagate_matrix["kosher"] = pickle.load(f_handle)
        with open("plateclick_data/halal_prop.pickle", "r") as f_handle:
            self.Propagate_matrix["halal"] = pickle.load(f_handle)

        self.Image_id_list = {}
        with open("plateclick_data/MainDishes_items.pickle", "r") as f_handle:
            self.Image_id_list["normal"] = pickle.load(f_handle)
        with open("plateclick_data/vegetarian_items.pickle", "r") as f_handle:
            self.Image_id_list["vegetarian"] = pickle.load(f_handle)
        with open("plateclick_data/vegan_items.pickle", "r") as f_handle:
            self.Image_id_list["vegan"] = pickle.load(f_handle)
        with open("plateclick_data/kosher_items.pickle", "r") as f_handle:
            self.Image_id_list["kosher"] = pickle.load(f_handle)
        with open("plateclick_data/halal_items.pickle", "r") as f_handle:
            self.Image_id_list["halal"] = pickle.load(f_handle)

        self.Dist_matrix_size = dict()
        self.Dist_matrix_size["normal"] = len(self.Image_id_list["normal"])
        self.Dist_matrix_size["vegetarian"] = len(self.Image_id_list["vegetarian"])
        self.Dist_matrix_size["vegan"] = len(self.Image_id_list["vegan"])
        self.Dist_matrix_size["kosher"] = len(self.Image_id_list["kosher"])
        self.Dist_matrix_size["halal"] = len(self.Image_id_list["halal"])

        self.nutrition_rank = {}
        with open("plateclick_data/MainDishes_ranks.pickle", "r") as f_handle:
            self.nutrition_rank["normal"] = pickle.load(f_handle)
        with open("plateclick_data/vegetarian_ranks.pickle", "r") as f_handle:
            self.nutrition_rank["vegetarian"] = pickle.load(f_handle)
        with open("plateclick_data/vegan_ranks.pickle", "r") as f_handle:
            self.nutrition_rank["vegan"] = pickle.load(f_handle)
        with open("plateclick_data/kosher_ranks.pickle", "r") as f_handle:
            self.nutrition_rank["kosher"] = pickle.load(f_handle)
        with open("plateclick_data/halal_ranks.pickle", "r") as f_handle:
            self.nutrition_rank["halal"] = pickle.load(f_handle)

        self.Kpp = KPlusPlus(self.Dist_matrix_size, N = 10)

        self.file_prefix = "../user/"

    def user_register(self, uid, category, goals):
        if uid not in self.user_dict.keys():
            self.user_dict[uid] = YummeUser(Dist_matrix_size=self.Dist_matrix_size[category], 
                                            Iteration=15, Category=category, Goals=goals)
        return True

    def user_verify(self, uid):
        return uid in self.user_dict

    def phase_i(self, uid, choice):
        
        try:
            if self.user_dict[uid].user_iteration > 1 and \
                self.user_dict[uid].user_iteration <= self.user_dict[uid].max_iteration:   # Maximum Iteration
                self.user_dict[uid].propagate(choice, self.Propagate_matrix[self.user_dict[uid].category])

            if self.user_dict[uid].user_iteration <= 2:
                id_list = self.Kpp.init_cluster(category=self.user_dict[uid].category)   # Initialization use K-means++
                url_list = self.convert_to_url(category=self.user_dict[uid].category, id_list=id_list)
                self.user_dict[uid].last_image_list = id_list
                self.user_dict[uid].user_image_visited += id_list
                self.user_dict[uid].user_iteration += 1
                return url_list
            elif self.user_dict[uid].user_iteration <= self.user_dict[uid].max_iteration:
                return self._phase_ii(uid, choice)
            else:
                return []
            
        except KeyboardInterrupt:
            pass

    def _phase_ii(self, uid, choice):
        try:

            upper_percentile = np.percentile(np.array(self.user_dict[uid].user_preference), 99)
            aggregate_preference = list()
            for prefer in self.user_dict[uid].user_preference:
                if prefer >= upper_percentile:
                    aggregate_preference.append(prefer)
                else:
                    aggregate_preference.append(0.0)

            aggregate_preference = np.array(aggregate_preference) / np.sum(aggregate_preference)
            cluster_1 = self.select_with_prob(aggregate_preference)
            cluster_2 = random.choice(list(set(range(self.Dist_matrix_size[self.user_dict[uid].category])).difference(self.user_dict[uid].user_image_propagated)))
            while cluster_1 == cluster_2 or (cluster_1 in self.user_dict[uid].user_image_visited and cluster_2 in self.user_dict[uid].user_image_visited):
                cluster_1 = self.select_with_prob(aggregate_preference)
                cluster_2 = random.choice(list(set(range(self.Dist_matrix_size[self.user_dict[uid].category])).difference(self.user_dict[uid].user_image_propagated)))

            id_list = [cluster_1, cluster_2]
            random.shuffle(id_list)
            url_list = self.convert_to_url(category=self.user_dict[uid].category, id_list = id_list)
            self.user_dict[uid].last_image_list = id_list
            self.user_dict[uid].user_image_visited += id_list
            self.user_dict[uid].user_iteration += 1
            return url_list
        except KeyboardInterrupt:
            pass

    def request_ranking(self, uid, choice):

        try:
            ranking_array = np.zeros(self.Dist_matrix_size[self.user_dict[uid].category])
            
            # Calories
            if int(self.user_dict[uid].goals["calories"]) == 0:
                logger.info("Low Calories")
                ranking_array += self.nutrition_rank[self.user_dict[uid].category]["C"]["L"]
            elif int(self.user_dict[uid].goals["calories"]) == 2:
                logger.info("High Calories")
                ranking_array += self.nutrition_rank[self.user_dict[uid].category]["C"]["M"]
            
            # Fat
            if int(self.user_dict[uid].goals["fat"]) == 0:
                logger.info("Low Fat")
                ranking_array += self.nutrition_rank[self.user_dict[uid].category]["F"]["L"]
            elif int(self.user_dict[uid].goals["fat"]) == 2:
                logger.info("High Fat")
                ranking_array += self.nutrition_rank[self.user_dict[uid].category]["F"]["M"]
            
            # Protein
            if int(self.user_dict[uid].goals["protein"]) == 0:
                logger.info("Low Protein")
                ranking_array += self.nutrition_rank[self.user_dict[uid].category]["P"]["L"]
            elif int(self.user_dict[uid].goals["protein"]) == 2:
                logger.info("High Protein")
                ranking_array += self.nutrition_rank[self.user_dict[uid].category]["P"]["M"]

            if np.sum(ranking_array) == 0:
                images_pool = np.array(list(set(random.sample(range(len(ranking_array)), 500)).difference(self.user_dict[uid].user_image_visited)))
            else:
                images_pool = np.array(list(set(np.argsort(ranking_array)[:500]).difference(self.user_dict[uid].user_image_visited)))
            
            positive_images = list(images_pool[np.argsort(-np.array(self.user_dict[uid].user_preference[images_pool]))[:10]])
            random_images = list(random.sample(set(images_pool).difference(set(positive_images)), 10))
            back_images = positive_images + random_images
            random.shuffle(back_images)
            self.user_dict[uid].test_images_list = back_images
            self.user_dict[uid].test_images_positive = positive_images
            self.user_dict[uid].test_images_random = random_images

            url_list = self.convert_to_url(category=self.user_dict[uid].category, id_list=back_images)

            return url_list
        except KeyboardInterrupt:
            # cleanup here, e.g. release locks
            pass

    def write_to_disk(self, uid, result):
        self.user_dict[uid].test_images_selection = result
        positive_samples_set = set(self.user_dict[uid].test_images_positive)
        positive_noway = 0

        for n_i in result["noway"]:
            if self.user_dict[uid].test_images_list[int(n_i[11:]) - 1] in positive_samples_set:
                positive_noway += 1
                
        print "PN: " + str(positive_noway) + " RN: " + str(len(result["noway"]) - positive_noway)

        with open(self.file_prefix + "u_" + uid + ".pickle", "w") as f_handle:
            pickle.dump(self.user_dict[uid], f_handle)
        del self.user_dict[uid]

    def convert_to_url(self, category, id_list):
        image_url_list = list()
        for id in id_list:
            image_url_list.append("http://cornell-nyc-sdl-yada-image.s3.amazonaws.com/" + self.Image_id_list[category][id] + ".jpg")
        return image_url_list

    def select_with_prob(self, prob_array):
        rand_num = random.random()
        cumulate = 0.0
        for i in range(len(prob_array)):
            cumulate += prob_array[i]
            if cumulate > rand_num:
                return i

class YummeUser():

    def __init__(self, Dist_matrix_size, Iteration, Category, Goals):
        self.max_iteration = Iteration
        self.category = Category # "normal" | "vegan" | "vegetarian" | "kosher" | "halal"
        self.goals = Goals # {"calories": "0" | "1" | "2", "fat": "0" | "1" | "2", "protein": "0" | "1" | "2"}

        self.user_preference = (1.0 / Dist_matrix_size) * np.ones(Dist_matrix_size)    # Normalize User Preference
        self.Dist_matrix_size = Dist_matrix_size
        self.delta = 0.2
        self.user_image_visited = list()
        self.user_image_propagated = list()
        self.last_image_list = list()

        ##### Testing MetaData #####
        self.test_images_list = list([])
        self.test_images_positive = list([])
        self.test_images_random = list([])
        self.test_images_selection = {"yummy":[], "noway":[]}
        ##### Testing MetaData #####

        ##### Debug Info #####
        self.debug = True
        self.preference_evolution = list([])
        self.preference_evolution.append(self.user_preference.tolist())
        self.added_vector = list([])
        ##### Debug Info #####

        self.user_iteration = 1

    def propagate(self, image_selected, Propagate_matrix):
        image_list_copy = list(self.last_image_list)
        update_array = np.zeros(len(self.user_preference))

        if len(self.last_image_list) == 10:
            positive_num = len(image_selected)
            negative_num = len(self.last_image_list) - positive_num

            if positive_num == 0:
                for image_id in image_list_copy:
                    update_array = update_array - Propagate_matrix[image_id].toarray()[0]
                    self.user_image_propagated += Propagate_matrix[image_id].nonzero()[1].tolist()
            elif negative_num == 0:
                for image_index in sorted(image_selected, reverse=True):
                    image_list_copy.pop(int(image_index))
                    update_array = update_array + Propagate_matrix[self.last_image_list[int(image_index)]].toarray()[0]
                    self.user_image_propagated += Propagate_matrix[self.last_image_list[int(image_index)]].nonzero()[1].tolist()
            else:
                for image_index in sorted(image_selected, reverse=True):
                    image_list_copy.pop(int(image_index))
                    update_array = update_array + negative_num * Propagate_matrix[self.last_image_list[int(image_index)]].toarray()[0]
                    self.user_image_propagated += Propagate_matrix[self.last_image_list[int(image_index)]].nonzero()[1].tolist()
                for image_id in image_list_copy:
                    update_array = update_array - positive_num * Propagate_matrix[image_id].toarray()[0]
                    self.user_image_propagated += Propagate_matrix[image_id].nonzero()[1].tolist()
                update_array = update_array / (positive_num * negative_num)

        else:
            for image_index in image_selected:
                image_list_copy.pop(int(image_index))
                update_array = update_array + Propagate_matrix[self.last_image_list[int(image_index)]].toarray()[0]
                self.user_image_propagated += Propagate_matrix[self.last_image_list[int(image_index)]].nonzero()[1].tolist()

            for image_id in image_list_copy:
                update_array = update_array - Propagate_matrix[image_id].toarray()[0]
                self.user_image_propagated += Propagate_matrix[image_id].nonzero()[1].tolist()

        self.user_preference = self.user_preference * np.exp(self.delta * update_array / (self.user_preference * self.Dist_matrix_size))
        self.user_preference = self.user_preference / np.sum(self.user_preference)

        if self.debug:
            self.preference_evolution.append(self.user_preference.tolist())
            self.added_vector.append(update_array.tolist())
            
class KPlusPlus():

    def __init__(self, Dist_matrix_size, N = 10):
        
        self.Dist_Pairwise = {}
        with open("plateclick_data/MainDishes_pairwise_dist.pickle", "r") as f_handle:
            self.Dist_Pairwise["normal"] = pickle.load(f_handle)
        with open("plateclick_data/vegan_pairwise_dist.pickle", "r") as f_handle:
            self.Dist_Pairwise["vegan"] = pickle.load(f_handle)
        with open("plateclick_data/vegetarian_pairwise_dist.pickle", "r") as f_handle:
            self.Dist_Pairwise["vegetarian"] = pickle.load(f_handle)
        with open("plateclick_data/kosher_pairwise_dist.pickle", "r") as f_handle:
            self.Dist_Pairwise["kosher"] = pickle.load(f_handle)
        with open("plateclick_data/halal_pairwise_dist.pickle", "r") as f_handle:
            self.Dist_Pairwise["halal"] = pickle.load(f_handle)
        
        self.Dist_matrix_size = Dist_matrix_size  # dict

        self.X = {}
        self.X["normal"] = range(self.Dist_matrix_size["normal"])
        self.X["vegetarian"] = range(self.Dist_matrix_size["vegetarian"])
        self.X["vegan"] = range(self.Dist_matrix_size["vegan"])
        self.X["kosher"] = range(self.Dist_matrix_size["kosher"])
        self.X["halal"] = range(self.Dist_matrix_size["halal"])
        self.N = N

    def init_cluster(self, category):
        cluster_list = [int(random.choice(self.X[category]))]
        while len(cluster_list) < self.N:
            min_Dist = np.array([float(min(self.get_distance(category=category, index_i=c, index_j=x) \
                        for c in cluster_list)) for x in self.X[category]])
            probs = min_Dist / min_Dist.sum()
            cumprobs = probs.cumsum()
            r = random.random()
            cluster_list.append(int(np.where(cumprobs >= r)[0][0]))

        return cluster_list

    def get_distance(self, category, index_i, index_j):
        if index_i > index_j:
            temp = index_i
            index_i = index_j
            index_j = temp
        elif index_i == index_j:
            return 0
        
        ind = (2 * self.Dist_matrix_size[category] - 1 - index_i) * index_i / 2 + (index_j - index_i - 1)
        return self.Dist_Pairwise[category][ind]
