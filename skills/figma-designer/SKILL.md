---
name: figma-designer
description: Create distinctive, polished designs in Figma through the official Figma MCP server and the Plugin API. Use when the person asks to design in Figma, make a Figma mockup or layout, build screens or components in Figma, change an existing Figma file, or capture a web page into Figma.
metadata:
  version: "1.0.0"
---

# Figma Designer

Create distinctive, production-grade designs directly in Figma via the official Figma MCP server. Every design should have a clear aesthetic point of view, no generic AI slop.

## When to Use

- User asks to create, build, or design something in Figma
- User wants to iterate on an existing Figma file
- User shares a Figma URL and wants modifications
- User wants wireframes, mockups, layouts, or UI components in Figma
- User wants to capture a web page into Figma

## Prerequisites

The official Figma MCP server (`https://mcp.figma.com/mcp`) must be connected to your agent and signed in. If it is not, help the person add it the way their agent adds a remote MCP server, then sign in through the browser when asked. In Claude Code the command is:

```bash
claude mcp add --transport http figma https://mcp.figma.com/mcp --scope user
```

Codex CLI and Gemini CLI add remote MCP servers through their own settings. Check the agent's current documentation for the exact step.

## Available MCP Tools

The names below are the server's own tool names. Your agent may show them with a prefix, such as `mcp__figma__whoami`.

| Tool | Purpose |
|------|---------|
| `whoami` | Get authenticated user info and plan keys |
| `create_new_file` | Create a new blank Figma file in drafts |
| `use_figma` | Execute Plugin API JS against a file (primary write tool) |
| `get_screenshot` | Screenshot a node for visual verification |
| `get_design_context` | Read a design, returns code, screenshot, hints |
| `generate_figma_design` | Capture/import a web page into Figma |
| `search_design_system` | Search for existing design system components |
| `get_metadata` | Get file metadata |

## Process

### Step 1: Understand the Brief & Style

Before writing any Plugin API code, gather these from the user. **Ask if not provided:**

- **What** is being designed (screens, components, wireframe, layout, dashboard, etc.)
- **Purpose**: who uses it and why
- **Existing file?**: does the user have a fileKey/URL, or do we need a new file?
- **Theme**: ask the user to pick one (or suggest one based on context):

