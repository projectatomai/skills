---
name: nano-banana
description: Generate an image from a text prompt with Google's Gemini image model (Nano Banana), with an optional visual theme. Use for "generate an image", "create an image", "make me a picture", "nano banana", "draw" or any request for an AI-generated image when a Gemini API key is available.
metadata:
  version: "1.0.0"
---

# Nano Banana: Gemini image generation

Generate an image from a text prompt with Google's Gemini image model, and show it to the person.

## Before you start

The person needs a Gemini API key from Google AI Studio, set as the environment variable `GEMINI_API_KEY`. Check that it is set without printing it:

```bash
[ -n "$GEMINI_API_KEY" ] && echo "key is set" || echo "GEMINI_API_KEY is not set"
```

If it is not set, stop and tell the person to set it in their shell or their secrets manager. Never ask them to paste the key into the chat, and never print it.

The commands need `curl` and `python3`.

Each image costs money on the person's account. Say so before the first one, and check Google's current pricing page if they ask how much.

## Step 1: Choose a theme

Unless the person has already described a style, ask them to pick a theme. Offer the four groups first, then the themes in the group they choose, plus "No theme".

- **Classic and artistic:** Monochrome, Sketch, Oil painting, Soft portrait
- **Bold and graphic:** Color block, Risograph, Enamel pin, Dynamite
- **Cinematic and moody:** Cinematic, Moody, Salon, Sunrise, Technicolor
- **Fantasy and sci-fi:** Steampunk, Cyborg, Surreal, Mythic fighter, Gothic clay, Runway

If they name a style of their own, use it.

### Theme to prompt

Add the theme's style suffix to the end of the person's prompt:

| Theme | Style suffix appended to prompt |
|-------|-------------------------------|
| Monochrome | `"in a high-contrast black and white monochrome photography style"` |
| Sketch | `"in a hand-drawn pencil sketch style on aged paper"` |
| Oil painting | `"in a classical oil painting style with visible brushstrokes and rich texture"` |
| Soft portrait | `"in a soft portrait photography style with gentle lighting and shallow depth of field"` |
| Color block | `"in a bold color block style with flat geometric shapes and vivid pastel tones"` |
| Risograph | `"in a risograph print style with halftone dots, misregistration, and limited ink colors"` |
| Enamel pin | `"in an enamel pin style with thick outlines, flat fills, and a metallic border"` |
| Dynamite | `"in an explosive dynamic style with intense energy, motion blur, and fiery elements"` |
| Cinematic | `"in a cinematic film still style with dramatic lighting, anamorphic lens, and color grading"` |
| Moody | `"in a moody atmospheric style with low-key lighting, deep shadows, and muted tones"` |
| Salon | `"in an elegant salon portrait style with soft studio lighting and refined composition"` |
| Sunrise | `"in a golden hour sunrise style with warm backlit glow and silhouette elements"` |
| Technicolor | `"in a vintage technicolor style with saturated primary colors and retro film grain"` |
| Steampunk | `"in a steampunk style with brass gears, Victorian machinery, and industrial gothic elements"` |
| Cyborg | `"in a cybernetic cyborg style with exposed mechanical parts, neon accents, and futuristic tech"` |
| Surreal | `"in a surreal dreamlike style with impossible geometry and melting reality"` |
| Mythic fighter | `"in an epic mythic warrior style with dramatic fantasy combat and magical effects"` |
| Gothic clay | `"in a gothic clay sculpture style with dark ornate details and stop-motion texture"` |
| Runway | `"in a high-fashion runway photography style with editorial lighting and avant-garde composition"` |
| No theme | *(no suffix, use prompt as-is)* |

For a style of their own, add `"in a {their style} style"`. Do not use a living artist's name as a style: describe the look in plain words.

## Step 2: Generate the image

Call the Gemini API with curl, save the response, and decode the image into a temporary PNG. Put the prompt in a file first, so quotes in it cannot break the command.

```bash
MODEL="gemini-3-pro-image-preview"
TMPFILE="$(mktemp -d)/image.png"
PROMPT_FILE=$(mktemp)
cat > "$PROMPT_FILE" <<'PROMPT'
THE PROMPT, WITH ITS STYLE SUFFIX
PROMPT
python3 - "$PROMPT_FILE" > "$PROMPT_FILE.json" <<'PY'
import json, sys
prompt = open(sys.argv[1]).read().strip()
print(json.dumps({"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"responseModalities": ["image", "text"]}}))
PY
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent" \
  -H "x-goog-api-key: ${GEMINI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d @"$PROMPT_FILE.json" > "$PROMPT_FILE.response"
python3 - "$PROMPT_FILE.response" "$TMPFILE" <<'PY'
import base64, json, sys
resp = json.load(open(sys.argv[1]))
if "error" in resp:
    print("ERROR:", resp["error"].get("message", "unknown error"))
    sys.exit(1)
candidates = resp.get("candidates") or [{}]
for part in (candidates[0].get("content") or {}).get("parts", []):
    data = part.get("inlineData") or part.get("inline_data")
    if data:
        open(sys.argv[2], "wb").write(base64.b64decode(data["data"]))
        print(sys.argv[2])
        break
else:
    print("ERROR: the response held no image")
    sys.exit(1)
PY
rm -f "$PROMPT_FILE" "$PROMPT_FILE.json" "$PROMPT_FILE.response"
```

Keep `"responseModalities": ["image", "text"]` in the request, or no image comes back.

Model names change. If the API answers that the model is not found, look up the current image model in Google's Gemini API documentation and set `MODEL` to it.

## Step 3: Show the image

Show the PNG to the person with whatever your agent uses to display an image, or give them its path. If they want to keep it, copy it from the temporary path to the folder they name.

## When something goes wrong

- **The key is not set:** ask the person to set `GEMINI_API_KEY`.
- **400:** the prompt was probably refused by the safety filters. Say so, and offer to reword it.
- **401 or 403:** the key is wrong, revoked or not allowed to use this model.
- **429:** rate limited. Wait and try once more, or tell the person.
- **No image in the response:** the model sometimes answers with text only. Try again with "Generate an image of:" at the start of the prompt.

## Notes

- Describe the style, colors and composition. Detailed prompts give better pictures.
- Do not make images of real people without their consent, and do not copy a named artist's style.
