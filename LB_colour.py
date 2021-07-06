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
import json
import PIL.Image
import pandas as pd

import plotly.graph_objs as go
import colorsys
import math
from sklearn.cluster import KMeans

PATH = "D:\\Python3.6\\Data"
username = "coencoensmeets"

def save_soup(url, filename):
	with request.urlopen(url) as response:
		html = response.read()
		soup = BeautifulSoup(html, 'html.parser')
		if filename is not None:
			with open(filename, 'w') as wf:
				wf.write(str(soup.prettify().encode('utf-8')))
	return soup

def step (r,g,b, repetitions=1):
	lum = math.sqrt( .241 * r + .691 * g + .068 * b )
	h, s, v = colorsys.rgb_to_hsv(r,g,b)
	h2 = int(h * repetitions)
	lum2 = int(lum * repetitions)
	v2 = int(v * repetitions)
	if h2 % 2 == 1:
		v2 = repetitions - v2
		lum = repetitions - lum
	return (h2, lum, v2)

def Dom_colour(image, palette_size=2):
	img = image.copy()
	img.thumbnail((50, 50))

	paletted = img.convert('P', palette=PIL.Image.ADAPTIVE, colors=palette_size)

	palette = paletted.getpalette()
	colour_counts = sorted(paletted.getcolors(), reverse=True)
	dominant_colours = []
	for x in range(0, len(colour_counts)):
		palette_index = colour_counts[x][1]
		dominant_colours.append(palette[palette_index*3:palette_index*3+3])

	Dif_colour = 0
	for i in range(0, 2):
		Dif_colour += abs(dominant_colours[0][i] - dominant_colours[1][i])

	score = Dif_colour
	dominant_colours[0].append(score)
	dominant_colour = dominant_colours[0]
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

	def get_image_link(self, link):
		soup1 = save_soup(link,'{}1_META.html'.format(PATH))
		script_json = soup1.find_all("script")[14].string
		json_data = script_json[script_json.find("*/")+2 : script_json.find("/*", 2)]
		y = json.loads(json_data)
		print(y["image"])
		return y["image"]

	def get_image(self, All=False):
		print("Getting images")
		for x in range(0, len(self.films)):
			print("Image: {}".format(x))
			if (len(self.films[x])==3) or (All==True):
				del self.films[x][3:]
				im = Image.open(requests.get(self.films[x][1], stream=True).raw)
				colour = Dom_colour(im)
				self.films[x].append(colour[0])
				self.films[x].append(colour[1])
				self.save()

	def create_list(self):
		Sorted = self.films
		for x in range(0, len(Sorted)):
			if (Sorted[x][3][3]):
				Sorted[x].append(list(step(Sorted[x][3][0], Sorted[x][3][1], Sorted[x][3][2], 6)))

		print(len(Sorted))

		Sorted.sort(key=lambda x: x[-1])
		df = pd.DataFrame(Sorted, columns =['Title', "link_img", "LetterboxdURI", "rgb", "rgb", "hls"])
		# print(df[["LetterboxdURI"]])
		df[["LetterboxdURI"]].to_csv('{}/{}.csv'.format(PATH, username), index=False)

	def create_image(self):
		Sorted = self.films
		for x in range(0, len(Sorted)):
			if (Sorted[x][3][3]):
				Sorted[x].append(list(step(Sorted[x][3][0], Sorted[x][3][1], Sorted[x][3][2], 6)))


		pixels = 5
		img = PIL.Image.new('RGB', (len(Sorted)*pixels, 100))
		img1 = ImageDraw.Draw(img, 'RGB')
		for x in range(0, len(Sorted)):
			img1.rectangle([x*pixels, 0, (x+pixels)*pixels,100], fill =(Sorted[x][3][0],Sorted[x][3][1],Sorted[x][3][2]))

		img.save("{}/{}.png".format(PATH, username))

	def create_plot(self, Mode="lines+markers"):
		Plot = []
		for i in range(0, len(self.films)):
			Plot.append(self.films[i][3])

		df = pd.DataFrame(Plot, columns =["R", "G", "B", "score"])

		trace = go.Scatter3d(x=df.R, y=df.G, z=df.B, mode=Mode,
							marker=dict(color=['rgb({},{},{})'.format(r,g,b) for r,g,b in zip(df.R.values, df.G.values, df.B.values)]))
		data = [trace]

		layout = go.Layout(margin=dict(l=0,
									   r=0,
									   b=0,
									   t=0))

		fig = go.Figure(data=data, layout=layout)
		fig.show()

	def get_films(self, All=False, image_set=False):
		print(All)
		if (All == True):
			print("All films")
			self.films = []
			self.save()
			self.load()

		#Get Data
		page = 1
		
		site = 'http://letterboxd.com/{}/films/by/date/page/{}/'.format(self.name, page)
		soup = save_soup(site,'{}_META.html'.format(PATH))
		try: 
			last_page = int(soup.find_all(class_='paginate-page')[-1].text)
		except:
			last_page = 1

		# last_page = 1 #

		for page in range(1, last_page+1):
			print("Page Number: {}/{}".format(page, last_page))
			site = 'http://letterboxd.com/{}/films/by/date/page/{}/'.format(self.name, page)
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

					self.add_film(film_temp)
					self.save()

User = user(username)
User.get_image(All=True)

User.create_image()
# User.create_list()
User.create_plot(Mode="markers")

#----Test with clustering-------------
# Test = User.films
# Plot = []
# for i in range(0, len(Test)):
# 	Plot.append(Test[i][3])

# df = pd.DataFrame(Plot, columns =["R", "G", "B", "score"])
# df= df[["R", "G", "B"]]
# km = KMeans(n_clusters=10)
# km.fit(df)
# df['cluster'] = km.labels_
# trace = go.Scatter3d(x=df.R, y=df.G, z=df.B, mode="markers",
# 							marker=dict(color=df.cluster))
# data = [trace]

# layout = go.Layout(margin=dict(l=0,
# 									   r=0,
# 									   b=0,
# 									   t=0))

# fig = go.Figure(data=data, layout=layout)
# fig.show()