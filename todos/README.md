# Daily TODO Reminders

Hub page for the `todos/` directory. Hui asks Claude (in any session) things like "remind me tomorrow to do X"; the local `daily-todo` skill files each request into the file for its **due date**, and a cloud routine (`daily-todo-reminder`) delivers that day's list every morning at 08:00 America/New_York as a phone push notification (plus an email to hsun26@ncsu.edu once a Gmail connector is attached to the routine).

## File format

One file per due date, named `todos/YYYY-MM-DD.md` (date in America/New_York):

```markdown
# TODO — 2026-10-11

- [ ] Email the advisor the revised EMSE response letter _(added 2026-10-10 19:20 ET)_
- [x] Submit the TRC follow-up _(added 2026-10-10 21:05 ET)_
```

- `- [ ]` = open, `- [x]` = done. Only open items are delivered.
- Items are written in English (repo-wide language rule in [CLAUDE.md](../CLAUDE.md)), translated from the original request if needed.
- The routine only reads the repo; it never writes to it. Marking items done happens locally through the skill.

These files are operational state, not knowledge pages: they are not registered individually in [index.md](../index.md), and adding/completing a TODO does not append to [log.md](../log.md).
