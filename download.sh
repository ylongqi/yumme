#!/bin/bash

mkdir -p flask_api/plateclick_data;
mkdir -p user/

wget --no-check-certificate https://s3.amazonaws.com/cornell-tech-sdl-yumme/vegan_prop.pickle -O flask_api/plateclick_data/vegan_prop.pickle
wget --no-check-certificate https://s3.amazonaws.com/cornell-tech-sdl-yumme/vegetarian_prop.pickle -O flask_api/plateclick_data/vegetarian_prop.pickle
wget --no-check-certificate https://s3.amazonaws.com/cornell-tech-sdl-yumme/MainDishes_prop.pickle -O flask_api/plateclick_data/MainDishes_prop.pickle
wget --no-check-certificate https://s3.amazonaws.com/cornell-tech-sdl-yumme/halal_prop.pickle -O flask_api/plateclick_data/halal_prop.pickle
wget --no-check-certificate https://s3.amazonaws.com/cornell-tech-sdl-yumme/kosher_prop.pickle -O flask_api/plateclick_data/kosher_prop.pickle

wget --no-check-certificate https://s3.amazonaws.com/cornell-tech-sdl-yumme/vegan_items.pickle -O flask_api/plateclick_data/vegan_items.pickle
wget --no-check-certificate https://s3.amazonaws.com/cornell-tech-sdl-yumme/vegetarian_items.pickle -O flask_api/plateclick_data/vegetarian_items.pickle
wget --no-check-certificate https://s3.amazonaws.com/cornell-tech-sdl-yumme/MainDishes_items.pickle -O flask_api/plateclick_data/MainDishes_items.pickle
wget --no-check-certificate https://s3.amazonaws.com/cornell-tech-sdl-yumme/halal_items.pickle -O flask_api/plateclick_data/halal_items.pickle
wget --no-check-certificate https://s3.amazonaws.com/cornell-tech-sdl-yumme/kosher_items.pickle -O flask_api/plateclick_data/kosher_items.pickle

wget --no-check-certificate https://s3.amazonaws.com/cornell-tech-sdl-yumme/vegan_ranks.pickle -O flask_api/plateclick_data/vegan_ranks.pickle
wget --no-check-certificate https://s3.amazonaws.com/cornell-tech-sdl-yumme/vegetarian_ranks.pickle -O flask_api/plateclick_data/vegetarian_ranks.pickle
wget --no-check-certificate https://s3.amazonaws.com/cornell-tech-sdl-yumme/MainDishes_ranks.pickle -O flask_api/plateclick_data/MainDishes_ranks.pickle
wget --no-check-certificate https://s3.amazonaws.com/cornell-tech-sdl-yumme/halal_ranks.pickle -O flask_api/plateclick_data/halal_ranks.pickle
wget --no-check-certificate https://s3.amazonaws.com/cornell-tech-sdl-yumme/kosher_ranks.pickle -O flask_api/plateclick_data/kosher_ranks.pickle

wget --no-check-certificate https://s3.amazonaws.com/cornell-tech-sdl-yumme/vegan_pairwise_dist.pickle -O flask_api/plateclick_data/vegan_pairwise_dist.pickle
wget --no-check-certificate https://s3.amazonaws.com/cornell-tech-sdl-yumme/vegetarian_pairwise_dist.pickle -O flask_api/plateclick_data/vegetarian_pairwise_dist.pickle
wget --no-check-certificate https://s3.amazonaws.com/cornell-tech-sdl-yumme/MainDishes_pairwise_dist.pickle -O flask_api/plateclick_data/MainDishes_pairwise_dist.pickle
wget --no-check-certificate https://s3.amazonaws.com/cornell-tech-sdl-yumme/halal_pairwise_dist.pickle -O flask_api/plateclick_data/halal_pairwise_dist.pickle
wget --no-check-certificate https://s3.amazonaws.com/cornell-tech-sdl-yumme/kosher_pairwise_dist.pickle -O flask_api/plateclick_data/kosher_pairwise_dist.pickle

# Nutritional information
wget --no-check-certificate https://s3.amazonaws.com/cornell-tech-sdl-yumme/vegan_nutrition.npy -O flask_api/plateclick_data/vegan_nutrition.npy
wget --no-check-certificate https://s3.amazonaws.com/cornell-tech-sdl-yumme/vegetarian_nutrition.npy -O flask_api/plateclick_data/vegetarian_nutrition.npy
wget --no-check-certificate https://s3.amazonaws.com/cornell-tech-sdl-yumme/MainDishes_nutrition.npy -O flask_api/plateclick_data/MainDishes_nutrition.npy
wget --no-check-certificate https://s3.amazonaws.com/cornell-tech-sdl-yumme/halal_nutrition.npy -O flask_api/plateclick_data/halal_nutrition.npy
wget --no-check-certificate https://s3.amazonaws.com/cornell-tech-sdl-yumme/kosher_nutrition.npy -O flask_api/plateclick_data/kosher_nutrition.npy
