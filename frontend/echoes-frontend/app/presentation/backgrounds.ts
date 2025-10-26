export const BACKGROUND_IMAGES = [
  "/videos/ComfyUI_00001_.webp", "/videos/ComfyUI_00002_.webp","/videos/ComfyUI_00003_.webp",
] as const;

export type BackgroundImage = (typeof BACKGROUND_IMAGES)[number];
