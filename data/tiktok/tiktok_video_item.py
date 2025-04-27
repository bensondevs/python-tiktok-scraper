from dataclasses import dataclass
from typing import Optional

@dataclass
class TikTokVideoItem:
    video_url: str
    thumbnail: str
    caption: str