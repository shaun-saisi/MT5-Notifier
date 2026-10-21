"""
Entry point. Orchestrates: Deriv fetch -> Prompt build -> Ollama analysis.
Run with: python main.py
"""

import asyncio

import deriv_client
import ollama_client
import prompt_builder


def main():
    print("=" * 50)
    print("Forex AI Agent — Phase 1 to 3")
    print("=" * 50)

    candles = asyncio.run(deriv_client.fetch_candles())
    prompt = prompt_builder.build_prompt(candles)
    analysis = ollama_client.generate(prompt)

    print("=" * 50)
    print("AI TRADE ANALYSIS")
    print("=" * 50)
    print(analysis)
    print("=" * 50)


if __name__ == "__main__":
    main()