import os
import logging

from tinytag import TinyTag

from ..models import Cd, Artist, Song


class LoadSourceDir:
    def __init__(self, location) -> None:
        self.location = location
        self.audio_extentions = [".flac", ".mp3", ".aac"]

    def walk(self):
        for path, directories, files in os.walk(self.location):
            for file in files:
                if os.path.splitext(file)[-1].lower() in self.audio_extentions:
                    full_path = os.path.join(path, file)
                    file_metadata = TinyTag.get(full_path)
                    yield file_metadata, full_path

    def load(self):
        i = 0
        for song_metadata, song_filepath in self.walk():
            logging.info(f"Processing file '{song_filepath}'")
            _artist, artist_was_created = Artist.objects.get_or_create(
                name=song_metadata.albumartist
            )
            logging.info(f"- Artist '{_artist.name}' (created: {artist_was_created})")
            _cd, cd_was_created = Cd.objects.get_or_create(
                title=song_metadata.album, artist=_artist
            )
            logging.info(f"- CD '{_cd.title}' (created: {cd_was_created})")
            _song, song_was_created = Song.objects.get_or_create(
                title=song_metadata.title,
                track=song_metadata.track,
                filepath=song_filepath,
                cd=_cd,
            )
            logging.info(f"- Song '{_song.title}' (created: {song_was_created})")
            logging.info("Done.")
            if i > 1000:
                return
            else:
                i += 1
