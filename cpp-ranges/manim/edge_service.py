"""Edge TTS speech service for manim-voiceover.

Microsoft Edge's "Read Aloud" engine exposes a huge catalogue of high-quality
neural voices, free of charge and with no API key.  This module wraps the
`edge-tts` library so that any `manim_voiceover.VoiceoverScene` can use it
exactly like the built-in `GTTSService`.

Why a local file?
─────────────────
The version of `manim-voiceover` installed in this workspace (0.4.0) does not
bundle an `edge` service module, so we provide our own thin adapter here.

Usage
─────
    from edge_service import EdgeTTSService

    class MyScene(VoiceoverScene):
        def construct(self):
            self.set_speech_service(
                EdgeTTSService(voice="en-IN-NeerjaNeural")
            )
            ...

Install dependency once (no API key needed):
    pip install edge-tts

A short, non-exhaustive list of nice English neural voices you can try
(run `edge-tts --list-voices` for the full catalogue — 400+ voices):

  Indian English
    en-IN-NeerjaNeural         (female, warm, news)
    en-IN-PrabhatNeural        (male, clear, news)

  US English
    en-US-JennyNeural          (female, friendly)
    en-US-AriaNeural           (female, conversational)
    en-US-GuyNeural            (male, casual)
    en-US-AvaMultilingualNeural (female, expressive, newer)
    en-US-AndrewMultilingualNeural (male, expressive, newer)

  UK English
    en-GB-SoniaNeural          (female)
    en-GB-RyanNeural           (male)
    en-GB-LibbyNeural          (female, young)

  Australian / Irish
    en-AU-NatashaNeural        (female)
    en-AU-WilliamNeural        (male)
    en-IE-EmilyNeural          (female)
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from manim import logger

from manim_voiceover._typing import VoiceoverData
from manim_voiceover.helper import remove_bookmarks
from manim_voiceover.services.base import (
    PathLike,
    SpeechService,
    initialize_speech_service,
    path_to_string,
)

try:
    import edge_tts
except ImportError:  # pragma: no cover
    logger.error(
        "Missing package. Run `pip install edge-tts` to use EdgeTTSService."
    )
    raise


# ─── Windows asyncio fix ─────────────────────────────────────────────────────
# edge-tts uses aiohttp.  On Windows + Python ≥3.8 the default
# ProactorEventLoop sometimes prints `RuntimeError: Event loop is closed`
# warnings as it shuts down.  Switching to the selector policy avoids them.
if sys.platform.startswith("win"):
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception:  # pragma: no cover
        pass


# ─── Helpers to keep edge-tts happy ──────────────────────────────────────────
def _normalize_rate(value: str | int | float) -> str:
    """edge-tts expects strings like '+0%', '-10%', '+15%'."""
    if isinstance(value, str):
        return value
    sign = "+" if value >= 0 else "-"
    return f"{sign}{abs(int(value))}%"


def _normalize_pitch(value: str | int | float) -> str:
    """edge-tts expects strings like '+0Hz', '-50Hz', '+25Hz'."""
    if isinstance(value, str):
        return value
    sign = "+" if value >= 0 else "-"
    return f"{sign}{abs(int(value))}Hz"


def _normalize_volume(value: str | int | float) -> str:
    """edge-tts expects strings like '+0%', '-25%'."""
    if isinstance(value, str):
        return value
    sign = "+" if value >= 0 else "-"
    return f"{sign}{abs(int(value))}%"


async def _synthesize_async(
    text: str,
    voice: str,
    rate: str,
    pitch: str,
    volume: str,
    out_path: str,
) -> None:
    communicate = edge_tts.Communicate(
        text,
        voice=voice,
        rate=rate,
        pitch=pitch,
        volume=volume,
    )
    await communicate.save(out_path)


class EdgeTTSService(SpeechService):
    """SpeechService class for Microsoft Edge's online Read-Aloud TTS.

    Wraps the `edge-tts <https://github.com/rany2/edge-tts>`__ library.
    No API key or sign-in is required; the service talks directly to the
    public Azure Cognitive Services endpoint used by Edge.
    """

    def __init__(
        self,
        voice: str = "en-IN-NeerjaNeural",
        rate: str | int | float = "+0%",
        pitch: str | int | float = "+0Hz",
        volume: str | int | float = "+0%",
        **kwargs: object,
    ) -> None:
        """
        Args:
            voice: Edge TTS voice short-name, e.g. ``"en-IN-NeerjaNeural"`` or
                ``"en-US-JennyNeural"``. Run ``edge-tts --list-voices`` for the
                full list.
            rate: Speaking rate. Either an Edge-style string
                (e.g. ``"+10%"`` or ``"-5%"``) or a number interpreted as a
                percentage delta from the default rate.
            pitch: Voice pitch shift. Either an Edge-style string
                (e.g. ``"+50Hz"``) or a number in Hz.
            volume: Output volume. Either an Edge-style string (e.g. ``"+0%"``)
                or a number interpreted as percentage delta.
        """
        initialize_speech_service(self, kwargs)
        self.voice = voice
        self.rate = _normalize_rate(rate)
        self.pitch = _normalize_pitch(pitch)
        self.volume = _normalize_volume(volume)

    def generate_from_text(
        self,
        text: str,
        cache_dir: PathLike | None = None,
        path: PathLike | None = None,
        **kwargs: object,
    ) -> VoiceoverData:
        if cache_dir is None:
            cache_dir = self.cache_dir

        # Per-call overrides take priority over instance defaults.
        voice = str(kwargs.pop("voice", self.voice))
        rate = _normalize_rate(kwargs.pop("rate", self.rate))  # type: ignore[arg-type]
        pitch = _normalize_pitch(kwargs.pop("pitch", self.pitch))  # type: ignore[arg-type]
        volume = _normalize_volume(kwargs.pop("volume", self.volume))  # type: ignore[arg-type]

        input_text = remove_bookmarks(text)
        # Anything that influences the produced audio MUST live in
        # input_data so the cache key changes when the user swaps voices.
        input_data = {
            "input_text": input_text,
            "service": "edge",
            "voice": voice,
            "rate": rate,
            "pitch": pitch,
            "volume": volume,
        }

        cached_result = self.get_cached_result(input_data, cache_dir)
        if cached_result is not None:
            return cached_result

        if path is None:
            audio_path = self.get_audio_basename(input_data) + ".mp3"
        else:
            audio_path = path_to_string(path)

        out_file = str(Path(cache_dir) / audio_path)

        try:
            asyncio.run(
                _synthesize_async(input_text, voice, rate, pitch, volume, out_file)
            )
        except Exception as exc:  # noqa: BLE001
            logger.error(f"edge-tts synthesis failed: {exc}")
            raise Exception(
                "edge-tts could not synthesize speech. "
                "Check your internet connection and that "
                f"voice={voice!r} is a valid Edge TTS voice "
                "(run `edge-tts --list-voices`)."
            ) from exc

        json_dict: VoiceoverData = {
            "input_text": text,
            "input_data": input_data,
            "original_audio": audio_path,
        }

        return json_dict
