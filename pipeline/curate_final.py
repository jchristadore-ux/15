#!/usr/bin/env python3
"""
FINAL CURATION — "15 YEARS OF US"

Takes the Phase 1 annotated archive (analysis/ARCHIVE_INVENTORY.csv) and the
locked edit decision list below, and emits the production deliverables:

    final/FINAL_PHOTO_MANIFEST.csv
    final/FINAL_PHOTO_MANIFEST.json
    final/CANVA_PRODUCTION_MANIFEST.csv
    final/FINAL_HERO_CANDIDATES.csv

The archive is read-only. Nothing here touches Google Drive.

Timeline used (verified by the client, not inferred):
    2002-03-15  relationship begins            -> 24 years together
    2011-08-13  married                        -> 15 years married
    2013-10-30  first daughter born
    2016-11-01  second daughter born
    2020-09     third daughter born

Frames dated 2000-2001 predate the official start of the relationship. They are
used deliberately: he was already in her life before it was "us".
"""

import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
INVENTORY = os.path.join(ROOT, "analysis", "ARCHIVE_INVENTORY.csv")
OUTDIR = os.path.join(ROOT, "final")

CHAPTERS = {
    1: "CHAPTER 1 - THE BEGINNING OF US",
    2: "CHAPTER 2 - JUST THE TWO OF US",
    3: "CHAPTER 3 - THEN EVERYTHING CHANGED",
    4: "CHAPTER 4 - THEN THERE WERE FIVE",
    5: "CHAPTER 5 - THE CHAOS",
    6: "CHAPTER 6 - THE LIFE WE BUILT",
    7: "CHAPTER 7 - STILL US",
}

# Voiceover, segmented. Text is the client's own, cut into placement blocks.
VOICEOVER = {
    "VO-1": "I spent a lot of time looking through these pictures, and I realized something.",
    "VO-2": "I wasn't really looking at pictures of our wedding. Or pictures of vacations. "
            "Or pictures of the kids. I was looking at my life.",
    "VO-3": "Twenty-four years together. Fifteen years married.",
    "VO-4": "And somehow, you're still the person I want sitting next to me at the end of every day.",
    "VO-5": "We've changed. A lot.",
    "VO-6": "Life hasn't always gone exactly the way we thought it would.",
    "VO-7": "We've had crazy years, hard years, really good years, and a whole lot of years "
            "where we were just trying to keep up with everything.",
    "VO-8": "But when I look at all of these pictures, I wouldn't change any of it. "
            "Because all of it led us here.",
    "VO-9": "To this family. To these three amazing girls. To the life we built together.",
    "VO-10": "And to you.",
    "VO-11": "I don't know what the next fifteen years are going to look like. "
             "But I know I want them. With you.",
    "VO-12": "Happy anniversary. I love you. And if I had to do it all over again... "
             "I'd still choose you.",
    "-": "",
}

# ---------------------------------------------------------------------------
# THE EDIT
#
# (unique_id, chapter, seconds, hero, on_screen_text, vo_cue, transition, reason)
#
# vo_cue is the VO segment that STARTS on this frame ("-" = VO continues or is
# silent). on_screen_text is text burned over the photograph itself; full-screen
# black cards are held separately in TEXT_CARDS below.
# ---------------------------------------------------------------------------

