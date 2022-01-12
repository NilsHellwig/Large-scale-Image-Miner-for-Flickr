import os
from dotenv import load_dotenv
import shutil
shutil.rmtree("dataset")
load_dotenv()

# Here is an example to show how this class works

# 1: Load the FlickrExtractor-Class
from flickr_extractor import FlickrExtractor
flickrExtractor = FlickrExtractor()

# 2: Init your Flickr-API Keys
key = os.getenv('KEY')
secret = os.getenv('SECRET')

# 3: Specify for which search term(s) you want to download images
labels = ["cats","dogs"]

# 4. Since the Extractor was created specifically to download image datasets for Machien Learning tasks,
# a training dataset, test dataset and validation dataset are always created. If you want all images for a search term in one folder and not spread over three folders,
# then you specify 0 images for Test and Validation.


flickrExtractor.extract(queries = labels, 
                        api_key = key, 
                        secret = secret, 
                        num_training = 70, 
                        num_testing = 20, 
                        num_validation = 20, 
                        height = 500, 
                        width = 500, 
                        create_source_file = True, 
                        starting_line = True,
                        sub_dir = True,
                        sub_dir_name = "dataset",
                        path_training = "dataset/train", 
                        path_testing = "dataset/test", 
                        path_validation = "dataset/validation", 
                        path_urls_training = "dataset/urls_training", 
                        path_urls_testing = "dataset/urls_test", 
                        path_urls_validation = "dataset/urls_validation")
