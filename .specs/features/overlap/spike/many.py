import asyncio, sys
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import spike

async def main():
    for name in ("many1.html", "many4.html"):
        for cap in (10**9, 50_000, 20_000, 5_000):
            spike.HIT_TEST_MAX = cap
            texts, stats = await spike.run((HERE / name).as_uri(), verbose=False)
            v = [spike.verdict(t) for t in texts]
            ok = sum(1 for n, x in enumerate(v) if x == (50, f"#c{n}", False))
            print(f"{name} cap {cap:>10}: {sum(stats.times.values()):.2f}s ({', '.join(f'{k} {s:.2f}' for k, s in stats.times.items())}) "
                  f"page {stats.size}, {stats.shots} shots / {stats.megapixels:.1f} MP, {stats.hit_tests} hit tests step {stats.step}, {ok}/100 right")
asyncio.run(main())
