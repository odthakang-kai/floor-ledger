# Floor Ledger

Personal sales scoreboard for an appliance associate: multi-item orders with order numbers, protection plan / install / haul-away attach rates, store card applications, leads with follow-ups, one-tap packdowns, hours, and weekly goals.

- **App (add to home screen, works offline):** https://odthakang-kai.github.io/floor-ledger/
- Everything you log is stored **on your phone only** (browser localStorage). Nothing is sent anywhere. Use **History → Save backup** now and then, and **Restore** to bring a backup onto a new phone.
- Icons: `python tools/make_icons.py` (standard library only).
- After changing the page, bump `VERSION` in `sw.js` only if you changed icons or the manifest; the page itself updates on the next online open.

Not affiliated with or endorsed by any retailer.
