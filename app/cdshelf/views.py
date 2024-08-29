from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Cd, Artist, SourceDir, Song
from .source_lib import LoadSourceDir
from .cdplayer_lib import CdPlayer


cd_player = CdPlayer()


def home(request):
    first_cds_list = Cd.objects.order_by("title")[:50]
    context = {"first_cds_list": first_cds_list}
    return render(request, "cdshelf\\home.html", context)


def artist(request, artist_id):
    _artist = get_object_or_404(Artist, pk=artist_id)
    cds = Cd.objects.filter(artist=_artist)
    return render(request, "cdshelf\\artist.html", {"artist": _artist, "cds": cds})


def cd(request, cd_id):
    _cd = get_object_or_404(Cd, pk=cd_id)
    songs = Song.objects.filter(cd=_cd)
    if request.method == "POST":
        data = request.POST
        track = int(data.get("track").split("|")[0])
        cd_player.insert(cd_id=cd_id, track=track)
        cd_player.play()
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
