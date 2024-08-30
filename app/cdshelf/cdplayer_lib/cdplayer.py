import logging
import threading
from django.shortcuts import get_object_or_404

import pygame

from ..models import Cd, Song


class CdPlayer:
    def __init__(self):
        self.queue = []
        self.paused = False
        pygame.init()
        pygame.mixer.init()
        self.music = pygame.mixer.music
        self.music_end_event = pygame.USEREVENT + 1
        self.music.set_endevent(self.music_end_event)

    def load_next_song(self):
        if len(self.queue) > 0:
            next_song = self.queue.pop(0)
            logging.info(f"Queue song: '{next_song}'")
            self.music.queue(next_song)

    def event_loop(self):
        while len(self.queue) > 0:
            for event in pygame.event.get():
                if event.type == self.music_end_event:
                    self.load_next_song()

    def play(self):
        if self.paused:
            logging.info("Unpausing")
            self.paused = False
            self.music.unpause()
            return

        if len(self.queue) > 0:
            logging.info("Play")
            first_song = self.queue.pop(0)
            logging.info(f"Load song: '{first_song}'")
            self.music.load(first_song)
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

    def eject(self):
        logging.info("CD ejected")
        self.music.stop()
        self.queue = []

    def insert(self, cd_id, track=0):
        _cd = get_object_or_404(Cd, pk=cd_id)
        logging.info(f"CD inserted: '{_cd}'")
        logging.info(f"Filter track >= {track}")
        songs = Song.objects.filter(cd=_cd).filter(track__gte=track).order_by("track")
        self.queue = [s.filepath for s in songs]
