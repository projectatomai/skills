---
name: grok-imagine
description: Generate and edit images with xAI's Grok Imagine API. Covers text to image, editing one image, and combining up to three images. Use for "grok image", "grok imagine", "xai image" or any image request where the person wants the xAI model and has an xAI API key.
metadata:
  version: "1.0.0"
---

# Grok Imagine: xAI image generation and editing

Generate an image from a text prompt, or edit one to three reference images, with xAI's Grok Imagine API. Save the result to a temporary file and show it to the person.

## Before you start

The person needs an xAI API key, set as the environment variable `XAI_API_KEY`. Check that it is set without printing it:

```bash
[ -n "$XAI_API_KEY" ] && echo "key is set" || echo "XAI_API_KEY is not set"
```

If it is not set, stop and tell the person to set it in their shell or their secrets manager. Never ask them to paste the key into the chat, and never print it.

Each image costs money on the person's account. Say so before the first one. The response reports the real cost, so pass it on.

The commands need `curl`, `jq` and `python3`.

## What the API expects

These shapes were tested against the live API. Models and prices change, so check xAI's documentation when a call is refused.

- **Generate:** `POST https://api.x.ai/v1/images/generations`
- **Edit:** `POST https://api.x.ai/v1/images/edits`
- **Models:** `grok-imagine-image` (fast, the default) and `grok-imagine-image-quality` (higher fidelity, costs more).
- **Generate body:** `{model, prompt, n?, response_format?}`. Without `response_format`, each result is a temporary hosted JPEG `url`. With `"response_format": "b64_json"`, each result is base64 in `b64_json`.
- **Edit body, one image:** `image` must be an object: `{"url": "<url or data URI>", "type": "image_url"}`.
- **Edit body, two or three images:** `image` must be an array of plain strings: `["<uri1>", "<uri2>"]`. The two forms do not mix. A string in the single slot is refused, and an object in the array is refused.
- **Response:** `{"data": [{"url": "...", "mime_type": "image/jpeg"}], "usage": {"cost_in_usd_ticks": N}}`. There is no revised prompt, and there are no `size`, `quality`, `style` or `seed` parameters. The model picks the aspect ratio, so put art direction in the prompt.
- **Cost in US dollars:** `usage.cost_in_usd_ticks / 1e10`. For example, 400000000 ticks is $0.04.

## Step 1: Pick the mode

1. **Text to image:** no reference picture. Use the generate endpoint.
2. **Edit one image:** one reference picture and a prompt. Use the edit endpoint with `image` as an object.
3. **Combine images:** two or three reference pictures, to merge subjects or carry a style across. Use the edit endpoint with `image` as an array of strings.
4. **Variations:** the same prompt several times. Use `n` on the generate endpoint.

Pick the mode yourself when the request makes it clear. A picture or image file the prompt refers to ("turn this into a sketch") means an edit. Two or three pictures named together means combine. A plain description means text to image. Ask only when you cannot tell.

## Step 2: Pick the model

Use `grok-imagine-image` unless the person asks for high quality or this is a final version, then use `grok-imagine-image-quality`. Do not raise the question yourself unless they ask about quality or cost.

## Step 3: Generate or edit

### Text to image

Put the prompt in a file first, so quotes in it cannot break the command.

