---
name: imagegen-2
description: Generate images with OpenAI's gpt-image-2 model, from a text prompt or from one or more reference pictures (image edit). Use for "generate an image", "imagegen", "gpt-image-2" or any OpenAI image request, and above all when a reference photo should drive the result, such as a portrait in a new style or brand visuals from a source picture.
metadata:
  version: "1.0.0"
---

# imagegen-2: OpenAI image generation

Generate an image from a text prompt, or from a prompt plus reference pictures, with OpenAI's `gpt-image-2` model. Save the result to a temporary PNG and show it to the person.

Reference pictures are where this model is strongest: keeping one subject recognisable across several styles works far better with a reference than with a description.

## Before you start

The person needs an OpenAI API key, set as the environment variable `OPENAI_API_KEY`. Check that it is set without printing it:

```bash
[ -n "$OPENAI_API_KEY" ] && echo "key is set" || echo "OPENAI_API_KEY is not set"
```

If it is not set, stop and tell the person to set it in their shell or their secrets manager. Never ask them to paste the key into the chat, and never print it. If they keep several keys for different projects, ask which project this image belongs to and let them point `OPENAI_API_KEY` at that key.

Each image costs money on the person's account, and more at larger sizes and higher quality. Say so before the first one, and check OpenAI's current pricing page if they ask how much.

The commands need `curl`, `jq` and `python3`.

## Step 1: Pick the mode

1. **Text to image:** no reference picture. Calls `/v1/images/generations`.
2. **Reference edit:** one or more reference pictures and a prompt. Calls `/v1/images/edits` as a multipart upload.
3. **Batch:** the same prompt several times, or several prompts against one reference. Repeat the single call.

Pick the mode yourself when the request makes it clear. A picture or image file the prompt refers to ("turn this into a watercolor") means a reference edit. A plain description means text to image. A request for several variations or styles means a batch. Ask only when you cannot tell.

## Step 2: Choose a theme (text to image only)

Unless the person has already described a style, ask them to pick a theme. Offer the four groups first, then the themes in the group they choose, plus "No theme".

- **Classic and artistic:** Monochrome, Sketch, Oil painting, Soft portrait
- **Bold and graphic:** Color block, Risograph, Enamel pin, Dynamite
- **Cinematic and moody:** Cinematic, Moody, Salon, Sunrise, Technicolor
- **Fantasy and sci-fi:** Steampunk, Cyborg, Surreal, Mythic fighter, Gothic clay, Runway

Skip this step when there is a reference picture (it already carries the look), when the prompt is already full art direction (more than about 30 words with style words in it), or when the prompt comes from the person's own prompt file.

Add the theme's style suffix to the end of the prompt:

| Theme | Style suffix |
|-------|--------------|
| Monochrome | `in a high-contrast black and white monochrome photography style` |
| Sketch | `in a hand-drawn pencil sketch style on aged paper` |
| Oil painting | `in a classical oil painting style with visible brushstrokes and rich texture` |
| Soft portrait | `in a soft portrait photography style with gentle lighting and shallow depth of field` |
| Color block | `in a bold color block style with flat geometric shapes and vivid pastel tones` |
| Risograph | `in a risograph print style with halftone dots, misregistration, and limited ink colors` |
| Enamel pin | `in an enamel pin style with thick outlines, flat fills, and a metallic border` |
| Dynamite | `in an explosive dynamic style with intense energy, motion blur, and fiery elements` |
| Cinematic | `in a cinematic film still style with dramatic lighting, anamorphic lens, and color grading` |
| Moody | `in a moody atmospheric style with low-key lighting, deep shadows, and muted tones` |
| Salon | `in an elegant salon portrait style with soft studio lighting and refined composition` |
| Sunrise | `in a golden hour sunrise style with warm backlit glow and silhouette elements` |
| Technicolor | `in a vintage technicolor style with saturated primary colors and retro film grain` |
| Steampunk | `in a steampunk style with brass gears, Victorian machinery, and industrial gothic elements` |
| Cyborg | `in a cybernetic cyborg style with exposed mechanical parts, neon accents, and futuristic tech` |
| Surreal | `in a surreal dreamlike style with impossible geometry and melting reality` |
| Mythic fighter | `in an epic mythic warrior style with dramatic fantasy combat and magical effects` |
| Gothic clay | `in a gothic clay sculpture style with dark ornate details and stop-motion texture` |
| Runway | `in a high-fashion runway photography style with editorial lighting and avant-garde composition` |
| No theme | *(no suffix, use the prompt as it is)* |

