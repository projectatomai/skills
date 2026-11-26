---
name: design-reference-review
description: Ground new or changed UI in real references, compare distinct concepts before committing, catch generic choices, and check the actual render and its interaction states. Use for any web or native UI design, redesign or visual polish.
metadata:
  version: "1.0.0"
---

# Design reference and review

Use this on UI design work. Run the full research and concept pass when the visual direction is open. For a change inside a direction the person already approved, use the existing product and its approved screens as the benchmark, and work only on the screens that change and the states that depend on them.

1. **Capture references and write down decisions.** For a new website or a large rebrand, aim for ten real sites that fit the audience and the task. Capture the actual page, keep its URL, and note what works in its layout, type, color and spacing. For native work, use examples from the platform and the product's own screens. Keep the captures with the design work, and record the approved design rules in the project's `DESIGN.md`, creating it for a new design system. Take principles from the references, cite the source, and translate them into the project's own identity. Do not copy a reference.
2. **Compare mock-ups that really differ.** Where the person has not chosen a direction, show three low-fidelity concepts side by side. Give each a different reference and a real difference in hierarchy, composition or interaction. Make them easy to compare, and do not write production UI yet. Build once the person chooses. A direction that already exists or was clearly approved is enough to start.
3. **Scan for generic choices.** Look for a default typeface nobody chose, a purple-gradient hero, glowing buttons, a decorative one-word italic headline, repeated statistic tiles and card grids that could belong to any product. Where the brief or the existing design does not support a pattern, replace it with something that serves the audience and the action. Approved brand tokens and components that fit the task come first.
4. **Get a fresh critique of the real render.** Give a fresh session, one that did not build the design, the actual render, recording or frames, the user's goal, and up to three approved comparisons. Leave out your own reasoning and the answer you expect. Ask for the most visible defects first and the three changes that would matter most, and for a 1 to 10 comparison if that helps. Check each finding against the brief, fix the real defects, capture again and confirm the fix in the new render. A score is a prompt for judgment. The evidence and the user's goal decide.
5. **Polish at the sizes and states people use.** On the web, check the changed pages at 375 CSS pixels wide and at a desktop width you support. Check spacing, clipping, wrapping and alignment, and the hover, focus and touch states. For native UI, capture the changed screens at the window and device sizes you support, and try the real buttons, selection, loading and empty states and motion. Respect reduced-motion settings, and keep keyboard and accessibility behavior intact. Reuse the project's components and tokens.

**Deliver proof by default.** Keep the final screenshots or recordings at the sizes you tested, and note the defects you fixed. Show motion in a real recording that includes the trigger, the visible action and the end. For a regression, reproduce it first, then show the real behavior after the fix.

This workflow adapts the five actions in [Prajwal Tomar's design thread](https://x.com/PrajwalTomar_/status/2124865857860059278) to work with approvals, native apps and existing design systems.
