"use client";

import Image from "next/image";
import Link from "next/link";
import {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
  type PointerEventHandler,
} from "react";

import { DraggableAgent } from "./DraggableAgent";
import {
  RealtimeVoiceAgent,
  type RealtimeVoiceAgentControls,
} from "./RealtimeVoiceAgent";
import { BACKGROUND_IMAGES } from "./backgrounds";

const AGENT_SIZE = { width: 220, height: 280 };
const SLIDE_AUDIO_SOURCES = BACKGROUND_IMAGES.map((_, index) => {
  const slideNumber = String(index + 1).padStart(2, "0");
  return `/slides/${slideNumber}.mp3`;
});

export default function PresentationPage() {
  return <PresentationContent />;
}

function PresentationContent() {
  const containerRef = useRef<HTMLDivElement>(null);
  const pointerOffsetRef = useRef({ x: 0, y: 0 });
  const pointerIdRef = useRef<number | null>(null);
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const playTimerRef = useRef<number | null>(null);
  const hasPresentedRef = useRef(false);
  const presentationPausedRef = useRef(false);
  const [position, setPosition] = useState({ x: 24, y: 24 });
  const [isDragging, setIsDragging] = useState(false);
  const [slideIndex, setSlideIndex] = useState(0);
  const voiceControlsRef = useRef<RealtimeVoiceAgentControls | null>(null);
  const [micEnabled, setMicEnabled] = useState(false);
  const [presentationPaused, setPresentationPaused] = useState(false);
  const [isSlideAudioActive, setSlideAudioActive] = useState(false);
  const [isAgentAudioActive, setAgentAudioActive] = useState(false);
  const isAudioActive = isSlideAudioActive || isAgentAudioActive;

  const slideCount = SLIDE_AUDIO_SOURCES.length;

  const currentBackground = useMemo(() => {
    if (!BACKGROUND_IMAGES.length) {
      return null;
    }

    const safeIndex = Math.min(slideIndex, BACKGROUND_IMAGES.length - 1);
    return BACKGROUND_IMAGES[safeIndex];
  }, [slideIndex]);

  const currentAudioSource = useMemo(() => {
    if (!SLIDE_AUDIO_SOURCES.length) {
      return null;
    }
    const safeIndex = Math.min(slideIndex, SLIDE_AUDIO_SOURCES.length - 1);
    return SLIDE_AUDIO_SOURCES[safeIndex];
  }, [slideIndex]);

  const clamp = useCallback((value: number, min: number, max: number) => {
    return Math.min(Math.max(value, min), max);
  }, []);

  const handlePointerDown = useCallback<PointerEventHandler<HTMLDivElement>>(
    (event) => {
      if (!containerRef.current) return;
      const rect = containerRef.current.getBoundingClientRect();
      pointerOffsetRef.current = {
        x: event.clientX - rect.left - position.x,
        y: event.clientY - rect.top - position.y,
      };
      pointerIdRef.current = event.pointerId;
      setIsDragging(true);
      event.currentTarget.setPointerCapture(event.pointerId);
    },
    [position.x, position.y],
  );

  const handlePointerMove = useCallback<PointerEventHandler<HTMLDivElement>>(
    (event) => {
      if (!isDragging || pointerIdRef.current !== event.pointerId) return;
      if (!containerRef.current) return;

      const rect = containerRef.current.getBoundingClientRect();
      const rawX =
        event.clientX - rect.left - pointerOffsetRef.current.x;
      const rawY =
        event.clientY - rect.top - pointerOffsetRef.current.y;

      const maxX = rect.width - AGENT_SIZE.width;
      const maxY = rect.height - AGENT_SIZE.height;

      setPosition({
        x: clamp(rawX, 0, Math.max(0, maxX)),
        y: clamp(rawY, 0, Math.max(0, maxY)),
      });
    },
    [clamp, isDragging],
  );

  const handlePointerUp = useCallback<PointerEventHandler<HTMLDivElement>>(
    (event) => {
      if (pointerIdRef.current !== event.pointerId) return;
      pointerIdRef.current = null;
      setIsDragging(false);
      event.currentTarget.releasePointerCapture(event.pointerId);
    },
    [],
  );

  const handleCycleBackground = useCallback(() => {
    if (slideCount <= 1) return;
    setSlideIndex((index) => (index + 1) % slideCount);
  }, [slideCount]);

  const handleMicChange = useCallback((enabled: boolean) => {
    setMicEnabled(enabled);
    setPresentationPaused(enabled);
  }, []);

  const handleMicToggle = useCallback(() => {
    if (voiceControlsRef.current) {
      voiceControlsRef.current.toggleMic();
    }
  }, []);

  const handleAgentAudioActivityChange = useCallback((active: boolean) => {
    setAgentAudioActive(active);
  }, []);

  const playCurrentSlideAudio = useCallback(() => {
    const audio = audioRef.current;
    if (!audio || !currentAudioSource) return;

    if (playTimerRef.current) {
      window.clearTimeout(playTimerRef.current);
      playTimerRef.current = null;
    }

    if (presentationPausedRef.current) {
      return;
    }

    const delay = hasPresentedRef.current ? 1000 : 0;

    playTimerRef.current = window.setTimeout(() => {
      audio
        .play()
        .catch((error) => {
          console.warn("Unable to play slide audio", error);
        });
    }, delay);

    hasPresentedRef.current = true;
  }, [currentAudioSource]);

  useEffect(() => {
    presentationPausedRef.current = presentationPaused;
    if (presentationPaused) {
      if (playTimerRef.current) {
        window.clearTimeout(playTimerRef.current);
        playTimerRef.current = null;
      }
      audioRef.current?.pause();
    } else {
      playCurrentSlideAudio();
    }
  }, [presentationPaused, playCurrentSlideAudio]);

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    if (!currentAudioSource) {
      audio.pause();
      return;
    }

    audio.pause();
    audio.src = currentAudioSource;
    audio.currentTime = 0;

    playCurrentSlideAudio();

    return () => {
      if (playTimerRef.current) {
        window.clearTimeout(playTimerRef.current);
        playTimerRef.current = null;
      }
      audio.pause();
    };
  }, [currentAudioSource, playCurrentSlideAudio]);

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    const handleEnded = () => {
      setSlideAudioActive(false);
      if (presentationPausedRef.current) {
        return;
      }
      setSlideIndex((index) => {
        if (index >= slideCount - 1) {
          return index;
        }
        return index + 1;
      });
    };

    const handlePlaying = () => setSlideAudioActive(true);
    const handlePause = () => setSlideAudioActive(false);

    audio.addEventListener("ended", handleEnded);
    audio.addEventListener("playing", handlePlaying);
    audio.addEventListener("pause", handlePause);

    return () => {
      audio.removeEventListener("ended", handleEnded);
      audio.removeEventListener("playing", handlePlaying);
      audio.removeEventListener("pause", handlePause);
    };
  }, [slideCount]);

  useEffect(() => {
    const audio = audioRef.current;
    return () => {
      if (playTimerRef.current) {
        window.clearTimeout(playTimerRef.current);
        playTimerRef.current = null;
      }
      audio?.pause();
    };
  }, []);

  return (
    <div className="relative min-h-dvh w-full overflow-hidden bg-black">
      <div
        className="absolute inset-0 h-full w-full cursor-pointer"
        onClick={handleCycleBackground}
        role="presentation"
      >
        <div className="relative h-full w-full">
          {currentBackground ? (
            <Image
              key={currentBackground}
              src={currentBackground}
              alt="Mountain valley backdrop"
              fill
              priority
              unoptimized
              className="object-cover"
            />
          ) : null}
        </div>
      </div>

      <div className="relative z-10 flex min-h-dvh flex-col justify-between pointer-events-none">
        <header className="flex flex-col gap-4 bg-gradient-to-b from-black/80 via-black/40 to-transparent px-6 py-6 text-white pointer-events-auto sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-xs uppercase tracking-wide text-slate-300">
              Conquests of Hannibal
            </p>
            <h1 className="text-xl font-semibold">Alpine Crossing</h1>
          </div>
          <div className="flex items-center gap-4">
            <RealtimeVoiceAgent
              controlRef={voiceControlsRef}
              onMicChange={handleMicChange}
              onAudioActivityChange={handleAgentAudioActivityChange}
            />
            <Link
              href="/"
              className="rounded-full border border-white/40 bg-black/40 px-4 py-2 text-xs font-semibold tracking-wide text-white transition hover:bg-white/20"
            >
              Back to lobby
            </Link>
          </div>
        </header>

        <div
          ref={containerRef}
          className="relative flex grow items-end justify-center px-6 pb-10 pointer-events-none"
        >
          <DraggableAgent
            isDragging={isDragging}
            onPointerDown={handlePointerDown}
            onPointerMove={handlePointerMove}
            onPointerUp={handlePointerUp}
            position={position}
            size={AGENT_SIZE}
            isAudioActive={isAudioActive}
          />

          <div className="relative z-10 w-full max-w-2xl rounded-3xl border border-white/40 bg-black/55 px-6 py-4 text-white backdrop-blur pointer-events-auto">
            <label
              htmlFor="question"
              className="mb-2 block text-xs uppercase tracking-wide text-slate-200"
            >
              Ask a question
            </label>
            <div className="flex items-center gap-3">
              <input
                id="question"
                type="text"
                defaultValue="Why did you cross the alps?"
                className="flex-1 rounded-full border border-white/20 bg-white/10 px-4 py-2 text-sm text-white placeholder:text-slate-200 focus:border-white/50 focus:outline-none"
              />
              <button
                type="button"
                onClick={handleMicToggle}
                aria-pressed={micEnabled}
                className={`flex h-10 w-10 items-center justify-center rounded-full text-lg transition ${
                  micEnabled
                    ? "bg-emerald-500 text-white shadow-lg shadow-emerald-500/40"
                    : "bg-white/20 text-white hover:bg-white/30"
                }`}
              >
                🎤
              </button>
              <button
                type="button"
                className="flex h-10 w-10 items-center justify-center rounded-full bg-indigo-500 text-white transition hover:bg-indigo-400"
              >
                ➤
              </button>
            </div>
          </div>
        </div>
      </div>
      <audio ref={audioRef} className="hidden" />
    </div>
  );
}
