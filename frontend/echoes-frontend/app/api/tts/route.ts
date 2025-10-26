import { NextResponse } from "next/server";

import { getOpenAIApiKey } from "@/lib/server/getOpenAIApiKey";

const TTS_ENDPOINT = "https://api.openai.com/v1/audio/speech";
const DEFAULT_VOICE = "verse";
const DEFAULT_FORMAT = "mp3" as const;
const MODEL = "gpt-4o-mini-tts";
type AudioFormat = typeof DEFAULT_FORMAT | "wav" | "ogg";

type TTSRequestBody = {
  text?: string;
  voice?: string;
  format?: AudioFormat;
};

const MIME_TYPES: Record<AudioFormat, string> = {
  mp3: "audio/mpeg",
  wav: "audio/wav",
  ogg: "audio/ogg",
};

export async function POST(request: Request) {
  const apiKey = await getOpenAIApiKey();

  if (!apiKey) {
    return NextResponse.json(
      { error: "OpenAI API key is not configured." },
      { status: 500 },
    );
  }

  let body: TTSRequestBody;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json(
      { error: "Invalid JSON body." },
      { status: 400 },
    );
  }

  const text = body.text?.trim();
  if (!text) {
    return NextResponse.json(
      { error: "Missing `text` in request body." },
      { status: 400 },
    );
  }

  const voice = body.voice ?? DEFAULT_VOICE;
  const format: AudioFormat = body.format ?? DEFAULT_FORMAT;

  const response = await fetch(TTS_ENDPOINT, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: MODEL,
      input: text,
      voice,
      format,
    }),
  });

  if (!response.ok) {
    const detail = await response.text();
    console.error("Failed to synthesize speech", detail);
    return NextResponse.json(
      { error: "Failed to synthesize speech." },
      { status: 500 },
    );
  }

  const audio = await response.arrayBuffer();
  const mimeType = MIME_TYPES[format] ?? MIME_TYPES[DEFAULT_FORMAT];

  return new Response(audio, {
    status: 200,
    headers: {
      "Content-Type": mimeType,
      "Content-Length": String(audio.byteLength),
      "Cache-Control": "no-store",
      "Content-Disposition": `inline; filename="speech.${format}"`,
    },
  });
}
