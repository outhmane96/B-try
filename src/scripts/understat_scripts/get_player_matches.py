import asyncio
import json
import aiohttp
from understat import Understat
from pathlib import Path

async def main():
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        # Using **kwargs
        player_matches = await understat.get_player_matches(
        1250,
        date= "2024-12-29")
        # Construct the absolute path to the JSON file
        base_dir = Path(__file__).resolve().parent.parent.parent.parent / "data/explore_understat"
        file_path = base_dir / "player_match_understat.json"
        
        # Ensure the directory exists before proceeding
        if not base_dir.exists():
            raise FileNotFoundError(f"Directory does not exist: {base_dir}")
        
        # Write the player data to the JSON file
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(player_matches, f, ensure_ascii=False, indent=4)
        
        print(f"Player data saved to {file_path}")
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
