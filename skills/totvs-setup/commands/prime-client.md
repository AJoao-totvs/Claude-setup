---
description: Prime agent with client/frontend codebase understanding
argument-hint: [clickup-task-ids]
---

# Prime Client: Load Frontend Context

**Input**: $ARGUMENTS

## Objective

Build comprehensive understanding of the client codebase by analyzing structure and key files.

## Process

### Step 0: Load External Context (if provided)

The argument is an optional ClickUp task ID or comma-separated list of IDs.

If ClickUp task IDs are provided and ClickUp MCP is available (tools prefixed with `mcp__clickup__`):
1. Fetch each task to get the summary, description, acceptance criteria, and context
2. Use this context to inform your understanding of what work is expected

### Step 1: Analyze the Codebase

1. Study the app routes (`src/app/`) — pages, layouts, loading/error boundaries
2. Study the feature components (`src/features/polls/components/`)
3. Study the shared UI primitives (`src/components/ui/`)
4. Check `package.json` for frontend dependencies

## Output

Produce a scannable summary of what you learned:

- **Purpose**: What the UI does
- **Tech Stack**: Next.js App Router, shadcn/ui, Tailwind 4
- **Components**: Key components and their responsibilities
- **Data Flow**: Server Components fetch data directly; Client Components use Server Actions for mutations
- **Patterns**: Server vs Client component split, how forms use Server Actions with `useActionState`

Use bullet points. Keep it concise.
