import { NextResponse } from "next/server";

const REALTIME_SESSION_URL = "https://api.openai.com/v1/realtime/sessions";

import { getOpenAIApiKey } from "@/lib/server/getOpenAIApiKey";

export async function POST() {
  const apiKey = await getOpenAIApiKey();

  if (!apiKey) {
    return NextResponse.json(
      { error: "OpenAI API key is not configured." },
      { status: 500 },
    );
  }

  const response = await fetch(REALTIME_SESSION_URL, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: "gpt-4o-realtime-preview",
      voice: "verse",
      modalities: ["audio", "text"],
      instructions:
        "You are Hannibal Barca, Carthaginian general and conqueror of the Alps. Speak only in this persona and never break character. Obey the client instructions exactly. When text is provided you must read it verbatim without adding or removing words, responding in Hannibal's voice. ONLY REPLY IN ENGLISH.",
    }),
  });

  if (!response.ok) {
    const detail = await response.text();
    console.error("Failed to create realtime session", detail);
    return NextResponse.json(
      { error: "Failed to create realtime session" },
      { status: 500 },
    );
  }

  const session = await response.json();
  return NextResponse.json({ client_secret: session.client_secret });
}
