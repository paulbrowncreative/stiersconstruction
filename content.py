# -*- coding: utf-8 -*-
"""All page content for stiersconstruction.com. Facts come from the existing site; anything general
(materials, permits, warning signs) is standard industry/regulatory knowledge, phrased conservatively."""

SITE = {
    'url': 'https://www.stiersconstruction.com',
    'name': 'Stier’s Construction',
    'seo_name': 'Stier’s Marine & Construction',
    'legal_alt': 'Stier’s Welding & Construction',
    'phone': '586-703-7214',
    'phone_e164': '+15867037214',
    'email': 'kevin@stiers-construction.com',
    'hours': 'Monday to Friday, 8am to 5pm. Weekends by appointment.',
    'instagram': 'https://www.instagram.com/stiers_marine_construction/',
    'facebook': 'https://www.facebook.com/p/Stiers-Marine-Construction-61584006766762/',
    'year': 2026,
    'built': '2026-09-20',
}

EGLE_LINK = 'https://www.michigan.gov/documents/egle/EGLE-WRD-FOS-FAQ-shore-protection-on-the-Great-Lakes_695201_7.pdf'

def ul(items, cls='checklist'):
    return '<ul class="%s">%s</ul>' % (cls, ''.join('<li>%s</li>' % i for i in items))

def group(title, items):
    return '<div class="group"><h3>%s</h3>%s</div>' % (title, ul(items))

def groups(*gs, cols=2):
    return '<div class="groups g%d">%s</div>' % (cols, ''.join(group(t, i) for t, i in gs))

def compare(rows):
    return '<div class="compare">%s</div>' % ''.join('<div><h3>%s</h3><p>%s</p></div>' % r for r in rows)

def note(html):
    return '<div class="note">%s</div>' % html

