from bottle import route
from bottle import run 
from bottle import HTTPError
from bottle import request

import album

@route("/albums/<artist>")
def albums(artist):
	albums_list = album.find(artist)
	if not albums_list:
		message = "Альбомов {} не найдено".format(artist)
		result = HTTPError(404, message)
	else:
		album_names = [album.album for album in albums_list]
		result = "<h1>Список альбомов {}:</h1> <br>".format(artist)
		result += "<br>".join(album_names)
	return result

@route("/albums", method= "POST")
def add_album():
	year = request.forms.get("year")
	artist = request.forms.get("artist")
	genre = request.forms.get("genre")
	album_name = request.forms.get("album")

	try:
		year = int(year)
	except ValueError:
		return HTTPError(400, "Некорректный год альбома :(")

	try:
		new_album= album.save_album(year,artist,genre,album_name)
	except AssertionError as err:
		result = HTTPError(400, str(err))
	except album.AlbumAlredyExists as err:
		result = HTTPError(409, str(err))
	else:
		print("Новый альбом с номером №{} <b>успешно<b> сохранён".format(new_album.id))
		result = "Новый альбом с номером №{} <b>успешно<b> сохранён".format(new_album.id)
	return result


if __name__ == "__main__":
	run(host="localhost", port=8080, debug=True)