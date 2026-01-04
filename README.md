# rps-plus-adk
Google ADK
# AI Referee – Rock–Paper–Scissors–Plus

This project implements a **conversational AI game referee** for a modified
Rock–Paper–Scissors game (“RPS-Plus”) using **Google ADK**.  
The system enforces strict rules, tracks state deterministically, and runs in
a simple CLI-based conversational loop.

---

## Game Rules
- Best of **3 rounds**
- Valid moves: `rock`, `paper`, `scissors`, `bomb`
- Each player may use **bomb only once per game**
- `bomb` beats rock, paper, and scissors
- `bomb` vs `bomb` results in a draw
- Invalid input **wastes the round**

---

## State Model
Game state is stored in a **Python dictionary**, not in prompts:

```python
{
  "round": 1,
  "max_rounds": 3,
  "user_score": 0,
  "bot_score": 0,
  "user_used_bomb": False,
  "bot_used_bomb": False
}