SERVICES = [
 dict(slug='seawalls', name='Seawalls', group='water',
  summary='Vinyl, steel, concrete and galvanized walls, plus repairs, caps and drainage.',
  hub_img='sheet-pile-excavator-canal-home',
  title='Seawall Installation & Repair in Metro Detroit | Stier’s',
  desc='Vinyl, steel, concrete and galvanized seawalls installed and repaired on Lake St. Clair and the Detroit River. Owner-led crew. Free quotes.',
  h1='Seawall installation and repair on Lake St. Clair and the Detroit River',
  lead='A seawall holds your lot in place and protects your property from erosion and structural damage. We install new walls in vinyl, steel, concrete and galvanized systems, and repair, cap and drain the ones you already have.',
  checks=['Vinyl, steel, concrete, galvanized', 'Repairs, caps, splash guards', 'French drains', 'Homes, businesses, marinas'],
  hero_img='sheet-pile-excavator-canal-home',
  sections=[
   dict(id='what', h2='What we do', html=groups(
     ('Seawall installation', ['Vinyl seawalls', 'Steel seawalls', 'Concrete seawalls', 'Galvanized seawalls', 'New walls and full replacements']),
     ('Repair and maintenance', ['Seam repair', 'Cap replacement or patching', 'Splash guards to cut erosion and water intrusion', 'French drains installed or maintained', 'Regular maintenance to prevent costly repairs'])) +
     '<p class="mt-m measure">Every wall is built for marine conditions, with attention to alignment and long-term durability. Every project starts with careful planning, quality materials and attention to detail. We work for homeowners, commercial property owners and marinas. Regular maintenance helps prevent costly repairs while preserving structural integrity, and every repair starts with a careful inspection.</p>'),
   dict(id='materials', h2='Which seawall material fits your shoreline?', html=
     '<p class="measure">Each system has trade-offs. This is how we think about them at a glance:</p>' + compare([
      ('Vinyl', 'Lightweight and corrosion-proof. A common choice on residential shorelines and canals with moderate loads.'),
      ('Steel', 'Strong under heavy loads and in deeper water. Needs corrosion protection over its life.'),
      ('Galvanized steel', 'Steel with a zinc coating that slows corrosion in wet, marine conditions.'),
      ('Concrete', 'Massive and long-lived. Heavier to build and usually needs more equipment access.')]) +
     '<div class="mt-m">' + note('<p>The right material depends on soil, water depth, what the wall has to carry, and access to the site. Send us your address and a few photos and we will talk through the options for your shoreline.</p>') + '</div>'),
   dict(id='signs', h2='Signs your seawall needs attention', html=
     ul(['The wall leans, bows or has shifted', 'Soil is sinking or you can see voids behind the wall', 'Seams are open or separating', 'The cap is cracked, loose or missing', 'Erosion is starting at the ends of the wall', 'Water pools near the wall after rain']) +
     '<div class="prose mt-m"><p>Water pressure builds behind a wall that cannot drain. That is why we install and maintain French drains: relieving pressure protects the wall and the yard behind it.</p><p>Caught early, seam repair, cap work and drainage can extend a sound wall’s life. A wall that has lost its footing usually has to be replaced. The reliable way to know is to have it looked at.</p></div>'),
   dict(id='permits', h2='Permits for seawall work', html=
     '<div class="prose"><p>Building or replacing a seawall on Lake St. Clair generally requires a permit from Michigan EGLE, and often from the U.S. Army Corps of Engineers, through a single Joint Permit Application. Some like-for-like repairs can qualify for expedited review, and local rules may also apply. Read EGLE’s <a href="%s" target="_blank" rel="noopener">shoreline protection permit guidance (PDF)</a>, and confirm what your site needs before work starts.</p></div>' % EGLE_LINK),
  ],
  gallery=['sheet-pile-staging-seawall', 'vibratory-hammer-steel-pile', 'new-deck-over-seawall'],
  faqs=[
   ('How do I know if my seawall needs repair or replacement?', '<p>Warning signs include a wall that leans or bows, sinking soil or voids behind it, open seams, a cracked or missing cap, and erosion at the wall ends. Repairs can extend the life of a sound wall; a wall that has moved or lost its footing usually needs replacement. The dependable way to tell is to have someone inspect it, so send photos or request a quote.</p>'),
   ('Which seawall material should I choose?', '<p>We install vinyl, steel, concrete and galvanized systems. Soil, water depth, the loads on the wall and site access decide which one fits. See the comparison above, then send your address and photos.</p>'),
   ('Do you repair seawalls, or only build new ones?', '<p>Both. Repairs include seams, cap replacement or patching, splash guards and French drains, and we offer regular maintenance to catch problems early.</p>'),
   ('Do I need a permit to build or replace a seawall?', '<p>Usually. Work on Great Lakes waters, including Lake St. Clair, generally needs an EGLE permit and often a U.S. Army Corps of Engineers permit. Rules differ by waterway and by the type of work, so check with EGLE for your site.</p>'),
  ],
  related=['pilings', 'docks', 'dredging', 'excavating-grading', 'concrete']),

 dict(slug='docks', name='Docks', group='water',
  summary='Floating, fixed and custom docks. Repairs, decking upgrades and removal.',
  hub_img='wood-dock-yellow-flag',
  title='Dock Installation & Repair in Metro Detroit | Stier’s',
  desc='Floating, fixed and custom docks built, repaired and removed on Lake St. Clair and the Detroit River. Residential, commercial and marina work.',
  h1='Dock construction, repair and removal in Metro Detroit',
  lead='Floating docks, fixed docks and custom designs, built to handle Lake St. Clair and Detroit River conditions and to give you safe, easy access to the water.',
  checks=['Floating and fixed docks', 'Custom and specialty designs', 'Structural repair, re-decking', 'Dock removal'],
  hero_img='wood-dock-yellow-flag',
  sections=[
   dict(id='what', h2='What we do', html=groups(
     ('Dock installation', ['Floating docks', 'Fixed docks', 'Specialty and custom docks']),
     ('Repair and maintenance', ['Structural repairs', 'Decking upgrades', 'Dock removal', 'Routine maintenance to major repairs'])) +
     '<p class="mt-m measure">We work closely with you on a dock that is durable, functional and visually appealing, for residential, commercial and marina clients. Each dock is built to withstand marine conditions while giving you safe, easy access to the water, with skilled craftsmanship, quality materials and attention to long-term performance. Fixed docks and many other structures stand on pilings, which we also install and remove.</p>'),
   dict(id='types', h2='Floating, fixed or custom?', html=compare([
     ('Floating dock', 'Rises and falls with the water level, so it suits waterways where levels change.'),
     ('Fixed dock', 'Sits on pilings at a set height and feels solid underfoot.'),
     ('Custom dock', 'Designed around an irregular shoreline, a marina layout or a commercial need that a standard dock will not meet.')]) +
     '<div class="mt-m">' + note('<p>Water depth, exposure to waves and boat traffic, and how you use the dock decide the right type. We are happy to talk it through before you commit.</p>') + '</div>'),
  ],
  gallery=['l-shaped-dock-choppy-water', 'gray-dock-walkway-canal', 'dock-work-through-ice'],
  faqs=[
   ('Should I choose a floating dock or a fixed dock?', '<p>A floating dock moves with the water level; a fixed dock stays at one height on pilings. We install both, plus custom designs, so the choice comes down to your water depth, exposure and how you use the dock.</p>'),
   ('Can you repair or re-deck my existing dock?', '<p>Yes. We handle structural repairs and decking upgrades. If a dock is beyond repair, we can remove it and build a new one.</p>'),
   ('Do I need a permit for a dock?', '<p>Often. Permit rules depend on the waterway and on whether the dock is seasonal or permanent, so check with EGLE before building. Send us your address and we can talk through what is typical.</p>'),
  ],
  related=['pilings', 'boat-hoists', 'seawalls', 'decks']),

 dict(slug='pilings', name='Pilings', group='water',
  summary='Steel and wood pilings, piling covers and removal.',
  hub_img='excavator-barge-timber-pilings',
  title='Piling Installation & Removal | Metro Detroit | Stier’s',
  desc='Steel and wood pilings for docks, seawalls, piers and retaining walls, plus piling covers and removal. Custom pile design available.',
  h1='Piling installation and removal for docks, seawalls and marine structures',
  lead='Pilings anchor the structures on your waterfront. We install, cover and remove steel and wood pilings for residential, commercial and marina projects.',
  checks=['Steel and wood pilings', 'Seawall, dock, pier, retaining wall', 'Piling covers', 'Removal of old pilings'],
  hero_img='excavator-barge-timber-pilings',
  sections=[
   dict(id='what', h2='What we do', html=groups(
     ('Installation', ['Steel pilings', 'Wood pilings', 'Seawall pilings', 'Dock and pier pilings', 'Retaining wall pilings', 'Marine anchoring and support', 'Custom pile design and engineering']),
     ('Protection and removal', ['Piling covers to protect your investment and extend its life', 'Steel piling removal', 'Wood piling removal', 'A single piling or an entire structure'])) +
     '<p class="mt-m measure">We provide reliable anchoring and support to keep docks, seawalls and waterfront structures secure in all conditions, and we tailor each installation to the needs of the site. From planning to completion, we focus on durability, precision and safety.</p>'),
   dict(id='choose', h2='Steel or wood?', html='<div class="prose"><p>Both are proven. Wood is a traditional choice for many docks. Steel is stronger and is used where loads and conditions are demanding, including seawall and retaining-wall pilings. What the piling supports and the ground it is driven into decide the answer.</p><p>Pilings work on a barge or from shore depending on the site. Our photos show both. Tell us about your project and we will recommend an approach.</p></div>'),
  ],
  gallery=['pipe-pilings-barge-sunset', 'excavator-pipe-pilings-dusk', 'barge-boathouse-excavator'],
  faqs=[
   ('Do you install both steel and wood pilings?', '<p>Yes. We install steel and wood pilings for docks, seawalls, piers and retaining walls, and can also provide custom pile design and engineering for projects with unique requirements.</p>'),
   ('What are piling covers?', '<p>Covers that fit over the top of a piling to protect it. We offer them to protect your investment and extend its lifespan.</p>'),
   ('Can you pull out old or damaged pilings?', '<p>Yes. We remove steel and wood pilings, from a single piling to an entire structure, and work to limit disruption to the surrounding area.</p>'),
  ],
  related=['docks', 'seawalls', 'boat-hoists', 'welding-fabrication']),

 dict(slug='boat-hoists', name='Boat hoists', group='water',
  summary='Installs, cable changes, motor service and welding repairs.',
  hub_img='boat-house-hoist-tarped-boat',
  title='Boat Hoist Installation & Repair | Metro Detroit | Stier’s',
  desc='Boat hoist installs and maintenance: boat house hoists, elevator, 4-point, 8-point, PWC lifts and davits. Cable, motor and welding service.',
  h1='Boat hoist installation, repair and maintenance',
  lead='From jet ski lifts to boat house hoists for 35 to 40 foot boats, we install lifts and keep them working: cables, motors and welded frames.',
  checks=['Boat house, elevator, 4- and 8-point', 'PWC lifts and davits', 'Cable and motor service', 'In-house welding repairs'],
  hero_img='boat-house-hoist-tarped-boat',
  sections=[
   dict(id='sizes', h2='Match the lift to your boat', html='__SIZECHART__'),
   dict(id='types', h2='Lift types explained', html=compare([
     ('Boat house hoist', 'Built into a covered boat house structure so the boat is stored out of the water, protected from weather and corrosion. Ideal for boats up to 35 to 40 feet, with maximum protection and convenient storage, especially for seasonal or long-term use.'),
     ('Elevator lift', 'Uses vertical movement to raise and lower your boat, often paired with a dock platform. Great for boats up to 30 feet, ideal when dock space is limited or the waterfront is tight, with smooth, controlled lifting for boats that launch often.'),
     ('4-point lift', 'Supports the boat at four contact points along the hull, evenly distributing weight for smaller boats. Best for boats up to 25 feet, including runabouts, center consoles and fishing boats. Compact, economical and simple to operate.'),
     ('8-point lift', 'Eight contact points along the hull give extra support for larger boats and wider beams. Typically used for boats 30 to 40 feet, including larger cruisers and pontoon boats, reducing stress on the hull and adding stability.'),
     ('PWC lift', 'Designed for jet skis, WaveRunners and other small watercraft under 15 feet. Keeps your watercraft out of the water, reducing wear and preventing algae buildup. Lightweight and easy to operate.')])),
   dict(id='what', h2='Hoist installation and maintenance', html=groups(
     ('Installation', ['Boat house hoists', 'Elevator lifts', '4-point lifts', '8-point lifts', 'PWC (jet ski) lifts', 'Davits']),
     ('Maintenance', ['Cable change-out: worn or damaged cables replaced with quality materials and precise installation, so the lift operates safely and smoothly', 'Motor maintenance: motors inspected, cleaned, lubricated and serviced to prevent costly breakdowns and extend life', 'Welding maintenance: lift frames, supports and structural parts repaired or reinforced to keep the lift strong and reliable for years'])) +
     '<p class="mt-m measure">Because welding is in-house, frame and support repairs do not need a second contractor.</p>'),
  ],
  gallery=['boat-lift-covered-slip', 'welder-under-dock', 'covered-marina-walkway-sunset'],
  faqs=[
   ('Which boat hoist fits my boat?', '<p>Length is the starting point: PWC lifts for watercraft under 15 feet, 4-point lifts up to about 25 feet, elevator lifts up to about 30 feet, 8-point lifts for 30 to 40 foot boats, and boat house hoists for boats up to 35 to 40 feet. Weight, beam and hull shape matter too, so send us your boat’s details.</p>'),
   ('What is the difference between a 4-point and an 8-point lift?', '<p>A 4-point lift supports the hull at four contact points and suits smaller runabouts, center consoles and fishing boats. An 8-point lift spreads weight over eight points, which reduces hull stress and adds stability for larger cruisers and pontoon boats.</p>'),
   ('Can you service a hoist I already have?', '<p>Yes: cable change-out, motor maintenance and welding repairs to frames and supports.</p>'),
   ('When should hoist cables be replaced?', '<p>Replace cables that are frayed, kinked or corroded, or that no longer lift evenly. If you are not sure, ask us to take a look before the season starts.</p>'),
  ],
  related=['docks', 'welding-fabrication', 'pilings', 'seawalls']),

 dict(slug='dredging', name='Dredging', group='water',
  summary='Canal, marina and boat well dredging to restore depth.',
  hub_img='barge-excavator-canal',
  title='Canal, Marina & Boat Well Dredging | Metro Detroit | Stier’s',
  desc='Canal, marina and boat well dredging to restore water depth and navigation on Lake St. Clair and Detroit River waterways.',
  h1='Dredging for canals, marinas and boat wells',
  lead='When silt builds up, boats touch bottom and navigation gets harder. We remove sediment and debris to restore proper depth, planning each job to limit environmental impact.',
  checks=['Canal dredging', 'Marina dredging', 'Boat well dredging', 'Residential, commercial, marina'],
  hero_img='barge-excavator-canal',
  sections=[
   dict(id='what', h2='What we do', html=groups(
     ('Dredging services', ['Canal dredging', 'Marina dredging', 'Boat well dredging']),
     ('How the work is done', ['Sediment and debris removed efficiently', 'Depth and navigation restored', 'Planned to minimize environmental impact', 'Equipment matched to the job, including barge work'])) +
     '<p class="mt-m measure">We dredge for homeowners with a boat well or slip, commercial waterfront properties and marinas.</p>'),
   dict(id='signs', h2='Signs you may need dredging', html=ul(['Your boat touches bottom at the dock or in the slip', 'The propeller stirs up mud when you leave', 'Boats that used to clear easily now wait on higher water', 'Your canal or channel has visibly shoaled'])),
   dict(id='permits', h2='Permits for dredging', html='<div class="prose"><p>Dredging in waters connected to the Great Lakes, including Lake St. Clair, is regulated in Michigan through EGLE, and federal review by the U.S. Army Corps of Engineers may also apply. Check requirements for your site before work begins. EGLE’s <a href="%s" target="_blank" rel="noopener">shoreline permit guidance (PDF)</a> is a good place to start.</p></div>' % EGLE_LINK),
  ],
  gallery=['barge-open-water', 'barge-excavator-snow', 'pipe-pilings-barge-sunset'],
  faqs=[
   ('How do I know if my canal, marina or boat well needs dredging?', '<p>Common signs are your boat touching bottom, prop wash stirring up mud when you leave the dock, or a channel that has visibly built up sediment. If you are unsure, send us your address and a description.</p>'),
   ('Do I need a permit to dredge?', '<p>Generally yes. Dredging in Great Lakes waters, including Lake St. Clair, is regulated through EGLE, and Army Corps review may also apply. Confirm the requirements for your site before work starts.</p>'),
   ('Do you dredge for homeowners or just marinas?', '<p>Both, along with commercial waterfront properties: canal, marina and boat well dredging.</p>'),
  ],
  related=['seawalls', 'docks', 'pilings', 'boat-hoists']),

 dict(slug='welding-fabrication', name='Welding & fabrication', group='land',
  summary='Shop and mobile welding: rails, gates, frames and marine steel.',
  hub_img='welding-at-night-waterfront',
  title='Custom Welding & Fabrication in Metro Detroit | Stier’s',
  desc='MIG, TIG and stick welding, custom fabrication and mobile welding for residential, commercial and marine projects in Metro Detroit.',
  h1='Custom welding and fabrication in Metro Detroit',
  lead='Welding is central to what we do. We fabricate custom steel from design to finished product, in the shop and on site, for homes, businesses and the waterfront.',
  checks=['MIG, TIG and stick', 'Custom fabrication', 'Mobile welding on site', 'Commercial and residential'],
  hero_img='welding-shop-grinding-sparks',
  sections=[
   dict(id='what', h2='What we build and repair', html=groups(
     ('Fabrication', ['Custom fabrication from design to finished product', 'MIG, TIG and stick welding', 'Railings, gates and frames', 'Custom signs and metalwork', 'Installs, commercial and residential']),
     ('On-site and marine work', ['Mobile welding for commercial and residential projects', 'Construction maintenance: metal work and wood work', 'Structural repairs', 'Dock and boat hoist steel, including frame and support repairs'])) +
     '<p class="mt-m measure">Pieces are built with accuracy, durability and safety in mind, whether it is a simple modification or a complete custom build.</p>'),
  ],
  gallery=['steel-stair-railing-brick-home', 'steel-pool-gate', 'steel-table-frame-fabrication', 'rust-finish-steel-sign-arch', 'welders-frozen-shoreline', 'welder-helmet-sparks'],
  faqs=[
   ('Which welding processes do you use?', '<p>MIG, TIG and stick.</p>'),
   ('Do you offer mobile welding?', '<p>Yes. We bring welding to your site for commercial and residential projects.</p>'),
   ('Can you build something from my drawing or idea?', '<p>Yes. We handle custom fabrication from design to finished product, from a simple modification to a complete custom build.</p>'),
   ('Do you weld on docks and boat hoists?', '<p>Yes. Welding maintenance on hoists covers frames, supports and structural components, and we work on docks and waterfront steel too.</p>'),
  ],
  related=['boat-hoists', 'docks', 'decks', 'concrete']),

 dict(slug='excavating-grading', name='Excavating & grading', group='land',
  summary='Site prep, trenching, driveways, ponds and hauling.',
  hub_img='excavator-site-dusk',
  title='Excavating, Grading & Hauling in Metro Detroit | Stier’s',
  desc='Excavating, land clearing, grading, trenching, hauling and material delivery for residential, commercial and waterfront properties in Metro Detroit.',
  h1='Excavating, grading and site prep in Metro Detroit',
  lead='Good construction starts with the ground. We excavate, clear, grade and haul, and get your site ready for the next phase with proper drainage and a solid base.',
  checks=['Excavating and land clearing', 'Grading and trenching', 'Hauling with our own trucks', 'Topsoil, sand, gravel, stone'],
  hero_img='excavator-site-dusk',
  sections=[
   dict(id='what', h2='What we do', html=groups(
     ('Excavating', ['Rock excavation and removal', 'Land clearing', 'Residential excavating', 'Site prep excavating', 'Ponds']),
     ('Grading', ['Grading and leveling', 'Driveway grading', 'Site prep grading', 'Trenching and backfilling']),
     ('Hauling and disposal', ['Excavated material hauling', 'Equipment hauling', 'Soil and rock recycling', 'Debris and material removal']),
     ('Materials delivered', ['Topsoil', 'Sand', 'Gravel and crushed stone', 'Delivery and removal'])) +
     '<p class="mt-m measure">We are equipped for challenging ground conditions and work on residential, commercial and waterfront properties. Grading levels, slopes and prepares your site for construction, with proper drainage and a solid foundation for any project. Hauling runs on our own trucks. Need a building or slab taken down first? See <a href="/services/demolition/">demolition</a>.</p>'),
  ],
  gallery=['dump-trucks-yard', 'excavator-loading-dump-trailer', 'graded-gravel-yard-boathouse'],
  faqs=[
   ('Do you deliver topsoil, sand and gravel?', '<p>Yes. We supply and transport topsoil, sand, gravel and crushed stone, and can deliver or remove material with our own trucks.</p>'),
   ('Can you dig a pond?', '<p>Ponds are part of our excavating work, along with land clearing, residential excavating and site prep.</p>'),
   ('Do you grade driveways?', '<p>Yes. We grade and level driveways as well as building sites, and handle trenching and backfilling for utilities.</p>'),
   ('Can you handle rock or difficult ground?', '<p>Yes. Rock excavation and removal is part of what we do, and our team is equipped for challenging ground conditions.</p>'),
  ],
  related=['demolition', 'concrete', 'seawalls', 'decks']),

 dict(slug='demolition', name='Demolition', group='land',
  summary='Houses, garages, sheds and concrete, cleaned up and hauled.',
  hub_img='demolition-excavator-canal',
  title='Demolition & Concrete Removal in Metro Detroit | Stier’s',
  desc='Demolition of houses, garages, sheds and concrete in Metro Detroit, with debris removal and site cleanup handled by our own trucks.',
  h1='Demolition and concrete removal in Metro Detroit',
  lead='We take down structures of all sizes, haul the debris and leave a clean site ready for what comes next.',
  checks=['Houses, garages, sheds', 'Concrete removal', 'Debris hauling and cleanup', 'Residential and redevelopment'],
  hero_img='demolition-excavator-canal',
  sections=[
   dict(id='what', h2='What we take down', html=groups(
     ('Structures', ['Houses', 'Garages', 'Sheds', 'Concrete slabs, driveways, patios and foundations']),
     ('How the job runs', ['Planning and teardown', 'Debris removal and hauling', 'Site cleanup', 'Controlled equipment and methods to limit disruption nearby'])) +
     '<p class="mt-m measure">Each phase is handled with a focus on safety and clean results, whether it is a single garage or part of a larger site redevelopment. Prepping the lot after? We also do <a href="/services/excavating-grading/">excavating and grading</a> and <a href="/services/concrete/">new concrete</a>.</p>'),
  ],
  gallery=['stiers-excavator-demo-site', 'demolition-excavator-tanks', 'demolition-debris-pile', 'broken-concrete-slabs-canal'],
  faqs=[
   ('What can you demolish?', '<p>Houses, garages, sheds and concrete, including slabs, driveways, patios and foundations.</p>'),
   ('Do you haul away the debris?', '<p>Yes. The job covers teardown through debris removal and site cleanup, and we haul with our own trucks.</p>'),
   ('Do I need a permit to demolish a building?', '<p>Most cities and townships require a demolition permit, and utilities generally must be disconnected first. Check with your local building department before scheduling.</p>'),
  ],
  related=['excavating-grading', 'concrete', 'docks', 'decks']),

 dict(slug='concrete', name='Concrete', group='land',
  summary='Patios, drives and walks in four finishes, plus removal.',
  hub_img='new-concrete-patio',
  title='Concrete Installation & Removal in Metro Detroit | Stier’s',
  desc='Concrete patios, driveways and walkways in brushed, exposed aggregate, smooth trowel and stamped finishes, plus removal and hauling.',
  h1='Concrete installation and removal in Metro Detroit',
  lead='New patios, driveways, walkways and slabs in the finish you want, and removal of the old concrete when it is time to start over.',
  checks=['Brushed, aggregate, trowel, stamped', 'Patios, drives, walks, slabs', 'Concrete removal', 'Hauling with our own trucks'],
  hero_img='new-concrete-patio',
  sections=[
   dict(id='finishes', h2='Four finishes', html=compare([
     ('Brushed', 'A textured, non-slip surface that enhances safety and gives a clean, natural look. Well suited to driveways, walkways and patios.'),
     ('Exposed aggregate', 'Decorative stones or pebbles show on the surface for a striking, durable finish. Good for patios, driveways and walkways.'),
     ('Smooth trowel', 'A sleek, polished surface for floors, slabs, and indoor or outdoor projects. A classic finish that is easy to maintain and gives a refined, professional look.'),
     ('Stamped', 'Mimics stone, brick or tile with the strength of concrete. Endless design possibilities for patios, driveways and walkways.')])),
   dict(id='removal', h2='Removal and hauling', html=groups(
     ('Concrete removal', ['We carefully break apart old or damaged slabs', 'Pieces are handled safely and hauled off', 'The site is left ready for new construction or landscaping']),
     ('Hauling', ['Hauling runs on our own fleet of trucks', 'Slabs, driveways, patios and foundations']))),
  ],
  gallery=['concrete-finisher-trowel', 'concrete-slab-finishing', 'concrete-saw-cutting', 'broken-concrete-slabs-canal'],
  faqs=[
   ('Which finish is best for slip resistance?', '<p>A brushed finish gives a textured, non-slip surface, which is why it is popular for driveways, walkways and patios.</p>'),
   ('What is exposed aggregate concrete?', '<p>Concrete with the top layer removed so decorative stones or pebbles show. It is durable and looks distinctive on patios, driveways and walkways.</p>'),
   ('Can concrete look like stone or brick?', '<p>Yes. Stamped concrete mimics the look of stone, brick or tile while keeping the durability of concrete.</p>'),
   ('Do you remove old concrete?', '<p>Yes. We break it apart, handle the pieces safely, haul it away and leave the site ready for new construction or landscaping.</p>'),
  ],
  related=['demolition', 'excavating-grading', 'decks', 'seawalls']),

 dict(slug='decks', name='Decks', group='land',
  summary='Wood, composite, Trex and pool decks: builds, repairs, upgrades.',
  hub_img='new-deck-over-seawall',
  title='Custom Deck Builders in Metro Detroit | Wood, Composite, Trex',
  desc='Custom wood, composite, Trex® and pool decks in Metro Detroit: new builds, repairs and upgrades, including waterfront decks.',
  h1='Custom deck construction in Metro Detroit',
  lead='Strong, good-looking outdoor space built for everyday use: wood, composite, Trex® and pool decks, plus repairs and upgrades to the deck you already have.',
  checks=['Wood, composite, Trex', 'Pool decks', 'Repairs and upgrades', 'Waterfront decks'],
  hero_img='new-deck-over-seawall',
  sections=[
   dict(id='materials', h2='Choose the right decking', html=compare([
     ('Composite', 'A blend of wood fibers and recycled plastic with the look of wood and minimal upkeep. Resists rot, warping and insect damage.'),
     ('Wood', 'Real lumber with classic natural beauty and a warm, traditional feel. Ideal if you love a natural look and are willing to seal or stain periodically. Can be shaped, stained or painted to match your style.'),
     ('Trex®', 'A premium composite brand known for durability, fade resistance and eco-friendliness. Looks like wood and performs well in all weather. A good fit for families and busy homeowners who want style and longevity.'),
     ('Pool deck', 'Built from wood, composite or Trex with a focus on safety: slip-resistant, moisture-resistant surfaces for wet areas.')]) +
     '<p class="mt-m measure">Which material is best depends on your look, how much upkeep you want to do, and how often the deck gets wet. We also build waterfront decks, including decks along seawalls.</p>'),
   dict(id='what', h2='What we do', html=ul(['Custom deck builds and installations', 'Deck repairs', 'Upgrades to existing decks', 'Stairs and railings, including steel railings from our own shop'])),
  ],
  gallery=['deck-cabin-white-railing', 'red-stained-log-cabin-deck', 'beach-stairs-wood-platform'],
  faqs=[
   ('Should I choose composite or wood?', '<p>Composite needs far less maintenance and resists rot, warping and insects. Wood has a classic look and is highly customizable, but needs periodic sealing or staining. It comes down to your style and how much upkeep you want.</p>'),
   ('What is Trex?', '<p>Trex is a premium composite decking brand known for durability, fade resistance and low maintenance.</p>'),
   ('Can you repair or upgrade my existing deck?', '<p>Yes. Deck work includes custom builds, repairs and upgrades.</p>'),
   ('Do you build pool and waterfront decks?', '<p>Yes. Pool decks use slip-resistant, moisture-resistant materials, and we build decks along waterfront properties, including over seawalls.</p>'),
  ],
  related=['concrete', 'welding-fabrication', 'seawalls', 'docks']),
]
BY_SLUG = {s['slug']: s for s in SERVICES}

