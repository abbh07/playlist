from pymodm import MongoModel, fields

from . import app


class DataValidationError(Exception):
    """Used for a data validation error when deserializing"""

class DatabaseConnectionError(Exception):
    """Custom Exception when database connection fails"""

class Playlist(MongoModel):
    index = fields.CharField(mongo_name='index')
    id = fields.CharField(mongo_name='_id', primary_key=True)
    title = fields.CharField(mongo_name='title')
    danceability = fields.FloatField(mongo_name='danceability')
    energy = fields.FloatField(mongo_name='energy')
    mode = fields.IntegerField(mongo_name='mode')
    acousticness = fields.FloatField(mongo_name='acousticness')
    tempo = fields.FloatField(mongo_name='tempo')
    duration_ms = fields.IntegerField(mongo_name='duration_ms')
    num_sections = fields.IntegerField(mongo_name='num_sections')
    num_segments = fields.IntegerField(mongo_name='num_segments')
    star_rating = fields.IntegerField(mongo_name='star_rating')

    def serialize(self) -> dict:
        """Serializes a playlist into a dictionary"""
        return {
            'index': self.index,
            'id': self.id,
            'title': self.title,
            'danceability': self.danceability,
            'energy': self.energy,
            'mode': self.mode,
            'acousticness': self.acousticness,
            'tempo': self.tempo,
            'duration_ms': self.duration_ms,
            'num_sections': self.num_sections,
            'num_segments': self.num_segments,
            'star_rating': self.star_rating
        }

    def deserialize(self, data: dict):
        """Deserialzes a playlist"""
        app.logger.info("Deserialize (%s)", data)
        try:
            self.index = data["index"]
            self.id = data["id"]
            self.title = data["title"]
            self.danceability = data["danceability"]
            self.energy = data["energy"]
            self.mode = data["mode"]
            self.acousticness = data["acousticness"]
            self.tempo = data["tempo"]
            self.duration_ms = data["duration_ms"]
            self.num_sections = data["num_sections"]
            self.num_segments = data["num_segments"]
            self.star_rating = data["star_rating"]
            
        except KeyError as error:
            raise DataValidationError("Invalid item: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError("Invalid item: body of request contained bad or no data")
        return self

    @classmethod
    def findAll(cls):
        """Gets all the data in the DB"""
        results = cls.objects.all()
        return results

    @classmethod
    def find(cls, title: str):
        """Finds a playlist's attribute by title"""
        try:
            results = cls.objects.raw({"title": title})
            if(results.count()):
                return results[0]
            else:
                return None
        except:
            return None

    @classmethod
    def update(cls, title: str, rating: int):
        """Updates the rating for a playlist"""
        app.logger.info("Rating: %d Title: %s", rating, title)
        try:
            results = cls.objects.raw({"title": title})
            if(results.count()):
                data = results[0]
                data.star_rating = rating
                data.save()
                return data
            else:
                return None
        except:
            return None
