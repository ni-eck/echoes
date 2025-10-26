"use client";

import Image from "next/image";
import { memo, type PointerEventHandler } from "react";

type DraggableAgentProps = {
  position: { x: number; y: number };
  isDragging: boolean;
  size: { width: number; height: number };
  isAudioActive: boolean;
  onPointerDown: PointerEventHandler<HTMLDivElement>;
  onPointerMove: PointerEventHandler<HTMLDivElement>;
  onPointerUp: PointerEventHandler<HTMLDivElement>;
};

function DraggableAgentComponent({
  isDragging,
  onPointerDown,
  onPointerMove,
  onPointerUp,
  position,
  size,
  isAudioActive,
}: DraggableAgentProps) {
  return (
    <div
      role="presentation"
      onPointerDown={onPointerDown}
      onPointerMove={onPointerMove}
      onPointerUp={onPointerUp}
      onPointerCancel={onPointerUp}
      className="group absolute left-0 top-0 z-20 cursor-grab active:cursor-grabbing pointer-events-auto"
      style={{
        width: size.width,
        height: size.height,
        transform: `translate3d(${position.x}px, ${position.y}px, 0)`,
        transition: isDragging ? "none" : "transform 200ms ease-out",
      }}
    >
      <div className="flex h-full w-full flex-col overflow-hidden rounded-3xl border border-white/40 bg-black/70 text-white backdrop-blur shadow-2xl">
        <div className="relative h-full w-full bg-black">
          {isAudioActive ? (
            <video
              key="orator-video"
              className="h-full w-full object-cover pointer-events-none"
              src="/videos/ComfyUI_00007_.mov"
              autoPlay
              muted
              loop
              playsInline
            />
          ) : (
            <Image
              key="orator-image"
              src="/frontal.jpg"
              alt="AI Orator"
              fill
              priority
              className="object-cover"
            />
          )}
          <div className="pointer-events-none absolute inset-0 bg-gradient-to-b from-transparent via-black/20 to-black/40" />
        </div>
        <div className="flex items-center justify-between px-4 py-2 text-xs uppercase tracking-wide text-slate-200">
          <span>AI Orator</span>
          <span className="rounded-full bg-white/20 px-2 py-0.5 text-[10px] text-white">
            Live
          </span>
        </div>
      </div>
    </div>
  );
}

export const DraggableAgent = memo(DraggableAgentComponent);
export type { DraggableAgentProps };