EDIT = [
    # -- CHAPTER 1 -----------------------------------------------------------
    ("P005", 1, 10.0, True,  "", "-", "FADE_FROM_BLACK",
     "The opening frame. She is seventeen, in her lacrosse uniform, stick in hand, and he has "
     "turned up to watch her game. It is the earliest hard-dated photograph of the two of them "
     "and it plants the lacrosse thread that pays off in Chapter 6. Hold it in silence."),
    ("P004", 1, 4.0, False, "", "-", "CUT",
     "Same day, same roll. Her number 11 fills the frame and he is pulling a face at her "
     "mid-conversation. Completely unposed - establishes the register of the whole film."),
    ("P011", 1, 6.0, True,  "", "VO-1", "SLOW_DISSOLVE",
     "The only formal-dress portrait of them as teenagers, hard-dated by the print stamp. "
     "Blue gown, borrowed-looking suit, both of them impossibly young. This is where the "
     "voiceover starts."),
    ("P006", 1, 3.5, False, "", "-", "CROSSFADE",
     "Him still in the letterman jacket, arms around her in someone's living room. Ties the "
     "high-school era together visually."),
    ("P001", 1, 3.5, False, "", "-", "CROSSFADE",
     "Dressed up for an evening out. One of the sharper early prints and a clean, straight-on "
     "read of both faces."),
    ("P012", 1, 4.0, False, "", "-", "CROSSFADE",
     "Caught laughing in a kitchen. The first frame in the film where they look like a couple "
     "rather than two people posing."),
    ("P009", 1, 3.0, False, "", "-", "CUT",
     "Clowning for the camera after a party. Keeps Chapter 1 from turning into a portrait gallery."),
    ("P017", 1, 3.5, False, "", "-", "CUT",
     "Arm's-length snapshot in the car before going somewhere - the 2003 version of a selfie. "
     "Small, ordinary, and exactly what the early years actually looked like."),
    ("P014", 1, 4.5, False, "", "-", "CROSSFADE",
     "Wrapped around each other in a parked car, lit by flash. Young and private."),
    ("P020", 1, 4.0, False, "", "-", "CUT",
     "The morning after - streamers and confetti all over the carpet. The texture of that whole "
     "period in one frame, and a breath before the chapter's closing image."),
    ("P018", 1, 7.0, True,  "", "-", "SLOW_DISSOLVE",
     "A kiss on the floor in the middle of a party, both oblivious to the room. Grainy and "
     "blown out, and it does not matter. Chapter 1 closes here."),

    # -- CHAPTER 2 -----------------------------------------------------------
    ("P022", 2, 3.5, False, "", "VO-2", "FADE_FROM_BLACK",
     "A dorm room - desk, corkboard, computer speakers. Establishes that this is a life being "
     "lived in rented rooms, not a highlight reel."),
    ("P036", 2, 3.5, False, "", "-", "CUT",
     "The student apartment with beer and NFL posters papering the wall. Funny now, and "
     "completely honest about who they were."),
    ("P051", 2, 2.5, False, "", "-", "CUT",
     "Mid-song with a microphone, fully committed. The first real laugh of the film."),
    ("P056", 2, 6.5, True,  "", "-", "SLOW_DISSOLVE",
     "He has swept her off her feet mid-laugh in a student room. The best single frame of the "
     "young relationship in the entire archive."),
    ("P057", 2, 3.5, False, "", "-", "CUT",
     "Sprawled together laughing in the back seat of a car. Faded and colour-shifted; the "
     "emotion carries straight through it."),
    ("P040", 2, 4.0, False, "", "-", "CROSSFADE",
     "She kisses his cheek. Quiet, affectionate, and one of the highest-scoring emotional "
     "frames of the dating years."),
    ("P050", 2, 3.5, False, "", "-", "CUT",
     "A harbour visit with a tall ship behind them. The beginning of the two of them going "
     "places together."),
    ("P058", 2, 4.0, False, "", "-", "CROSSFADE",
     "At a marina in front of a sportfishing boat, on an early trip south. Their youngest faces "
     "in the whole archive. NOTE: scan is sideways - rotate before use."),
    ("P037", 2, 3.5, False, "", "-", "CUT",
     "A crowded resort beach with a storm coming in. Early travel, before any of it was planned "
     "around anyone else."),
    ("P028", 2, 4.0, False, "", "-", "CROSSFADE",
     "On the cabin sofa, both laughing at something off camera. Warm, easy, unposed."),
    ("P025", 2, 4.0, False, "", "-", "CROSSFADE",
     "Toasting with wine glasses in the cabin. The first frame where they look like adults "
     "rather than students."),
    ("P034", 2, 7.0, True,  "", "VO-3", "SLOW_DISSOLVE",
     "The most intimate frame in the archive: the two of them mid-kiss on a sofa, no audience, "
     "warm afternoon light. Land 'Twenty-four years together. Fifteen years married.' here."),
    ("P061", 2, 3.5, False, "", "-", "CUT",
     "One of her birthdays during the dating years - the 'Happy Birthday' tiara makes the "
     "occasion unmistakable, and she is sitting on his lap."),
    ("P083", 2, 4.0, False, "", "-", "CROSSFADE",
     "Hard-dated 25 May 2007. Their most glamorous frame of the dating years - black strapless "
     "dress, waistcoat and tie."),
    ("P081", 2, 2.5, False, "", "-", "CUT",
     "St Patrick's Day 2007, hard-dated, him in a novelty 'GOT BEER?' hat. Deliberately placed "
     "against the formal frame before it."),
    ("P072", 2, 4.0, False, "", "-", "CUT",
     "The wall at 409 Taylor, signed by everyone who ever lived there. No people in it and it "
     "still says more about those years than a portrait would. NOTE: scanned upside down - rotate."),
    ("P070", 2, 6.0, True,  "", "-", "SLOW_DISSOLVE",
     "His graduation, with the ceremony banner readable behind them - the biggest documented "
     "milestone of the pre-marriage years, and the two of them alone in it. NOTE: scanned "
     "upside down - rotate. Already black and white."),
    ("P044", 2, 4.5, False, "", "-", "CROSSFADE",
     "Arm in arm in front of a house they clearly wanted photographed. The first appearance of "
     "the idea of a home."),
    ("P092", 2, 6.0, True,  "", "VO-4", "SLOW_DISSOLVE",
     "Laughing in a snowstorm with snow visibly settled on his head. The most joyful couple "
     "frame of the late pre-children years, and the right place for 'you're still the person "
     "I want sitting next to me.'"),
    ("P096", 2, 4.0, False, "", "-", "CROSSFADE",
     "The house. No people in it, which is why it works right after the wedding card - the "
     "marriage is represented by what they built, not by a ceremony. NOTE: scanned rotated and "
     "hazy; straighten and warm it up."),
    ("P103", 2, 4.0, False, "", "-", "CUT",
     "Him refinishing cabinets in the driveway, dust hanging in the sun. Unglamorous, "
     "off-centre, and the truest 'building a life' image in the archive."),
    ("P097", 2, 5.0, True,  "", "-", "CROSSFADE",
     "The cleanest, best-exposed couple portrait of the whole pre-children era, both looking "
     "straight down the lens and genuinely happy."),
    ("P106", 2, 5.5, True,  "", "-", "CROSSFADE",
     "Atlantis, both of them alone in the shallows with the towers behind. A vacation, not the "
     "honeymoon - and the best-looking print of the later scans."),
    ("P100", 2, 7.0, True,  "", "-", "SLOW_DISSOLVE",
     "Laughing together in turquoise water. The last frame of the two of them before everything "
     "changes, and it should feel like the end of an era when you cut away from it."),

    # -- CHAPTER 3 -----------------------------------------------------------
    ("P107", 3, 9.0, True,  "", "VO-5", "FADE_FROM_BLACK",
     "Hospital room, first daughter, both parents beaming. The exact hinge from couple to "
     "family. Longest hold in the first half of the film."),
    ("P108", 3, 3.0, False, "", "-", "CROSSFADE",
     "Dressed up for an occasion as a family of three. The new shape of things, still slightly "
     "unfamiliar."),
    ("P110", 3, 3.5, False, "", "-", "CUT",
     "First birthday outdoors, cupcake and a burlap 'ONE' banner. One year gone already."),
    ("P111", 3, 3.0, False, "", "-", "CUT",
     "First proper Christmas as three."),
    ("P112", 3, 4.0, False, "", "-", "CROSSFADE",
     "At home on the couch - him and the baby, no occasion, nobody dressed for it. The everyday "
     "texture that this era of the archive is otherwise short on."),
    ("P114", 3, 3.0, False, "", "-", "CUT",
     "First real trip as a family of three."),
    ("P115", 3, 5.0, True,  "", "-", "CROSSFADE",
     "Outdoors on an overcast day, all three of them. The strongest family-of-three frame in "
     "the archive and the emotional centre of this chapter."),
    ("P116", 3, 3.0, False, "", "-", "CUT",
     "Her thirtieth, with the balloons to prove it. Thirty, married, one child - a marker of "
     "exactly where they were."),
    ("P109", 3, 5.0, True,  "", "VO-6", "SLOW_DISSOLVE",
     "The two of them alone at a cold-weather game, cheek to cheek. One of only a handful of "
     "couple-alone frames in a decade - which is precisely why it earns five seconds here."),
    ("P120", 3, 2.5, False, "", "-", "CUT",
     "The parents dressed for a formal event and a small child photobombing at knee height. "
     "The first sign of the chaos chapter arriving."),
    ("P122", 3, 3.5, False, "", "-", "CUT",
     "Her third birthday cake, 30 October 2016. Two days before her sister arrives - the "
     "audience will not know that yet."),
    ("P119", 3, 5.0, True,  "", "-", "SLOW_DISSOLVE",
     "Pregnant on a pontoon boat with a toddler in a life jacket tucked against her. Almost "
     "nothing else in the archive shows a pregnancy. It hands you straight into Chapter 4."),

    # -- CHAPTER 4 -----------------------------------------------------------
    ("P123", 4, 5.0, True,  "", "-", "FADE_FROM_BLACK",
     "Second birth, framed almost identically to the first three years earlier. Cut them close "
     "together in the grade so the rhyme is visible."),
    ("P124", 4, 9.0, True,  "", "-", "SLOW_DISSOLVE",
     "All four of them together for the first time, in black and white, in the hospital bed. "
     "The highest-scoring photograph in the entire archive. Give it the longest hold of the "
     "middle of the film."),
    ("P125", 4, 4.5, False, "", "-", "CROSSFADE",
     "The older sister meeting the baby. Where the sibling story begins."),
    ("P126", 4, 4.0, False, "", "-", "CUT",
     "Him on the couch with both girls, two weeks in. Exhausted and completely content."),
    ("P137", 4, 3.0, False, "", "-", "CUT",
     "Backyard first birthday for the younger one - high chair, tulle, a crown banner."),
    ("P138", 4, 3.0, False, "", "-", "CUT",
     "Thanksgiving, both parents hoisting a daughter off the floor for the photo."),
    ("P153", 4, 3.5, False, "", "-", "CROSSFADE",
     "An autumn walk, both of them grinning back over their shoulders with the toddler between "
     "them. Ordinary and warm."),
    ("P156", 4, 3.0, False, "", "-", "CUT",
     "Christmas portrait by the tree, one daughter in each of their arms."),
    ("P128", 4, 4.5, True,  "", "-", "CROSSFADE",
     "The two of them alone on a wooded path, cheek to cheek, on a day out with no children in "
     "it. Deliberately placed mid-chapter as a reminder that they are still in there."),
    ("P186", 4, 5.0, True,  "", "-", "SLOW_DISSOLVE",
     "First day of school - the sisters hugging before they leave. One of the best photographs "
     "anyone in this family has ever taken."),
    ("P202", 4, 7.0, True,  "", "-", "SLOW_DISSOLVE",
     "March 2020. The girls' hands flat against the glass storm door with a grandparent kept "
     "outside on the step. The most historically specific frame in the archive - it dates "
     "itself without a caption."),
    ("P228", 4, 5.0, True,  "", "-", "CROSSFADE",
     "On the beach late in the third pregnancy, both older girls in shot. The clearest "
     "'four, about to be five' image there is."),
    ("P218", 4, 7.0, True,  "", "-", "SLOW_DISSOLVE",
     "Going-home day: hospital bed, newborn in the car seat, both parents in masks. The whole "
     "of 2020 in one photograph."),
    ("P229", 4, 3.0, False, "", "-", "CUT",
     "Home on the front steps, everyone masked, the carrier between them."),
    ("P230", 4, 5.5, True,  "", "-", "CROSSFADE",
     "Shot from directly overhead: mother and all three girls laid out in a row on the rug, "
     "the newborn in costume for her first Halloween. Nothing else in the archive is framed "
     "like it."),
    ("P241", 4, 3.5, False, "", "-", "CUT",
     "All five, dressed up, outside for a celebration. The new default shape of the family."),
    ("P245", 4, 6.0, True,  "", "-", "SLOW_DISSOLVE",
     "Family of five on the beach. The arithmetic of the chapter title, finished."),

    # -- CHAPTER 5 -----------------------------------------------------------
    ("P131", 5, 2.0, False, "", "VO-7", "HARD_CUT",
     "Matching poses in the backyard. The chaos montage opens on a joke."),
    ("P151", 5, 1.8, False, "", "-", "HARD_CUT",
     "Father-daughter clowning selfie in winter coats."),
    ("P158", 5, 2.2, False, "", "-", "HARD_CUT",
     "Every board game in the house emptied across the family room floor. No people needed."),
    ("P168", 5, 1.8, False, "", "-", "HARD_CUT",
     "A doughnut balanced on one head while the other reaches in. Birthday, technically."),
    ("P208", 5, 2.0, False, "", "-", "HARD_CUT",
     "All three of them mid-pose in front of the television following an exercise video. "
     "Lockdown, filed under comedy."),
    ("P215", 5, 2.0, False, "", "-", "HARD_CUT",
     "Four faces crammed into a car selfie, nobody behaving."),
    ("P240", 5, 2.0, False, "", "-", "HARD_CUT",
     "Couch selfie, everyone laughing at once."),
    ("P273", 5, 2.2, False, "", "-", "HARD_CUT",
     "The girls crowding into his selfie outside. High emotional score for a photograph that is "
     "essentially a scrum."),
    ("P267", 5, 2.5, True,  "", "-", "HARD_CUT",
     "Him hoisting all three girls at once in the sea. Physically ridiculous and the best "
     "action frame in the archive."),
    ("P249", 5, 1.8, False, "", "-", "HARD_CUT",
     "A Barbie-themed birthday party he is fully participating in."),
    ("P322", 5, 2.0, False, "", "-", "HARD_CUT",
     "Face-pulling selfie at the kitchen counter, ten years into fatherhood."),
    ("P350", 5, 4.0, True,  "", "-", "HARD_CUT",
     "The girls decorating his shaved head with rhinestone stickers while he sits there and "
     "takes it. The single funniest photograph in the archive - hold it longer than the rest "
     "of the montage and let the laugh land."),
    ("P373", 5, 2.2, False, "", "-", "HARD_CUT",
     "Caught mid-gasp opening a present on Christmas Eve."),
    ("P407", 5, 2.5, False, "", "-", "HARD_CUT",
     "Basketball camp, both of them mugging with balls held up. Ends the montage on the girls "
     "as they are now."),

    # -- CHAPTER 6 -----------------------------------------------------------
    ("P236", 6, 3.5, False, "", "VO-8", "FADE_FROM_BLACK",
     "The Rockefeller tree in New York, everyone in coats and masks. A real family trip in a "
     "strange year."),
    ("P242", 6, 4.0, False, "", "-", "CROSSFADE",
     "The eldest carrying the youngest through fallen leaves. The sisters looking after each "
     "other, without being asked to."),
    ("P258", 6, 6.0, True,  "", "-", "SLOW_DISSOLVE",
     "All five on the playroom floor in Christmas pyjamas, every face genuinely going. If one "
     "photograph had to represent the family, it is this one."),
    ("P278", 6, 3.0, False, "", "-", "CUT",
     "Choosing a Christmas tree in the dark at the lot. A tradition, mid-tradition."),
    ("P286", 6, 6.0, True,  "", "-", "SLOW_DISSOLVE",
     "All three girls draped over him while he reads aloud. Unposed, slightly soft, and the "
     "entire family-of-five dynamic in one frame."),
    ("P295", 6, 7.0, True,  "", "-", "SLOW_DISSOLVE",
     "Dusk on the marina dock, all of them from behind - him carrying one, leading another, "
     "the third following. Motion-blurred, dark, and the most cinematic frame in the archive."),
    ("P302", 6, 5.5, True,  "", "-", "CROSSFADE",
     "Three sisters tangled together on empty sand at last light. Composition and colour both "
     "hold up for a long hold."),
    ("P333", 6, 4.5, False, "", "-", "CROSSFADE",
     "The five of them on the church steps after a First Communion. The most formal family "
     "milestone in the recent archive."),
    ("P337", 6, 3.5, False, "", "-", "CUT",
     "Her on the back porch actually reading a handmade card while the child yells the contents "
     "at her from a foot away. Nobody is posing and that is the point."),
    ("P345", 6, 3.0, False, "", "-", "CUT",
     "Fourth of July on the lake dock before swimming. A tradition that repeats every year in "
     "this archive - one instance of it stands for all of them."),
    ("P348", 6, 3.0, False, "", "-", "CUT",
     "Awards night at the lake camp, each girl holding the plaque she was given."),
    ("P356", 6, 3.5, False, "", "-", "CUT",
     "The youngest's fifth birthday at home - the baby of Chapter 4, five years on."),
    ("P363", 6, 3.0, False, "", "-", "CUT",
     "Halloween in costume before trick-or-treating, all five."),
    ("P005_REPRISE", 6, 1.5, True, "", "-", "MATCH_CUT",
     "REPRISE of the opening frame - her at seventeen in her lacrosse uniform. A single "
     "flashed insert immediately before the girls in their own jerseys. This is the callback; "
     "do not explain it with text."),
    ("P312", 6, 3.0, False, "", "-", "MATCH_CUT",
     "Studio portrait of a daughter in full kit, stick across her shoulders. Twenty-five years "
     "after her mother stood on the same kind of field."),
    ("P391", 6, 2.5, False, "", "-", "CUT",
     "In-game, running through a field gone to dandelions, name and number readable."),
    ("P360", 6, 3.5, False, "", "-", "CUT",
     "Backyard goal: big sister in full kit, the smallest one in front of her with her own "
     "stick, copying. The sport passing down inside the family in one frame."),
    ("P386", 6, 5.5, True,  "", "VO-9", "CROSSFADE",
     "All three girls from behind, the family surname across their backs, tallest to smallest. "
     "The best summary frame of where this family has arrived - and the exact place to land "
     "'to these three amazing girls'."),
    ("P387", 6, 6.0, True,  "", "-", "SLOW_DISSOLVE",
     "The same three, in black and white, glancing back across an enormous empty field. Closes "
     "the lacrosse callback and the chapter's forward motion."),
    ("P397", 6, 3.0, False, "", "-", "CUT",
     "Last day of school at the front door, holding the sign between them."),
    ("P409", 6, 4.5, False, "", "-", "SLOW_DISSOLVE",
     "The most recent family-of-five photograph in the archive - August 2026, days before the "
     "anniversary. The last time you see all five together."),

    # -- CHAPTER 7 -----------------------------------------------------------
    ("P331", 7, 4.0, False, "", "-", "FADE_FROM_BLACK",
     "Her and two of the girls, three faces filling the frame. The family is still here - it "
     "just starts to move out of the centre from this point on."),
    ("P313", 7, 4.5, False, "", "-", "CROSSFADE",
     "Her in the MAMA beanie with the youngest, cheek to cheek in winter light. Her as a "
     "mother, one last time before the film hands her back to him."),
    ("P292", 7, 6.5, True,  "", "-", "SLOW_DISSOLVE",
     "Her alone on the gunwale of a boat, turned to the horizon, wind in her hair. The rarest "
     "thing in the archive: a solo portrait of her. This is where the film changes subject."),
    ("P237", 7, 3.0, False, "", "-", "CUT",
     "The two of them in matching ridiculous costumes by their own Christmas tree. Keeps the "
     "ending honest before it gets tender."),
    ("P338", 7, 3.5, False, "", "-", "CUT",
     "Both of them in matching club lacrosse shirts on the sideline. This is what the two of "
     "them look like now, and it quietly closes the lacrosse thread on the couple instead of "
     "the kids."),
    ("P173", 7, 4.5, False, "", "-", "CROSSFADE",
     "Their own portrait from a family photo day - arms around each other on the lawn, no "
     "children in the frame."),
    ("P129", 7, 6.0, True,  "", "VO-10", "SLOW_DISSOLVE",
     "Sunglasses, cheek to cheek, a crowd behind them. A rare post-children frame where they "
     "look exactly like the two people from Chapter 2."),
    ("P270", 7, 6.0, True,  "", "-", "CROSSFADE",
     "The best-composed couple photograph of the recent years - huge cloud-filled sky, "
     "turquoise sea, both laughing instead of posing."),
    ("P294", 7, 7.0, True,  "", "VO-11", "SLOW_DISSOLVE",
     "Dressed for an evening out, full length, palms and colonial architecture behind. The "
     "strongest 'we are still a couple' frame in the digital archive."),
    ("P256", 7, 7.0, True,  "", "-", "SLOW_DISSOLVE",
     "Formally dressed on a balcony above a river valley, alone, visibly older and completely "
     "at ease. The penultimate image."),
    ("P271", 7, 12.0, True, "", "VO-12", "SLOW_DISSOLVE",
     "FINAL FRAME. Golden hour by the water, her leaning into his shoulder, the treeline behind "
     "them gone gold. The tightest, best-lit, most unguarded photograph of the two of them in "
     "the archive - and it is EXIF-dated 13 August 2022, their eleventh anniversary. Hold it, "
     "then fade."),
]

