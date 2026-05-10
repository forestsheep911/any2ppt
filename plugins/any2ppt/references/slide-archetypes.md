# Slide Archetypes

Use archetypes to keep slides structured and presentable.

## Core Archetypes

- Cover: title, subtitle, source, visual thesis.
- Thesis: central argument with 2-3 supporting pillars.
- Timeline: dated sequence or historical progression.
- Comparison: two or more sides contrasted across shared dimensions.
- Evidence cards: several source-backed observations arranged as cards.
- Process: step-by-step flow, causal chain, or operating model.
- Map: geographic or domain layout when location matters.
- Data chart: quantitative claim with chart and takeaway.
- Tension: competing forces, contradictions, or trade-offs.
- Closing: final synthesis and memorable conclusion.

## Selection Rules

- Use timelines for chronology, not for unrelated bullet lists.
- Use comparison when the audience must see contrast quickly.
- Use evidence cards when several details support one claim.
- Use process diagrams for causality or workflow.
- Use a thesis slide early when the deck needs argumentative framing.
- Avoid using the same archetype too many times in a row unless repetition clarifies the deck.

## Naming and Validation

`slide-storyboarder` writes the chosen archetype on each slide as `**Archetype**: <name>`. Use one of the names in the "Core Archetypes" list (case-insensitive). Parenthetical clarifications are fine — `Thesis (four pillars)` and `Comparison (two columns)` both validate as `thesis` and `comparison` respectively.

The `any2ppt-dev review` tool warns (`SLIDE-ARCHETYPE-UNKNOWN`) when an archetype name is not in the list above. If a new archetype is genuinely needed, add it here first, otherwise reshape the slide to fit an existing one.

## Per-Archetype Support Point Bands

The `any2ppt-dev review` tool checks the number of support points per slide. The bands match the storyboarder skill (`SKILL.md`, "Support Point Counts by Archetype"):

- `cover`, `closing`: not constrained.
- `process`: 2-7.
- `evidence cards`: 2-10.
- `timeline`: 2-10.
- `thesis`: 2-6.
- All other archetypes (comparison, tension, map, data chart): 2-4.
