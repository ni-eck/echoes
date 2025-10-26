import Link from "next/link";

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col bg-slate-950 text-slate-100">
      <header className="border-b border-slate-800 bg-slate-900/70 backdrop-blur">
        <div className="mx-auto flex max-w-4xl items-center justify-between px-6 py-5">
          <span className="text-lg font-semibold tracking-wide">Echoes</span>
          <div className="text-sm text-slate-400">Prototype workspace</div>
        </div>
      </header>

      <main className="mx-auto flex w-full max-w-4xl grow flex-col px-6 pb-10 pt-8">
        <section className="flex grow flex-col rounded-3xl border border-slate-800 bg-slate-900/70 p-6 shadow-lg">
          <div className="mb-6 space-y-3 text-center sm:text-left">
            <h1 className="text-3xl font-semibold text-slate-50">
              Ask the Echoes Assistant
            </h1>
            <p className="text-sm text-slate-400">
              Start a conversation or jump straight into the immersive
              presentation to meet the AI guide.
            </p>
          </div>

          <div className="flex grow flex-col overflow-hidden rounded-2xl border border-slate-800 bg-slate-950/60">
            <div className="flex grow flex-col gap-6 overflow-y-auto bg-gradient-to-b from-slate-950 via-slate-940 to-slate-950 p-6">
              <div className="flex items-start gap-4">
                <div className="mt-1 h-9 w-9 shrink-0 rounded-full bg-indigo-500/40 backdrop-blur" />
                <div className="max-w-lg rounded-2xl bg-slate-900/70 px-4 py-3 text-left text-sm text-slate-200 shadow">
                  Welcome to Echoes! I can guide you through historic moments
                  and immersive stories. What would you like to explore?
                </div>
              </div>
              <div className="flex flex-row-reverse items-start gap-4">
                <div className="mt-1 h-9 w-9 shrink-0 rounded-full bg-slate-100/80" />
                <div className="max-w-lg rounded-2xl bg-indigo-500/30 px-4 py-3 text-left text-sm text-slate-100 shadow">
                  Show me the Alpine expedition with Marcus Aurelius.
                </div>
              </div>
            </div>

            <div className="border-t border-slate-800 bg-slate-900/80 p-4">
              <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
                <div className="flex grow items-center gap-3 rounded-2xl border border-slate-800 bg-slate-950/70 px-4 py-3">
                  <textarea
                    rows={1}
                    className="w-full resize-none bg-transparent text-sm text-slate-100 placeholder:text-slate-500 focus:outline-none"
                    placeholder="Type your next question..."
                  />
                  <button
                    type="button"
                    className="rounded-full bg-indigo-500/80 p-2 text-slate-100 transition hover:bg-indigo-400/80"
                  >
                    <span className="sr-only">Send message</span>↗
                  </button>
                </div>
                <Link
                  href="/presentation"
                  className="inline-flex items-center justify-center rounded-2xl bg-indigo-500 px-5 py-3 text-sm font-medium text-white transition hover:bg-indigo-400"
                >
                  Enter Presentation
                </Link>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
