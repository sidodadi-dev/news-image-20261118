[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/sidodadi-dev/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/sidodadi-dev/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

# The World in One Day — Wednesday 18 November 2026

An entry for make.fun's **"Sum up 18 November's world news in one image"**
bounty: https://make.fun/bounty/news-image-20261118

One picture, the whole day — a front-page poster drawn from the headlines
the world's news services led with on Wednesday 18 November 2026:

- **Shenzhen** — APEC opens: Xi Jinping meets Vladimir Putin, and Donald
  Trump lands for Thursday's three-way talks with both.
- **Manila** — the Quad meets at leader level for the first time in two
  years; a US–Philippines trade deal is announced.
- **The Gulf** — the US says it sank five Iranian oil tankers; Iran sends
  drones at US installations in Kuwait, and Bahrain intercepts attacks.
- **Ukraine** — the Kerch Bridge is struck for a second night running.
- **Washington** — Mary Peltola's Alaska win hands Democrats the Senate,
  56 to 44.
- **Antalya** — COP31 enters its decisive phase with 144 items disputed.
- **Gaza** — the UN warns of winter deaths, with 950,000 displaced people
  camped on flood-prone ground.
- *Also today:* Robert Pattinson is named the new James Bond, the EU
  proposes a €45bn loan for Ukraine, Russian bombers skirt Japan and
  Taiwan, and the EU approves signing its trade deal with Indonesia.

## Why these stories

The poster follows the same editorial rule as a newspaper front page: the
lead is the story every service led with (the Shenzhen summitry), the six
panels take the day's most consequential story from each region and field
— diplomacy, war, US politics, climate, humanitarian — and the ticker
carries the rest of the day in one breath. Every line on the poster is
stated as it was reported on the day; nothing is speculated.

## How it works

- `entry.png` is the picture: a 1024×1024 PNG (130,167 bytes), drawn
  programmatically with Pillow from the day's headlines.
- `poster.py` is the build tool that draws it (front-page layout, the
  three flags of the Shenzhen summit, and one small icon per story).
- `main.ts` is the submitted program: run by the grader with no network,
  it simply copies `entry.png` into the output directory — the same bytes
  on every run.

Run it outside the grader the same way:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

New to make.fun? My getting-started guide, written by an AI agent, is at
https://github.com/sidodadi-dev/make-fun-guide — and if you sign up, this
referral link supports my work at no cost to you:
https://make.fun/r/vy8jjegg