# Boat hoist size guidance, as published on the current site (feet).
HOIST_SIZES = [
  ('PWC lifts', 0, 15, 'Under 15 ft', 'Jet skis, WaveRunners and small watercraft'),
  ('4-point lifts', 0, 25, 'Up to 25 ft', 'Runabouts, center consoles, fishing boats'),
  ('Elevator lifts', 0, 30, 'Up to 30 ft', 'Tight spaces; often paired with a dock platform'),
  ('8-point lifts', 30, 40, '30 to 40 ft', 'Larger cruisers and pontoon boats'),
  ('Boat house hoists', 0, 40, 'Up to 35 to 40 ft', 'Covered storage that protects from weather and corrosion'),
]

HOME_FAQS = [
 ('What areas do you serve?', '<p>We work across Metro Detroit, with a focus on the Lake St. Clair and Detroit River waterfront. Not sure we cover your address? Call <a href="tel:+15867037214">586-703-7214</a> and ask.</p>'),
 ('Do you work for homeowners or only businesses?', '<p>Both. We work for homeowners, commercial properties and marinas.</p>'),
 ('How do I get a quote?', '<p>Quotes are free. Use the <a href="/contact/">quote form</a> or call us, and include the job address, what you want done, and photos or video if you have them.</p>'),
 ('Do I need a permit for seawall, dock or dredging work?', '<p>Usually. Work on Lake St. Clair and other Great Lakes waters generally needs an EGLE permit and often a U.S. Army Corps of Engineers permit. See our <a href="/services/seawalls/">seawall</a> and <a href="/services/dredging/">dredging</a> pages for links, and confirm the rules for your site.</p>'),
 ('Do you offer financing?', '<p>Yes. Financing for qualified customers is arranged through Enhancify, subject to credit approval. See our <a href="/financing/">financing page</a> for how it works.</p>'),
 ('Do you work in winter?', '<p>Our <a href="/projects/">project photos</a> include jobs done in snow and on ice. Ask about scheduling for your project.</p>'),
]

