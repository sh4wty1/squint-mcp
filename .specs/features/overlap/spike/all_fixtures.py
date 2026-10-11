import asyncio, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import spike

FIX = Path(__file__).parents[4] / "tests" / "fixtures"
SKIP = {"polling.html", "polling-briefly.html", "visit.html"}

async def main():
    for f in sorted(FIX.glob("*.html")):
        if f.name in SKIP:
            continue
        for vp in ((1440, 900), (390, 844)):
            try:
                texts, stats = await asyncio.wait_for(spike.run(f.as_uri(), vp, verbose=False), 60)
            except Exception as e:
                print(f"{f.name} {vp}: ERROR {type(e).__name__} {str(e)[:120]}")
                continue
            found = [(t["sel"], spike.verdict(t)) for t in texts if spike.verdict(t)]
            took = sum(stats.times.values())
            print(f"{f.name} {vp[0]}: {stats.size} {took:.2f}s texts {stats.texts} cand {stats.candidates} groups {stats.groups} shots {stats.shots} hits {stats.hit_tests} -> {found}")

asyncio.run(main())
