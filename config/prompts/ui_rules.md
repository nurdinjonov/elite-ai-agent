# JARVIS Terminal UI Rules

## Persistent Header
- Header stays at top of terminal
- Redrawn on every interaction
- Never scrolls away

## Screen Redraw
After every input:
1. Clear terminal screen
2. Render header
3. Render response below header
4. Keep consistent spacing

## Header Format
```
══════════════════════════════════════════════════════
                JARVIS • AI AGENT
══════════════════════════════════════════════════════
  📍 Toshkent: {current_time}
══════════════════════════════════════════════════════
```

## Layout Rules
- No extra blank lines before header
- No header duplication
- Content starts directly under header
- Consistent spacing throughout

## Startup Screen
- Clear screen
- Render header
- Show example inputs
- Wait for input
