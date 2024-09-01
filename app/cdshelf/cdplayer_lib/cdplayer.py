import logging
import threading
from django.shortcuts import get_object_or_404

import pygame

from ..models import Cd, Song


class CdPlayer:
    def __init__(self):
        self.queue = []
        self.recently_played = []
        self.paused = False
        self.now_playing = None
        self.up_next = None
        pygame.init()
        pygame.mixer.init()
        self.music = pygame.mixer.music
        self.music_end_event = pygame.USEREVENT + 1
        self.music.set_endevent(self.music_end_event)

    def load_next_song(self):
        if len(self.queue) > 0:
            self.up_next = self.queue.pop(0)
            logging.info(f"Queue song: '{self.up_next}'")
            self.music.queue(self.up_next)
        else:
            self.up_next = None

    def event_loop(self):
        while len(self.queue) > 0:
            for event in pygame.event.get():
                if event.type == self.music_end_event:
                    self.recently_played.append(self.now_playing)
                    self.now_playing = self.up_next
                    self.load_next_song()

    def play(self):
        if self.music.get_busy():
            logging.info("Already playing")
            return

        if self.paused:
            logging.info("Unpausing")
            self.paused = False
            self.music.unpause()
            return

        if len(self.queue) > 0:
            logging.info("Play")
            self.now_playing = self.queue.pop(0)
            logging.info(f"Load song: '{self.now_playing}'")
            self.music.load(self.now_playing)
            self.music.play()
            self.load_next_song()

            event_thread = threading.Thread(target=self.event_loop)
            event_thread.start()
        else:
            logging.info("No queued music to play")

    def pause(self):
        logging.info("Pausing")
        self.paused = True
        self.music.pause()

    def next(self):
        logging.info("Next")
        if self.up_next:
            self.recently_played.append(self.now_playing)
            self.now_playing = self.up_next
            self.music.load(self.now_playing)
            self.music.play()
            self.load_next_song()
        else:
            self.eject()

    def previous(self):
        logging.info("Previous")
        if len(self.recently_played) > 0:
            self.queue.insert(0, self.up_next)
            self.queue.insert(0, self.now_playing)
            self.now_playing = self.recently_played.pop()
            self.music.load(self.now_playing)
            self.music.play()
            self.load_next_song()
        else:
            logging.info("Restart first song")
            self.music.play(start=0.0)

    def eject(self):
        logging.info("CD ejected")
        self.queue = []
        self.up_next = None
        self.now_playing = None
        self.cd_id = None
        self.track = None
        if self.music.get_busy():
            self.music.stop()

    def insert(self, cd_id, track=0):
        _cd = get_object_or_404(Cd, pk=cd_id)
        logging.info(f"CD inserted: '{_cd}'")
        logging.info(f"Filter track >= {track}")
        songs = Song.objects.filter(cd=_cd).filter(track__gte=track).order_by("track")
        self.queue = [s.filepath for s in songs]
        skipped = Song.objects.filter(cd=_cd).filter(track__lt=track).order_by("track")
        self.recently_played = [s.filepath for s in skipped]
