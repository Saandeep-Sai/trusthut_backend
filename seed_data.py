"""
TrustHut Hyderabad Seed Data Script
Usage:
  python seed_data.py          → inserts only (skips if already seeded)
  python seed_data.py --reset  → deletes old seed posts then re-inserts
"""

import uuid, os, sys, django, random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trusthut_backend.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from apps.core.firebase import get_firestore_client
from apps.core.config import POSTS_COLLECTION

def days_ago(n):
    return (datetime.utcnow() - timedelta(days=n)).isoformat()

# ─────────────────────────────────────────────────────────────────────────────
# All media_url values use LoremFlickr keyword API.
# Format: https://loremflickr.com/800/500/<keyword1>,<keyword2>,...
# LoremFlickr returns real Flickr CC photos matching those keywords.
# ─────────────────────────────────────────────────────────────────────────────
POSTS = [

    # ── UNSAFE HIGHWAYS ──────────────────────────────────────────────────────
    {
        "title": "Severe Pothole Cluster — Mehdipatnam Flyover",
        "description": "Multiple large potholes have formed on the approach to the Mehdipatnam flyover. Three two-wheelers have skidded here in the past week. The craters are about 8–10 inches deep and span almost the full lane width. Avoid left lane completely.",
        "location_name": "Mehdipatnam Flyover, Hyderabad",
        "latitude": 17.3960, "longitude": 78.4385,
        "accessibility_type": "general", "risk_level": "unsafe",
        "post_type": "highway", "risk_category": "bad_road", "route_name": "NH-65",
        "media_url": "https://loremflickr.com/800/500/pothole,road,damage",
        "created_at": days_ago(2),
    },
    {
        "title": "Blind Sharp Turn — Tolichowki Underpass Exit",
        "description": "The exit ramp from the Tolichowki underpass curves sharply to the right with almost zero visibility. No signage warning of the bend. Buses frequently cross the centre line here. Approach slowly and use horn.",
        "location_name": "Tolichowki Underpass, Hyderabad",
        "latitude": 17.4042, "longitude": 78.4212,
        "accessibility_type": "general", "risk_level": "unsafe",
        "post_type": "highway", "risk_category": "sharp_turn", "route_name": "Tolichowki–Mehdipatnam Rd",
        "media_url": "https://loremflickr.com/800/500/curve,road,dangerous",
        "created_at": days_ago(5),
    },
    {
        "title": "Broken Street Lights — PVNR Expressway (Night Danger)",
        "description": "A 2 km stretch between the Rajendra Nagar and Attapur exits of the PVNR Expressway has no functional street lighting. Complete darkness after 9 PM. Cattle have been spotted on the road at night multiple times.",
        "location_name": "PVNR Expressway, Rajendra Nagar Side, Hyderabad",
        "latitude": 17.3610, "longitude": 78.4480,
        "accessibility_type": "general", "risk_level": "unsafe",
        "post_type": "highway", "risk_category": "no_lighting", "route_name": "PVNR Expressway",
        "media_url": "https://loremflickr.com/800/500/dark,highway,night",
        "created_at": days_ago(1),
    },
    {
        "title": "Accident-Prone Intersection — LB Nagar X Roads",
        "description": "The LB Nagar X roads see at least 2–3 accidents per week. Signal timing is broken — the green light for the Vanasthalipuram side stays on too long. Approaching vehicles from Vijayawada highway do not slow down sufficiently.",
        "location_name": "LB Nagar X Roads, Hyderabad",
        "latitude": 17.3472, "longitude": 78.5506,
        "accessibility_type": "general", "risk_level": "unsafe",
        "post_type": "highway", "risk_category": "accident", "route_name": "NH-65 (LB Nagar)",
        "media_url": "https://loremflickr.com/800/500/accident,road,crash",
        "created_at": days_ago(3),
    },
    {
        "title": "Waterlogged Road — Attapur Bridge After Rain",
        "description": "The low bridge near Attapur accumulates water up to 1.5 feet during even moderate rainfall. Drainage is completely blocked. At least one car stalled here last week during the evening downpour. Do not attempt if water is visible.",
        "location_name": "Attapur Bridge, Hyderabad",
        "latitude": 17.3742, "longitude": 78.4389,
        "accessibility_type": "general", "risk_level": "unsafe",
        "post_type": "highway", "risk_category": "bad_road", "route_name": "Attapur–Mehdipatnam Road",
        "media_url": "https://loremflickr.com/800/500/flooded,road,water",
        "created_at": days_ago(1),
    },
    {
        "title": "ORR Exit 14 — Surface Erosion and Crash Risk",
        "description": "The exit 14 deceleration lane on the Outer Ring Road near Patancheru has severe surface erosion. The road edge has crumbled, reducing lane width by 40%. Trucks exiting at speed have very little margin for error.",
        "location_name": "ORR Exit 14, Patancheru, Hyderabad",
        "latitude": 17.5280, "longitude": 78.2930,
        "accessibility_type": "general", "risk_level": "unsafe",
        "post_type": "highway", "risk_category": "bad_road", "route_name": "Outer Ring Road (ORR)",
        "media_url": "https://loremflickr.com/800/500/road,erosion,damaged",
        "created_at": days_ago(6),
    },
    {
        "title": "Kukatpally Y-Junction — Signal Failure",
        "description": "The traffic signal at the Kukatpally Y-junction has been non-functional for 4 days. This junction handles three-way traffic from KPHB, JNTU, and Miyapur directions. Rush-hour near-misses are happening constantly.",
        "location_name": "Kukatpally Y-Junction, Hyderabad",
        "latitude": 17.4948, "longitude": 78.3996,
        "accessibility_type": "general", "risk_level": "unsafe",
        "post_type": "highway", "risk_category": "accident", "route_name": "Kukatpally Main Road",
        "media_url": "https://loremflickr.com/800/500/traffic,signal,junction",
        "created_at": days_ago(4),
    },
    {
        "title": "Gachibowli Flyover — Road Divider Gap",
        "description": "There is a 3-metre gap in the central road divider on the Gachibowli flyover. Two-wheelers are making illegal U-turns through this gap at high speed. One collision has already occurred this week. Extremely dangerous.",
        "location_name": "Gachibowli Flyover, Hyderabad",
        "latitude": 17.4401, "longitude": 78.3489,
        "accessibility_type": "general", "risk_level": "unsafe",
        "post_type": "highway", "risk_category": "accident", "route_name": "Gachibowli–Financial District Road",
        "media_url": "https://loremflickr.com/800/500/highway,flyover,barrier",
        "created_at": days_ago(2),
    },
    {
        "title": "ORR Miyapur Stretch — Night Fog + No Cats' Eyes",
        "description": "The ORR stretch between Miyapur and Bachupally is notorious for dense fog during winter mornings. Road reflectors (cats' eyes) are completely missing for nearly 4 km. Speed limit signs are also absent. High accident risk at dawn.",
        "location_name": "ORR Miyapur–Bachupally, Hyderabad",
        "latitude": 17.5108, "longitude": 78.3624,
        "accessibility_type": "general", "risk_level": "unsafe",
        "post_type": "highway", "risk_category": "no_lighting", "route_name": "ORR (Miyapur Section)",
        "media_url": "https://loremflickr.com/800/500/fog,road,night,visibility",
        "created_at": days_ago(9),
    },
    {
        "title": "Nagole Junction — Frequent Rear-End Accidents",
        "description": "The Nagole junction approach from Uppal side has a sudden lane narrowing. The reduction from 4 lanes to 2 occurs within 80 metres with no advance warning signs. Rear-end collisions happen almost daily in the evening.",
        "location_name": "Nagole Junction, Hyderabad",
        "latitude": 17.3854, "longitude": 78.5618,
        "accessibility_type": "general", "risk_level": "unsafe",
        "post_type": "highway", "risk_category": "accident", "route_name": "Uppal–Nagole Road",
        "media_url": "https://loremflickr.com/800/500/accident,car,collision",
        "created_at": days_ago(2),
    },

    # ── MODERATE HIGHWAYS ─────────────────────────────────────────────────────
    {
        "title": "Heavy Congestion — Panjagutta Circle Morning Peak",
        "description": "Panjagutta circle becomes completely grid-locked between 8:30 AM and 10:30 AM. Traffic backs up over 1.5 km toward Punjagutta metro. U-turn vehicles from Greenlands Road make it significantly worse.",
        "location_name": "Panjagutta Circle, Hyderabad",
        "latitude": 17.4239, "longitude": 78.4490,
        "accessibility_type": "general", "risk_level": "moderate",
        "post_type": "highway", "risk_category": "congestion", "route_name": "Raj Bhavan Road",
        "media_url": "https://loremflickr.com/800/500/traffic,jam,congestion",
        "created_at": days_ago(4),
    },
    {
        "title": "Kondapur Signal — Sharp Right Turn Unmarked",
        "description": "The right turn from the Kondapur main signal toward Botanical Garden road is extremely sharp and poorly lit. No cautionary road markings. Two-wheelers frequently skid on gravel left by construction vehicles.",
        "location_name": "Kondapur Signal, Hyderabad",
        "latitude": 17.4585, "longitude": 78.3647,
        "accessibility_type": "general", "risk_level": "moderate",
        "post_type": "highway", "risk_category": "sharp_turn", "route_name": "Kondapur Main Road",
        "media_url": "https://loremflickr.com/800/500/sharp,bend,road",
        "created_at": days_ago(8),
    },
    {
        "title": "Hitech City Underpass — Evening Congestion",
        "description": "The underpass near Hitech City cyber towers experiences severe congestion between 6–9 PM daily. The entry narrows from two lanes to one due to a badly parked food stall on the left. Average wait time exceeds 20 minutes.",
        "location_name": "Hitech City Underpass, Hyderabad",
        "latitude": 17.4474, "longitude": 78.3762,
        "accessibility_type": "general", "risk_level": "moderate",
        "post_type": "highway", "risk_category": "congestion", "route_name": "Mindspace Road",
        "media_url": "https://loremflickr.com/800/500/tunnel,traffic,underpass",
        "created_at": days_ago(9),
    },
    {
        "title": "Madhapur Junction — Road Surface Deterioration",
        "description": "The main road at Madhapur junction has developed cracks and surface depressions over a 400m stretch. Heavy IT-sector bus traffic has accelerated the damage. Avoid the leftmost lane heading toward Peddamma temple road.",
        "location_name": "Madhapur Junction, Hyderabad",
        "latitude": 17.4514, "longitude": 78.3929,
        "accessibility_type": "general", "risk_level": "moderate",
        "post_type": "highway", "risk_category": "bad_road", "route_name": "Madhapur Main Road",
        "media_url": "https://loremflickr.com/800/500/cracked,asphalt,road",
        "created_at": days_ago(10),
    },
    {
        "title": "Shamshabad Road — No Lighting Near Airport Approach",
        "description": "The 3 km stretch on the old Shamshabad road before the RGIA airport approach has no working streetlights. Trucks parked on the shoulder are virtually invisible at night. Extremely hazardous for unfamiliar drivers.",
        "location_name": "Shamshabad–Airport Road, Hyderabad",
        "latitude": 17.2403, "longitude": 78.4294,
        "accessibility_type": "general", "risk_level": "moderate",
        "post_type": "highway", "risk_category": "no_lighting", "route_name": "Airport Road",
        "media_url": "https://loremflickr.com/800/500/dark,street,night,lamp",
        "created_at": days_ago(7),
    },
    {
        "title": "Manikonda Road — Severe Pothole Damage",
        "description": "The road connecting Manikonda to the Financial District has at least 15 large potholes in a 600m stretch. After recent rains they are filled with water, making depth estimation impossible. Several vehicles have suffered tyre and axle damage.",
        "location_name": "Manikonda–Financial District Road, Hyderabad",
        "latitude": 17.4067, "longitude": 78.3882,
        "accessibility_type": "general", "risk_level": "moderate",
        "post_type": "highway", "risk_category": "bad_road", "route_name": "Manikonda Road",
        "media_url": "https://loremflickr.com/800/500/pothole,water,road",
        "created_at": days_ago(4),
    },

    # ── UNSAFE PLACES ─────────────────────────────────────────────────────────
    {
        "title": "Broken Footpath — Banjara Hills Rd No. 12",
        "description": "The footpath alongside Road No. 12 in Banjara Hills has large slabs that are broken and upturned. Wheelchair users cannot pass at all. Elderly pedestrians have tripped here. The damage extends roughly 200 metres.",
        "location_name": "Road No. 12, Banjara Hills, Hyderabad",
        "latitude": 17.4228, "longitude": 78.4488,
        "accessibility_type": "wheelchair", "risk_level": "unsafe",
        "post_type": "place", "risk_category": "", "route_name": "",
        "media_url": "https://loremflickr.com/800/500/broken,pavement,sidewalk",
        "created_at": days_ago(11),
    },
    {
        "title": "Open Manhole — Abids Main Road",
        "description": "An open manhole without any cover or warning marking in the middle of the footpath on Abids main road. The drop is approximately 4 feet. A child almost fell in yesterday evening. Needs immediate barricading and cover restoration.",
        "location_name": "Abids Main Road, Hyderabad",
        "latitude": 17.3938, "longitude": 78.4760,
        "accessibility_type": "general", "risk_level": "unsafe",
        "post_type": "place", "risk_category": "", "route_name": "",
        "media_url": "https://loremflickr.com/800/500/manhole,street,open",
        "created_at": days_ago(3),
    },
    {
        "title": "Broken Tactile Path — Ameerpet Metro Entrance",
        "description": "The tactile (yellow) paving tiles guiding visually impaired commuters at the Ameerpet metro entrance have been shattered by construction vehicles. Visually impaired users are now navigating without guidance in a high-footfall zone.",
        "location_name": "Ameerpet Metro Station, Hyderabad",
        "latitude": 17.4375, "longitude": 78.4488,
        "accessibility_type": "wheelchair", "risk_level": "unsafe",
        "post_type": "place", "risk_category": "", "route_name": "",
        "media_url": "https://loremflickr.com/800/500/construction,sidewalk,damage",
        "created_at": days_ago(5),
    },
    {
        "title": "Crumbling Footbridge — Koti Women's College Area",
        "description": "The pedestrian footbridge near Koti Women's College has severe concrete spalling. Metal rebar is exposed on the handrails and mid-section. Multiple pedestrians have reported cuts from exposed rebar edges. Emergency repair required.",
        "location_name": "Koti, Hyderabad",
        "latitude": 17.3820, "longitude": 78.4836,
        "accessibility_type": "elder", "risk_level": "unsafe",
        "post_type": "place", "risk_category": "", "route_name": "",
        "media_url": "https://loremflickr.com/800/500/bridge,concrete,crumbling",
        "created_at": days_ago(6),
    },

    # ── MODERATE PLACES ───────────────────────────────────────────────────────
    {
        "title": "No Ramp Access — Jubilee Hills Check Post Metro Exit",
        "description": "The Jubilee Hills Check Post metro station exit has no ramp for wheelchair or stroller access. Only steep stairs. Despite repeated complaints, no temporary ramp has been installed. Wheelchair users are forced to take a 500m detour.",
        "location_name": "Jubilee Hills Check Post Metro Station, Hyderabad",
        "latitude": 17.4319, "longitude": 78.4108,
        "accessibility_type": "wheelchair", "risk_level": "moderate",
        "post_type": "place", "risk_category": "", "route_name": "",
        "media_url": "https://loremflickr.com/800/500/stairs,accessibility,metro",
        "created_at": days_ago(12),
    },
    {
        "title": "Elevator Out of Service — Hitech City Metro",
        "description": "The elevator at Hitech City metro station (Platform 1 side) has been non-functional for 11 days. Commuters with disabilities are forced to use narrow staircases with heavy crowds during peak hours. HMRL helpline has not responded.",
        "location_name": "Hitech City Metro Station, Hyderabad",
        "latitude": 17.4435, "longitude": 78.3773,
        "accessibility_type": "elder", "risk_level": "moderate",
        "post_type": "place", "risk_category": "", "route_name": "",
        "media_url": "https://loremflickr.com/800/500/elevator,broken,repair",
        "created_at": days_ago(13),
    },
    {
        "title": "Overflowing Drain Blocking Footpath — Secunderabad",
        "description": "An overflowing storm drain near Paradise Circle in Secunderabad has completely blocked the pedestrian footpath. Pedestrians are walking on the main road creating a safety hazard. Strong odour also reported by local residents.",
        "location_name": "Paradise Circle, Secunderabad, Hyderabad",
        "latitude": 17.4408, "longitude": 78.4988,
        "accessibility_type": "general", "risk_level": "moderate",
        "post_type": "place", "risk_category": "", "route_name": "",
        "media_url": "https://loremflickr.com/800/500/drain,flood,street,water",
        "created_at": days_ago(14),
    },
    {
        "title": "Street Light Outage — Jubilee Hills Road No. 36",
        "description": "Six consecutive street lights have been non-functional on Road No. 36 since the last power surge. The area is a residential zone with heavy pedestrian movement after 8 PM. Multiple residents have reported feeling unsafe walking home.",
        "location_name": "Road No. 36, Jubilee Hills, Hyderabad",
        "latitude": 17.4278, "longitude": 78.4168,
        "accessibility_type": "general", "risk_level": "moderate",
        "post_type": "place", "risk_category": "", "route_name": "",
        "media_url": "https://loremflickr.com/800/500/streetlight,broken,dark",
        "created_at": days_ago(15),
    },
    {
        "title": "Footpath Encroachment — Begumpet Main Road",
        "description": "A row of tea and snack stalls have permanently encroached on the 5-foot-wide footpath on Begumpet main road near the airport road junction. Pedestrians, including wheelchair users, have zero walking space and are forced onto the road.",
        "location_name": "Begumpet Main Road, Hyderabad",
        "latitude": 17.4393, "longitude": 78.4689,
        "accessibility_type": "wheelchair", "risk_level": "moderate",
        "post_type": "place", "risk_category": "", "route_name": "",
        "media_url": "https://loremflickr.com/800/500/street,vendor,encroachment",
        "created_at": days_ago(18),
    },
]

