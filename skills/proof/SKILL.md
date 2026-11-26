---
name: proof
description: Capture visual proof that finished work works - a screenshot of a web page or app window, or a short screen recording for a flow. Use at the end of a task, for "/proof", or whenever asked to verify a result with a screenshot.
metadata:
  version: "1.0.0"
---

# Proof

End a task with visual proof of the real result. Use a screenshot for a single result and a short screen recording for a flow, an interaction or several features. Show the result where the person will use it: the production site, the signed build, or a clearly labeled simulator or local server.

Capture the actual result, not a mock-up of it. For a web page, use the steps below. For a native app, use whatever screen capture tool you are allowed to use in this session.

If a capture fails, fix that capture and keep going with the rest of the work. When no image is possible, give the next best evidence, such as the saved file, a record read back from the system, or a test result, and say that the screenshot is still owed. Label test data as test data.

## Which page to capture

Work out the address from what you were given, in this order:

1. **A full URL**: use it as it is (`/proof https://example.com/pricing`).
2. **A path**: add it to the running local server (`/proof /account` becomes `http://localhost:3000/account`).
3. **A port**: use `http://localhost:<port>` (`/proof 4000`).
4. **The word "mobile"**: use the default address at a 390×844 viewport.
5. **Nothing**: work it out from the task, and fall back to `http://localhost:3000`.

## Steps with a browser tool

These use the Playwright MCP tool names. With another browser tool, do the same four things in the same order.

```
1. browser_navigate        → the address
2. browser_resize          → the viewport (1440×900 by default, 390×844 for mobile)
3. browser_wait_for        → the network to go idle, or a key element to appear
4. browser_take_screenshot → a file named proof-<timestamp>.png
```

If the screenshot is blank, all white or an error page:

- Wait two seconds and take it once more.
- If it fails again, say so, and carry on with the other checks you can make.

## What to send back

- The screenshot or recording.
- One line with the address, the viewport and the time, for example: `http://localhost:3000/account · 1440×900 · 2026-05-05T14:32:01Z`
- A short note if a retry was needed.

Do not add a summary of what you built. The picture is the proof.

## Examples

| You are asked | What to capture |
|---|---|
| `/proof` | `localhost:3000` at 1440×900 |
| `/proof /account` | `localhost:3000/account` |
| `/proof 4000` | `localhost:4000` |
| `/proof https://example.com` | That page |
| `/proof mobile` | `localhost:3000` at 390×844 |
| `/proof https://example.com/waitlist mobile` | That page at 390×844 |

## When something goes wrong

| Problem | What to do |
|---|---|
| The local server is not running | Read the project's instructions for starting it, start it if you are allowed to, and try again. |
| The page shows a 404 or 500 | Send the screenshot of the error page and say it is an error. |
| No browser tool is available | Use another capture tool you are allowed to use, then say what is still missing. |
| The screenshot is blank | Retry once after two seconds, and report it if it is still blank. |
