import os
import sys
import pickle
import time

from bs4 import BeautifulSoup
from urllib import request
import json
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import requests
import re
import PIL.Image
import pandas as pd
import numpy

import plotly.graph_objs as go
import colorsys
import math
from sklearn.cluster import KMeans

def save_soup(url, filename):
	with request.urlopen(url) as response:
		html = response.read()
		soup = BeautifulSoup(html, 'html.parser')
		if filename is not None:
			with open(filename, 'w') as wf:
				wf.write(str(soup.prettify().encode('utf-8')))
	return soup

def Dom_colour(image, palette_size=5):
	img = image.copy()
	img.thumbnail((50, 50))

	pixels = list(img.getdata())
	df = pd.DataFrame(pixels, columns=["R", "G", "B"])
	km = KMeans(n_clusters=3)
	km.fit(df[["R", "G", "B"]])
	df['cluster'] = km.labels_
	df_count = df.copy()
	df_count = df_count.groupby('cluster').count()
	max_cluster = df_count["R"].idxmax()
	dominant_colours = [int(x) for x in km.cluster_centers_[max_cluster]]
	return dominant_colours

def checkfordig(film_title):
	if "-" in film_title:
		check = film_title.rsplit('-', 1)[1]
		if film_title.rsplit('-', 1)[1].isdigit():
			string = film_title.rsplit('-', 1)[0]
		else:
			string = film_title
	else:
		string= film_title
	return string

def sort(List, N_clusters=10):
	df = pd.DataFrame(List, columns =["Title", "link_img", "LetterboxdURI", "R", "G", "B", "H", "V", "S"])
	km = KMeans(n_clusters=N_clusters)
	km.fit(df[["R", "G", "B"]])
	df['cluster'] = km.labels_
	cluster_numpy = km.cluster_centers_
	cluster = [x.tolist() for x in cluster_numpy]
	for i in range(0, len(cluster)):
		cluster[i].append(i)
		cluster[i]= [int(x) for x in cluster[i]]
		cluster[i].extend(colorsys.rgb_to_hsv(cluster[i][0], cluster[i][1], cluster[i][2]))

	df_cluster = pd.DataFrame(cluster, columns=["R", "G", "B", "cluster", "H", "S", "V"])
	df_cluster.sort_values(by=["V", "S", "H"], inplace=True, ascending=True)
	df["cluster_sorted"] = True
	for i in range(0, N_clusters):
		cluster_number = int(df_cluster.iloc[i]["cluster"])
		df["cluster_sorted"][df["cluster"]==cluster_number] = i

	df.sort_values(by=["cluster_sorted", "S", "V", "H"], inplace=True, ascending=False)
	del df['cluster_sorted']
	List_out = df.values.tolist()

	return List_out

