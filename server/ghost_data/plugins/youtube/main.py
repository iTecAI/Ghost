from util.plugin_tools import PluginTemplate, PluginManifest, PluginResult
from typing import Any, TypedDict
from datetime import datetime
from pytube import Search, YouTube
import logging

from concurrent.futures import ThreadPoolExecutor, as_completed


class YTAuthor(TypedDict):
    name: str
    channel_id: str
    channel_url: str


class YoutubeResult(PluginResult):
    has_audio: bool
    has_video: bool
    resolutions: list[str]
    author: YTAuthor
    length: int
    views: int
    date: datetime


def search(
    plugin: "YoutubeDownloadManager", search_term: str, filters: dict[str, Any]
) -> list[YoutubeResult]:
    results: list[YouTube] = Search(search_term).results

    parsed_results: list[YoutubeResult] = []
    with ThreadPoolExecutor(max_workers=6) as executor:
        result_seq = [
            executor.submit(
                lambda f: YoutubeResult(
                    id=f.video_id,
                    title=f.title,
                    thumbnail=f.thumbnail_url,
                    has_audio=len(f.streams.filter(only_audio=True)) > 0,
                    has_video=len(f.streams.filter(only_video=True)) > 0,
                    resolutions=[
                        x
                        for x in list(
                            set(
                                [
                                    getattr(i, "resolution", None)
                                    for i in f.streams.filter(only_video=True)
                                ]
                            )
                        )
                        if x != None
                    ],
                    author=YTAuthor(
                        name=f.author,
                        channel_id=f.channel_id,
                        channel_url=f.channel_url,
                    ),
                    length=f.length,
                    views=f.views,
                    date=f.publish_date,
                ),
                i,
            )
            for i in results
        ]
        for future in as_completed(result_seq):
            try:
                parsed_results.append(future.result())
            except:
                logging.exception("Failed to parse YT result")

    if "channel" in filters.keys():
        parsed_results = [
            i
            for i in parsed_results
            if i["author"]["name"].lower() != filters["channel"].lower()
        ]

    return parsed_results


class YoutubeDownloadManager(PluginTemplate):
    hook_search = search

    def __init__(self, config: dict, manifest: PluginManifest) -> None:
        super().__init__(config, manifest)