**Theme options (always present these if user hasn't specified a style):**

| Theme | Description |
|-------|-------------|
| Light clean | White/light gray backgrounds, crisp shadows, high contrast text |
| Dark mode | Near-black backgrounds with subtle hue, soft glowing accents |
| Glassmorphism | Frosted glass panels, background blur, translucent layers |
| Brutally minimal | Extreme whitespace, hairline rules, restrained 2-color palette |
| Maximalist chaos | Dense layers, overlapping elements, saturated color |
| Retro-futuristic | CRT glow, scanlines, neon on dark |
| Organic / natural | Rounded forms, earth tones, hand-drawn feel |
| Luxury / refined | Gold accents, serif typography, generous spacing |
| Editorial / magazine | Strong grid, dramatic type scale, photo-forward |
| Brutalist / raw | Monospace type, harsh borders, exposed structure |
| Art deco / geometric | Symmetry, metallic gradients, decorative geometry |
| Soft / pastel | Rounded corners, gentle gradients, light and airy |
| Industrial / utilitarian | Tight grids, status indicators, data-dense |
| Swiss / international | Strict grid, clean sans-serif, asymmetric balance |
| Neo-Tokyo | High contrast, glitch accents, layered depth |
| Neumorphic | Soft extruded shapes, monochrome, subtle inner/outer shadows |
| Gradient-forward | Bold gradient backgrounds and fills, vibrant color transitions |
| Wireframe / lo-fi | Grayscale placeholders, no polish, structure only |

If the user says something generic like "modern" or "professional", default to **Light clean** or **Dark mode** and confirm.

No two designs should look the same, vary palettes and typography even within the same theme across generations.

### Step 2: File Setup & Account Selection

1. **Get planKey**: call `whoami` to get the user's plans.
   - **One plan** → use its `key` field automatically.
   - **Multiple plans** → **always ask the user which account/team to save to.** Present the plan names and let them pick.
2. **Create or locate file:**
   - No file exists → `create_new_file` with the planKey, fileName, and `editorType: "design"`
   - User provides a URL → extract fileKey from `figma.com/design/:fileKey/:fileName`
   - Branch URL (`figma.com/design/:fileKey/branch/:branchKey/:fileName`) → use branchKey as fileKey
3. **Store the fileKey**: every subsequent call needs it.

### Step 3: Design in Figma

Use `use_figma` to execute Plugin API JavaScript against the target file.

**Always pass these parameters:**
- `fileKey`: the file key from Step 2
- `code`: Plugin API JavaScript (max 50,000 chars)
- `description`: concise description of what the code does
- `skillNames`: always pass `"figma-designer"` for logging

**Before creating components**, call `search_design_system` to check for existing design system components. Import matches via `importComponentByKeyAsync` / `importComponentSetByKeyAsync` instead of recreating them.

#### Plugin API Capabilities Reference

**Shapes & Frames:**
```js
figma.createFrame()        // containers, artboards
figma.createRectangle()    // rectangles
figma.createEllipse()      // circles, ovals
figma.createPolygon()      // triangles, hexagons
figma.createStar()         // stars
figma.createLine()         // lines
figma.createVector()       // custom SVG paths via vectorPaths
```

**Fills, solids, gradients, images:**
```js
// Solid
node.fills = [{ type: 'SOLID', color: { r: 0.1, g: 0.1, b: 0.15 }, opacity: 1 }]

// Linear gradient
node.fills = [{
  type: 'GRADIENT_LINEAR',
  gradientStops: [
    { position: 0, color: { r: 0.1, g: 0.8, b: 0.4, a: 1 } },
    { position: 1, color: { r: 0.05, g: 0.3, b: 0.5, a: 1 } }
  ],
  gradientTransform: [[1, 0, 0], [0, 1, 0]]  // 2x3 affine matrix
}]

// Also: GRADIENT_RADIAL, GRADIENT_ANGULAR, GRADIENT_DIAMOND
```

**Effects, shadows, blurs, glow:**
```js
// GOTCHA: blendMode is REQUIRED on all shadow effects, omitting it causes a validation error
node.effects = [
  { type: 'DROP_SHADOW', blendMode: 'NORMAL', color: { r: 0, g: 0, b: 0, a: 0.25 }, offset: { x: 0, y: 4 }, radius: 12, spread: 0, visible: true },
  { type: 'INNER_SHADOW', blendMode: 'NORMAL', color: { r: 1, g: 1, b: 1, a: 0.1 }, offset: { x: 0, y: 1 }, radius: 2, spread: 0, visible: true },
  { type: 'LAYER_BLUR', radius: 8, visible: true },
  { type: 'BACKGROUND_BLUR', radius: 20, visible: true }
]
```

**Strokes:**
```js
node.strokes = [{ type: 'SOLID', color: { r: 1, g: 1, b: 1 }, opacity: 0.2 }]
node.strokeWeight = 1
node.strokeAlign = 'INSIDE'  // INSIDE, OUTSIDE, CENTER
node.dashPattern = [6, 4]    // dashed lines
```

**Corner radius:**
```js
node.cornerRadius = 12
// Or per-corner:
node.topLeftRadius = 16
node.topRightRadius = 16
node.bottomLeftRadius = 0
node.bottomRightRadius = 0
```

**Auto Layout:**
```js
frame.layoutMode = 'HORIZONTAL'  // or 'VERTICAL'
frame.primaryAxisAlignItems = 'CENTER'   // MIN, CENTER, MAX, SPACE_BETWEEN
frame.counterAxisAlignItems = 'CENTER'   // MIN, CENTER, MAX
frame.itemSpacing = 16
frame.paddingTop = 24
frame.paddingRight = 24
frame.paddingBottom = 24
frame.paddingLeft = 24
frame.primaryAxisSizingMode = 'AUTO'  // AUTO or FIXED
frame.counterAxisSizingMode = 'AUTO'
frame.layoutWrap = 'WRAP'  // for wrapping grids
```

**Typography:**
```js
// MUST load font before any text operations
await figma.loadFontAsync({ family: 'Inter', style: 'Bold' })
// GOTCHA: Style names have spaces: "Semi Bold" NOT "SemiBold", "Extra Bold" NOT "ExtraBold"

const text = figma.createText()
text.fontName = { family: 'Inter', style: 'Bold' }
text.characters = 'Hello World'
text.fontSize = 32
text.letterSpacing = { value: -1, unit: 'PIXELS' }  // or 'PERCENT'
text.lineHeight = { value: 40, unit: 'PIXELS' }     // or 'AUTO'
text.textAlignHorizontal = 'CENTER'  // LEFT, CENTER, RIGHT, JUSTIFIED
text.textAlignVertical = 'CENTER'    // TOP, CENTER, BOTTOM
text.textCase = 'UPPER'             // ORIGINAL, UPPER, LOWER, TITLE
text.textDecoration = 'UNDERLINE'   // NONE, UNDERLINE, STRIKETHROUGH
text.fills = [{ type: 'SOLID', color: { r: 1, g: 1, b: 1 } }]

// Rich text, per-range styling
text.setRangeFontSize(0, 5, 48)
text.setRangeFills(0, 5, [{ type: 'SOLID', color: { r: 0.2, g: 0.8, b: 0.4 } }])
text.setRangeFontName(0, 5, { family: 'Inter', style: 'Bold' })
```

**Blend modes & opacity:**
```js
node.opacity = 0.8
node.blendMode = 'MULTIPLY'  // NORMAL, MULTIPLY, SCREEN, OVERLAY, DARKEN,
// LIGHTEN, COLOR_DODGE, COLOR_BURN, HARD_LIGHT, SOFT_LIGHT, DIFFERENCE,
// EXCLUSION, HUE, SATURATION, COLOR, LUMINOSITY, PASS_THROUGH
```

**Nesting & hierarchy:**
```js
parentFrame.appendChild(childNode)
// Coordinates are relative to parent
childNode.x = 20
childNode.y = 20
```

**Components & instances:**
```js
const component = figma.createComponent()
const instance = component.createInstance()
// ALWAYS search existing design system first via search_design_system
// Then import: await figma.importComponentByKeyAsync(componentKey)
```

**Boolean operations:**
```js
figma.union([nodeA, nodeB], parentFrame)
figma.subtract([nodeA, nodeB], parentFrame)
figma.intersect([nodeA, nodeB], parentFrame)
figma.exclude([nodeA, nodeB], parentFrame)
```

**Vectors (custom paths):**
```js
const vector = figma.createVector()
vector.vectorPaths = [{
  windingRule: 'EVENODD',
  data: 'M 0 0 L 100 0 L 100 100 L 0 100 Z'  // SVG path syntax
}]
```

**Page management:**
```js
figma.currentPage                          // current page
// GOTCHA: Do NOT set figma.currentPage directly, use async method:
await figma.setCurrentPageAsync(page)
figma.currentPage.findAll(n => n.type === 'FRAME')  // query nodes
await figma.listAvailableFontsAsync()      // list available fonts
figma.group(nodes, parent)                 // group nodes
node.remove()                              // delete a node
```

### Step 4: Verify & Iterate

After the initial design pass:
1. **Always screenshot**: call `get_screenshot` with the fileKey and the root frame's nodeId to verify visually
2. If the user requests changes, call `use_figma` again on the same fileKey
3. To modify existing elements, find them by name: `figma.currentPage.findOne(n => n.name === 'Screen 3')`
4. You CAN iterate, this is the key advantage over static generation

## Reading Existing Designs

To read/inspect an existing Figma design before modifying:
- `get_design_context`: returns code representation, screenshot, and contextual hints. Primary tool for understanding a design.
- `get_screenshot`: visual snapshot of a specific node
- `get_metadata`: file-level metadata

Extract fileKey and nodeId from URLs:
- `figma.com/design/:fileKey/:fileName?node-id=:nodeId` → convert `-` to `:` in nodeId
- `figma.com/design/:fileKey/branch/:branchKey/:fileName` → use branchKey as fileKey

## Web Page Capture

To capture a web page into Figma (not Plugin API, separate workflow):
1. Call `generate_figma_design` without `outputMode` first to get options
2. Choose `newFile` or `existingFile` mode
3. Poll with the returned `captureId` every 5 seconds (up to 10 times) until `status: 'completed'`

Use `generate_figma_design` ONLY for initial web page capture. For all updates and modifications, use `use_figma`.

## Design principles

Pick one direction before you place anything, and say it in a sentence: who it is for, the mood, and the one thing the design should be remembered for. Then make every choice serve that sentence.

- **Type.** Build hierarchy with real contrast in size and weight. Tighten large headlines and open up small uppercase labels. Check which fonts the file has with `figma.listAvailableFontsAsync()` before you settle on a pairing.
- **Color.** Keep the palette small: a base, a text color and one or two accents, saved as styles or variables. On dark themes use a near-black with a little hue, and on light themes a tinted off-white.
- **Space.** Use one spacing scale inside a section, such as steps of 8px. Choose roomy or dense on purpose.
- **Depth.** Add depth only where the direction calls for it: a soft shadow, a thin low-opacity stroke, a gentle gradient. A wireframe or a strictly minimal theme needs none.
- **Variety.** Do not repeat the last design. Change the palette, the type and the layout between projects, even within the same theme.

For deeper guidance on visual direction, Anthropic's [Frontend Design](https://github.com/anthropics/skills/tree/main/skills/frontend-design) skill pairs well with this one.

### Figma-Specific Best Practices

- Use auto-layout for structured, responsive-feeling layouts
- Group related elements with named frames for clean layer structure
- Add subtle strokes (0.5-1px, low opacity) for definition between elements
- Name every layer clearly, `Header / Title`, `Card / Active State`, etc.
- Split complex designs across multiple `use_figma` calls to avoid execution timeouts

### Avoid

- Unnamed layers.
- Uneven spacing. Use auto-layout or one manual scale.
- The same look every time: the same palette, font pairing and card grid.
- Decoration that does not serve the direction you picked.

## Font Safety

Not all fonts are available in every Figma file. To be safe:
1. `Inter` is the safe fallback, since it is available in every file. Use its range of weights.
2. Before using a non-standard font, wrap in try/catch:
```js
try {
  await figma.loadFontAsync({ family: 'Space Mono', style: 'Regular' })
} catch {
  await figma.loadFontAsync({ family: 'Inter', style: 'Regular' })
}
```
3. Use `figma.listAvailableFontsAsync()` to check what's available when the user wants specific typography

## Limitations

- **No animation**: Figma is static. Suggest prototyping in Figma or code for motion.
- **No external images from URL**: images require raw bytes (Uint8Array). For placeholder images, use colored rectangles or gradients.
- **No CSS/HTML**: everything is Figma scene graph nodes.
- **Font loading is async**: always `await figma.loadFontAsync()` before text operations.
- **Execution time limits**: for very complex designs, split across multiple `use_figma` calls.
- **Code max length**: `use_figma` caps the code length per call (50,000 characters when this was written).

Tool names, limits and plan rules change. Check Figma's MCP server documentation when something here does not match what you see.
