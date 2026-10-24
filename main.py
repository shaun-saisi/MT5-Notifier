"""
Forex AI Agent — Stage 3: Analysis-only mode.
Fetches 3 timeframes for 5 pairs, scores each via Ollama, prints decisions.
NO TRADE PLACEMENT YET.
Run: python main.py
"""

import json
import re

import config
import mt5_client
import ollama_client
import prompt_builder


def parse_json(raw):
    """
    Extract a JSON object from the AI response.
    Handles cases where the model wraps output in markdown fences.
    """
    # Strip ```json ... ``` fences if present
    text = raw.strip()
    fence = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
    if fence:
        text = fence.group(1).strip()

    # Find the first { ... } block
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None

    try:
        return json.loads(text[start:end + 1])
    except json.JSONDecodeError:
        return None


def analyze_symbol(symbol):
    """Fetch data, score via AI, return decision dict or None."""
    mtf = mt5_client.fetch_multi_timeframe(symbol)
    prompt = prompt_builder.build_scoring_prompt(symbol, mtf)
    raw = ollama_client.generate(prompt)
    decision = parse_json(raw)

    if decision is None:
        print(f"  [WARN] Could not parse AI response for {symbol}:")
        print("         " + raw.replace("\n", " ")[:200])
        return None

    return decision


def main():
    print("=" * 60)
    print("Forex AI Agent — Analysis only (no trades placed)")
    print("=" * 60)

    mt5_client.connect()

    results = []
    try:
        for symbol in config.SYMBOLS:
            print(f"\n[{symbol}] Analyzing...")
            try:
                decision = analyze_symbol(symbol)
            except Exception as e:
                print(f"  [ERROR] {e}")
                continue

            if decision is None:
                continue

            results.append(decision)
            print(f"  direction: {decision.get('direction')}")
            print(f"  score:     {decision.get('score')}")
            print(f"  entry:     {decision.get('entry')}")
            print(f"  sl:        {decision.get('sl')}")
            print(f"  tp:        {decision.get('tp')}")
            print(f"  reason:    {decision.get('reason')}")
    finally:
        mt5_client.disconnect()

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    qualified = [
        d for d in results
        if d.get("direction") in ("BUY", "SELL")
        and isinstance(d.get("score"), (int, float))
        and d["score"] >= config.MIN_SCORE
    ]

    if not qualified:
        print(f"No pair reached the {config.MIN_SCORE}-point threshold. No trade.")
    else:
        qualified.sort(key=lambda d: d["score"], reverse=True)
        best = qualified[0]
        print(f"Best setup: {best['symbol']} {best['direction']} "
              f"(score {best['score']})")
        print("  (analysis only — no order placed)")


if __name__ == "__main__":
    main()