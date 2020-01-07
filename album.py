import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()

class Error(Exception):
	pass
class AlbumAlredyExists(Error):
	pass

class Album(Base):
	"""
	Описывает структуру таблицы album для хранения записей музыкальной
	библиотеки
	"""

	__tablename__ = "album"

	id = sa.Column(sa.INTEGER, primary_key=True)
	year = sa.Column(sa.INTEGER)
	artist = sa.Column(sa.TEXT)
	genre = sa.Column(sa.TEXT)
	album = sa.Column(sa.TEXT)


def connect_db():
	engine = sa.create_engine(DB_PATH)
	Base.metadata.create_all(engine)
	session = sessionmaker(engine)
	return session()

def save_album (year, artist, genre, album):
	assert isinstance(year, int), "Неверный ввод года"
	assert isinstance(artist, str), "Неверный ввод музыканта"
	assert isinstance(genre, str), "Неверный ввод жанра"
	assert isinstance(album, str), "Неверный ввод альбома"

	session = connect_db()
	save = session.query(Album).filter(Album.artist == artist, Album.album == album).first()
	if save is not None:
		raise AlbumAlredyExists("Такой альбом уже существует и имеет номер №{}".format(save.id))

	album = Album(
		year=year,
		artist=artist,
		genre=genre,
		album=album,
	)
	session.add(album)
	session.commit()
	return album

def find(artist):
	"""
	Находит все альбомы в базе данных по заданному артисту
	"""
	session = connect_db()
	albums = session.query(Album).filter(Album.artist == artist).all()
	return albums