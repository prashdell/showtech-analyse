# Showtech Analyse Project Rules

## Workspace Boundaries

- **Primary Workspace**: `C:\Users\SERIAL-REDACTED-SERIAL-REDACTED\SERIAL-REDACTED-SERIAL-REDACTED\Documents\AI\Devin\showtech_analyse`
- **Strict Enforcement**: All project files MUST be created within this workspace
- **No External Files**: Do not create files outside the project workspace unless explicitly requested

## File Creation Rules

1. **Code Files**: All Python scripts, analyzers, and utilities go in the root workspace
2. **Skills**: Project-specific skills go in `./skills/` directory
3. **Configuration**: All config files go in `./.devin/` directory
4. **Documentation**: Markdown files go in root or `./docs/` if created
5. **Data**: Analysis results and data files go in root workspace
6. **Logs**: Log files go in `./.devin/logs/` directory

## Skill Management

- **Local Skills**: Skills are stored locally in `./skills/` for this project
- **No Global Sync**: Skills are NOT synced to global `~/.devin/skills/` directory
- **Project Isolation**: Skills remain project-specific and don't affect global configuration

## Enforcement

- Before creating any file, verify the path is within the workspace
- Use relative paths from workspace root whenever possible
- Confirm workspace boundaries before making changes
- If asked to create files outside workspace, request explicit confirmation