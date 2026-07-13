"""
Seed script for the Bleach Codex vertical slice.

Currently scoped to characters who already have real portrait/full-body
images provided: Ichigo, Rukia, Byakuya, Orihime, Sado, Uryu, Yoruichi.
Isshin, Masaki, Karin, and Yuzu are intentionally left out for now since
they don't have images yet, add them back the same way once art exists.

USAGE:
    1. Start your FastAPI server: uvicorn app.main:app --reload
    2. In a separate terminal, run: python seed_data.py

This makes real HTTP calls to your running API, the same endpoints your
frontend uses. Nothing here talks to MongoDB directly.

Safe to re-run: clear_all() wipes every collection first, so running this
multiple times never creates duplicates.
"""

import httpx
import os

BASE_URL = os.environ.get("BLEACH_CODEX_API_URL", "http://127.0.0.1:8000")

client = httpx.Client(base_url=BASE_URL, timeout=45.0)


def create_character(name, biography, personality=None, appearance=None, portrait_filename=None, full_body_filename=None):
    resp = client.post("/characters/", json={
        "name": name, "biography": biography, "personality": personality, "appearance": appearance,
        "portrait_filename": portrait_filename, "full_body_filename": full_body_filename,
    })
    resp.raise_for_status()
    return resp.json()["_id"]


def create_relationship(a_id, b_id, rel_type, note=None):
    resp = client.post("/relationships/", json={
        "character_a_id": a_id, "character_b_id": b_id,
        "relationship_type": rel_type, "plot_relevance_note": note,
    })
    resp.raise_for_status()
    return resp.json()["_id"]


def create_arc(name, order_index, chapter_range=None, episode_range=None):
    resp = client.post("/arcs/", json={
        "name": name, "order_index": order_index,
        "chapter_range": chapter_range, "episode_range": episode_range,
    })
    resp.raise_for_status()
    return resp.json()["_id"]


def link_arc(character_id, arc_id):
    resp = client.post(f"/characters/{character_id}/arcs/{arc_id}")
    resp.raise_for_status()


def create_source(source_type, reference, note=None):
    resp = client.post("/sources/", json={"type": source_type, "reference": reference, "note": note})
    resp.raise_for_status()
    return resp.json()["_id"]


def create_power(character_id, power_type, ability_description, rules_and_limitations=None,
                  evolution_notes=None, first_shown_source_id=None, other_type_label=None,
                  image_filename=None):
    resp = client.post("/powers/", json={
        "character_id": character_id, "power_type": power_type,
        "ability_description": ability_description,
        "rules_and_limitations": rules_and_limitations,
        "evolution_notes": evolution_notes,
        "first_shown_source_id": first_shown_source_id,
        "other_type_label": other_type_label,
        "image_filename": image_filename,
    })
    resp.raise_for_status()
    return resp.json()["_id"]


def clear_all():
    """Deletes every existing record across all 6 collections before reseeding."""
    print("Clearing existing data...")
    endpoints = ["/lore-events/", "/powers/", "/relationships/", "/arcs/", "/sources/", "/characters/"]
    total_deleted = 0
    for endpoint in endpoints:
        items = client.get(endpoint).json()
        for item in items:
            client.delete(f"{endpoint}{item['_id']}")
            total_deleted += 1
    print(f"  Deleted {total_deleted} existing records.")
    print()


