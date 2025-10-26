"use client";

import {
  useCallback,
  useEffect,
  useRef,
  useState,
  type MutableRefObject,
} from "react";

type AgentStatus =
  | "idle"
  | "requesting-permissions"
  | "connecting"
  | "connected"
  | "error";

export type RealtimeVoiceAgentControls = {
  micEnabled: boolean;
  toggleMic: () => void;
  setMicEnabled: (enabled: boolean) => void;
};

type RealtimeVoiceAgentProps = {
  controlRef?: MutableRefObject<RealtimeVoiceAgentControls | null>;
  onMicChange?: (enabled: boolean) => void;
  onAudioActivityChange?: (active: boolean) => void;
};

export function RealtimeVoiceAgent({
  controlRef,
  onMicChange,
  onAudioActivityChange,
}: RealtimeVoiceAgentProps) {
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const pcRef = useRef<RTCPeerConnection | null>(null);
  const dataChannelRef = useRef<RTCDataChannel | null>(null);
  const localStreamRef = useRef<MediaStream | null>(null);
  const micStateRef = useRef(false);
  const [status, setStatus] = useState<AgentStatus>("idle");
  const [micEnabled, setMicEnabled] = useState(false);
  const shouldRestartAfterUnmuteRef = useRef(false);

  const cleanup = useCallback(() => {
    if (dataChannelRef.current) {
      try {
        dataChannelRef.current.close();
      } catch {
        // ignore
      }
      dataChannelRef.current = null;
    }

    if (pcRef.current) {
      pcRef.current.close();
      pcRef.current = null;
    }

    if (localStreamRef.current) {
      localStreamRef.current.getTracks().forEach((track) => track.stop());
      localStreamRef.current = null;
    }
    onAudioActivityChange?.(false);
  }, [onAudioActivityChange]);

  const applyMicState = useCallback((enabled: boolean) => {
    setMicEnabled(enabled);
  }, []);

  const cancelCurrentResponse = useCallback(() => {
    const channel = dataChannelRef.current;
    if (channel && channel.readyState === "open") {
      try {
        channel.send(
          JSON.stringify({
            type: "response.cancel",
          }),
        );
        shouldRestartAfterUnmuteRef.current = true;
      } catch (error) {
        console.debug("Failed to cancel realtime response", error);
      }
    }
  }, []);

  const requestResumePrompt = useCallback(() => {
    const channel = dataChannelRef.current;
    if (!channel || channel.readyState !== "open") {
      return false;
    }

    try {
      channel.send(
        JSON.stringify({
          type: "response.create",
          response: {
            instructions:
              "You have resumed speaking. In Hannibal's voice, ask the user what they would like to discuss next without breaking character.",
            modalities: ["audio"],
          },
        }),
      );
      return true;
    } catch (error) {
      console.debug("Failed to send resume prompt", error);
      return false;
    }
  }, []);

  const toggleMic = useCallback(() => {
    setMicEnabled((prev) => !prev);
  }, []);

  useEffect(() => {
    if (!controlRef) return;

    controlRef.current = {
      micEnabled,
      toggleMic,
      setMicEnabled: applyMicState,
    };

    return () => {
      if (controlRef.current?.toggleMic === toggleMic) {
        controlRef.current = null;
      }
    };
  }, [applyMicState, controlRef, micEnabled, toggleMic]);

  useEffect(() => {
    micStateRef.current = micEnabled;

    if (localStreamRef.current) {
      localStreamRef.current.getAudioTracks().forEach((track) => {
        track.enabled = micEnabled;
      });
    }
    onMicChange?.(micEnabled);
  }, [micEnabled, onMicChange]);

  useEffect(() => {
    const audioEl = audioRef.current;
    if (audioEl) {
      if (micEnabled) {
        audioEl.muted = false;
        audioEl
          .play()
          .catch(() => {
            // Autoplay restrictions can block play until user interaction
          });
      } else {
        audioEl.muted = true;
        audioEl.pause();
      }
    }

    const channel = dataChannelRef.current;
    if (!channel || channel.readyState !== "open") {
      return;
    }

    if (!micEnabled) {
      cancelCurrentResponse();
      onAudioActivityChange?.(false);
      shouldRestartAfterUnmuteRef.current = true;
    } else if (shouldRestartAfterUnmuteRef.current) {
      const sent = requestResumePrompt();
      shouldRestartAfterUnmuteRef.current = !sent;
    }
  }, [cancelCurrentResponse, micEnabled, onAudioActivityChange, requestResumePrompt]);

  useEffect(() => {
    const audioEl = audioRef.current;
    if (!audioEl || !onAudioActivityChange) return;

    const handlePlaying = () => onAudioActivityChange(true);
    const handlePause = () => onAudioActivityChange(false);
    const handleEnded = () => onAudioActivityChange(false);

    audioEl.addEventListener("playing", handlePlaying);
    audioEl.addEventListener("pause", handlePause);
    audioEl.addEventListener("ended", handleEnded);

    return () => {
      audioEl.removeEventListener("playing", handlePlaying);
      audioEl.removeEventListener("pause", handlePause);
      audioEl.removeEventListener("ended", handleEnded);
    };
  }, [onAudioActivityChange]);

  useEffect(() => {
    let cancelled = false;

    async function requestSession() {
      if (!navigator.mediaDevices) {
        setStatus("error");
        return;
      }

      setStatus("requesting-permissions");
      try {
        const localStream = await navigator.mediaDevices.getUserMedia({
          audio: true,
        });

        if (cancelled) {
          localStream.getTracks().forEach((track) => track.stop());
          return;
        }

        localStream.getAudioTracks().forEach((track) => {
          track.enabled = micStateRef.current;
        });

        localStreamRef.current = localStream;
        setStatus("connecting");

        const tokenResponse = await fetch("/api/realtime-session", {
          method: "POST",
        });

        if (!tokenResponse.ok) {
          throw new Error("Failed to fetch realtime session");
        }

        const tokenPayload = await tokenResponse.json();
        const clientSecret: string | undefined =
          tokenPayload?.client_secret?.value;

        if (!clientSecret) {
          throw new Error("Missing realtime client secret");
        }

        const pc = new RTCPeerConnection({
          iceServers: [{ urls: "stun:stun.l.google.com:19302" }],
        });
        pcRef.current = pc;

        pc.ontrack = (event) => {
          const [stream] = event.streams;
          const audioEl = audioRef.current;
          if (audioEl) {
            audioEl.srcObject = stream;
            audioEl
              .play()
              .catch(() => {
                // Autoplay restrictions; user may need to interact with the page.
              });
          }
      };

        localStream.getTracks().forEach((track) => {
          pc.addTrack(track, localStream);
        });
        pc.addTransceiver("audio", { direction: "sendrecv" });

        const dataChannel = pc.createDataChannel("oai-events");
        dataChannelRef.current = dataChannel;

        dataChannel.onopen = () => {
        if (micStateRef.current) {
          const sent = requestResumePrompt();
          shouldRestartAfterUnmuteRef.current = !sent;
        } else {
          shouldRestartAfterUnmuteRef.current = true;
        }
        };

        dataChannel.onmessage = (event) => {
          console.debug("[OpenAI realtime]", event.data);
        };

        dataChannel.onclose = () => {
          if (dataChannelRef.current === dataChannel) {
            dataChannelRef.current = null;
          }
        };

        const offer = await pc.createOffer();
        await pc.setLocalDescription(offer);

        await waitForIceGathering(pc);

        if (cancelled) {
          return;
        }

        const sdpResponse = await fetch(
          "https://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview",
          {
            method: "POST",
            headers: {
              Authorization: `Bearer ${clientSecret}`,
              "Content-Type": "application/sdp",
            },
            body: pc.localDescription?.sdp,
          },
        );

        if (!sdpResponse.ok) {
          throw new Error("Failed to negotiate realtime connection");
        }

        const answer = await sdpResponse.text();
        if (cancelled) {
          return;
        }
        await pc.setRemoteDescription({ type: "answer", sdp: answer });
        setStatus("connected");
      } catch (error) {
        console.error("Realtime voice agent error", error);
        setStatus("error");
      }
    }

    requestSession();

    return () => {
      cancelled = true;
      cleanup();
    };
  }, [cleanup, requestResumePrompt]);

  return (
    <div className="flex items-center gap-3 text-xs text-slate-300">
      <span
        className={`inline-flex h-2.5 w-2.5 rounded-full ${
          status === "connected"
            ? "bg-emerald-400 animate-pulse"
            : status === "error"
              ? "bg-rose-500"
              : "bg-amber-400 animate-pulse"
        }`}
        aria-hidden="true"
      />
      <span>
        {status === "connected"
          ? micEnabled
            ? "Listening…"
            : "Voice agent ready"
          : status === "requesting-permissions"
            ? "Requesting microphone…"
            : status === "connecting"
              ? "Connecting to voice agent…"
              : status === "error"
                ? "Voice agent unavailable"
                : "Starting voice agent…"}
      </span>
      <audio ref={audioRef} autoPlay playsInline className="hidden" />
    </div>
  );
}

async function waitForIceGathering(pc: RTCPeerConnection) {
  if (pc.iceGatheringState === "complete") {
    return;
  }

  await new Promise<void>((resolve) => {
    function checkState() {
      if (pc.iceGatheringState === "complete") {
        pc.removeEventListener("icegatheringstatechange", checkState);
        resolve();
      }
    }

    pc.addEventListener("icegatheringstatechange", checkState);
  });
}
