import datetime
import time
import random
import uuid
import os
import requests
import pandas as pd
from flickrapi import FlickrAPI
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


class FlickrExtractor:
    def extract(self, queries=[], path_training="train", path_testing="test", path_validation="valid", num_training=300, num_testing=50, num_validation=50, height=None, width=None, path_urls_training="training_urls", path_urls_testing="testing_urls", path_urls_validation="validation_urls", create_source_file=False, api_key="", secret="", starting_line=True, sub_dir=False, sub_dir_name=None):
        print("Flickr Extractor started...\n")
        print("Pictures to extract: ", str(num_training*len(queries) + num_testing*len(queries) + num_validation*len(queries)))

        # Sollen alle Bilder in einem Unterordner gespeichert werden, dann wird dieser erstellt.
        if sub_dir == True:
            try:
                os.mkdir(sub_dir_name)
            except:
                pass

        # Die Bilder werden entweder in einem Trainings-, Test- und Validationsdatensatz gespeichert. Diese drei Ordner müssen zunächst erstellt werden
        try:
            os.mkdir(path_training)
            os.mkdir(path_testing)
            os.mkdir(path_validation)
        except:
            pass

        # Die Quellen der Bilder können optional (create_source_file == True) in einer .csv-Datei gespeichert werden.
        # Dadurch können wir später zurückverfolgen, unter welcher URL das Bild zu finden war auf Flickr.
        if create_source_file == True:
            training_source_file = open(path_urls_training + ".csv", 'a')
            testing_source_file = open(path_urls_testing + ".csv", 'a')
            validation_source_file = open(path_urls_validation + ".csv", 'a')

            # Sollen .csv-Dateien mit Bildquellen gespeichert werden, dann kann auch ein Header hinzugefügt werden.
            # Ist das Attribut starting_line == True, dann wird ein Header hinzugefügt.
            # Das Attribut wurde implementiert, da man so einfacher die Daten zu zwei verschiedenen Zeitpunkten herunterladen kann.
            # Angenommen ich lade an einem Tag die Bilder zu den ersten 100 Vögeln herunter, dann muss nur dann ein Header hinzugefügt werden zu den .csv-Dateien
            # und nicht erneut, wenn die Bilder der übrigen Vogelarten heruntergeladen werden müssen.
            if starting_line == True:
                training_source_file.write("id,label,url,path\n")
                testing_source_file.write("id,label,url,path\n")
                validation_source_file.write("id,label,url,path\n")
                training_source_file.close()
                testing_source_file.close()
                validation_source_file.close()
        
        # Für jede Vogelart (query) werden nun Bilder heruntergeladen.
        for progress, query in enumerate(queries):
            # Da das Herunterladen lange dauern kann, kann es von Interesse sein, den Progress anzeigen zu lassen.
            start = time.time()
            
            # Anzahl an Bildern, die insgesamt pro Art herunter geladen werden müssen.
            MAX_COUNT = num_training + num_testing + num_validation

            # Nun sollen die URLs von bis zu MAX_COUNT Bildern gefetcht werden. Dazu dient die Funktion get_urls.
            urls = self.get_urls(query, MAX_COUNT, api_key, secret)

            # Da die ersten paar Ergebnisse auf Flickr möglicherweise populärer sind, als die letzten, die gefetcht werden, mischen wir nun die Liste mit den URLs. 
            random.shuffle(urls)

            # Konnten nicht so viele Bilder gefunden werden, wie erwünscht, dann wird dennoch darauf geachtet, dass das
            # Verhältniss zwischen den drei Datensätzen (train/test/validation) ungefähr proportional ist, zur erwünschten Anzahl.
            if len(urls) < MAX_COUNT:
                urls_training = urls[:round((num_training/MAX_COUNT)*len(urls))]
                urls_testing = urls[round((num_training/MAX_COUNT)*len(urls)): round(((num_training+num_testing)/MAX_COUNT)*len(urls))]
                urls_validation = urls[round(((num_training+num_testing)/MAX_COUNT)*len(urls)):]
            else:
                # Anderenfalls kann der Train/Test/Validation-Split wie spezifiziert durchgeführt werden.
                urls_training = urls[:num_training]
                urls_testing = urls[num_training: num_training + num_testing]
                urls_validation = urls[num_training + num_testing: num_training + num_testing + num_validation]

            # Die Bilder werden anschließend in Unterordnern gespeichert. Der Ordnername entspricht dem Label bzw. dem wissenschaftlichen Namen der Vogelart.
            os.mkdir(path_training+"/"+query)
            os.mkdir(path_testing+"/"+query)
            os.mkdir(path_validation+"/"+query)

            # Speichern wir nun die Bilder der Trainingsmenge.
            for idx, url in enumerate(urls_training):
                # Wie auch bei den anderen drei Ordnern (Test/Validation) bekommt jedes Bild als Dateinamen eine individuelle ID, 
                # sodass keine Überscheidungen bzw. Dopplungen vokommen können. Prinzipiell ist es möglich, dass auf Flickr zwei Bilder
                # den selben Dateinamen besitzen. Daher dieser Schritt.
                file_name = str(uuid.uuid4())
                try:
                    # download_image speichert das Bild, welches unter der url zu finden ist als .jpg. 
                    self.download_image(url, path_training+"/"+query+"/"+file_name, height, width)
                except:
                    pass
                
                # Soll eine Datei mit Quellen erstellt werden, dann speichern wir die URL des heruntergeladenen Bildes in der entsprechenden .csv-Datei.
                if create_source_file == True:
                    self.write_image_source_to_url(file_name, url, query, path_training+"/"+query+"/"+file_name, path_urls_training)

            for idx, url in enumerate(urls_testing):
                file_name = str(uuid.uuid4())
                try:
                    self.download_image(url, path_testing+"/"+query+"/"+file_name, height, width)
                except:
                    pass
                if create_source_file == True:
                    self.write_image_source_to_url(file_name, url, query, path_testing+"/"+query+"/"+file_name, path_urls_testing)

            for idx, url in enumerate(urls_validation):
                file_name = str(uuid.uuid4())
                try:
                    self.download_image(url, path_validation+"/"+query+"/"+file_name, height, width)
                except:
                    pass
                if create_source_file == True:
                    self.write_image_source_to_url(file_name, url, query, path_validation+"/"+query+"/"+file_name, path_urls_validation)

            # Wurden alle Bilder gespeichert, dann kann angegeben werden, wie Lange der Download aller Bilder einer Vogelart gedauert hat.
            end = time.time()
            print("Progress ", str('{:.1%}'.format(round((progress + 1) / len(queries), 3))), ": ", query, len(urls_training), len(urls_testing), len(urls_validation), " - this took:", str(round(end - start, 1)), "seconds")

    def write_image_source_to_url(self, id, original_url, query, path, path_source_file):
        writer = open(path_source_file + ".csv", 'a')
        line = id+","+query+","+original_url+","+path+"\n"
        writer.write(line)

    def get_urls(self, query, MAX_COUNT, api_key, secret):
        count = 0
        urls = []
        # Die Suche nach der Art 'Alle alle' sorgt nicht dafür, dass Vogelbilder von dieser Art zurückgegeben werden.
        # Die query wird daher in diesem Fall noch erweitert.
        if query == "Alle alle":
            # Neben Alle alle wird auch der gewöhnliche Name 'Little auk' hinzugefügt
            query = "Alle alle Little auk"
        flickr = FlickrAPI(api_key, secret)
        # Da die Anzahl an maximalen Fetches pro Suche nur 500 beträgt (per_page Argument) (siehe hier: https://www.flickr.com/services/api/flickr.photos.search.html)
        # werden immer mehrere Suchen durchgeführt, indem Bilder zu vielen verschiedenen Jahreszeiten betrachtet werden.
        # Es werden also einfach also zunächst alle Bilder zwischen 2018 und heute (datetime.datetime(now.year, now.month, now.day), 2015 und 2018 und schließlich vor 2015 gesammelt.
        now = datetime.datetime.now()
        time_intervalls = [datetime.datetime(2015,1,1), datetime.datetime(2018,1,1), datetime.datetime(now.year, now.month, now.day)]
        it = 0
        while count < MAX_COUNT and it < len(time_intervalls):
            if it == len(time_intervalls) - 1:
                photos = flickr.walk(text=query, per_page=500,sort='relevance', extras = "url_o", max_upload_date=time_intervalls[len(time_intervalls)-1-it])
            else:
                photos = flickr.walk(text=query, per_page=500,sort='relevance', extras = "url_o", max_upload_date=time_intervalls[len(time_intervalls)-1-it], min_upload_date=time_intervalls[len(time_intervalls)-2-it])
            # Es ist möglich, dass in einem Intervall keine Fotos auf Flickr vorhanden sind. Um dies zu verhindern, wird ein try / except block verwendet.
            try:
                k = 0
                for photo in photos:
                    if count < MAX_COUNT:
                        try:
                            url = photo.get('url_o')
                            if url != None and url.endswith(".jpg"):
                                count = count+1
                                urls.append(url)
                        except:
                            pass
                    else:
                        break
                    k += 1
            except:
                pass
            it += 1
        return urls

    def download_image(self, url, path, height, width):
        # Wird eine height / width übergeben, dann wird die Größe des Bildes angepasst.
        if height != None or width != None:
            img = Image.open(requests.get(url, stream=True).raw)
            img = img.resize((width, height), Image.ANTIALIAS)
        else:
            img = Image.open(requests.get(url, stream=True).raw)
        img.save(path+".jpg")