EDIT = [e for e in EDIT if e[0] != "P186_SKIP"]

# Full-screen text cards, keyed to the frame they follow ("START" = before all).
TEXT_CARDS = [
    ("START",  "AFTER_P005", 5.0, "March 15, 2002.", 1),
    ("CARD2",  "AFTER_P018", 6.0, "Before the house.\nBefore the kids.\nBefore all of this —\nthere was just us.", 2),
    ("CARD3",  "AFTER_P092", 5.0, "August 13, 2011.", 2),
    ("CARD4",  "AFTER_P100", 4.5, "Then everything changed.", 3),
    ("CARD5",  "AFTER_P119", 4.0, "And then there were five.", 4),
    ("CARD6",  "AFTER_P245", 3.5, "Life got loud.", 5),
    ("CARD7",  "AFTER_P407", 4.5, "We built a whole life.", 6),
    ("CARD8",  "AFTER_P409", 5.0, "A lot has changed.", 7),
    ("CARD9",  "AFTER_P256", 4.0, "But one thing hasn't.", 7),
    ("END1",   "AFTER_P271", 5.0, "24 YEARS TOGETHER.\n15 YEARS MARRIED.", 7),
    ("END2",   "AFTER_P271", 5.0, "I'D STILL CHOOSE YOU.", 7),
    ("END3",   "AFTER_P271", 6.0, "HAPPY 15TH ANNIVERSARY, MY LOVE.\n\n15 years down. Forever to go.", 7),
]