class user:
	def __init__(self, name):
		self.name = name
		self.file_data = "{}\\Data_colour_{}.lb".format(PATH, name)
		try:
			self.load()
			self.get_films(All=False, image_set=True)

		except:
			self.films = []
			self.get_films(All=True, image_set=True)
			self.save()

	def save(self):
		with open(self.file_data, 'wb') as file:
			pickle.dump(self.__dict__, file) 

	def load(self):
		self.__dict__ = pickle.load(open(self.file_data, "rb"))

	def add_film(self, film):
		self.films.append(film)

	def create_list(self, Sorted=False):
		df = pd.DataFrame(self.films, columns =["Title", "link_img", "LetterboxdURI", "R", "G", "B", "H", "V", "S", "cluster"])
		df[["LetterboxdURI"]].to_csv('{}/{}.csv'.format(PATH, username), index=False)

	def create_image(self):
		pixels = 5
		img = PIL.Image.new('RGB', (len(self.films)*pixels, 100))
		img1 = ImageDraw.Draw(img, 'RGB')
		for x in range(0, len(self.films)):
			img1.rectangle([x*pixels, 0, (x+pixels)*pixels,600], fill =(self.films[x][3], self.films[x][4], self.films[x][5]))

		img.save("{}/{}.png".format(PATH, username))

	def create_plot(self, Mode="lines+markers"):
		df = pd.DataFrame(self.films, columns =["Title", "link_img", "LetterboxdURI", "R", "G", "B", "H", "V", "S", "cluster"])

		trace = go.Scatter3d(x=df.R, y=df.G, z=df.B, mode=Mode,
							marker=dict(color=['rgb({},{},{})'.format(r,g,b) for r,g,b in zip(df.R.values, df.G.values, df.B.values)]),
							text = ["Title: {}".format(x) for x in df["Title"] ])
		data = [trace]

		layout = go.Layout(title ="RGB Graph", margin=dict(l=0,
									   r=0,
									   b=0,
									   t=0),
		scene = dict(
                    xaxis_title='Red',
                    yaxis_title='Green',
                    zaxis_title='Blue'))

		fig = go.Figure(data=data, layout=layout)
		fig.show()

	def get_image_link(self, link):
		soup1 = save_soup(link,'{}1_META.html'.format(PATH))
		script_json = soup1.find_all("script")[14].string
		json_data = script_json[script_json.find("*/")+2 : script_json.find("/*", 2)]
		y = json.loads(json_data)
		print(y["image"])
		return y["image"]

	def get_image(self, All=False):
		print("Getting images: {}".format(All))
		for x in range(0, len(self.films)):
			print("Image: {}/{}".format(x, len(self.films)))
			if (len(self.films[x])==3) or (All==True):
				del self.films[x][3:]
				im = Image.open(requests.get(self.films[x][1], stream=True).raw)
				colour = Dom_colour(im)
				self.films[x].extend(colour)
				self.films[x].extend(colorsys.rgb_to_hsv(colour[0], colour[1], colour[2]))
				self.save()
		self.films =  sort(self.films)

	def get_films(self, All=False, image_set=False):
		print(All)
		if (All == True):
			print("All films")
			self.films = []
			self.save()
			self.load()

		if ("_" in self.name):
			link_download = "https://letterboxd.com/{}/page/{}/"
			username= "{}/list/{}".format(self.name.split("_")[0], self.name.split("_")[1])
		else:
			link_download = 'http://letterboxd.com/{}/films/by/date/page/{}/'
			username= self.name
		
		page = 1
		site = link_download.format(username, page)
		print(site)
		soup = save_soup(site,'{}_META.html'.format(PATH))
		try: 
			last_page = int(soup.find_all(class_='paginate-page')[-1].text)
		except:
			last_page = 1

		for page in range(1, last_page+1):
			print("Page Number: {}/{}".format(page, last_page))
			site = link_download.format(username, page)
			soup = save_soup(site,'{}_META.html'.format(PATH))

			movie_li = [lm for lm in soup.find_all(
					'li', class_='poster-container')]

			for i in range(0, int(len(movie_li))):

				film_temp = []

				# Retrieve title
				film_title = movie_li[i].div['data-target-link'].split('/')[2]
				Check = any(film_title in film_check for film_check in self.films)
				if ((Check == False)):
					if (image_set == True):
						film_id = movie_li[i].div['data-film-id'].split('/')[0]
						
						film_title_temp = movie_li[i].img["alt"]
						
						Replace= [["!", ""],[" ", "-"], [",", "-"], ["'", "-"], ["&", ""],["(", "-"],[")", "-"], [".", ""], [":", ""], ["ü", "u"],["ä", "a"],["ö", "o"],["ï", "i"],["ë", "e"], ["--", "-"], ["--", "-"]]
						
						for x in range(0, len(Replace)):
							film_title_temp = film_title_temp.replace(Replace[x][0], Replace[x][1])
						film_title_link = film_title_temp.lower()
						
						string = ""
						for number in film_id:
							string += "/{}".format(number)
						
						link = "https://a.ltrbxd.com/resized/film-poster{}/{}-{}-0-70-0-105-crop.jpg".format(string, film_id, film_title_link)
						try:
							im = Image.open(requests.get(link, stream=True).raw)
							film_link = link
						
						except:
							film_link = self.get_image_link('http://letterboxd.com{}'.format(movie_li[i].div['data-target-link']))

					film_temp.append(film_title)
					film_temp.append(film_link)
					film_temp.append('http://letterboxd.com{}'.format(movie_li[i].div['data-target-link']))

					print("Film done: {}".format(film_temp[0]))
					print(film_temp)

					self.add_film(film_temp)
					self.save()

if __name__ == "__main__":
	if (sys.argv[1] == "-h"):
		print("Check out the Github page: {}".format("https://github.com/coencoensmeets/Letterboxd-sorter"))
		exit()

	if (os.path.isdir(sys.argv[1]) == True):
		print("Using {} for exporting of files".format(sys.argv[1]))
		PATH = str(sys.argv[1])

	elif (sys.argv[1]== "-here"):
		PATH = str(os.getcwd())
		print("Using current directory for export of files: {}".format(directory))


	else:
		PATH = str(os.getcwd())
		print("Could not recognise directory. Using current directory for export of files: {}".format(directory))

	username = str(sys.argv[2])
	if ("/" in username):
		username = "{}_{}".format(username.split("/")[3], username.split("/")[5])
	print(username)

	User = user(username)
	User.get_image(All=False)

	if (len(sys.argv)==3):
		Options = "-L"
	else:
		Options = sys.argv[3]

	if ("L" in Options):
		User.create_list()
		print("List created")

	if ("I" in Options):
		User.create_image()
		print("Image created")

	if ("Pm" in Options):
		User.create_plot(Mode="markers")
		print("plot created without lines")

	if ("Pl" in Options):
		User.create_plot()
		print("plot created with lines")