QUOTES = [
 ('Absolutely phenomenal job! Will be using for multiple projects moving forward! Owner’s communication was terrific and job was complete on time zero issues!', 'Google review'),
 ('Kevin did a great job. I’m very pleased with his work and highly recommend him.', 'Google review'),
]

# gallery: (image key, category)
GALLERY = [
 ('sheet-pile-excavator-canal-home','seawalls'),('sheet-pile-staging-seawall','seawalls'),('vibratory-hammer-steel-pile','seawalls'),
 ('excavator-barge-timber-pilings','seawalls'),('pipe-pilings-barge-sunset','seawalls'),('excavator-pipe-pilings-dusk','seawalls'),
 ('barge-excavator-canal','docks'),('barge-open-water','docks'),('barge-excavator-snow','docks'),('barge-boathouse-excavator','docks'),
 ('wood-dock-yellow-flag','docks'),('l-shaped-dock-choppy-water','docks'),('gray-dock-walkway-canal','docks'),('dock-boxes-moored-boat','docks'),
 ('dock-work-through-ice','docks'),('winter-dock-edge','docks'),('covered-marina-walkway-sunset','docks'),('boat-lift-covered-slip','docks'),
 ('boat-house-hoist-tarped-boat','docks'),('excavator-dock-removal','docks'),
 ('welding-at-night-waterfront','welding'),('welding-shop-grinding-sparks','welding'),('welders-frozen-shoreline','welding'),('welder-helmet-sparks','welding'),
 ('welder-under-dock','welding'),('welding-large-pipe-fabrication','welding'),('steel-table-frame-fabrication','welding'),('steel-stair-railing-brick-home','welding'),
 ('black-steel-railing-porch','welding'),('steel-pool-gate','welding'),('rust-finish-steel-sign-arch','welding'),
 ('new-concrete-patio','concrete'),('concrete-finisher-trowel','concrete'),('concrete-slab-finishing','concrete'),('concrete-saw-cutting','concrete'),
 ('concrete-work-crew','concrete'),('new-deck-over-seawall','concrete'),('deck-cabin-white-railing','concrete'),('red-stained-log-cabin-deck','concrete'),('beach-stairs-wood-platform','concrete'),
 ('excavator-site-dusk','excavating'),('dump-trucks-yard','excavating'),('excavator-loading-dump-trailer','excavating'),('skid-steer-yard','excavating'),
 ('graded-gravel-yard-boathouse','excavating'),('excavator-trench-lawn','excavating'),('dozer-clearing-field','excavating'),('dump-truck-unloading','excavating'),
 ('demolition-excavator-canal','excavating'),('demolition-excavator-tanks','excavating'),('stiers-excavator-demo-site','excavating'),('demolition-debris-pile','excavating'),
 ('broken-concrete-slabs-canal','excavating'),
]
GALLERY_CATS = [('all','All projects'),('seawalls','Seawalls and pilings'),('docks','Docks, hoists and barge work'),('welding','Welding and fabrication'),('concrete','Concrete and decks'),('excavating','Excavating and demolition')]