def main():
    clear_all()

    print("Seeding characters...")
    ichigo_id = create_character(
        "Ichigo Kurosaki",
        "Gained Shinigami powers as a teenager and became a Substitute Shinigami, protecting Karakura "
        "Town from Hollows.",
        personality="Brash, short tempered, but fiercely protective of everyone around him.",
        appearance="Distinctive bright orange hair, brown eyes.",
        portrait_filename="ichigo_face.jpg",
        full_body_filename="ichigo_full-removebg-preview.png",
    )
    rukia_id = create_character(
        "Rukia Kuchiki",
        "Lieutenant of the 13th Division under Captain Ukitake, adopted into the noble Kuchiki family "
        "by Byakuya. Transfers her Shinigami powers to Ichigo Kurosaki, setting the series in motion.",
        personality="Quiet, composed, modest despite her noble status.",
        appearance="Short and petite, violet eyes, black cropped hair.",
        portrait_filename="rukia_face.webp",
        full_body_filename="rukia_full-removebg-preview.png",
    )
    byakuya_id = create_character(
        "Byakuya Kuchiki",
        "Captain of the 6th Division, head of the noble Kuchiki family, adoptive older brother to Rukia "
        "through his late wife Hisana's dying wish.",
        personality="Rigid, stoic, deeply bound by nobility and tradition.",
        appearance="Tall, refined bearing, long dark hair, noble Kuchiki attire.",
        portrait_filename="byakuya_face.webp",
        full_body_filename="Byakuya_Full-removebg-preview.png",
    )
    orihime_id = create_character(
        "Orihime Inoue",
        "Ichigo's classmate at Karakura High School and childhood friend of Tatsuki Arisawa. Raised "
        "alone by her older brother Sora until his death, after which she lived independently. Her "
        "latent spiritual power later awakens into the Shun Shun Rikka, six fairy spirits that reject "
        "harm rather than simply attacking it.",
        personality="Gentle and easily flustered, prone to elaborate imaginative tangents, but fiercely "
                    "devoted to protecting the people she cares about even at great personal risk.",
        appearance="Long burnt orange hair, brown eyes, distinguished by the flower shaped hairpins "
                   "given to her by her late brother.",
        portrait_filename="inoue_face.webp",
        full_body_filename="inoue_full-removebg-preview.png",
    )
    sado_id = create_character(
        "Yasutora Sado",
        "A classmate of Ichigo at Karakura High School, of Japanese and Mexican descent, known to "
        "everyone as Chad. Raised by his grandfather Oscar after his parents' deaths, who taught him "
        "to use his great size and strength only to protect others, never to harm them. His latent "
        "power awakens while defending Karin Kurosaki from a Hollow.",
        personality="Quiet and stoic, almost entirely nonviolent by personal principle, speaks rarely "
                    "but is unwaveringly loyal to Ichigo.",
        appearance="Extremely tall and muscular, dark skinned, with a tattoo on his left shoulder "
                   "reading Amore e Morte.",
        portrait_filename="sado_face.webp",
        full_body_filename="sado_full-removebg-preview.png",
    )
    uryu_id = create_character(
        "Uryu Ishida",
        "The last known pure blooded Quincy of his generation, and a classmate of Ichigo at Karakura "
        "High School. Trained by his grandfather Soken, who was killed by a Hollow the Shinigami "
        "failed to reach in time, fueling Uryu's early hatred of Shinigami. Joins Ichigo's group to "
        "rescue Rukia, partly to prove the Quincy are not obsolete.",
        personality="Proud, meticulous, and initially standoffish toward Ichigo, softening into "
                    "genuine loyalty over time. Lives by a personal code he calls the Pride of the "
                    "Quincy.",
        appearance="Slender and bespectacled, with straight black hair, wears a white Quincy uniform "
                   "in combat.",
        portrait_filename="uryu_face.webp",
        full_body_filename="uryu_full-removebg-preview.png",
    )
    yoruichi_id = create_character(
        "Yoruichi Shihoin",
        "Former captain of the 2nd Division and commander of the Onmitsukido, and head of the noble "
        "Shihoin family, until she defected from Soul Society to help clear Kisuke Urahara's name. "
        "Spends over a century living in the human world, often in the form of a black cat, before "
        "leading Ichigo's group into Soul Society.",
        personality="Playful and teasing, irreverent toward her own noble status, but a sharp "
                    "strategist and devoted mentor underneath the humor.",
        appearance="Dark skinned, golden eyed, with long purple hair kept in a ponytail, frequently "
                   "disguised as an ordinary black cat.",
        portrait_filename="yoruichi_face.webp",
        full_body_filename="yoruichi_full.webp",
    )
    print(f"  Created 7 characters.")

    renji_id = create_character(
        "Renji Abarai",
        "Lieutenant of the 6th Division under Byakuya Kuchiki. Grew up an orphan in the 78th district "
        "of Rukongai alongside Rukia, the two of them the only survivors of their group of friends. "
        "Joined the Shinigami Academy with her, later serving in the 11th Division before transferring "
        "to the 6th.",
        personality="Loud, brash, and prone to bravado, deeply competitive especially toward Byakuya, "
                    "but fiercely loyal underneath the swagger.",
        appearance="Tall and muscular, bright red hair tied back, tribal tattoos covering his arms, "
                   "neck, and forehead.",
        portrait_filename="renji_face.webp",
        full_body_filename="renji_full-removebg-preview.png",
    )
    toshiro_id = create_character(
        "Toshiro Hitsugaya",
        "Captain of the 10th Division, the youngest captain in the history of the Gotei 13. Grew up in "
        "West Rukongai with his grandmother and his close childhood friend Momo Hinamori.",
        personality="Mature and serious well beyond his apparent age, short tempered, and openly hates "
                    "being treated like a child. Deeply protective of Momo Hinamori.",
        appearance="Short in stature with turquoise eyes and short, spiky white hair, wears a sleeveless "
                   "captain's haori and carries his oversized Zanpakuto across his back rather than at "
                   "his hip.",
        portrait_filename="toshiro_face.png",
        full_body_filename="toshiro_full-removebg-preview.png",
    )
    rangiku_id = create_character(
        "Rangiku Matsumoto",
        "Lieutenant of the 10th Division under Toshiro Hitsugaya. Childhood friends with Gin Ichimaru "
        "for over a century, though they grew estranged as adults.",
        personality="Free spirited, laid back, and self centered on the surface, loves drinking, but "
                    "deeply loyal to the people she cares about underneath it.",
        appearance="Tall and voluptuous, with long wavy strawberry blonde hair worn loose.",
        portrait_filename="rangiku_face.webp",
        full_body_filename="rangiku_full.webp",
    )
    soifon_id = create_character(
        "Soi Fon",
        "Captain of the 2nd Division and Commander of the Onmitsukido, the Soul Society's stealth "
        "force. Former bodyguard and protege of Yoruichi Shihoin during her childhood.",
        personality="Cold, strict, and domineering, holds herself and her subordinates to exacting "
                    "standards. Carries a deep, conflicted devotion toward Yoruichi that borders on "
                    "obsession, still stung by feeling abandoned when Yoruichi left Soul Society.",
        appearance="Small and slight, with black hair worn in two long braids, one wrapped in white "
                   "cloth.",
        portrait_filename="soifon_face.webp",
        full_body_filename="soifon_full.webp",
    )
    yamamoto_id = create_character(
        "Genryusai Yamamoto",
        "Captain Commander of the Gotei 13 and Captain of the 1st Division. Founded the Shinigami "
        "Academy roughly a thousand years before the current story.",
        personality="Rigid, stern, and near unshakeable, believes firmly that law and order must be "
                    "upheld for the good of Soul Society. Treats his oldest surviving students almost "
                    "like sons.",
        appearance="An elderly man with a very muscular build, long white beard, and numerous scars "
                   "across his body from centuries of battle.",
        portrait_filename="yamamoto_face.webp",
        full_body_filename="yamamoto_full.webp",
    )
    gin_id = create_character(
        "Gin Ichimaru",
        "Captain of the 3rd Division, secretly allied with Sosuke Aizen for the entire Soul Society "
        "arc, only revealing his true allegiance at its climax.",
        personality="Aloof and sarcastic, wears a perpetual fox like closed eye smile that unsettles "
                    "nearly everyone around him. Says little directly, needling people more through "
                    "what he withholds than what he actually says.",
        appearance="Tall and thin, with short silver hair and a perpetually closed, smiling expression.",
        portrait_filename="gin_face.jpg",
        full_body_filename="gin_full.webp",
    )
    kira_id = create_character(
        "Izuru Kira",
        "Lieutenant of the 3rd Division under Gin Ichimaru. Academy classmate and close friend of both "
        "Renji Abarai and Momo Hinamori.",
        personality="Gloomy, introspective, and indecisive on the surface, often mistaken for weak "
                    "because of it, but capable of real severity when someone he's loyal to is "
                    "threatened.",
        appearance="Blond hair combed into three points, with one length swept over his left eye, blue "
                   "eyes.",
        portrait_filename="kira_face.webp",
        full_body_filename="kira_full-removebg-preview.png",
    )
    omaeda_id = create_character(
        "Marechiyo Omaeda",
        "Lieutenant of the 2nd Division under Soi Fon, born into a wealthy noble family within Soul "
        "Society.",
        personality="Pompous, greedy, and often played for laughs with his cowardly first instincts, "
                    "but a genuinely formidable fighter whenever he actually commits to a fight.",
        appearance="Large and heavyset, with a shaved head save for a topknot, and ostentatious gold "
                   "jewelry.",
        portrait_filename="marechiyo_face.jpg",
        full_body_filename="marechiyo_full-removebg-preview.png",
    )
    sasakibe_id = create_character(
        "Chojiro Sasakibe",
        "Lieutenant of the 1st Division under Yamamoto for over 110 years, the longest serving "
        "lieutenant to a single captain in the Gotei 13.",
        personality="Quiet and dutiful, a man of very few words, holds unwavering loyalty and "
                    "admiration for Yamamoto. Developed an unexpected fondness for English culture "
                    "during a mission abroad.",
        appearance="Tanned skin, white pupil-less eyes, short silver gray hair, and a thin black "
                   "mustache.",
        portrait_filename="chojiro_face.webp",
        full_body_filename="chojiro_full-removebg-preview.png",
    )
    print(f"  Created 9 more characters.")

    print("Seeding relationships...")
    create_relationship(
        byakuya_id, rukia_id, "sibling",
        note="Adoptive siblings, Rukia was adopted into the Kuchiki family after Byakuya's late wife "
             "Hisana, Rukia's biological sister, asked him to find and care for her.",
    )
    create_relationship(
        yoruichi_id, byakuya_id, "ally",
        note="Old acquaintance, knew Byakuya since he was young and taught him some Shunpo techniques "
             "including Utsusemi, though this was informal rather than a formal mentor and student "
             "relationship.",
    )
    create_relationship(
        ichigo_id, rukia_id, "friend",
        note="Rukia is the Soul Reaper who transferred her powers to Ichigo, setting the entire story "
             "in motion. Closest friend and most trusted ally. Explicitly not romantic.",
    )
    create_relationship(orihime_id, rukia_id, "friend")
    create_relationship(ichigo_id, orihime_id, "friend")
    create_relationship(
        ichigo_id, orihime_id, "spouse",
        note="Confirmed in the story's final chapter and epilogue, well beyond this vertical slice's "
             "Soul Society arc scope. Kept here as the standing, eventual relationship.",
    )
    create_relationship(
        ichigo_id, byakuya_id, "enemy",
        note="Byakuya arrests Rukia and stands as one of Ichigo's central opponents during the Soul "
             "Society rescue.",
    )
    create_relationship(
        ichigo_id, byakuya_id, "ally",
        note="Comes to respect Ichigo greatly after their fight and fights alongside him in later "
             "arcs.",
    )
    create_relationship(
        ichigo_id, uryu_id, "rival",
        note="Friendly rivals since their first meeting, each pushing the other to grow stronger.",
    )
    create_relationship(
        ichigo_id, uryu_id, "friend",
        note="Beneath the rivalry, a real friendship, Uryu joins the Soul Society rescue in part to "
             "help Ichigo despite his stated reasons being about Quincy pride.",
    )
    create_relationship(
        ichigo_id, sado_id, "friend",
        note="Best friends since middle school, bound by a promise to throw punches for each other.",
    )
    create_relationship(orihime_id, uryu_id, "friend")
    create_relationship(orihime_id, sado_id, "friend")
    create_relationship(uryu_id, sado_id, "friend")
    create_relationship(
        yoruichi_id, ichigo_id, "mentor",
        note="Trains Ichigo directly, most notably guiding his push toward Bankai before the Soul "
             "Society rescue.",
    )
    create_relationship(rukia_id, uryu_id, "ally")
    create_relationship(rukia_id, sado_id, "ally")

    # Squad hierarchies
    create_relationship(yamamoto_id, sasakibe_id, "captain", note="Lieutenant for over 110 years.")
    create_relationship(soifon_id, omaeda_id, "captain")
    create_relationship(gin_id, kira_id, "captain")
    create_relationship(toshiro_id, rangiku_id, "captain", note="Personality opposites who are unusually close for a captain and lieutenant.")
    create_relationship(byakuya_id, renji_id, "captain")

    # Yamamoto as Captain-Commander stands above every other captain
    create_relationship(yamamoto_id, soifon_id, "superior")
    create_relationship(yamamoto_id, gin_id, "superior")
    create_relationship(yamamoto_id, toshiro_id, "superior")
    create_relationship(yamamoto_id, byakuya_id, "superior")
    create_relationship(
        yamamoto_id, yoruichi_id, "superior",
        note="Former commander, from before her defection from Soul Society.",
    )

    create_relationship(
        yoruichi_id, soifon_id, "mentor",
        note="Trained her as a bodyguard and protege during her own time as Captain of the 2nd "
             "Division and commander of the Onmitsukido. Soi Fon still carries deep, conflicted "
             "admiration for her.",
    )
    create_relationship(
        gin_id, rangiku_id, "friend",
        note="Childhood friends for over a century, though they grew estranged as adults.",
    )
    create_relationship(renji_id, kira_id, "friend", note="Academy classmates.")
    create_relationship(
        renji_id, rukia_id, "friend",
        note="Childhood friends since their days as orphans together in Rukongai.",
    )
    create_relationship(
        renji_id, rukia_id, "spouse",
        note="Confirmed in the story's final chapter and epilogue, well beyond this vertical slice's "
             "Soul Society arc scope.",
    )
    print("  Created 32 relationships.")

    print("Seeding arc...")
    soul_society_arc_id = create_arc(
        "Soul Society Arc", order_index=1,
        chapter_range="Chapters 43-184", episode_range="Episodes 20-109",
    )
    print(f"  Created 1 arc.")

    print("Linking characters to the Soul Society Arc...")
    for char_id in [ichigo_id, rukia_id, byakuya_id, orihime_id, sado_id, uryu_id, yoruichi_id,
                    renji_id, toshiro_id, rangiku_id, soifon_id, yamamoto_id, gin_id, kira_id,
                    omaeda_id, sasakibe_id]:
        link_arc(char_id, soul_society_arc_id)
    print("  Linked 16 characters to the arc.")

    print("Seeding sources...")
    ch182_id = create_source("manga_chapter", "Chapter 182", note="Ichigo's Bankai fully realized against Byakuya.")
    print("  Created 1 source.")

    print("Seeding powers...")
    create_power(
        ichigo_id, "shikai",
        "Zangetsu in its base sealed and released form, a large, black, cleaver like blade with no "
        "true release command, Ichigo simply wields it directly.",
    )
    create_power(
        ichigo_id, "bankai",
        "Tensa Zangetsu, grants significantly increased speed and a more compact black blade, "
        "amplifying Ichigo's signature Getsuga Tensho technique.",
        rules_and_limitations="Achieving Bankai normally takes 10+ years of training, Ichigo bypassed "
            "this using Urahara's Tenshintai device, which forcibly materializes the Zanpakuto spirit "
            "but is capped at 3 consecutive days of use due to the risk of the wielder's soul tearing "
            "apart.",
        evolution_notes="Later retrained during a nearly 2,000 hour session in the Dangai, emerging "
            "with a new Zangetsu form featuring black chains and a redesigned outfit.",
        first_shown_source_id=ch182_id,
    )
    create_power(
        rukia_id, "shikai",
        "Sode no Shirayuki, an ice type Zanpakuto activated with the release command Dance. Regarded "
        "as one of the most beautiful Zanpakuto in Soul Society.",
        rules_and_limitations="Its actual ability lowers the wielder's own body temperature below "
            "freezing, the blade extends her reach, but isn't the direct source of the cold itself.",
    )
    create_power(
        rukia_id, "bankai",
        "Hakka no Togame, dramatically changes Rukia's appearance into a white, ice covered kimono "
        "with a half crown of ice, her hair and irises turn white.",
        rules_and_limitations="Despite attaining it, Rukia remained within the traditional Bankai "
            "training period and avoided using it in real battle except as an absolute last resort.",
    )
    create_power(
        byakuya_id, "bankai",
        "Senbonzakura Kageyoshi, disperses into thousands of cherry blossom shaped blade shards, "
        "multiplying his Shikai's already numerous fragments to an even greater degree.",
    )
    create_power(
        orihime_id, "other",
        "Shun Shun Rikka, six fairy spirits living in her hairpins. Santen Kesshun forms a triangular "
        "defensive barrier that repels attacks. Souten Kisshun reverses damage done to a person or "
        "object within its half oval barrier, effectively healing by rejecting the injury from having "
        "happened at all. Koten Zanshun, using the spirit Tsubaki, is her only offensive technique, "
        "cutting through an enemy from both sides at once.",
        rules_and_limitations="Effectiveness is tied directly to Orihime's emotional state, doubt and "
            "hesitation weaken the spirits, while resolve and conviction strengthen them. Tsubaki is "
            "the only spirit capable of attack and is vulnerable to counterattack whenever used.",
        evolution_notes="Later training lets her invoke techniques without needing to chant the full "
            "incantation first.",
        other_type_label="Shun Shun Rikka",
    )
    create_power(
        sado_id, "other",
        "Right arm transforms into an armored form he calls Brazo Derecha de Gigante, dramatically "
        "increasing his striking power and letting him fire concentrated blasts of spiritual energy "
        "from his fist.",
        rules_and_limitations="Early on he could only fire the energy blast a few times before "
            "exhausting himself.",
        evolution_notes="Later awakens a second armored form on his left arm, Brazo Izquierda del "
            "Diablo, while in Hueco Mundo, giving him a dedicated offensive arm alongside the "
            "defensive right one.",
        other_type_label="Fullbring: Brazo Derecha de Gigante",
    )
    create_power(
        uryu_id, "quincy",
        "Forms a spiritual bow by gathering Reishi from the surrounding air, firing it as Heilig "
        "Pfeil, arrows of concentrated spirit energy. Uses Hirenkyaku for high speed movement, the "
        "Quincy equivalent of a Shinigami's Shunpo.",
        rules_and_limitations="As a Quincy, his power comes from absorbing ambient spiritual "
            "particles rather than channeling his own internal reserve the way Shinigami do, so he "
            "performs best in Reishi dense environments such as Soul Society.",
        evolution_notes="After later losing and regaining his powers, he gains an upgraded bow called "
            "Ginrei Kojaku, capable of firing far more shots at once.",
    )
    create_power(
        yoruichi_id, "other",
        "A master of Hakuda hand to hand combat and Shunpo, forgoing use of a Zanpakuto almost "
        "entirely. Also possesses a unique ability to shapeshift into a black cat at will, retaining "
        "her spiritual power and speed in that form despite its physical limitations.",
        rules_and_limitations="Her Shunpo is unmatched in Soul Society, earning her the title Flash "
            "Goddess, though a century spent mostly in cat form leaves her noticeably winded after "
            "extended use.",
        evolution_notes="Later develops Shunko, a technique fusing Hakuda with Kido for even greater "
            "offensive power.",
        other_type_label="Hakuda and Shunpo Mastery",
    )
    create_power(
        renji_id, "shikai",
        "Zabimaru, released with the command Howl. Its sealed form is an ordinary katana with a red "
        "hilt. In Shikai it becomes a six segmented blade connected by a stretchable thread, doubling "
        "as a whip and a sword, letting Renji strike from unpredictable angles or wrap around an "
        "opponent before crushing them.",
        rules_and_limitations="The segments make it more useful as a whip than a conventional sword, "
            "and Renji himself states that out of every lieutenant's Zanpakuto, Zabimaru is the most "
            "difficult to master. Extended whip attacks leave him briefly vulnerable while he retrieves "
            "the segments.",
        evolution_notes="Much later in the story Zabimaru is reforged into a true Shikai form after "
            "Renji reassesses his relationship with it before the Thousand Year Blood War.",
    )
    create_power(
        renji_id, "bankai",
        "Hihio Zabimaru, an enlarged version of his Shikai resembling the skeletal structure of a "
        "giant snake with a baboon skull over his shoulder and fur covering his right arm. Rather than "
        "cutting, it catches opponents in its jaws and crushes or smashes them.",
        rules_and_limitations="The segments are held together by Renji's own spiritual power rather "
            "than the physical thread used in Shikai, letting him detach and reform them at will. Its "
            "signature technique, Hikotsu Taiho, fires a dense blast of energy from the mouth but "
            "drains a significant portion of his spiritual power each time.",
        evolution_notes="Achieved specifically during the Soul Society arc, after Renji's first defeat "
            "at Byakuya's hands convinces him he needs to grow stronger to save Rukia.",
    )
    create_power(
        toshiro_id, "shikai",
        "Hyorinmaru, released with the command Reign over the frosted heavens. Sealed as an unusually "
        "long katana with a star shaped guard. In Shikai the blade extends slightly and gains a "
        "crescent shaped ice blade attached by a long chain that can extend at will.",
        rules_and_limitations="Regarded as the strongest ice type Zanpakuto in Soul Society, freezing "
            "anything it touches without needing ambient water to be present. Toshiro is skilled "
            "enough that he rarely needs to use even this form, relying on Hyorinmaru's sealed state "
            "for most fights.",
        evolution_notes="Later develops additional ice techniques by combining Hyorinmaru with "
            "Rangiku's Haineko.",
    )
    create_power(
        toshiro_id, "bankai",
        "Daiguren Hyorinmaru, already attained by this point in the story despite rarely being shown "
        "or used this early, giving Toshiro a pair of ice wings and dramatically amplifying his ice "
        "abilities.",
        rules_and_limitations="Considered one of the most powerful Bankai among the captains, "
            "achieved at an unusually young age, one of the reasons Toshiro became the youngest "
            "captain in Gotei 13 history.",
        evolution_notes="Later lost entirely to a Sternritter during the Thousand Year Blood War, "
            "forcing him to fight using only creative applications of his Shikai.",
    )
    create_power(
        rangiku_id, "shikai",
        "Haineko, whose Shikai turns the entire blade into a cloud of ash that Rangiku can direct and "
        "manipulate at will, using it to cut from a distance or obscure an opponent's vision.",
        rules_and_limitations="No Bankai has ever been shown or confirmed for Haineko, unusual among "
            "long serving lieutenants, Rangiku rarely discusses why.",
        evolution_notes="Later combined with Toshiro's Hyorinmaru to create a vacuum ice technique "
            "neither Zanpakuto could produce alone.",
    )
    create_power(
        soifon_id, "shikai",
        "Suzumebachi, released with the command Sting all enemies to death. Shrinks into a black and "
        "gold gauntlet with a stinger worn on her middle finger. Striking the same spot on a target "
        "twice is lethal.",
        rules_and_limitations="The mark left by the first strike, called the hornet's crest, can be "
            "held in place for as long as Soi Fon wishes, waiting for the right moment to land the "
            "second, fatal blow to the same spot.",
        evolution_notes="Soi Fon can also use her poison defensively, stabbing herself with Suzumebachi "
            "to counteract a separate toxin already in her system.",
    )
    create_power(
        soifon_id, "bankai",
        "Jakuho Raikoben, already attained though rarely used or shown this early. Encases her right "
        "arm and shoulder in a golden missile launcher, converting her from a close range assassin "
        "into a long range weapon for a single, devastating shot.",
        rules_and_limitations="Requires anchoring herself to a fixed structure beforehand to absorb "
            "the recoil, and can normally only be fired once every three days without seriously "
            "draining her. Soi Fon considers relying on it an affront to her pride as an assassin, "
            "which is why she avoids using it.",
        evolution_notes="Remains one of the least seen Bankai in the entire series specifically "
            "because of how rarely she chooses to use it.",
    )
    create_power(
        yamamoto_id, "shikai",
        "Ryujin Jakka, the oldest and most powerful fire type Zanpakuto in Soul Society. Sealed as a "
        "plain wooden cane, disguising its true form. Released with the command All things in the "
        "universe turn to ashes, engulfing Yamamoto and the surrounding area in flame.",
        rules_and_limitations="The flames can be controlled with great precision to strike only "
            "chosen targets, and resealing the Zanpakuto does not extinguish flames already in "
            "motion. Its Shikai alone is powerful enough to fight two captains simultaneously.",
        evolution_notes="Yamamoto's Bankai is deliberately kept unknown for nearly the entire story, "
            "only revealed as Zanka no Tachi far beyond this vertical slice's Soul Society arc scope.",
    )
    create_power(
        gin_id, "shikai",
        "Shinso, released with the command Shoot to kill. Extends to an extraordinary length at "
        "extreme speed to pierce a target from a distance most opponents assume is out of range.",
        rules_and_limitations="Its true, far more dangerous ability, a poison that breaks down cells "
            "on contact, is deliberately withheld here since it is not revealed until long after this "
            "point in the story.",
        evolution_notes="The full nature of Shinso is only revealed near the end of Gin's own arc, "
            "well beyond this vertical slice's scope.",
    )
    create_power(
        kira_id, "shikai",
        "Wabisuke, released with the command Raise your head. An ordinary looking katana whose blade "
        "bends into an L shaped hook on release, with the cutting edge on the inside of the angle.",
        rules_and_limitations="Anything Wabisuke strikes doubles in weight, and the effect compounds "
            "with repeated hits, three strikes make a target eight times heavier, a fourth makes it "
            "sixteen times heavier. The weight increase vanishes once Kira's Shikai deactivates. No "
            "Bankai has been shown for Wabisuke.",
        evolution_notes="Kira later loses this Zanpakuto and is reconstructed with different "
            "abilities far beyond this vertical slice's scope.",
    )
    create_power(
        omaeda_id, "shikai",
        "Gegetsuburi, released into a massive spiked iron ball on a heavy chain capable of crushing "
        "bone with a single hit.",
        rules_and_limitations="The sheer size and weight of the weapon makes it slow to swing "
            "compared to a standard blade, though Omaeda's own considerable strength compensates for "
            "this. No Bankai has been shown for Gegetsuburi.",
        evolution_notes="Omaeda is frequently underestimated because of his personality, despite "
            "Gegetsuburi being a genuinely dangerous weapon in a real fight.",
    )
    create_power(
        sasakibe_id, "shikai",
        "Gonryomaru, released with the command Pierce. Sealed as an ornate katana with a double fanned "
        "guard, its Shikai transforms it into a rapier strong enough to pierce even powerful opponents.",
        rules_and_limitations="Favors precision, thrusting attacks over broad cutting strikes, "
            "reflecting Sasakibe's own quiet, disciplined character.",
        evolution_notes="Sasakibe is one of only two lieutenants in the Gotei 13, alongside Renji, "
            "known to have attained Bankai, Koko Gonryo Rikyu, which summons a dome of lightning from "
            "pillars driven into the ground, though it is not shown on screen until far later in the "
            "story, immediately before his death in the Thousand Year Blood War.",
    )
    print("  Created 21 powers.")

    print()
    print("Seeding complete. Character ids for reference:")
    print(f"  Ichigo:    {ichigo_id}")
    print(f"  Rukia:     {rukia_id}")
    print(f"  Byakuya:   {byakuya_id}")
    print(f"  Orihime:   {orihime_id}")
    print(f"  Sado:      {sado_id}")
    print(f"  Uryu:      {uryu_id}")
    print(f"  Yoruichi:  {yoruichi_id}")
    print(f"  Renji:     {renji_id}")
    print(f"  Toshiro:   {toshiro_id}")
    print(f"  Rangiku:   {rangiku_id}")
    print(f"  Soi Fon:   {soifon_id}")
    print(f"  Yamamoto:  {yamamoto_id}")
    print(f"  Gin:       {gin_id}")
    print(f"  Kira:      {kira_id}")
    print(f"  Omaeda:    {omaeda_id}")
    print(f"  Sasakibe:  {sasakibe_id}")
    print()
    print(f"Try it out: GET {BASE_URL}/characters/{ichigo_id}/full")


if __name__ == "__main__":
    main()