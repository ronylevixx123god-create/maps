ASTRO-INSPIRED FLOATING SPACEPORT — 300 x 300

Original generated build inspired by the supplied screenshot; not an exact replica.
Minecraft Java 1.8.8 / classic MCEdit Alpha .schematic for WorldEdit 6.
Dimensions: 300 wide x 300 long x 96 high. Approximately 550,000 non-air blocks.
Flat octagonal deck within a 300 x 300 footprint; clipped corners.
Four accessible sci-fi buildings, central plaza, pedestals for NPCs/crates,
observation pylons, decorative shuttles, seating and floating asteroids.
No entities, NPCs, functional crates, protection regions or plugins included.
The screenshot's galaxy sky requires a separate client resource pack.

IMPORT ON YOUR TEST SERVER FIRST
1. Back up the world. Stop the server before copying files if necessary.
2. Put Astro-Inspired-Spaceport-300.schematic into plugins/WorldEdit/schematics/.
3. Start the server. Join in creative mode with flight and WorldEdit permission.
4. Go to a clear area in the sky, ideally in a void world. Stand/fly at the
   desired CENTER of the spawn at Y=100. The deck will be one block below you.
   The structure extends about 150 blocks in each horizontal direction, with
   the tallest objects reaching roughly 85 blocks above your position.
5. Load using WorldEdit 6:
   //schematic load mcedit Astro-Inspired-Spaceport-300
6. Paste non-air blocks:
   //paste -a
   This is a large paste; the server may pause. Wait and do not repeat it.
7. Inspect before opening to players. Use //undo if you need to remove the paste.
8. At the safe central plaza set the world's spawn using /setworldspawn.
   If your server uses Essentials, configure /setspawn as well, as appropriate.
9. Add your own NPCs, crates, region protection and any desired PvP exit.
   Side edges are not fully player-proof; protect the spawn and configure
   void-fall handling before public use. No terrain or warzone is included.

The schematic does not create a world by itself. It is a build to import into
an existing world. Pasting over terrain does not remove that terrain with -a.
Do not paste over your current spawn or live server without a backup.

VALIDATION
Gzip and NBT parsed independently; dimensions, array sizes, legacy block IDs,
spawn clearance, and non-air count checked. Preview rendered from actual blocks.
Not loaded in Minecraft or WorldEdit in this environment. In-game lighting,
visual appearance and server performance still need testing.

INCLUDED
- Astro-Inspired-Spaceport-300.schematic
- Top-Down-Preview.png (actual block-derived top view)
- build_spawn.py (editable deterministic generator; needs Python, numpy, Pillow)
- README.txt