# Final-frame shortlist. The client picks; this is the ranking and the argument.
HERO_CANDIDATES = ["P271", "P256", "P294", "P129", "P270"]

HERO_WHY = {
    "P271": "RECOMMENDED. The tightest and best-lit two-shot of the two of them in the entire "
            "archive: low golden sun, the treeline behind them turned gold, her leaning into his "
            "shoulder, neither of them performing for the lens. It is also the only strong "
            "recent couple frame with a HIGH-confidence EXIF date - 13 August 2022, which is "
            "their eleventh wedding anniversary. Ending the film on a photograph taken on an "
            "anniversary, without ever saying so on screen, is the closing move.",
    "P256": "The most grown-up image of the two of them that exists: formal clothes, a river "
            "valley behind, both visibly older than the couple in Chapter 2 and completely at "
            "ease with it. Reads as 'this is who we became'. Marked down only because the "
            "framing is a little distant - their faces are small in the frame, which costs it "
            "some power on a final 12-second hold.",
    "P294": "Full-length, beautifully lit, the two of them dressed for an evening out with palms "
            "and colonial architecture behind. The strongest straightforward 'we are still a "
            "couple' portrait in the digital archive. Loses to P271 only because it was taken "
            "on a family holiday and reads slightly as a vacation photograph.",
    "P129": "The best pure couple frame of the post-children years - sunglasses, cheek to cheek, "
            "crowd behind, both of them looking exactly like the people from the early chapters. "
            "The strongest emotional argument of the five. Its drawback is age: 2017 is nine "
            "years ago, and a final frame that old slightly undercuts 'still us'.",
    "P270": "The best-composed photograph of the two of them from the recent years - dramatic "
            "cloud-filled sky, turquoise water, a single red beach chair anchoring the "
            "background, and both of them laughing rather than posing. It is a selfie, which is "
            "the only thing keeping it out of the top two for a last image.",
}

