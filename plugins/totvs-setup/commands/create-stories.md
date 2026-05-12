---
description: Generate ClickUp tasks from a PRD
argument-hint: <path-to-prd> [--list LIST_ID] [--folder FOLDER_NAME]
---

# Create ClickUp Tasks from PRD

Generate structured user stories/tasks from a Product Requirements Document. When ClickUp MCP is configured, automatically creates the tasks in ClickUp.

**Input**: $ARGUMENTS

---

## Phase 1: LOAD

Read the PRD file provided as input. If no path given, look for:
1. `.agents/PRDs/*.prd.md` files
2. `PRD.md` at project root
3. Ask the user which PRD to use

Extract:
- User stories already defined in the PRD
- Acceptance criteria from success criteria and requirements
- Implementation phases and their deliverables
- Technical constraints and dependencies

Parse optional flags from arguments:
- `--list` or `-l`: ClickUp list ID to create tasks in
- `--folder` or `-f`: Folder name within the space

---

## Phase 2: ANALYZE

### Break Down into Tasks

For each feature or requirement in the PRD:

1. **Create a user story** in the format:
   ```
   As a [user type], I want to [action], so that [benefit]
   ```

2. **Define acceptance criteria** (3-5 per task):
   ```
   Given [context], when [action], then [expected result]
   ```

3. **Estimate complexity**: Small / Medium / Large
   - Small: Single file change, clear implementation
   - Medium: Multiple files, some design decisions
   - Large: Cross-cutting concerns, architecture changes

4. **Identify dependencies** between tasks

### Task Categories

Group tasks by type:
- **Feature**: New functionality
- **Enhancement**: Improvement to existing functionality
- **Bug**: Fix for known issues
- **Technical**: Infrastructure, refactoring, tooling
- **Spike**: Research or investigation needed

---

## Phase 3: STRUCTURE

### For Each Task, Create

```markdown
## [TASK-ID] Task Title

**Type**: Feature | Enhancement | Technical | Spike
**Priority**: Urgent | High | Normal | Low
**Complexity**: Small | Medium | Large
**Phase**: (from PRD implementation phases)
**Tags**: (relevant tags like `frontend`, `backend`, `api`, `database`)

### Description
As a [user type], I want to [action], so that [benefit].

### Acceptance Criteria
- [ ] Given [context], when [action], then [result]
- [ ] Given [context], when [action], then [result]
- [ ] Given [context], when [action], then [result]

### Technical Notes
- Key implementation details
- Files likely to be modified
- Patterns to follow (reference CLAUDE.md or project conventions)

### Dependencies
- Blocked by: [other task IDs]
- Blocks: [other task IDs]
```

### Ordering

Order tasks by:
1. Phase (from PRD implementation phases)
2. Dependencies (blocked tasks come after their blockers)
3. Priority (Urgent/High first within each phase)

---

## Phase 4: VALIDATE

Before output, verify:
- [ ] Every PRD requirement maps to at least one task
- [ ] No task is too large (break down if > 1 day of work)
- [ ] Acceptance criteria are testable and specific
- [ ] Dependencies form a valid DAG (no circular dependencies)
- [ ] Tasks cover the full SDLC: types, validation, services, routes, UI, tests
- [ ] Each task can be independently reviewed and merged

---

## Phase 5: OUTPUT

Create the directory if it doesn't exist: `mkdir -p .agents/stories`

Save the tasks to `.agents/stories/` directory as a markdown file.

---

## Phase 6: CLICKUP INTEGRATION (when MCP is available)

**Check if the ClickUp MCP server is available.** Look for tools prefixed with `mcp__clickup__`. If available, offer to push tasks directly to ClickUp.

### If ClickUp MCP IS available:

1. **Ask the user** before creating tasks:
   ```
   I've generated {count} tasks. Would you like me to create these in ClickUp?
   - List: {LIST_ID} (or ask if not provided via --list)
   ```

2. **If user confirms**, create tasks in ClickUp for each story.

3. **Report created tasks**:
   ```markdown
   ## ClickUp Tasks Created

   | ID | Title | Type | Priority |
   |----|-------|------|----------|
   | abc123 | Task title | Feature | High |
   | def456 | Task title | Technical | Normal |
   ...
   ```

### If ClickUp MCP is NOT available:

Output the tasks as markdown only and note:
```
ClickUp MCP is not configured. To push tasks to ClickUp automatically:
1. Run: claude mcp add clickup https://mcp.clickup.com/mcp
2. Authenticate via OAuth when prompted
3. Re-run this command
```

---

## Tips

- Keep tasks small enough to complete in 1-2 days
- Acceptance criteria should be verifiable without asking the author
- Technical tasks need acceptance criteria too (build passes, tests pass, etc.)
- Reference the PRD section for each task so reviewers can trace back
