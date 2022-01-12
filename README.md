# TheFlickrFetcher
TheFlickrFetcher is a tool that allows you to download large amounts of image data from Flickr. Up to 1500 images can be downloaded for one search term. The tool is primarily aimed at machine learning experts to systematically collect image data in a folder structure. A folder can be downloaded for training, testing and validation. The folder structure is then also compatible with generators from Tensorflow / Keras. Additionally, it is possible to save the URLs of the images to be downloaded in a .CSV-File. The only requirement is Python 3 (+ packages from requirements.txt) and a free API key from Flickr.

## Installation
* Python 3
* Install all required packages (requirements.txt: `pip install -r requirements.txt`)
* The use of flickr_extractor.py is demonstrated in script.py (`python script.js`).

```python
import os
from dotenv import load_dotenv
load_dotenv()

# 1: Load the FlickrExtractor-Class
from flickr_extractor import FlickrExtractor
flickrExtractor = FlickrExtractor()

# 2: Init your Flickr-API Keys
key = os.getenv('KEY')
secret = os.getenv('SECRET')

# 3: Specify for which search term(s) you want to download images
labels = ["cats","dogs"]

flickrExtractor.extract(queries = labels, 
                        api_key = key, 
                        secret = secret, 
                        num_training = 70, 
                        num_testing = 20, 
                        num_validation = 10, 
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
```
## (Advanced) Parameters of extract()

default parameters:

```queries=[], path_training="train", path_testing="test", path_validation="valid", num_training=300, num_testing=50, num_validation=50, height=None, width=None, path_urls_training="training_urls", path_urls_testing="testing_urls", path_urls_validation="validation_urls", create_source_file=False, api_key="", secret="", starting_line=True, sub_dir=False, sub_dir_name=None```

- `queries`: the querys for which you want to extract the images
- `path_training`: the path of the folder with images for training
- `path_testing`: the path of the folder with images for testing
- `path_validation`: the path of the folder with images for validation
- `num_training`: number of images for training
- `num_testing`: number of images for testing
- `num_validation`: number of images for validation
- `height`: individual height for all images to be downloaded (if not specified, all images have the original original size)
- `width`: individual width for all images to be downloaded (if not specified, all images have the original original size)
- `path_urls_training`: path of .CSV-File to save paths of downloaded training-images
- `path_urls_testing`: path of .CSV-File to save paths of downloaded testing-images
- `path_urls_validation`: path of .CSV-File to save paths of downloaded validation-images
- `create_source_file`: specify whether the urls should be saved at all
- `api_key`: Flickr API key
- `secret`: Flickr secret key
- `starting_line`: specify if a header should be added to the .CSV-File
- `sub_dir`: `True` if all images are to be stored in a subderectory. The name must still be added to the pathname of each folder specification.
- `sub_dir_name`: Name of the sub directory