---
description: Prime agent with codebase understanding
argument-hint: [clickup-task-ids]
---

# Prime: Load Project Context

**Input**: $ARGUMENTS

## Objective

Build comprehensive understanding of this codebase by analyzing structure and key files.

## Process

### Step 0: Load External Context (if provided)

The argument is an optional ClickUp task ID or comma-separated list of IDs.

If ClickUp task IDs are provided and ClickUp MCP is available (tools prefixed with `mcp__clickup__`):
1. Fetch each task to get the summary, description, acceptance criteria, and context
2. Use this context to inform your understanding of what work is expected

### Step 1: Analyze the Codebase

1. Read `CLAUDE.md` and `CODEBASE-GUIDE.md` for project conventions
2. Study the feature slice (`src/features/polls/`)
3. Study the app routes (`src/app/`)
4. Check recent commits with `git log --oneline -5`

## Output

Produce a scannable summary of what you learned:

- **Project Purpose**: One sentence
- **Tech Stack**
  - Frontend: framework, UI library, state management
  - Backend: framework, database, validation
- **Data Model**: Core entities
- **Key Patterns**: Database, API, state management patterns
- **Current State**: Recent commits, current branch

Use bullet points. Keep it concise.
