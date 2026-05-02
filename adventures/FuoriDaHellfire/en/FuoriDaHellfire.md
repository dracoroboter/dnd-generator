> ⚠️ Auto-translated from Italian. The Italian version is the source of truth.

# Fuori da Hellfire

## Lore

Greyhawkins is a port city where the bizarre is the norm — but nobody expected what happened at the Oakshore docks. A series of murders, corrupted rats everywhere, and behind it all an elf with a too-wide smile and a melody that got inside your head: **Korex**.

The party unmasked him, defeated his rats, and put him to flight. Korex escaped into the sewers beneath the docks — sewers nobody knew existed. The Oakshore Guard doesn't have the resources to pursue him underground. It's up to the party.

## Introduction

> The rain beats down on the Oakshore docks. Sheriff Udo Hutchinson looks at you with a mix of gratitude and impatience. "He escaped into the sewers. The old ones, under the east pier — we didn't even know they were still open." He checks the sword at his hip. "I'm coming with you. Bring him up. Alive or dead, I don't care. Just make sure he doesn't come back."

The PCs have just finished the fight with the rats. Korex fled through a grate in the floor of the warehouse at the docks. Udo, having just returned to Oakshore from a personal trip, found the district in chaos and has no intention of sending people into the sewers without going himself.

## General Plot

- **Act 1 — The Descent**: the PCs enter the sewers pursuing Korex. Dark tunnels, traps left by Korex to slow them down, servants left behind to cover his escape. The environment becomes progressively stranger — the sewers are older and larger than they should be.
- **Act 2 — The Lair**: the PCs reach Korex's hideout. Final confrontation with the bard and his last defenders. Korex can be captured alive (if the PCs resist the charm) or killed.
- **Act 3 — The Discovery**: with the Korex matter resolved, the PCs find the Anello del Virtuoso on his finger — a cursed artifact containing the soul of an ancient bard. Whoever touches it risks putting it on. Whoever wears it gains power, but begins to be possessed. If no PC touches it, a guard puts it on and the problem explodes anyway.

## DM Tips

- **Tone**: maintain the camp from the starter kit. Korex is theatrical, the rats are grotesque, the sewers are over-the-top. But the final cliffhanger must have a shift in register — the moment when the comedy stops and the players realize there's something serious going on.
- **Korex in combat**: he doesn't fight fair. He charms, runs, sends servants ahead. If cornered, he begs for mercy — and lies.
- **Capture vs kill**: both options are valid. If captured alive, Korex can provide information (a mix of truth and lies). If killed, the information can be found in his notes in the lair.
- **The cliffhanger**: after the milestone, the Anello del Virtuoso comes into play. The ring was on Korex's finger — it's the source of his power. It contains the soul of an ancient bard who wants to return to life. Three-tier mechanic: passive attraction → touch (WIS save DC 20 or forced wearing) → progressive possession. If no PC touches it, an NPC guard puts it on and attacks. Details in `DiscussioneNarrativa.md`.

**Recommended difficulty:** 3 PCs at level 3 + Udo Hutchinson + Fin Ditasvelte (NPC companion)
**Scalability:** for 4+ PCs, Udo stays behind to watch the entrance and Fin doesn't join (the charm hasn't broken yet). For 2 PCs, keep both companions.

## Main NPCs

Full sheets in `characters/`.

- **Udo Hutchinson** — sheriff of Oakshore, veteran. Joins the PCs at the sewer entrance. Party tank.
- **Korex** — CE elf bard, antagonist. Musical charmer, manipulator, coward.
- **Fin Ditasvelte** — CN halfling rogue, formerly charmed by Korex. Emerges from the sewer confused and furious, joins the PCs for revenge. Ring bearer (scenario B).
- **Jason Accordion** — TN human bard, soul within the Anello del Virtuoso. Saga villain.

Charmed thug stat block: see `MON_TeppistaCharmato.md`.

## Adventure Structure

| # | name | type | file |
|---|------|------|------|
| 1 | Discesa nelle Fogne | dungeon / exploration | [01_DiscesaNelleFogne/DiscesaNelleFogne.md](01_DiscesaNelleFogne/DiscesaNelleFogne.md) |
| 2 | Tana di Korex | dungeon / final encounter | [02_TanaDiKorex/TanaDiKorex.md](02_TanaDiKorex/TanaDiKorex.md) |

## Future Hooks

- The Anello del Virtuoso → lv4-6 saga: who was the bard in the ring? Race against time to remove it before total possession
- Korex (if captured alive) → source of unreliable information for future adventures
- The ancient sewers → why are they so large? Who built them? The hidden passage in the lair leads deeper
- The bard in the ring has his own plan — he's not an ally

---

## Appendix — Anello del Virtuoso Cheat Sheet

Quick reference for the DM. Full details in `NPC_JasonAccordion.md` and `DiscussioneNarrativa.md`.

**Appearance**: blackened silver ring, musical ouroboros engraving. It's on Korex's finger.

### Activation — 3 Tiers

1. **Attraction** (passive, narrative): when Korex falls, anyone who sees the ring feels curiosity. No roll.
2. **Touch**: whoever touches the ring → WIS save DC 20. Failure = compelled to wear it. Success = manages to set it down, attraction remains.
3. **Worn**: the ring tightens, cannot be removed. Automatic attunement.

### Immediate Effects

| benefits | drawbacks |
|----------|-----------|
| +2 to one ability score (by class) | The ring cannot be removed |
| 1 bard spell 1/day without a slot | Nightmares the first night (no long rest) |
| Advantage on saves against charm | Constant cold in the hand |
| | Vulnerability to psychic damage |

### Possession — Grip Tracking

Each use of the 1/day spell → roll **d8**.
- **2-8**: it works.
- **1**: fails + psychic wave 1d4+grip to everyone within 10 ft + grip +1.

| grip | narrative | mechanical |
|------|-----------|------------|
| 0 | Cold, nightmares | Psychic vulnerability |
| 1-2 | Jason's tics, rare whispers | Wave 1d4+1/+2 |
| 3-4 | Jason speaks often, foreign memories | Wave 1d4+3/+4, WIS save DC 14 under stress |
| 5-6 | Jason takes control for 1d4 rounds | Wave 1d4+5/+6, WIS save DC 15 |
| 7+ | Permanent control attempt | Wave 1d4+7+, WIS save DC 16+ |

**Reducing grip**: successful WIS save vs Jason (−1), *Lesser Restoration* (−1), *Greater Restoration* (−2).

### Removal

*Remove Curse* loosens the ring for 1d4 hours, then it returns. Permanent removal: find Jason's skeleton + burn it with salt + a wizard who knows the original ritual.

### Plan A vs Plan B

- **A** (PC touches): progressive possession of the PC.
- **B variant** (Fin touches): WIS 10, Jason possesses him easily.
- **B base** (nobody touches): guard puts it on → attack → PCs defeat them → the ring remains.

**"Free"** = new host without defenses, not escape from the ring. Korex knew how to resist it.
