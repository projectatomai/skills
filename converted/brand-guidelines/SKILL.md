---
name: brand-guidelines
description: Applies Anthropic's official brand colors and typography to any sort of artifact that may
  benefit from having Anthropic's look-and-feel. Use it when brand colors or style guidelines, visual
  formatting, or company design standards apply.
license: Apache-2.0. Complete terms in LICENSE.txt
compatibility: Converted by Skillfarm to read the same in Claude Code, Codex CLI and Gemini CLI.
metadata:
  source: https://github.com/anthropics/skills/tree/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/brand-guidelines
  source-commit: e4bb5d960d87126ff3b3a8af1a104b7db67560ba
  original-author: Anthropic
  converted-by: Skillfarm (https://skillfarm.ai)
  converter-version: '1'
---

> **Skillfarm multi-agent version.** Converted from [anthropics/skills](https://github.com/anthropics/skills/tree/e4bb5d960d87126ff3b3a8af1a104b7db67560ba/skills/brand-guidelines) by Anthropic so it reads the same in Claude Code, Codex CLI and Gemini CLI. The original text follows this note unchanged. NOTICE.md lists every change.
>
> How to read it, whichever agent you are:
> - It was written for a sandbox with its tools already installed. Here, check that what it needs is present before you start, and ask the person before you install anything.

# Anthropic Brand Styling

## Overview

To access Anthropic's official brand identity and style resources, use this skill.

**Keywords**: branding, corporate identity, visual identity, post-processing, styling, brand colors, typography, Anthropic brand, visual formatting, visual design

## Brand Guidelines

### Colors

**Main Colors:**

- Dark: `#141413` - Primary text and dark backgrounds
- Light: `#faf9f5` - Light backgrounds and text on dark
- Mid Gray: `#b0aea5` - Secondary elements
- Light Gray: `#e8e6dc` - Subtle backgrounds

**Accent Colors:**

- Orange: `#d97757` - Primary accent
- Blue: `#6a9bcc` - Secondary accent
- Green: `#788c5d` - Tertiary accent

### Typography

- **Headings**: Poppins (with Arial fallback)
- **Body Text**: Lora (with Georgia fallback)
- **Note**: Fonts should be pre-installed in your environment for best results

## Features

### Smart Font Application

- Applies Poppins font to headings (24pt and larger)
- Applies Lora font to body text
- Automatically falls back to Arial/Georgia if custom fonts unavailable
- Preserves readability across all systems

### Text Styling

- Headings (24pt+): Poppins font
- Body text: Lora font
- Smart color selection based on background
- Preserves text hierarchy and formatting

### Shape and Accent Colors

- Non-text shapes use accent colors
- Cycles through orange, blue, and green accents
- Maintains visual interest while staying on-brand

## Technical Details

### Font Management

- Uses system-installed Poppins and Lora fonts when available
- Provides automatic fallback to Arial (headings) and Georgia (body)
- No font installation required - works with existing system fonts
- For best results, pre-install Poppins and Lora fonts in your environment

### Color Application

- Uses RGB color values for precise brand matching
- Applied via python-pptx's RGBColor class
- Maintains color fidelity across different systems