HERO_NOTE = {
    "P271": "Also works as the final frame with no text over it at all.",
    "P256": "If you choose this one, crop in slightly - roughly 15% off each edge.",
    "P294": "Swap with P271 if you would rather end on the two of you dressed up than in ordinary clothes.",
    "P129": "If you pick this, move P271 to the penultimate slot so the film still ends recent.",
    "P270": "Strongest of the five if you want the last frame to be a laugh rather than a stillness.",
}


def layout_for(row):
    w, h = int(row["width"]), int(row["height"])
    ratio = w / h
    if ratio > 1.15:
        return "FULL_BLEED_LANDSCAPE"
    if ratio < 0.87:
        return "VERTICAL_CENTERED_ON_BLURRED_FILL"
    return "FULL_BLEED_SOFT_CROP"


def year_of(row):
    d = row["estimated_date"]
    return d[:4] if d and d[0].isdigit() else "UNKNOWN"


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    inv = {r["unique_id"]: r for r in csv.DictReader(open(INVENTORY))}

    photo_rows, canva_rows = [], []
    seq = 0
    build_step = 0
    pending_cards = {c[1]: [] for c in TEXT_CARDS}
    for c in TEXT_CARDS:
        pending_cards[c[1]].append(c)

    def emit_cards(anchor):
        # pop, so a reprised photograph never re-fires a card already placed
        nonlocal build_step
        for card_id, _a, dur, text, chap in pending_cards.pop(anchor, []):
            build_step += 1
            canva_rows.append({
                "sequence": f"{build_step:03d}",
                "filename": "(text card)",
                "Drive_path": "—",
                "chapter": CHAPTERS[chap],
                "year": "—",
                "people": "—",
                "duration_seconds": dur,
                "layout": "TEXT_CARD_BLACK",
                "hero": "NO",
                "on_screen_text": text,
                "voiceover": "",
                "transition": "FADE_THROUGH_BLACK",
                "notes": f"Full-screen card ({card_id}). Centred, letterspaced, no photograph behind it.",
            })

    for uid, chap, dur, hero, ost, vo, trans, reason in EDIT:
        base = uid.replace("_REPRISE", "")
        row = inv[base]
        reprise = uid.endswith("_REPRISE")
        seq += 1
        build_step += 1

        note_bits = []
        if row["date_confidence"] in ("LOW", "UNKNOWN"):
            note_bits.append(f"date confidence {row['date_confidence']} - placement is by era, not by a known day")
        if row["technical_quality"] != "GOOD":
            note_bits.append(f"technical quality {row['technical_quality']}")
        if "upside down" in row["notes"] or "sideways" in row["notes"] or "rotated" in row["notes"]:
            note_bits.append("SCAN ORIENTATION: rotate before placing")
        if reprise:
            note_bits.append("REPRISE of sequence 001 - same file used twice, intentionally")
        if int(row["hero_score"]) >= 9:
            note_bits.append("top-tier hero score in the archive")

        # ONE numbering scheme across both manifests: the build step. Every screen
        # in the film - photograph or text card - has exactly one number.
        rec = {
            "sequence": f"{build_step:03d}",
            "photo_index": f"{seq} of 110",
            "filename": row["filename"],
            "drive_path": row["drive_path"],
            "drive_url": row["drive_url"],
            "approximate_date": row["estimated_date"],
            "date_confidence": row["date_confidence"],
            "chapter": CHAPTERS[chap],
            "people": row["family_grouping"],
            "people_detail": row["people_visible"],
            "event": row["event"],
            "theme": row["theme"],
            "emotional_score": int(row["emotional_score"]),
            "story_score": int(row["story_score"]),
            "technical_score": int(row["technical_score"]),
            "hero_score": int(row["hero_score"]),
            "duration_seconds": dur,
            "layout": layout_for(row),
            "on_screen_text": ost,
            "voiceover_section": vo if vo != "-" else "",
            "voiceover_text": VOICEOVER.get(vo, ""),
            "transition": trans,
            "selection_reason": reason,
            "notes": "; ".join(note_bits),
            "unique_id": uid,
            "source_label": row["sheet_label"],
        }
        photo_rows.append(rec)

        canva_rows.append({
            "sequence": f"{build_step:03d}",
            "filename": row["filename"],
            "Drive_path": row["drive_path"],
            "chapter": CHAPTERS[chap],
            "year": year_of(row),
            "people": row["family_grouping"],
            "duration_seconds": dur,
            "layout": layout_for(row),
            "hero": "YES" if hero else "NO",
            "on_screen_text": ost,
            "voiceover": VOICEOVER.get(vo, ""),
            "transition": trans,
            "notes": "; ".join(note_bits),
        })

        emit_cards(f"AFTER_{base}")

    # ---- FINAL_PHOTO_MANIFEST.csv / .json
    cols = ["sequence", "photo_index", "filename", "drive_path", "drive_url", "approximate_date",
            "date_confidence", "chapter", "people", "people_detail", "event", "theme",
            "emotional_score", "story_score", "technical_score", "hero_score",
            "duration_seconds", "layout", "on_screen_text", "voiceover_section",
            "voiceover_text", "transition", "selection_reason", "notes",
            "unique_id", "source_label"]
    with open(os.path.join(OUTDIR, "FINAL_PHOTO_MANIFEST.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(photo_rows)

    total = sum(r["duration_seconds"] for r in photo_rows)
    card_total = sum(c[2] for c in TEXT_CARDS)
    by_chapter = {}
    for r in photo_rows:
        by_chapter.setdefault(r["chapter"], {"photographs": 0, "seconds": 0.0})
        by_chapter[r["chapter"]]["photographs"] += 1
        by_chapter[r["chapter"]]["seconds"] += r["duration_seconds"]

    doc = {
        "film": "15 YEARS OF US",
        "occasion": "15th wedding anniversary; 24 years together",
        "verified_timeline": {
            "relationship_began": "2002-03-15",
            "married": "2011-08-13",
            "years_together": 24,
            "years_married": 15,
            "first_daughter_born": "October 30",
            "second_daughter_born": "November 1",
            "third_daughter": "youngest",
        },
        "wedding_photographs": "INTENTIONALLY ABSENT. The physical wedding album is a separate "
                               "annual tradition and is deliberately not used. There is no wedding "
                               "chapter and none is needed.",
        "primary_song": "Just Breathe - Pearl Jam",
        "photograph_count": len(photo_rows),
        "unique_files": len({r["filename"] for r in photo_rows}),
        "photo_runtime_seconds": round(total, 1),
        "text_card_seconds": round(card_total, 1),
        "estimated_total_runtime": f"{int((total + card_total) // 60)}m {int((total + card_total) % 60)}s",
        "chapters": by_chapter,
        "voiceover": VOICEOVER,
        "text_cards": [{"id": c[0], "after": c[1], "seconds": c[2], "text": c[3]} for c in TEXT_CARDS],
        "photographs": photo_rows,
    }
    with open(os.path.join(OUTDIR, "FINAL_PHOTO_MANIFEST.json"), "w") as f:
        json.dump(doc, f, indent=2)

    # ---- CANVA_PRODUCTION_MANIFEST.csv
    ccols = ["sequence", "filename", "Drive_path", "chapter", "year", "people",
             "duration_seconds", "layout", "hero", "on_screen_text", "voiceover",
             "transition", "notes"]
    with open(os.path.join(OUTDIR, "CANVA_PRODUCTION_MANIFEST.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=ccols)
        w.writeheader()
        w.writerows(canva_rows)

    # ---- FINAL_HERO_CANDIDATES.csv
    hcols = ["rank", "filename", "drive_path", "drive_url", "date", "date_confidence",
             "description", "emotional_score", "visual_score", "story_score",
             "why_it_works_as_the_final_image", "note", "unique_id"]
    with open(os.path.join(OUTDIR, "FINAL_HERO_CANDIDATES.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=hcols)
        w.writeheader()
        for i, uid in enumerate(HERO_CANDIDATES, 1):
            r = inv[uid]
            w.writerow({
                "rank": i,
                "filename": r["filename"],
                "drive_path": r["drive_path"],
                "drive_url": r["drive_url"],
                "date": r["estimated_date"],
                "date_confidence": r["date_confidence"],
                "description": r["people_visible"],
                "emotional_score": r["emotional_score"],
                "visual_score": r["technical_score"],
                "story_score": r["story_score"],
                "why_it_works_as_the_final_image": HERO_WHY[uid],
                "note": HERO_NOTE[uid],
                "unique_id": uid,
            })

    print(f"photographs      : {len(photo_rows)} ({doc['unique_files']} unique files)")
    print(f"photo runtime    : {total/60:.1f} min")
    print(f"text cards       : {len(TEXT_CARDS)} ({card_total:.0f}s)")
    print(f"estimated total  : {doc['estimated_total_runtime']}")
    for k, v in by_chapter.items():
        print(f"  {k:<40} {v['photographs']:>3} photos  {v['seconds']:>5.1f}s")


if __name__ == "__main__":
    main()
