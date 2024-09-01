import logging

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Cd, Artist, SourceDir, Song
from .source_lib import LoadSourceDir
from .cdplayer_lib import CdPlayer


cd_player = CdPlayer()


def home(request):
    logging.info("Loading home page")
    cds_list = Cd.objects.order_by("title")
    context = {"cds_list": cds_list}
    return render(request, "cdshelf\\home.html", context)


def artist(request, artist_id):
    _artist = get_object_or_404(Artist, pk=artist_id)
    cds = Cd.objects.filter(artist=_artist)
    return render(request, "cdshelf\\artist.html", {"artist": _artist, "cds": cds})


def cd(request, cd_id):
    _cd = get_object_or_404(Cd, pk=cd_id)
    songs = Song.objects.filter(cd=_cd)
    return render(request, "cdshelf\\cd.html", {"cd": _cd, "songs": songs})


def source_dirs(request):
    source_dirs_list = SourceDir.objects.order_by("name")[:5]
    return render(
        request, "cdshelf\\source_dirs.html", {"source_dirs_list": source_dirs_list}
    )


def load_source_dir(request, source_dir_id):
    _source_dir = get_object_or_404(SourceDir, pk=source_dir_id)
    LoadSourceDir(location=_source_dir.location).load()
    return HttpResponse(f"Loaded: {_source_dir}")


def pause(request):
    cd_player.pause()
    return HttpResponse("Paused playback")


def play(request):
    cd_id = request.GET.get("cd_id", None)
    track = request.GET.get("track", None)
    if cd_id:
        if not track:
            track = 1
        logging.info(f"Insert CD '{cd_id}' and start as of track {track}")
        cd_player.insert(cd_id=cd_id, track=track)

    cd_player.play()
    return HttpResponse("Started playback")


def eject(request):
    cd_player.eject()
    return HttpResponse("Stopped playback")


def next(request):
    cd_player.next()
    return HttpResponse("Next song")


def previous(request):
    cd_player.previous()
    return HttpResponse("Previous song")


def search(request):
    cds = []
    artists = []
    songs = []
    query = request.POST.get("q", None)
    if query:
        logging.info(f"Search CDs, Artists and Songs with query '{query}'")
        cds = Cd.objects.filter(title__icontains=query)
        artists = Artist.objects.filter(name__icontains=query)
        songs = Song.objects.filter(title__icontains=query)

    return render(
        request,
        "cdshelf\\search.html",
        {"cds": cds, "artists": artists, "songs": songs},
    )