# ─────────────────────────────────────────────────────────────────────────────
def delete_seed_data(db):
    """Remove all previously seeded admin posts."""
    print("🗑️  Deleting existing seed data (user_name = 'TrustHut Admin')...")
    docs = db.collection(POSTS_COLLECTION).where('user_name', '==', 'TrustHut Admin').stream()
    deleted = 0
    for doc in docs:
        doc.reference.delete()
        deleted += 1
    print(f"   Deleted {deleted} existing seed post(s).")

def seed(reset=False):
    db = get_firestore_client()

    if reset:
        delete_seed_data(db)
    else:
        existing = list(db.collection(POSTS_COLLECTION).where('user_name', '==', 'TrustHut Admin').limit(1).stream())
        if existing:
            print("⚠️  Seed data already exists. Run with --reset to delete and re-seed.")
            return

    print(f"\n🌱 Seeding {len(POSTS)} Hyderabad posts into Firestore...\n")
    for i, p in enumerate(POSTS):
        post_id = str(uuid.uuid4())
        doc = {
            "post_id": post_id,
            "user_id": "seed-admin-hyderabad",
            "user_name": "TrustHut Admin",
            "title": p["title"],
            "description": p["description"],
            "location_name": p["location_name"],
            "latitude": p["latitude"],
            "longitude": p["longitude"],
            "accessibility_type": p["accessibility_type"],
            "risk_level": p["risk_level"],
            "post_type": p["post_type"],
            "risk_category": p.get("risk_category", ""),
            "route_name": p.get("route_name", ""),
            "media_url": p["media_url"],
            "media_type": "image",
            "likes_count": random.randint(0, 45),
            "created_at": p["created_at"],
            "updated_at": p["created_at"],
        }
        db.collection(POSTS_COLLECTION).document(post_id).set(doc)
        print(f"  [{i+1:02d}/{len(POSTS)}] ✅ {p['title'][:60]}")

    print(f"\n🎉 Done! {len(POSTS)} posts inserted into '{POSTS_COLLECTION}'.")

if __name__ == "__main__":
    reset = "--reset" in sys.argv
    seed(reset=reset)