For a style of their own, add `in a {their style} style`. Do not use a living artist's name as a style: describe the look in plain words.

## Step 3: Generate

Put the prompt in a file first, so quotes in it cannot break the command.

```bash
OUT="$(mktemp -d)/image.png"
PROMPT_FILE=$(mktemp)
cat > "$PROMPT_FILE" <<'PROMPT'
THE PROMPT, WITH ITS STYLE SUFFIX
PROMPT
```

This snippet saves the image from a response file. Use it after every call:

```bash
save_image() {
python3 - "$1" "$2" <<'PY'
import base64, json, sys
resp = json.load(open(sys.argv[1]))
if "error" in resp:
    print("API ERROR:", resp["error"].get("message", "unknown")); sys.exit(1)
item = resp["data"][0]
open(sys.argv[2], "wb").write(base64.b64decode(item["b64_json"]))
print(sys.argv[2])
if item.get("revised_prompt"):
    print("revised prompt:", item["revised_prompt"])
PY
}
```

### Text to image

```bash
jq -nc --arg model gpt-image-2 --rawfile prompt "$PROMPT_FILE" --arg size 1024x1024 \
  '{model: $model, prompt: ($prompt|rtrimstr("\n")), n: 1, size: $size}' > "$PROMPT_FILE.json"
curl -s -X POST https://api.openai.com/v1/images/generations \
  -H "Authorization: Bearer ${OPENAI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d @"$PROMPT_FILE.json" > "$PROMPT_FILE.response"
save_image "$PROMPT_FILE.response" "$OUT"
```

### Reference edit

The reference must be a PNG, JPG or WebP of 25 MB or less. `--form-string` and `prompt=<file` keep odd characters in the prompt or the path from being read as curl syntax.

```bash
REF="PATH_OF_THE_REFERENCE_PICTURE"
curl -s -X POST https://api.openai.com/v1/images/edits \
  -H "Authorization: Bearer ${OPENAI_API_KEY}" \
  --form-string model=gpt-image-2 \
  -F "image=@\"${REF}\"" \
  -F "prompt=<${PROMPT_FILE}" \
  --form-string n=1 \
  --form-string size=1024x1024 > "$PROMPT_FILE.response"
save_image "$PROMPT_FILE.response" "$OUT"
```

For several reference pictures (a subject and a style, for example), repeat the field as `image[]`:

```bash
-F "image[]=@\"${SUBJECT}\"" -F "image[]=@\"${STYLE_REF}\""
```

When you are done, remove `$PROMPT_FILE`, `$PROMPT_FILE.json` and `$PROMPT_FILE.response`.

### Batch

Repeat the single call for each variation or each style, one after another, so the cost stays easy to follow. Run them in parallel only if the person asks. Tell the person how many images the batch will make before you start.

If the person keeps their prompts in a file in the project, read the prompts from it and do not ask them to paste the prompts again. Save each result under the output path they name, one file for each style.

## Step 4: Show the image

Show the PNG to the person with whatever your agent uses to display an image, or give them its path. If they want to keep it and have not said where, ask.

## Size and quality

Sizes: `1024x1024` (square, the default), `1024x1536` (portrait), `1536x1024` (landscape) and `auto`.

Quality: `low`, `medium`, `high` and `auto` (the default). Add `"quality": "high"` to the JSON body, or `--form-string quality=high` to the edit call, when the person wants the best result. It is slower and costs more.

Model names, sizes and prices change. If the API refuses a value, check OpenAI's image generation documentation for the current ones.

## When something goes wrong

- **The key is not set:** ask the person to set `OPENAI_API_KEY`.
- **401:** the key is wrong or revoked.
- **400 `invalid_request_error`:** usually a prompt the safety system refused, or a reference picture it cannot read. Show the API's message and offer to reword.
- **`content_policy_violation`:** the prompt or the reference was refused. Do not retry. Explain it to the person.
- **429:** rate limited. Wait 20 seconds and try once more, and tell the person if it continues.
- **No image in the response:** try once more. If it fails again, show the error.

## Notes

- The response holds the PNG as base64 in `data[0].b64_json`. It may also hold a `revised_prompt`, which shows how the model read the request. Pass it on if the person wants to see it.
- Do not make or edit images of real people without their consent.
