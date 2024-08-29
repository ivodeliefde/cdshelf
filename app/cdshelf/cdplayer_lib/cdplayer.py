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
            logging.info("Go!")
            next_song = self.queue.pop(0)
            self.music.queue(next_song)

    def event_loop(self):
        while len(self.queue) > 0:
            for event in pygame.event.get():
                if event.type == self.music_end_event:
                    self.load_next_song()

    def play(self):
        if self.paused:
            logging.info("unpausing")
            self.paused = False
            self.music.unpause()
            return

        first_song = self.queue.pop(0)
        self.music.load(first_song)
        self.music.play()
        self.load_next_song()

        event_thread = threading.Thread(target=self.event_loop)
        event_thread.start()

    def pause(self):
        self.pause = True
        self.music.pause()

    def stop(self):
        self.music.stop()

    def insert(self, cd_id, track=0):
        _cd = get_object_or_404(Cd, pk=cd_id)
        songs = Song.objects.filter(cd=_cd).order_by("track").filter(track__gte=track)
        for s in songs:
            self.queue.append(s.filepath)
