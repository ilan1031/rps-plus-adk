"""
AI Referee – Rock–Paper–Scissors–Plus
Google ADK compliant (current PyPI version)
CLI-based, deterministic, error-free
"""

import random
from google.adk import Agent, tools

# ==================================================
# GAME STATE (Single Source of Truth)
# ==================================================

game_state = {
    "round": 1,
    "max_rounds": 3,
    "user_score": 0,
    "bot_score": 0,
    "user_used_bomb": False,
    "bot_used_bomb": False,
}

# ==================================================
# GAME LOGIC (Pure Python)
# ==================================================

def validate_move(move: str) -> dict:
    """Validate user move and bomb usage."""
    move = move.strip().lower()
    valid_moves = ["rock", "paper", "scissors", "bomb"]

    if move not in valid_moves:
        return {"valid": False, "reason": "Invalid move"}

    if move == "bomb" and game_state["user_used_bomb"]:
        return {"valid": False, "reason": "Bomb already used"}

    return {"valid": True, "move": move}


def resolve_round(user_move: str, bot_move: str) -> dict:
    """Resolve winner using RPS-Plus rules."""
    if user_move == bot_move:
        return {"winner": "draw", "reason": "Both chose the same move"}

    if user_move == "bomb" and bot_move != "bomb":
        return {"winner": "user", "reason": "Bomb beats all"}

    if bot_move == "bomb" and user_move != "bomb":
        return {"winner": "bot", "reason": "Bomb beats all"}

    rules = {
        "rock": "scissors",
        "scissors": "paper",
        "paper": "rock",
    }

    if rules[user_move] == bot_move:
        return {"winner": "user", "reason": f"{user_move} beats {bot_move}"}

    return {"winner": "bot", "reason": f"{bot_move} beats {user_move}"}


def update_game_state(user_move: str, bot_move: str, winner: str) -> dict:
    """Update scores, round, and bomb usage."""
    if user_move == "bomb":
        game_state["user_used_bomb"] = True
    if bot_move == "bomb":
        game_state["bot_used_bomb"] = True

    if winner == "user":
        game_state["user_score"] += 1
    elif winner == "bot":
        game_state["bot_score"] += 1

    game_state["round"] += 1
    return game_state

# ==================================================
# ADK TOOLS (Correct for current google-adk)
# ==================================================

validate_move_tool = tools.FunctionTool(validate_move)
resolve_round_tool = tools.FunctionTool(resolve_round)
update_game_state_tool = tools.FunctionTool(update_game_state)

# ==================================================
# ADK AGENT (NO INSTRUCTIONS – REQUIRED)
# ==================================================

referee_agent = Agent(
    name="rps_plus_referee",
    tools=[
        validate_move_tool,
        resolve_round_tool,
        update_game_state_tool,
    ],
)

# ==================================================
# CLI GAME LOOP
# ==================================================

def print_rules():
    print("""
🎮 Rock–Paper–Scissors–Plus
Rules:
- Best of 3 rounds
- Moves: rock, paper, scissors, bomb
- Bomb can be used once per player
- Bomb beats all; bomb vs bomb is draw
- Invalid input wastes the round
""")

def main():
    print_rules()

    while game_state["round"] <= game_state["max_rounds"]:
        print(f"\n🔢 Round {game_state['round']}")
        user_input = input("Your move: ")

        # Tool: validate
        validation = validate_move(user_input)

        # Bot move
        bot_choices = (
            ["rock", "paper", "scissors"]
            if game_state["bot_used_bomb"]
            else ["rock", "paper", "scissors", "bomb"]
        )
        bot_move = random.choice(bot_choices)

        if not validation["valid"]:
            print(f"❌ Invalid: {validation['reason']}")
            print(f"🤖 Bot: {bot_move}")
            print("➡️ Bot wins this round")
            update_game_state("invalid", bot_move, "bot")
            continue

        user_move = validation["move"]

        # Tool: resolve
        result = resolve_round(user_move, bot_move)

        # Tool: update state
        update_game_state(user_move, bot_move, result["winner"])

        print(f"👤 You:  {user_move}")
        print(f"🤖 Bot: {bot_move}")
        print(f"🏆 Winner: {result['winner'].upper()}")
        print(f"📌 Reason: {result['reason']}")
        print(
            f"📊 Score → You {game_state['user_score']} : "
            f"{game_state['bot_score']} Bot"
        )

    print("\n🏁 GAME OVER")
    if game_state["user_score"] > game_state["bot_score"]:
        print("🎉 Final Result: You win!")
    elif game_state["bot_score"] > game_state["user_score"]:
        print("🤖 Final Result: Bot wins!")
    else:
        print("🤝 Final Result: Draw!")


if __name__ == "__main__":
    main()
