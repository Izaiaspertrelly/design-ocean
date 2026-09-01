---
name: PertrellyUI
description: >-
  Use this when building web UI, pages, components, posters, or apps that must
  look designed rather than generic AI. Craft, type, color, space, motion,
  interaction, and UX writing.
---
# PertrellyUI: Frontend Design

This skill guides the creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

## Context Gathering Protocol

Design skills produce generic output without project context. You MUST have confirmed design context before doing any design work.

**Required context** — every design skill needs at minimum:
- **Target audience**: Who uses this product and in what context?
- **Use cases**: What jobs are they trying to get done?
- **Brand personality/tone**: How should the interface feel?

**CRITICAL**: You cannot infer this context by reading the codebase. Code tells you what was built, not who it's for or what it should feel like. Only the creator can provide this context.

**Gathering order:**
1. **Check current instructions**: If your loaded instructions already contain a **Design Context** section, proceed immediately.
2. **Check `.pertrellyui.md`**: If not in instructions, read `.pertrellyui.md` from the project root. If it exists and contains the required context, proceed.
3. **Ask the user**: If neither source has context, you MUST ask the user to clarify the target audience, use cases, and brand personality before proceeding.

## Design Direction

Commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work. The key is intentionality, not intensity.

Then implement working code that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

### Typography
Consult `references/typography.md` for scales, pairing, and loading strategies.

Choose fonts that are beautiful, unique, and interesting. Pair a distinctive display font with a refined body font.

**DO**: Use a modular type scale with fluid sizing (clamp)
**DO**: Vary font weights and sizes to create clear visual hierarchy
**DON'T**: Use overused fonts (Inter, Roboto, Arial, Open Sans, system defaults)
**DON'T**: Use monospace typography as lazy shorthand for "technical/developer" vibes

### Color & Theme
Consult `references/color-and-contrast.md` for OKLCH, palettes, and dark mode.

Commit to a cohesive palette. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.

**DO**: Use modern CSS color functions (oklch, color-mix, light-dark) for perceptually uniform, maintainable palettes
**DO**: Tint your neutrals toward your brand hue, even a subtle hint creates subconscious cohesion
**DON'T**: Use pure black (`#000`) or pure white (`#fff`) as default; always tint unless a locked brand token says otherwise
**DON'T**: Use the generic AI color palette: cyan-on-dark, purple-to-blue gradients, neon accents on dark backgrounds

### Layout & Space
Consult `references/spatial-design.md` for grids, rhythm, and container queries.

**DO**: Create visual rhythm through varied spacing, tight groupings, generous separations
**DO**: Use fluid spacing with clamp() that breathes on larger screens
**DON'T**: Wrap everything in cards
**DON'T**: Use identical card grids (icon + heading + text, repeated)

### Visual Details
**DO**: Use intentional, purposeful decorative elements that reinforce brand
**DON'T**: Use glassmorphism everywhere
**DON'T**: Use rounded elements with a thick colored border on one side as a lazy accent

### Motion
Consult `references/motion-design.md` for timing, easing, and reduced motion.

**DO**: Use motion to convey state changes (entrances, exits, feedback)
**DO**: Use exponential easing (ease-out-quart/quint/expo) for natural deceleration
**DON'T**: Animate layout properties (width, height, padding, margin). Use transform and opacity only

### Interaction
Consult `references/interaction-design.md` for forms, focus, and loading patterns.

**DO**: Use progressive disclosure. Start simple, reveal sophistication through interaction
**DO**: Design empty states that teach the interface
**DON'T**: Make every button primary. Hierarchy matters

### Responsive
Consult `references/responsive-design.md` for mobile-first, fluid design, and container queries.

**DO**: Use container queries (`@container`) for component-level responsiveness
**DO**: Adapt the interface for different contexts. Don't just shrink it
**DON'T**: Hide critical functionality on mobile

### UX Writing
Consult `references/ux-writing.md` for labels, errors, and empty states.

**DO**: Make every word earn its place
**DON'T**: Repeat information users can already see

## The AI Slop Test

If you showed this interface to someone and said "AI made this," would they believe you immediately? If yes, that's the problem.

A distinctive interface should make someone ask "how was this made?" not "which AI made this?"

## Implementation Principles

Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code. Minimalist designs need restraint and precision.

Interpret creatively. No design should be the same. NEVER converge on common choices across generations.

On branded work, the project's brand tokens, type, and logo rules override the generic DON'Ts in this skill when they conflict.