```bash
OUT="$(mktemp -d)/grok-imagine.jpg"
PROMPT_FILE=$(mktemp)
cat > "$PROMPT_FILE" <<'PROMPT'
THE PROMPT
PROMPT
jq -nc --arg m grok-imagine-image --rawfile p "$PROMPT_FILE" '{model:$m, prompt:($p|rtrimstr("\n")), n:1}' > "$PROMPT_FILE.json"
curl -sS -X POST https://api.x.ai/v1/images/generations \
  -H "Content-Type: application/json" -H "Authorization: Bearer ${XAI_API_KEY}" \
  --data @"$PROMPT_FILE.json" > "$PROMPT_FILE.response"
python3 - "$PROMPT_FILE.response" "$OUT" <<'PY'
import base64, json, subprocess, sys
r = json.load(open(sys.argv[1]))
if "data" not in r:
    print("API ERROR:", json.dumps(r)[:300]); sys.exit(1)
img = r["data"][0]
if img.get("b64_json"):
    data = base64.b64decode(img["b64_json"])
else:
    # Download with curl. The image host can refuse Python's default client.
    data = subprocess.run(["curl", "-sSL", img["url"]], check=True, capture_output=True).stdout
open(sys.argv[2], "wb").write(data)
print(sys.argv[2])
print("cost: $%.4f" % (r.get("usage", {}).get("cost_in_usd_ticks", 0) / 1e10))
PY
rm -f "$PROMPT_FILE" "$PROMPT_FILE.json" "$PROMPT_FILE.response"
```

For several variations, set `n` to the number wanted and save every item of `r["data"]` to its own file.

### Edit one image

A web address can go straight into the body. A local file must be sent as a base64 `data:` URI, which is too long for a command argument, so build the body in a file with Python.

```bash
BODY=$(mktemp)
python3 - "PATH_OR_URL_OF_THE_PICTURE" "THE PROMPT" "$BODY" <<'PY'
import base64, json, mimetypes, sys
ref, prompt, out = sys.argv[1:4]
if ref.startswith("http"):
    url = ref
else:
    mime = mimetypes.guess_type(ref)[0] or "image/png"
    url = f"data:{mime};base64," + base64.b64encode(open(ref, "rb").read()).decode()
json.dump({"model": "grok-imagine-image", "prompt": prompt,
           "image": {"url": url, "type": "image_url"}}, open(out, "w"))
PY
curl -sS -X POST https://api.x.ai/v1/images/edits \
  -H "Content-Type: application/json" -H "Authorization: Bearer ${XAI_API_KEY}" \
  --data @"$BODY" > "$BODY.response"
```

Then save the result from `$BODY.response` with the same Python snippet as text to image, and remove `$BODY` and `$BODY.response`.

### Combine two or three images

The same as editing one image, but `image` is an array of plain strings. Three pictures is the limit.

```bash
BODY=$(mktemp)
python3 - "$BODY" "THE PROMPT" "first.png" "second.jpg" <<'PY'
import base64, json, mimetypes, sys
out, prompt, *refs = sys.argv[1:]
def to_uri(p):
    if p.startswith("http"):
        return p
    mime = mimetypes.guess_type(p)[0] or "image/png"
    return f"data:{mime};base64," + base64.b64encode(open(p, "rb").read()).decode()
json.dump({"model": "grok-imagine-image", "prompt": prompt,
           "image": [to_uri(p) for p in refs[:3]]}, open(out, "w"))
PY
```

Then send `$BODY` to the edit endpoint and save the result as above.

## Step 4: Show the image

Show the saved file to the person with whatever your agent uses to display an image, or give them its path, and tell them the cost. If they want to keep it, copy it to the folder they name.

Hosted `url` results are temporary. Always download the image straight away, as the snippets do, and never hand the person the raw address as a lasting link.

## When something goes wrong

- **The key is not set:** ask the person to set `XAI_API_KEY`.
- **401:** the key is wrong or revoked.
- **422 "invalid type: map" or "invalid type: string":** `image` has the wrong shape. One image needs an object with `url` and `type`. Two or three need an array of strings.
- **"Internal error" or "Image generation failed":** often a source picture that is too small or damaged, or a passing fault at xAI. Try once more. If it fails again with a good picture, show the person the message.
- **Empty reply or a reply that is not JSON:** usually a timeout on a large body with several pictures. Shrink the sources to 1024 pixels or less on the long side and try again.
- **Model not found:** the model names have changed. Look up the current ones in xAI's documentation.

## Notes

- Results are JPEG. Ask for `b64_json` only when you need the bytes without a second download.
- Do not make or edit images of real people without their consent.
