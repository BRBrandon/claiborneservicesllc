#!/usr/bin/env python3
"""Static site generator for Claiborne Services LLC."""
import os, html, json

ROOT = os.path.dirname(os.path.abspath(__file__))
PHONE = "(615) 900-4501"
PHONE_TEL = "+16159004501"
EMAIL = "shawn@claiborneservicesllc.com"
SITE_URL = "https://claiborneservicesllc.pplx.app"
# Replace GA_MEASUREMENT_ID with the real G-XXXXXXXXXX once Shawn creates the GA4 property.
GA_MEASUREMENT_ID = "G-XXXXXXXXXX"

# ============ Google Business Profile (live data from connector) ============
def _load_json(rel):
    with open(os.path.join(ROOT, rel), "r", encoding="utf-8") as f:
        return json.load(f)

GBP_META = _load_json("data/gbp_meta.json")
GBP_REVIEWS = _load_json("data/gbp_reviews.json")

GBP_PLACE_ID  = GBP_META["place_id"]
GBP_CID       = GBP_META["cid"]
GBP_MAPS_URI  = GBP_META["maps_uri"]
GBP_WRITE_URL = GBP_META["new_review_uri"]
GBP_RATING    = GBP_REVIEWS["average_rating"]
GBP_COUNT     = GBP_REVIEWS["total_review_count"]
# Keep `GBP` as the maps URL for legacy references in templates.
GBP = GBP_MAPS_URI

def _fmt_rating(v):
    s = f"{float(v):.1f}"
    return s.rstrip("0").rstrip(".") if s.endswith(".0") else s

# Remap every non-verified id literal to a visually-verified relevant image.
_IMG_FIX = {
  "1466692476868-aef1dfb1e735": "px:440731",          # -> green field
  "1601574465779-76d6dbb88557": "px:96715",            # -> cleared field
  "1635350736475-c8cef4b21906": "1473773508845-188df298d2d1",  # -> forest floor/path
  "1448375240586-882707db888b": "1416879595882-3373a0480b5b",  # -> forest canopy
  "1503387762-592deb58ef4e":   "1500382017468-9049fed747ef",   # -> golden field
  "1543674892-7d64d45df18b":   "px:167698",            # -> forest
  "1530541930197-ff16ac917b0e": "px:2219024",          # -> cement/site work (was campfire)
  "1605152276897-4f618f831968": "px:1078884",          # -> excavator (was 'Service' sign)
  "1589923188900-85dae523342b": "px:585419",            # -> worker w/ log on site (was planting)
  "1625246333195-78d9c38ad449": "px:2310904",          # -> pipes/excavation (was corn)
  "1564540583246-934409427776": "px:2058134",          # -> plans (was bathroom)
  "1542401886-65d6c61db217":   "px:585419",             # -> worker w/ log
  "1626885930974-4b69aa21bbf9": "px:2219024",          # -> site/loader
  "1591955506264-3f5a6834570a": "px:585419",            # -> timber/worker
  "1518709268805-4e9042af9f23": "px:2310904",          # -> trenching/pipes
  "1599707367072-cd6ada2bc375": "px:1078884",          # -> excavator
  "1558618666-fcd25c85cd64":   "px:1078884",            # -> excavator (was dozer/ok)
  "1517048676732-d65bc937f952": "px:1216589",          # -> crew (was meeting)
  "1621905251918-48416bd8575a": "px:1078884",          # -> excavator hero
  "1504917595217-d4dc5ebe6122": "px:585419",            # -> worker w/ log (tree work)
  "1542273917363-3b1817f69a2d": "1502082553048-f009c37129b9",  # -> foggy forest (plans dup)
  "1574691250077-03a929faece5": "px:585419",            # -> worker/timber (was resort)
}
# Sentinel: any non-local image now routes to a 'Photo Coming Soon' placeholder.
# This kills every stock photo (Pexels px: ids and bare Unsplash ids) site-wide in one place.
PLACEHOLDER = "local:assets/img/jobs/placeholder-need-photo.jpg"
PLACEHOLDER_PATH = "assets/img/jobs/placeholder-need-photo.jpg"

def img(pid, w=1200):
    """Return a responsive image URL. Local files prefixed 'local:'; everything else falls back to a placeholder card."""
    pid = _IMG_FIX.get(pid, pid)
    # All stock photos (Pexels px: and bare Unsplash ids) get redirected to the placeholder.
    if not (isinstance(pid, str) and pid.startswith("local:")):
        pid = PLACEHOLDER
    # Local file: ignore width (browser will downscale via CSS); path is relative to site root.
    return pid[6:]

def is_placeholder(pid):
    """True when this pid resolves to the 'photo coming soon' placeholder."""
    return img(pid, 100) == PLACEHOLDER_PATH

def hero_bg(pid, w=1600, pfx="", overlay=False):
    """Return inline-style background for a hero. Falls back to brand green when image would be a placeholder."""
    if is_placeholder(pid):
        return "background:linear-gradient(160deg,#2a5732 0%,#1f3d23 100%)"
    if overlay:
        return f"background-image:linear-gradient(rgba(20,30,20,.62),rgba(20,30,20,.62)),url('{pfx + img(pid, w)}')"
    return f"background-image:url('{pfx + img(pid, w)}')"

# image ids — all visually verified for relevant subject matter
HERO = "px:1078884"          # orange excavator on a job site (kept for OG / fallback)
HOME_HERO = "local:assets/img/jobs/banner-mulching-cat265-hm316.jpg"  # homepage banner: Cat 265 + HM316
MULCH_HERO = "local:assets/img/jobs/banner-mulching-cat265-hm316.jpg"  # forestry mulching page hero
EXCAV_HERO = "local:assets/img/jobs/banner-excavation-cat305.jpg"  # excavation page hero: Cat 305
EXCAV = "local:assets/img/jobs/banner-excavation-cat305.jpg"   # Cat 305 real photo (temporary: used for all excavation slots)
EXCAV_STOCK = "px:1078884"   # kept for OG / fallback only
TREE_STOCK = "px:585419"     # original stock (kept for Chippers card)
TREE = "local:assets/img/jobs/tree-bucket-storm-franklin.jpg"  # Haulotte 55XA storm-damage removal in Franklin, TN (temporary: used for all tree-services slots)
TREE2 = "px:1029243"         # tall tree against sky
LAND_STOCK = "px:96715"      # original stock (kept for Dump trailers card)
LAND = "local:assets/img/jobs/banner-mulching-cat265-hm316.jpg"  # Cat 265 + HM316 banner (temporary: used for all land-clearing slots)
MULCH = "1473773508845-188df298d2d1"   # cleared/mulched forest floor with path
SITEPREP_STOCK = "px:2219024"   # original stock (kept for stump-grinder card)
SITEPREP = "local:assets/img/jobs/banner-siteprep-pad.jpg"  # Cat tracked skid steer + roller compacting a pad (temporary: used for all site-prep slots)
CREW = "px:1216589"          # two workers in hardhats on site
DOZER = "px:1078884"         # heavy equipment
LOGS = "px:585419"           # worker / timber
TRENCH = "local:assets/img/jobs/banner-excavation-cat305.jpg"  # temporary: same Cat 305 photo for trench thumbnails
TRENCH_STOCK = "px:2310904"  # kept for fallback
FOREST = "1416879595882-3373a0480b5b"    # forest canopy
FIELD = "1500382017468-9049fed747ef"     # golden open field
PLANS = "px:2058134"         # plans / drawing
CRANE = "px:585419"          # crew on site
ROWS = "1486754735734-325b5831c3ad"      # cultivated field rows
FOGFOREST = "1502082553048-f009c37129b9" # foggy forest
FORESTPATH = "1473773508845-188df298d2d1"
LAND2 = "px:440731"          # green field
GALLERY_IDS = [HERO, TREE, LAND, MULCH, SITEPREP, TREE2, CREW, LOGS, TRENCH, FOREST, FIELD,
               FORESTPATH, PLANS, FOGFOREST, ROWS, LAND2, "px:167698"]

def logo_img(prefix="", cls=""):
    css_cls = ("brand-logo " + cls).strip()
    return f'<img class="{css_cls}" src="{prefix}assets/img/logo.png" alt="Claiborne Services LLC" width="316" height="320">'

# ---- icon helpers ----
def icon(name):
    s = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    paths = {
      'phone':'<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>',
      'message':'<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
      'shield':'<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
      'home':'<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>',
      'layers':'<polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>',
      'star':'<polygon points="12 2 15 9 22 9 17 14 19 21 12 17 5 21 7 14 2 9 9 9 12 2"/>',
      'check':'<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>',
      'mail':'<rect x="2" y="4" width="20" height="16" rx="2"/><polyline points="22 6 12 13 2 6"/>',
      'pin':'<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
      'dollar':'<line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>',
      'clock':'<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    }
    return s + paths.get(name,'') + '</svg>'

def social_icon(name):
    # Official brand-accurate SVG paths (Simple Icons v15, CC0).
    # LinkedIn uses Bootstrap Icons (Simple Icons removed it per LinkedIn brand policy).
    # Nextdoor uses a custom house mark (Simple Icons only ships the wordmark, which doesn't read at 18px).
    paths={
     'fb':('0 0 24 24','<path d="M9.101 23.691v-7.98H6.627v-3.667h2.474v-1.58c0-4.085 1.848-5.978 5.858-5.978.401 0 .955.042 1.468.103a8.68 8.68 0 0 1 1.141.195v3.325a8.623 8.623 0 0 0-.653-.036 26.805 26.805 0 0 0-.733-.009c-.707 0-1.259.096-1.675.309a1.686 1.686 0 0 0-.679.622c-.258.42-.374.995-.374 1.752v1.297h3.919l-.386 2.103-.287 1.564h-3.246v8.245C19.396 23.238 24 18.179 24 12.044c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.628 3.874 10.35 9.101 11.647Z"/>'),
     'ig':('0 0 24 24','<path d="M7.0301.084c-1.2768.0602-2.1487.264-2.911.5634-.7888.3075-1.4575.72-2.1228 1.3877-.6652.6677-1.075 1.3368-1.3802 2.127-.2954.7638-.4956 1.6365-.552 2.914-.0564 1.2775-.0689 1.6882-.0626 4.947.0062 3.2586.0206 3.6671.0825 4.9473.061 1.2765.264 2.1482.5635 2.9107.308.7889.72 1.4573 1.388 2.1228.6679.6655 1.3365 1.0743 2.1285 1.38.7632.295 1.6361.4961 2.9134.552 1.2773.056 1.6884.069 4.9462.0627 3.2578-.0062 3.668-.0207 4.9478-.0814 1.28-.0607 2.147-.2652 2.9098-.5633.7889-.3086 1.4578-.72 2.1228-1.3881.665-.6682 1.0745-1.3378 1.3795-2.1284.2957-.7632.4966-1.636.552-2.9124.056-1.2809.0692-1.6898.063-4.948-.0063-3.2583-.021-3.6668-.0817-4.9465-.0607-1.2797-.264-2.1487-.5633-2.9117-.3084-.7889-.72-1.4568-1.3876-2.1228C21.2982 1.33 20.628.9208 19.8378.6165 19.074.321 18.2017.1197 16.9244.0645 15.6471.0093 15.236-.005 11.977.0014 8.718.0076 8.31.0215 7.0301.0839m.1402 21.6932c-1.17-.0509-1.8053-.2453-2.2287-.408-.5606-.216-.96-.4771-1.3819-.895-.422-.4178-.6811-.8186-.9-1.378-.1644-.4234-.3624-1.058-.4171-2.228-.0595-1.2645-.072-1.6442-.079-4.848-.007-3.2037.0053-3.583.0607-4.848.05-1.169.2456-1.805.408-2.2282.216-.5613.4762-.96.895-1.3816.4188-.4217.8184-.6814 1.3783-.9003.423-.1651 1.0575-.3614 2.227-.4171 1.2655-.06 1.6447-.072 4.848-.079 3.2033-.007 3.5835.005 4.8495.0608 1.169.0508 1.8053.2445 2.228.408.5608.216.96.4754 1.3816.895.4217.4194.6816.8176.9005 1.3787.1653.4217.3617 1.056.4169 2.2263.0602 1.2655.0739 1.645.0796 4.848.0058 3.203-.0055 3.5834-.061 4.848-.051 1.17-.245 1.8055-.408 2.2294-.216.5604-.4763.96-.8954 1.3814-.419.4215-.8181.6811-1.3783.9-.4224.1649-1.0577.3617-2.2262.4174-1.2656.0595-1.6448.072-4.8493.079-3.2045.007-3.5825-.006-4.848-.0608M16.953 5.5864A1.44 1.44 0 1 0 18.39 4.144a1.44 1.44 0 0 0-1.437 1.4424M5.8385 12.012c.0067 3.4032 2.7706 6.1557 6.173 6.1493 3.4026-.0065 6.157-2.7701 6.1506-6.1733-.0065-3.4032-2.771-6.1565-6.174-6.1498-3.403.0067-6.156 2.771-6.1496 6.1738M8 12.0077a4 4 0 1 1 4.008 3.9921A3.9996 3.9996 0 0 1 8 12.0077"/>'),
     'threads':('0 0 24 24','<path d="M12.186 24h-.007c-3.581-.024-6.334-1.205-8.184-3.509C2.35 18.44 1.5 15.586 1.472 12.01v-.017c.03-3.579.879-6.43 2.525-8.482C5.845 1.205 8.6.024 12.18 0h.014c2.746.02 5.043.725 6.826 2.098 1.677 1.29 2.858 3.13 3.509 5.467l-2.04.569c-1.104-3.96-3.898-5.984-8.304-6.015-2.91.022-5.11.936-6.54 2.717C4.307 6.504 3.616 8.914 3.589 12c.027 3.086.718 5.496 2.057 7.164 1.43 1.783 3.631 2.698 6.54 2.717 2.623-.02 4.358-.631 5.8-2.045 1.647-1.613 1.618-3.593 1.09-4.798-.31-.71-.873-1.3-1.634-1.75-.192 1.352-.622 2.446-1.284 3.272-.886 1.102-2.14 1.704-3.73 1.79-1.202.065-2.361-.218-3.259-.801-1.063-.689-1.685-1.74-1.752-2.964-.065-1.19.408-2.285 1.33-3.082.88-.76 2.119-1.207 3.583-1.291a13.853 13.853 0 0 1 3.02.142c-.126-.742-.375-1.332-.75-1.757-.513-.586-1.308-.883-2.359-.89h-.029c-.844 0-1.992.232-2.721 1.32L7.734 7.847c.98-1.454 2.568-2.256 4.478-2.256h.044c3.194.02 5.097 1.975 5.287 5.388.108.046.216.094.321.142 1.49.7 2.58 1.761 3.154 3.07.797 1.82.871 4.79-1.548 7.158-1.85 1.81-4.094 2.628-7.277 2.65Zm1.003-11.69c-.242 0-.487.007-.739.021-1.836.103-2.98.946-2.916 2.143.067 1.256 1.452 1.839 2.784 1.767 1.224-.065 2.818-.543 3.086-3.71a10.5 10.5 0 0 0-2.215-.221z"/>'),
     'li':('0 0 16 16','<path d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854zm4.943 12.248V6.169H2.542v7.225zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248S2.4 3.226 2.4 3.934c0 .694.521 1.248 1.327 1.248zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016l.016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225z"/>'),
     'yt':('0 0 24 24','<path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>'),
     'x':('0 0 24 24','<path d="M14.234 10.162 22.977 0h-2.072l-7.591 8.824L7.251 0H.258l9.168 13.343L.258 24H2.33l8.016-9.318L16.749 24h6.993zm-2.837 3.299-.929-1.329L3.076 1.56h3.182l5.965 8.532.929 1.329 7.754 11.09h-3.182z"/>'),
     'yelp':('0 0 24 24','<path d="m7.6885 15.1415-3.6715.8483c-.3769.0871-.755.183-1.1452.155-.2611-.0188-.5122-.0414-.7606-.213a1.179 1.179 0 0 1-.331-.3594c-.3486-.5519-.3656-1.3661-.3697-2.0004a6.2874 6.2874 0 0 1 .3314-2.0642 1.857 1.857 0 0 1 .1073-.2474 2.3426 2.3426 0 0 1 .1255-.2165 2.4572 2.4572 0 0 1 .1563-.1975 1.1736 1.1736 0 0 1 .399-.2831 1.082 1.082 0 0 1 .4592-.0837c.2355.0016.5139.052.91.1734.0555.0191.1237.0382.1856.0572.3277.1013.7048.2404 1.1499.3987.6863.2404 1.3663.487 2.0463.7397l1.2117.4423c.2217.0807.4363.18.6412.297.174.0984.3273.2298.4512.387a1.217 1.217 0 0 1 .192.4309 1.2205 1.2205 0 0 1-.872 1.4522c-.0468.0151-.0852.0239-.1085.0293l-1.105.2553-.0031-.001zM18.8208 7.565a1.8506 1.8506 0 0 0-.2042-.1754 2.4082 2.4082 0 0 0-.2077-.1394 2.3607 2.3607 0 0 0-.2269-.109 1.1705 1.1705 0 0 0-.482-.0796 1.0862 1.0862 0 0 0-.4498.1263c-.2107.1048-.4388.2732-.742.5551-.042.0417-.0947.0886-.142.133-.2502.2351-.5286.5252-.8599.863a114.6363 114.6363 0 0 0-1.5166 1.5629l-.8962.9293a4.1897 4.1897 0 0 0-.4466.5483 1.541 1.541 0 0 0-.2364.5459 1.2199 1.2199 0 0 0 .0107.4518l.0046.02a1.218 1.218 0 0 0 1.4184.923 1.162 1.162 0 0 0 .1105-.0213l4.7781-1.104c.3766-.087.7587-.1667 1.097-.3631.2269-.1316.4428-.262.5909-.5252a1.1793 1.1793 0 0 0 .1405-.4683c.0733-.6512-.2668-1.3908-.5403-1.963a6.2792 6.2792 0 0 0-1.2001-1.7103zM8.9703.0754a8.6724 8.6724 0 0 0-.83.1564c-.2754.066-.548.1383-.8146.2236-.868.2844-2.0884.8063-2.295 1.8065-.1165.5655.1595 1.1439.3737 1.66.2595.6254.614 1.1889.9373 1.7777.8543 1.5545 1.7245 3.0993 2.5922 4.6457.259.4617.5416 1.0464 1.043 1.2856a1.058 1.058 0 0 0 .1013.0383c.2248.0851.4699.1016.7041.0471a4.3015 4.3015 0 0 0 .0418-.0097 1.2136 1.2136 0 0 0 .5658-.3397 1.1033 1.1033 0 0 0 .079-.0822c.3463-.435.3454-1.0833.3764-1.6134.1042-1.771.2139-3.5423.3009-5.3142.0332-.6712.1055-1.3333.0655-2.0096-.0328-.5579-.0368-1.1984-.3891-1.6563-.6218-.8073-1.9476-.741-2.8523-.6158zm2.084 15.9505a1.1053 1.1053 0 0 0-1.2306-.4145 1.1398 1.1398 0 0 0-.1526.0633 1.4806 1.4806 0 0 0-.2171.1354c-.1992.1475-.3668.3392-.5196.5315-.0386.049-.074.1143-.12.1562l-.7686 1.0573a113.9168 113.9168 0 0 0-1.2913 1.789c-.278.3895-.5184.7184-.7083 1.0094-.036.0547-.0734.116-.1075.1647-.2277.3522-.3566.6092-.4228.8381a1.0945 1.0945 0 0 0-.046.4721c.0211.1655.0768.3246.1635.467.046.0715.0957.1406.1487.207a2.334 2.334 0 0 0 .1754.1825 1.843 1.843 0 0 0 .2108.1732c.5304.369 1.1112.6342 1.722.8391a6.0958 6.0958 0 0 0 1.5716.3004c.091.0046.1821.0025.2728-.006a2.3878 2.3878 0 0 0 .2506-.0351 2.3862 2.3862 0 0 0 .2447-.071 1.1927 1.1927 0 0 0 .4175-.2658c.1127-.113.1994-.249.2541-.3989.0889-.2214.1473-.5026.1857-.92.0034-.0593.0118-.1305.0177-.1958.0304-.3463.0443-.7531.0666-1.2315.0375-.7357.067-1.4681.0903-2.2026 0 0 .0495-1.3053.0494-1.306.0113-.3008.002-.6342-.0814-.9336a1.396 1.396 0 0 0-.1756-.4054zm8.6754 2.0439c-.1605-.176-.3878-.3514-.7462-.5682-.0518-.0288-.1124-.0674-.1684-.1009-.2985-.1795-.658-.3684-1.078-.5965a120.7615 120.7615 0 0 0-1.9427-1.042l-1.1515-.6107c-.0597-.0175-.1203-.0607-.1766-.0878-.2212-.1058-.4558-.2045-.6992-.2498a1.4915 1.4915 0 0 0-.2545-.0265 1.1527 1.1527 0 0 0-.1648.01 1.1077 1.1077 0 0 0-.9227.9133 1.4186 1.4186 0 0 0 .0159.439c.0563.3065.1932.6096.3346.875l.615 1.1526c.3422.65.6884 1.2963 1.0435 1.9406.229.4202.4196.7799.5982 1.078.0338.056.0721.1163.1011.1682.2173.3584.392.584.569.7458.1146.1107.252.195.4026.247.1583.0525.326.071.4919.0546a2.368 2.368 0 0 0 .251-.0435c.0817-.022.1622-.048.241-.0784a1.863 1.863 0 0 0 .2475-.1143 6.1018 6.1018 0 0 0 1.2818-.9597c.4596-.4522.8659-.9454 1.182-1.51.044-.08.0819-.163.1138-.2483a2.49 2.49 0 0 0 .0773-.2411c.0186-.083.033-.1669.0429-.2513a1.188 1.188 0 0 0-.0565-.491 1.0933 1.0933 0 0 0-.248-.4041z"/>'),
     'nd':('0 0 68 55','<path d="M22.1789 8.27054V0.791992H12.2953V14.4821L0.696289 21.7701L5.95482 30.14L12.2953 26.154V53.8538H55.8828V26.154L62.2233 30.14L67.4819 21.7701L34.0863 0.791992L22.1789 8.27054Z"/>'),
     'google':('0 0 24 24','<path d="M12.48 10.92v3.28h7.84c-.24 1.84-.853 3.187-1.787 4.133-1.147 1.147-2.933 2.4-6.053 2.4-4.827 0-8.6-3.893-8.6-8.72s3.773-8.72 8.6-8.72c2.6 0 4.507 1.027 5.907 2.347l2.307-2.307C18.747 1.44 16.133 0 12.48 0 5.867 0 .307 5.387.307 12s5.56 12 12.173 12c3.573 0 6.267-1.173 8.373-3.36 2.16-2.16 2.84-5.213 2.84-7.667 0-.76-.053-1.467-.173-2.053H12.48z"/>'),
    }
    vb, body = paths.get(name, ('0 0 24 24',''))
    return f'<svg width="18" height="18" viewBox="{vb}" fill="currentColor" aria-hidden="true">{body}</svg>'

# ---- shared fragments ----
def _hours_data_attr():
    """Build 'Mo 07:00-18:00;Tu 07:00-18:00;...' for the open-status badge."""
    parts = []
    for h in GBP_META.get("hours", []):
        d = _DAY_ABBR.get(h.get("day", ""))
        if d and h.get("open") and h.get("close"):
            parts.append(f"{d} {h['open']}-{h['close']}")
    return ";".join(parts)

def open_status_badge():
    return f'<span class="open-status" data-open-status data-hours="{_hours_data_attr()}" aria-live="polite"><span class="status-dot" aria-hidden="true"></span><span class="status-text">Checking hours…</span></span>'

def header(prefix=""):
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<div class="topbar">
  <div class="container topbar-inner">
    <span class="topbar-tagline">Family-owned &middot; Insured &middot; Middle Tennessee</span>
    {open_status_badge()}
    <div class="topbar-social" aria-label="Follow Claiborne Services">
      <a href="https://www.facebook.com/claiborneservicesllc" aria-label="Facebook" target="_blank" rel="noopener">{social_icon('fb')}</a>
      <a href="https://www.instagram.com/claiborneservicesllc/" aria-label="Instagram" target="_blank" rel="noopener">{social_icon('ig')}</a>
      <a href="https://www.threads.com/@claiborneservicesllc" aria-label="Threads" target="_blank" rel="noopener">{social_icon('threads')}</a>
      <a href="https://www.linkedin.com/company/claiborneservicesllc" aria-label="LinkedIn" target="_blank" rel="noopener">{social_icon('li')}</a>
      <a href="https://www.youtube.com/@claiborneservicesllc" aria-label="YouTube" target="_blank" rel="noopener">{social_icon('yt')}</a>
      <a href="https://x.com/claibornellc" aria-label="X (Twitter)" target="_blank" rel="noopener">{social_icon('x')}</a>
      <a href="https://www.yelp.com/biz/claiborne-services-franklin" aria-label="Yelp" target="_blank" rel="noopener">{social_icon('yelp')}</a>
      <a href="https://nextdoor.com/page/claiborne-services-llc-franklin-tn" aria-label="Nextdoor" target="_blank" rel="noopener">{social_icon('nd')}</a>
    </div>
  </div>
</div>
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="{prefix}index.html" aria-label="Claiborne Services LLC home">
      {logo_img(prefix)}
      <span class="brand-tag"><small>Tree &middot; Land &middot; Excavation</small></span>
    </a>
    <button class="nav-toggle" aria-label="Toggle navigation" aria-expanded="false"><span></span><span></span><span></span></button>
    <nav class="main-nav" aria-label="Primary">
      <a href="{prefix}index.html">Home</a>
      <div class="has-dropdown">
        <a href="{prefix}services/tree-services.html" aria-haspopup="true">Services &#9662;</a>
        <div class="dropdown">
          <a href="{prefix}services/tree-services.html">Tree Services</a>
          <a href="{prefix}services/land-clearing.html">Land Clearing</a>
          <a href="{prefix}services/forestry-mulching.html">Forestry Mulching</a>
          <a href="{prefix}services/site-preparation.html">Site Preparation</a>
          <a href="{prefix}services/excavation.html">Excavation</a>
          <a href="{prefix}equipment.html">Our Equipment</a>
        </div>
      </div>
      <a href="{prefix}service-area.html">Service Area</a>
      <a href="{prefix}reviews.html">Reviews</a>
      <div class="has-dropdown">
        <a href="{prefix}faq.html" aria-haspopup="true">Resources &#9662;</a>
        <div class="dropdown">
          <a href="{prefix}faq.html">FAQs</a>
          <a href="{prefix}pricing.html">Pricing Guide</a>
          <a href="{prefix}financing.html">Financing</a>
          <a href="{prefix}insurance.html">Licensed &amp; Insured</a>
          <a href="{prefix}equipment.html">Equipment</a>
          <a href="{prefix}gallery.html">Gallery</a>
          <a href="{prefix}discounts.html">Discounts</a>
          <a href="{prefix}partners.html">Partners</a>
        </div>
      </div>
      <a href="{prefix}about.html">About</a>
      <a href="{prefix}contact.html">Contact</a>
    </nav>
    <div class="header-cta">
      <a class="header-phone" href="tel:{PHONE_TEL}">{icon('phone')}<span>{PHONE}</span></a>
      <a class="header-textlink" href="sms:{PHONE_TEL}">Text Us</a>
      <a class="btn btn--primary" href="{prefix}contact.html">Get a Free Quote</a>
    </div>
  </div>
</header>'''

def trustbar():
    rating = _fmt_rating(GBP_RATING)
    google_line = f'<a href="{GBP_MAPS_URI}" target="_blank" rel="noopener" class="trustbar-google" aria-label="View Google reviews"><strong>{rating}</strong> on Google &middot; {GBP_COUNT} reviews</a>'
    items = [
      ('shield','Licensed &amp; Insured'),
      ('home','Family-Owned, Franklin-Based'),
      ('layers','Full-Service (Tree + Land + Excavation)'),
      ('star', google_line),
      ('check','100% Satisfaction Guarantee'),
    ]
    lis = "".join(f'<li>{icon(i)}<span>{t}</span></li>' for i,t in items)
    return f'<section class="trustbar" aria-label="Why choose Claiborne Services"><ul>{lis}</ul></section>'

def finance_callout():
    return f'''<div class="finance-callout">{icon('dollar')}<p><strong>Financing available through QuickBooks.</strong> Qualified customers may be able to pay over time with monthly payment options, subject to approval.</p></div>'''

def footer(prefix=""):
    return f'''<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="brand brand--footer" href="{prefix}index.html" aria-label="Claiborne Services LLC home">{logo_img(prefix, 'brand-logo--footer')}<span class="brand-tag" style="color:#fff"><small style="color:#aebbae">Tree &middot; Land &middot; Excavation</small></span></a>
        <p>Family-owned tree service, land clearing, and excavation serving Williamson, Maury, Davidson counties and surrounding Middle Tennessee.</p>
        <div class="footer-social">
          <a href="https://www.facebook.com/claiborneservicesllc" aria-label="Facebook" target="_blank" rel="noopener">{social_icon('fb')}</a>
          <a href="https://www.instagram.com/claiborneservicesllc/" aria-label="Instagram" target="_blank" rel="noopener">{social_icon('ig')}</a>
          <a href="https://www.threads.com/@claiborneservicesllc" aria-label="Threads" target="_blank" rel="noopener">{social_icon('threads')}</a>
          <a href="https://www.linkedin.com/company/claiborneservicesllc" aria-label="LinkedIn" target="_blank" rel="noopener">{social_icon('li')}</a>
          <a href="https://www.youtube.com/@claiborneservicesllc" aria-label="YouTube" target="_blank" rel="noopener">{social_icon('yt')}</a>
          <a href="https://x.com/claibornellc" aria-label="X (Twitter)" target="_blank" rel="noopener">{social_icon('x')}</a>
          <a href="https://www.yelp.com/biz/claiborne-services-franklin" aria-label="Yelp" target="_blank" rel="noopener">{social_icon('yelp')}</a>
          <a href="https://nextdoor.com/page/claiborne-services-llc-franklin-tn" aria-label="Nextdoor" target="_blank" rel="noopener">{social_icon('nd')}</a>
          <a href="{GBP}" aria-label="Google Business Profile" target="_blank" rel="noopener">{social_icon('google')}</a>
        </div>
      </div>
      <div>
        <h4>Services</h4>
        <ul>
          <li><a href="{prefix}services/tree-services.html">Tree Services</a></li>
          <li><a href="{prefix}services/land-clearing.html">Land Clearing</a></li>
          <li><a href="{prefix}services/forestry-mulching.html">Forestry Mulching</a></li>
          <li><a href="{prefix}services/site-preparation.html">Site Preparation</a></li>
          <li><a href="{prefix}services/excavation.html">Excavation</a></li>
        </ul>
      </div>
      <div>
        <h4>Service Area</h4>
        <ul>
          <li><a href="{prefix}service-area/franklin-tn.html">Franklin</a></li>
          <li><a href="{prefix}service-area/brentwood-tn.html">Brentwood</a></li>
          <li><a href="{prefix}service-area/spring-hill-tn.html">Spring Hill</a></li>
          <li><a href="{prefix}service-area/thompsons-station-tn.html">Thompson's Station</a></li>
          <li><a href="{prefix}service-area/nolensville-tn.html">Nolensville</a></li>
          <li><a href="{prefix}service-area/columbia-tn.html">Columbia</a></li>
          <li><a href="{prefix}service-area/mt-pleasant-tn.html">Mt. Pleasant</a></li>
          <li><a href="{prefix}service-area/nashville-tn.html">Nashville</a></li>
        </ul>
      </div>
      <div>
        <h4>Resources</h4>
        <ul>
          <li><a href="{prefix}faq.html">FAQs</a></li>
          <li><a href="{prefix}pricing.html">Pricing Guide</a></li>
          <li><a href="{prefix}financing.html">Financing</a></li>
          <li><a href="{prefix}insurance.html">Licensed &amp; Insured</a></li>
          <li><a href="{prefix}equipment.html">Our Equipment</a></li>
          <li><a href="{prefix}gallery.html">Gallery</a></li>
          <li><a href="{prefix}discounts.html">Discounts</a></li>
          <li><a href="{prefix}partners.html">Trusted Partners</a></li>
        </ul>
      </div>
      <div>
        <h4>Company &amp; Contact</h4>
        <ul>
          <li><a href="{prefix}about.html">About</a></li>
          <li><a href="{prefix}reviews.html">Reviews</a></li>
          <li><a href="{prefix}contact.html">Contact</a></li>
          <li style="margin-top:8px"><a href="tel:{PHONE_TEL}">Call {PHONE}</a></li>
          <li><a href="sms:{PHONE_TEL}">Text Us</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>Mon&ndash;Fri, 7am&ndash;6pm</li>
        </ul>
      </div>
    </div>
  </div>
  <div class="footer-bottom">
    <div class="container">
      <span>&copy; 2025 Claiborne Services LLC. All rights reserved. License #TN-Pending &middot; Insured. &middot; <a href="{prefix}about.html#bruno" class="footer-bruno-link">CEO Bruno approves this site.</a></span>
      <span><a href="{prefix}sitemap.xml">Sitemap</a></span>
    </div>
  </div>
</footer>'''

def mobile_bar():
    return f'''<nav class="mobile-bar" aria-label="Quick contact">
  <a class="call" href="tel:{PHONE_TEL}">{icon('phone')}Call Now</a>
  <a class="text" href="sms:{PHONE_TEL}">{icon('message')}Text Us</a>
  <a class="quote" href="contact.html">{icon('check')}Get a Quote</a>
</nav>'''

def cta_banner(prefix=""):
    return f'''<section class="cta-banner">
  <div class="container">
    <h2>Get a Free Quote in 60 Seconds</h2>
    <p>Tell us about your tree, land, or excavation project. We'll come out, look it over, and give you an honest, no-pressure estimate.</p>
    <div class="flex-cta" style="justify-content:center">
      <a class="btn btn--outline" href="{prefix}contact.html">Get a Free Quote</a>
      <a class="btn btn--ghost" href="tel:{PHONE_TEL}" style="border-color:#fff">{icon('phone')}Call {PHONE}</a>
    </div>
  </div>
</section>'''

def page(title, desc, body, prefix="", head_extra="", mobile_prefix=None, page_path="", lang="en"):
    mb = mobile_bar()
    if mobile_prefix is not None:
        mb = mb.replace('href="contact.html"', f'href="{mobile_prefix}contact.html"')
    og = og_tags(title.split(" | ")[0] if " | " in title else title, desc, page_path)
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{og}
{ga_snippet()}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="preconnect" href="https://images.unsplash.com" crossorigin>
<link rel="stylesheet" href="{prefix}assets/css/styles.css">
<link rel="icon" type="image/x-icon" href="{prefix}assets/img/favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="{prefix}assets/img/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="{prefix}assets/img/favicon-16.png">
<link rel="icon" type="image/png" sizes="192x192" href="{prefix}assets/img/favicon-192.png">
<link rel="apple-touch-icon" sizes="180x180" href="{prefix}assets/img/apple-touch-icon.png">
{head_extra}
</head>
<body>
{header(prefix)}
<main id="main">
{body}
</main>
{footer(prefix)}
{mb}
<script src="{prefix}assets/js/main.js" defer></script>
</body>
</html>'''

# ============ FAQ + schema helpers ============
def faq_block(faqs):
    items=""
    for q,a in faqs:
        items+=f'''<div class="faq-item"><button class="faq-q">{q}</button><div class="faq-a"><p>{a}</p></div></div>'''
    return f'<div class="faq">{items}</div>'

def faq_schema(faqs):
    import json
    data={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}
    return '<script type="application/ld+json">'+json.dumps(data)+'</script>'

def service_schema(name, desc):
    import json
    data={"@context":"https://schema.org","@type":"Service","serviceType":name,
          "description":desc,"areaServed":"Middle Tennessee",
          "provider":{"@type":"LocalBusiness","name":"Claiborne Services LLC","telephone":PHONE_TEL,
                      "email":EMAIL,"address":{"@type":"PostalAddress","addressRegion":"TN","addressLocality":"Franklin"}}}
    return '<script type="application/ld+json">'+json.dumps(data)+'</script>'

def breadcrumb_schema(items):
    """items = [(name, url_path_without_leading_slash_or_full_url), ...]"""
    data = {"@context":"https://schema.org","@type":"BreadcrumbList",
            "itemListElement":[
                {"@type":"ListItem","position":i+1,"name":n,
                 "item":(u if u.startswith("http") else f"{SITE_URL}/{u.lstrip('/')}")}
                for i,(n,u) in enumerate(items)]}
    return '<script type="application/ld+json">'+json.dumps(data)+'</script>'

def og_tags(title, desc, path="", image_path="assets/img/og-default.jpg"):
    url = f"{SITE_URL}/{path.lstrip('/')}" if path else SITE_URL
    img_url = f"{SITE_URL}/{image_path.lstrip('/')}"
    safe_title = html.escape(title, quote=True)
    safe_desc = html.escape(desc, quote=True)
    return f'''<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Claiborne Services LLC">
<meta property="og:title" content="{safe_title}">
<meta property="og:description" content="{safe_desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{img_url}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{safe_title}">
<meta name="twitter:description" content="{safe_desc}">
<meta name="twitter:image" content="{img_url}">'''

def ga_snippet():
    if not GA_MEASUREMENT_ID or GA_MEASUREMENT_ID == "G-XXXXXXXXXX":
        # Inject as comment so it's obvious where to drop the real ID, but no network call.
        return "<!-- GA4: paste your Measurement ID into build.py GA_MEASUREMENT_ID then rebuild -->"
    return f'''<script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA_MEASUREMENT_ID}', {{ 'anonymize_ip': true }});
</script>'''

_DAY_ABBR = {"Monday":"Mo","Tuesday":"Tu","Wednesday":"We","Thursday":"Th","Friday":"Fr","Saturday":"Sa","Sunday":"Su"}
def _opening_hours_spec():
    spec = []
    for h in GBP_META.get("hours", []):
        if not h.get("open") or not h.get("close"):
            continue
        spec.append({
            "@type":"OpeningHoursSpecification",
            "dayOfWeek": h["day"],
            "opens": h["open"],
            "closes": h["close"],
        })
    return spec

def localbusiness_schema():
    # Embed top 6 real Google reviews so Google sees structured review content.
    top = [r for r in GBP_REVIEWS.get("reviews", []) if r.get("comment")][:6]
    reviews_jsonld = [{
        "@type":"Review",
        "reviewRating":{"@type":"Rating","ratingValue":str(r["rating"]),"bestRating":"5"},
        "author":{"@type":"Person","name":r["name"]},
        "datePublished":r["date"],
        "reviewBody":r["comment"],
    } for r in top]
    data={
        "@context":"https://schema.org",
        "@type":"LocalBusiness",
        "@id":f"https://claiborneservicesllc.pplx.app/#localbusiness",
        "name":"Claiborne Services LLC",
        "image":img(HERO,1200),
        "logo":"https://claiborneservicesllc.pplx.app/assets/img/favicon-512.png",
        "url":"https://claiborneservicesllc.pplx.app/",
        "telephone":PHONE_TEL,
        "email":EMAIL,
        "priceRange":"$$",
        "address":{"@type":"PostalAddress","addressLocality":"Franklin","addressRegion":"TN","addressCountry":"US"},
        "areaServed":[f"{c} TN" for c in GBP_META.get("service_area_cities", [])],
        "aggregateRating":{"@type":"AggregateRating","ratingValue":_fmt_rating(GBP_RATING),"reviewCount":str(GBP_COUNT),"bestRating":"5"},
        "review":reviews_jsonld,
        "openingHoursSpecification":_opening_hours_spec(),
        "sameAs":[GBP_MAPS_URI],
        "description":GBP_META.get("description","Family-owned tree service, land clearing, forestry mulching, site preparation, and excavation serving Middle Tennessee."),
    }
    return '<script type="application/ld+json">'+json.dumps(data)+'</script>'

def ba_slider(before_id, after_id, label="Before / After", pfx=""):
    return f'''<div class="ba-slider" aria-label="{label} comparison slider">
      <img class="ba-before" src="{pfx + img(before_id,900)}" alt="{label} — before" loading="lazy">
      <img class="ba-after" src="{pfx + img(after_id,900)}" alt="{label} — after" loading="lazy" style="clip-path:inset(0 0 0 50%)">
      <span class="ba-label before">Before</span><span class="ba-label after">After</span>
      <div class="ba-handle"></div>
    </div>'''

def review_card(text, author, meta):
    return f'''<div class="review-card"><div class="stars" aria-label="5 out of 5 stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p>"{text}"</p><div class="review-author">{author}</div><div class="review-meta">{meta}</div></div>'''

def _stars_html(n):
    n = int(round(n))
    filled = "&#9733;" * n
    empty  = "&#9734;" * (5 - n)
    return f'<div class="stars" aria-label="{n} out of 5 stars">{filled}{empty}</div>'

_MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
def _fmt_date(iso):
    try:
        y,m,d = iso.split("-")[:3]
        return f"{_MONTHS[int(m)-1]} {int(d)}, {y}"
    except Exception:
        return iso

def google_review_card(r, show_reply=True):
    name    = html.escape(r.get("name","Google user"))
    photo   = html.escape(r.get("photo",""))
    initial = (r.get("name","G") or "G")[:1].upper()
    rating  = int(r.get("rating",5))
    date    = _fmt_date(r.get("date",""))
    comment = html.escape(r.get("comment","") or "").replace("\n","<br>")
    reply   = html.escape(r.get("reply","") or "")
    avatar = (
        f'<img class="gr-avatar" src="{photo}" alt="" referrerpolicy="no-referrer" loading="lazy" onerror="this.replaceWith(Object.assign(document.createElement(\'div\'),{{className:\'gr-avatar gr-avatar--initial\',textContent:\'{initial}\'}}))">'
        if photo else
        f'<div class="gr-avatar gr-avatar--initial">{initial}</div>'
    )
    body = f'<p class="gr-text">{comment}</p>' if comment else ''
    reply_html = (
        f'<div class="gr-reply"><div class="gr-reply-label">Response from the owner</div><p>{reply}</p></div>'
        if show_reply and reply else ''
    )
    return f'''<article class="google-review-card">
  <header class="gr-head">
    {avatar}
    <div class="gr-who">
      <div class="gr-name">{name}</div>
      <div class="gr-meta"><span class="gr-stars" aria-label="{rating} out of 5 stars">{('&#9733;' * rating)}</span><span class="gr-date">{date}</span></div>
    </div>
    <a class="gr-source" href="{GBP_MAPS_URI}" target="_blank" rel="noopener" aria-label="View on Google" title="View on Google"><span class="gr-source-g" aria-hidden="true"></span></a>
  </header>
  {body}
  {reply_html}
</article>'''

def gbp_badge():
    """Compact Google rating badge — for hero/trust contexts."""
    rating = _fmt_rating(GBP_RATING)
    return f'''<a class="gbp-badge" href="{GBP_MAPS_URI}" target="_blank" rel="noopener" aria-label="View Claiborne Services on Google — {rating} stars, {GBP_COUNT} reviews">
  <span class="gbp-badge-g" aria-hidden="true"></span>
  <span class="gbp-badge-text"><strong>{rating}</strong></span>
  <span class="gbp-badge-stars" aria-hidden="true">{('&#9733;' * int(round(GBP_RATING)))}</span>
  <span class="gbp-badge-count">({GBP_COUNT} reviews)</span>
</a>'''

PROCESS = '''<div class="process">
  <div class="process-step"><div class="process-num">1</div><h3>Contact</h3><p>Call, text, or fill out the quote form. Tell us what you need done.</p></div>
  <div class="process-step"><div class="process-num">2</div><h3>Free Estimate</h3><p>We come out, walk the property, and give you an honest, written price.</p></div>
  <div class="process-step"><div class="process-num">3</div><h3>Schedule</h3><p>Pick a day that works. We confirm and show up when we say we will.</p></div>
  <div class="process-step"><div class="process-num">4</div><h3>Job Done</h3><p>We finish the work and clean up as if we were never there.</p></div>
</div>'''

def write_page(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full,"w") as f: f.write(content)
    print("wrote", path)

# ============ HOMEPAGE ============
def build_home():
    services = [
      ("Tree Services", TREE, "Removal, trimming, and stump grinding handled safely by an experienced crew.", "services/tree-services.html"),
      ("Land Clearing", LAND, "Lot clearing and brush removal to turn overgrown acreage into usable land.", "services/land-clearing.html"),
      ("Forestry Mulching", MULCH, "Clear underbrush and small trees in one pass, leaving a clean mulched finish.", "services/forestry-mulching.html"),
      ("Site Preparation", SITEPREP, "Pad prep and building-site clearing so your project starts on solid ground.", "services/site-preparation.html"),
      ("Excavation", EXCAV, "Trenching, grading, drainage, and earthwork with the right machine for the job.", "services/excavation.html"),
    ]
    tiles=""
    for name,pid,d,link in services:
        tiles+=f'''<a class="card" href="{link}" style="text-decoration:none">
          <img src="{img(pid,600)}" alt="{name} job site in Middle Tennessee" loading="lazy">
          <div class="card-body"><h3>{name}</h3><p>{d}</p><span class="card-link">Learn more &rarr;</span></div></a>'''

    discounts=[
      ("Senior Citizen","10% off","Age 65+, ID at estimate","discounts.html#senior"),
      ("First Responder, Veteran &amp; Military","10% off","Police, fire, EMS, 911, and all military &mdash; active or veteran","discounts.html#first-responder"),
      ("Claiborne Family Tribute","10&ndash;15% off","Alzheimer's, lupus, or autism households","discounts.html#tribute"),
      ("Currey Ingram Academy","10% off","Current and former students, families, faculty, and staff","discounts.html#currey-ingram"),
    ]
    dcards=""
    for n,p,e,link in discounts:
        dcards+=f'<a class="discount-card" href="{link}" style="border-top-color:var(--orange);text-decoration:none;color:inherit"><div class="pct">{p}</div><h3>{n}</h3><p style="color:var(--muted);margin:0">{e}</p></a>'

    # Pick top 3 GBP reviews with substantial comments for the homepage
    _all_gbp = [r for r in GBP_REVIEWS.get("reviews", []) if (r.get("comment") or "").strip()]
    _all_gbp.sort(key=lambda r: (-int(r.get("rating", 0)), -len(r.get("comment") or "")))
    home_reviews = _all_gbp[:3]
    rcards = "".join(google_review_card(r, show_reply=False) for r in home_reviews)

    cities=["Franklin","Brentwood","Spring Hill","Thompson's Station","Nolensville","Columbia","Mt. Pleasant","Nashville"]
    citylinks="".join(f'<a href="service-area/{c.lower().replace(" ","-").replace(".","").replace("\'","")}-tn.html" class="chip">{c}</a>' for c in cities)

    body=f'''
<section class="hero hero--banner" style="{hero_bg(HOME_HERO,1800)};background-position:center 55%">
  <div class="container">
    <p class="eyebrow" style="color:#F0C99A">Family-Owned &middot; Insured &middot; Middle Tennessee</p>
    <h1>Middle Tennessee's Full-Service Tree, Land Clearing &amp; Excavation Team</h1>
    <p class="hero-sub">Family-owned, insured, and built on real work, fair pricing, and respect for your property. Serving Williamson, Maury, and Davidson counties and beyond &mdash; including Franklin, Brentwood, Spring Hill, Thompson's Station, Nolensville, Columbia, Mt. Pleasant, Nashville, and surrounding communities.</p>
    <div class="hero-cta">
      <a class="btn btn--primary" href="contact.html">Get a Free Quote</a>
      <a class="btn btn--ghost" href="tel:{PHONE_TEL}">{icon('phone')}Call Now</a>
    </div>
  </div>
</section>
<div class="photo-credit"><div class="container"><p>Forestry mulching in progress &mdash; our Cat 265 with HM316 mulcher head in Middle Tennessee.</p></div></div>
{trustbar()}

<section class="section">
  <div class="container center">
    <p class="eyebrow">What We Do</p>
    <h2>One Call Covers Tree, Land, and Excavation</h2>
    <p class="lead">Most companies do one of these. We do all three (and more).</p>
  </div>
  <div class="container" style="margin-top:40px"><div class="grid grid-3">{tiles}</div></div>
</section>


<section class="section">
  <div class="container">
    <div class="feature feature--rev">
      <div class="feature-text">
        <p class="eyebrow">Why Claiborne</p>
        <h2>A Family Business Built on Real Work</h2>
        <p>Claiborne Services is family-owned and based in Franklin. We started this company because we believe land work should be done honestly &mdash; fair prices, clear communication, and respect for the property we're standing on.</p>
        <p>When you call, you talk to the people doing the work. No call centers, no runaround. Just a crew that shows up, does the job right, and leaves your place better than we found it.</p>
        <a class="btn btn--outline" href="about.html">Read our story</a>
      </div>
      <div><img src="{img(CREW,900)}" alt="Claiborne Services crew working on a Middle Tennessee job site" loading="lazy"></div>
    </div>
  </div>
</section>

<section class="section bg-forest">
  <div class="container">
    <div class="stats">
      <div><div class="stat-num">Since 2023</div><div class="stat-label">Serving Middle Tennessee</div></div>
      <div><div class="stat-num">500+</div><div class="stat-label">Projects completed</div></div>
      <div><div class="stat-num">100%</div><div class="stat-label">Satisfaction guarantee</div></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container center">
    <p class="eyebrow"><a href="{GBP_MAPS_URI}" target="_blank" rel="noopener" style="color:inherit;text-decoration:none">{_fmt_rating(GBP_RATING)} Stars on Google &middot; {GBP_COUNT} Reviews</a></p>
    <h2>What Our Neighbors Say</h2>
    <div style="margin-top:14px">{gbp_badge()}</div>
  </div>
  <div class="container" style="margin-top:36px"><div class="google-reviews-grid grid grid-3">{rcards}</div>
    <p class="center" style="margin-top:28px"><a class="btn btn--outline" href="reviews.html">See all {GBP_COUNT} reviews</a> <a class="btn btn--ghost" href="{GBP_WRITE_URL}" target="_blank" rel="noopener">Leave a Google review</a></p>
  </div>
</section>

<section class="section bg-alt">
  <div class="container">{finance_callout()}
    <p class="center" style="margin-top:20px"><a class="btn btn--primary" href="contact.html">Ask About Financing</a></p>
  </div>
</section>

<section class="section">
  <div class="container center">
    <p class="eyebrow">Giving Back</p>
    <h2>Discount Programs for Our Community</h2>
    <p class="lead">We keep our pricing accessible and offer multiple discount programs for the people who serve and support our community.</p>
  </div>
  <div class="container" style="margin-top:36px"><div class="grid grid-4">{dcards}</div>
    <p class="center" style="margin-top:28px"><a class="btn btn--forest" href="discounts.html">See All Discount Programs</a></p>
  </div>
</section>

<section class="section bg-alt">
  <div class="container">
    <div class="feature">
      <div class="feature-text">
        <p class="eyebrow">Where We Work</p>
        <h2>Serving Middle Tennessee</h2>
        <p>From Franklin and Brentwood to Columbia, Mt. Pleasant, and Nashville &mdash; we cover Williamson, Maury, and Davidson counties and the communities around them.</p>
        <div class="filter-chips" style="justify-content:flex-start">{citylinks}</div>
      </div>
      <div><iframe class="map-embed" title="Claiborne Services service area map" loading="lazy" src="https://maps.google.com/maps?cid={GBP_CID}&z=10&output=embed"></iframe></div>
    </div>
  </div>
</section>

<section class="section"><div class="container" style="max-width:980px">
  <div class="bruno-block">
    <div class="bruno-photo"><img src="assets/img/bruno.jpg" alt="CEO Bruno &mdash; the Claiborne Services brindle English Bulldog mascot in a yellow hardhat" loading="lazy"></div>
    <div class="bruno-text">
      <p class="eyebrow">Meet the Mascot</p>
      <h2 style="margin-bottom:.2em">CEO Bruno</h2>
      <p>Our first few logo ideas felt generic &mdash; every tree service ends up with the same look. So we looked across the room at Bruno, our brindle English Bulldog and the unofficial mayor of Dallas Downs. We added a yellow hardhat, and just like that we had a mascot that actually fit us: family-owned, friendly, and serious about the work.</p>
      <p style="margin-top:14px"><a class="card-link" href="about.html#bruno">Read the full story on our About page &rarr;</a></p>
    </div>
  </div>
</div></section>

{cta_banner()}
'''
    head = localbusiness_schema()
    write_page("index.html", page(
        "Claiborne Services LLC | Tree, Land Clearing &amp; Excavation in Middle Tennessee",
        "Family-owned tree service, land clearing, forestry mulching, site prep, and excavation across Franklin, Brentwood, Spring Hill, Columbia, Nashville and Middle Tennessee. Licensed, insured, 4.9 stars.",
        body, prefix="", head_extra=head))

# ============ SERVICE PAGES ============
def build_service(slug, name, hero_id, tagline, paras, pricing, included, equipment, faqs, ba_list, gallery_ids, review, real_jobs=None, hero_credit=None):
    pfx="../"
    pricing_rows="".join(f'<div><span>{a}</span><span>{b}</span></div>' for a,b in pricing)
    inc="".join(f'<li>{i}</li>' for i in included)
    bas="".join(f'<div>{ba_slider(b[0],b[1],b[2],pfx)}</div>' for b in ba_list)
    ba_grid_cls = "grid-2" if len(ba_list)>1 else ""
    def _gp(g, w): 
        u = img(g, w)
        # Every non-stock image is local; img() also routes stock ids to a local placeholder. Always prepend pfx on subpages.
        return pfx + u
    thumbs="".join(f'<img src="{_gp(g,500)}" alt="{name} job in Middle Tennessee" loading="lazy" data-lightbox data-full="{_gp(g,1400)}">' for g in gallery_ids)
    paras_html="".join(f"<p>{p}</p>" for p in paras)
    # ---- Real-job photo gallery (local files), rendered above the stock gallery ----
    real_jobs_html = ""
    if real_jobs:
        cards = ""
        for src, caption in real_jobs:
            url = img(src, 1400)
            full = img(src, 1600)
            cards += f'''<figure class="real-job">
              <img src="{pfx}{url}" alt="{caption}" loading="lazy" data-lightbox data-full="{pfx}{full}">
              <figcaption>{caption}</figcaption>
            </figure>'''
        real_jobs_html = f'''
<section class="section">
  <div class="container center"><p class="eyebrow">Real Work, Our Crew</p><h2>Recent {name} Jobs</h2>
    <p class="lead" style="max-width:640px;margin:8px auto 0">Photos from actual Claiborne Services job sites &mdash; no stock images.</p>
  </div>
  <div class="container" style="margin-top:30px"><div class="real-jobs-grid">{cards}</div></div>
</section>'''

    body=f'''
<section class="hero hero--page{' hero--banner' if hero_credit else ''}" style="{hero_bg(hero_id,1600,pfx)};background-position:center 55%">
  <div class="container">
    <p class="eyebrow" style="color:#F0C99A">Middle Tennessee Service</p>
    <h1>{name} in Middle Tennessee</h1>
    <p class="hero-sub">{tagline}</p>
    <div class="hero-cta"><a class="btn btn--primary" href="{pfx}contact.html">Get a Free Quote</a><a class="btn btn--ghost" href="tel:{PHONE_TEL}">{icon('phone')}Call Now</a></div>
  </div>
</section>
{f'<div class="photo-credit"><div class="container"><p>{hero_credit}</p></div></div>' if hero_credit else ''}
{trustbar()}

<section class="section">
  <div class="container" style="max-width:820px">
    <p class="eyebrow">What's Involved</p>
    <h2>{name}, Done Right</h2>
    {paras_html}
  </div>
</section>

<section class="section--tight">
  <div class="container">
    <div class="pricing">
      <h3 style="margin-top:0">Rough Pricing</h3>
      <div class="pricing-rows">{pricing_rows}</div>
      <small>Every job is different, so every job is custom-quoted. These ranges are a starting point &mdash; we'll give you an exact, written price when we come out. No surprises.</small>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="feature">
      <div class="feature-text">
        <p class="eyebrow">No Mess Left Behind</p>
        <h2>What's Included</h2>
        <ul class="checklist">{inc}</ul>
      </div>
      <div><img src="{_gp(gallery_ids[0],900)}" alt="{name} work in progress" loading="lazy" style="border-radius:14px;box-shadow:var(--shadow);height:100%;object-fit:cover"></div>
    </div>
  </div>
</section>

<section class="section bg-alt">
  <div class="container center"><p class="eyebrow">How It Works</p><h2>Our Process</h2></div>
  <div class="container" style="margin-top:36px">{PROCESS}</div>
</section>

<section class="section--tight">
  <div class="container" style="max-width:820px">
    <div class="finance-callout" style="margin-bottom:24px">{icon('layers')}<p><strong>Equipment we use:</strong> {equipment}</p></div>
    {finance_callout()}
  </div>
</section>

<section class="section">
  <div class="container center"><p class="eyebrow">Good to Know</p><h2>Frequently Asked Questions</h2></div>
  <div class="container" style="margin-top:32px">{faq_block(faqs)}</div>
</section>

{real_jobs_html}

<section class="section bg-alt">
  <div class="container center">
    <p class="eyebrow">More Photos</p>
    <h2>See more of our work</h2>
    <p style="max-width:560px;margin:12px auto 24px;color:var(--muted)">Browse real photos from across every service we run &mdash; tree work, land clearing, mulching, site prep, and excavation.</p>
    <a class="btn btn--outline" href="{pfx}gallery.html">See full gallery</a>
  </div>
</section>

{('<section class="section"><div class="container" style="max-width:720px">' + review_card(*review) + '</div></section>') if review else ''}

<section class="section--tight bg-alt">
  <div class="container"><iframe class="map-embed" title="Service area map" loading="lazy" src="https://maps.google.com/maps?cid={GBP_CID}&z=10&output=embed" style="min-height:300px"></iframe></div>
</section>

{cta_banner(pfx)}
<div class="lightbox"><button class="lightbox-close" aria-label="Close">&times;</button><img src="" alt=""></div>
'''
    head = service_schema(name, tagline) + faq_schema(faqs) + localbusiness_schema()
    write_page(f"services/{slug}.html", page(
        f"{name} in Middle Tennessee | Claiborne Services LLC",
        f"{name} across Franklin, Brentwood, Columbia, Nashville and Middle Tennessee. {tagline} Licensed, insured, family-owned. Free quotes.",
        body, prefix=pfx, head_extra=head, mobile_prefix=pfx))

def build_all_services():
    # TREE
    build_service("tree-services","Tree Services",TREE,
      "Safe tree removal, trimming, and stump grinding from a crew that respects your property.",
      ["When a tree comes down &mdash; or needs to &mdash; you want a crew that knows what they're doing. We handle removals, trimming, and stump grinding across Middle Tennessee, from a single hazardous tree near the house to clearing several at once.",
       "We work safely and deliberately around structures, fences, and outbuildings. Every job ends with the brush hauled off and the site raked clean.",
       "Whether it's a storm-damaged oak, an overgrown property line, or a stump that's been bugging you for years, we'll give you a straight answer and a fair price."],
      [("Tree trimming / pruning","starts around $750"),("Small tree removal","starts around $750"),("Large / hazardous tree removal","$1,500&ndash;$3,500+"),("Stump grinding","starts at $300")],
      ["All brush and debris hauled off the property","Stump grinding included if requested","Careful work around homes, fences, and outbuildings","Yard raked and cleaned as if we were never there","Free written estimate before any work begins"],
      "Chainsaws, stump grinders, skid steers, mini skid steers, dump trailers, and lightweight self-propelled lifts as the job requires &mdash; the right tool for each tree, with no shortcuts.",
      [("How much does tree removal cost?","Most removals run between $1,500 and $3,500 depending on the tree's size, location, and how close it is to structures. We give a firm written price after looking at the tree &mdash; never a guess over the phone."),
       ("Do you grind the stump too?","Yes. Stump grinding can be added to any removal, or booked on its own. Just let us know at the estimate so we can include it in the price."),
       ("Are you insured to take down trees near my house?","Yes. We're insured and happy to provide a certificate before any job. We work carefully around structures to protect your property."),
       ("Do you haul away the debris?","Always. Hauling brush, limbs, and logs off your property is included in every tree job unless you have an onsite option for disposal."),
       ("Can you handle an emergency or storm-damaged tree?","Call or text us as soon as it's safe. We prioritize hazardous trees that are on a structure, blocking access, or threatening to fall."),
       ("Do you trim trees, or only remove them?","Both. We do crown thinning, deadwood removal, clearance pruning, and shaping &mdash; not just removals."),
       ("How soon can you come out?","We usually get to estimates within a few days, and we'll always tell you honestly when we can schedule the actual work."),
       ("Will you make a mess of my yard?","Cleanup is part of the job. We rake up, blow off hard surfaces, and do our best to minimize turf disturbance. When heavy machinery is needed there can be some minor marks on the grass, but we work carefully and leave your property looking as pristine as we can.")],
      [],
      [TREE,TREE,TREE,TREE],
      None,
      real_jobs=[
        ("local:assets/img/jobs/tree-bucket-storm-franklin.jpg","Storm damaged limb removal using our Haulotte 55XA self-propelled articulating boom lift in Franklin, TN."),
        ("local:assets/img/jobs/tree-haulotte-drone-backyard.jpg","Drone view of a backyard tree job in Franklin, TN &mdash; our Haulotte 55XA articulating boom lift giving us the reach to trim a row of overgrown pines to reclaim the yard."),
      ],
      hero_credit="Storm damaged limb removal using our Haulotte 55XA self-propelled articulating boom lift in Franklin, TN.")

    # LAND CLEARING
    build_service("land-clearing","Land Clearing",LAND,
      "Lot clearing and brush removal that turns overgrown, unusable acreage into open, workable land.",
      ["Overgrown land has potential &mdash; you just can't see it yet. We clear lots, fence lines, and acreage of brush, scrub, saplings, and unwanted trees so you can build, farm, graze, or finally use the property the way you want.",
       "Depending on the lot, we'll combine our equipment to knock down brush, remove trees, and grub out roots, then haul off or mulch the debris. We're careful about what stays &mdash; mature trees you want to keep, drainage, and property lines.",
       "From a half-acre homesite to multiple acres of rough ground, we'll walk it with you, give you a per-acre range, and get it done."],
      [("Light brush clearing","$1,500&ndash;$3,000 per acre"),("Medium clearing (brush + small trees)","$3,000&ndash;$6,000 per acre"),("Heavy clearing (mature trees + grubbing)","$6,000&ndash;$12,000+ per acre"),("Debris haul-off / burning","quoted per job")],
      ["Brush, scrub, and saplings cleared","Unwanted trees removed and hauled or mulched","Stumps and roots grubbed out where needed","Mature trees you want kept are protected","Property lines and drainage respected","Site left graded and workable"],
      "Excavators, skid steers, and mulching heads &mdash; matched to the size and density of your lot.",
      [("How much does land clearing cost per acre?","It depends heavily on density. Light brush might run $1,500&ndash;$3,000 an acre, while heavy timber with stump grubbing can reach $6,000&ndash;$12,000+. We give a firm per-acre price after walking the property."),
       ("Do you haul off the debris or burn it?","Either. We can haul material off, chip and mulch it on site, or burn it where permitted. We'll talk through the cheapest option for your job."),
       ("Can you clear around trees I want to keep?","Yes. Selective clearing is one of our specialties. Mark or point out what stays and we'll work around it."),
       ("Will the land be ready to build on after clearing?","Clearing gets it open and workable. If you need a finished building pad, our site preparation service handles grading and compaction as the next step."),
       ("Do I need a permit to clear my land?","Sometimes, depending on your county and whether wetlands or drainage are involved. We'll flag anything we notice, but the permit is ultimately the property owner's responsibility."),
       ("How long does it take?","A typical residential lot is one to a few days. Larger acreage depends on density and access &mdash; we'll give you a realistic timeline up front."),
       ("Can you clear a fence line or right-of-way?","Yes. Fence lines, trails, and right-of-way clearing are common jobs for us."),
       ("Is forestry mulching cheaper than full clearing?","Often, yes &mdash; if you don't need the roots removed. See our forestry mulching page; we'll recommend whichever fits your goal and budget.")],
      [],
      [LAND,LAND,LAND,LAND],
      None,
      real_jobs=[
        ("local:assets/img/jobs/land-cat265-grapple-burn.jpg","Lot clearing in progress &mdash; our CAT 265 with grapple rake stacking brush for a controlled burn on a Spring Hill, TN property."),
      ])

    # FORESTRY MULCHING
    build_service("forestry-mulching","Forestry Mulching",MULCH_HERO,
      "Clear underbrush and small trees in a single pass &mdash; leaving a clean, mulched ground cover behind.",
      # hero_credit (passed below via kwarg)
      ["Forestry mulching is the efficient way to clear underbrush, saplings, and small trees without the cost and disturbance of hauling everything off. A mulching head mounted on an excavator or skid steer grinds vegetation in place, leaving a layer of natural mulch that protects the soil and suppresses regrowth.",
       "Because there's no burning and nothing to haul, it's often faster and cleaner than traditional clearing &mdash; and it leaves the ground ready to use. It's ideal for thinning wooded lots, clearing trails, reclaiming pasture, and managing overgrowth along fence lines.",
       "If you want the land opened up without tearing up the topsoil, mulching is usually the smart call. We'll tell you honestly whether mulching or full clearing fits your goals."],
      [("Light underbrush mulching","$1,750&ndash;$2,500 per acre"),("Medium density (brush + saplings)","$2,500&ndash;$4,500 per acre"),("Heavy density / larger trees","$4,500&ndash;$8,000+ per acre"),("Trail or fence-line mulching","quoted per job")],
      ["Underbrush, saplings, and small trees ground in place","Natural mulch layer left to protect soil","No burning and no debris to haul off","Helps suppress regrowth of cleared brush","Mature trees you want kept are protected","Ground left clean and usable in one pass"],
      "Excavators and skid steers fitted with forestry mulching heads, sized to the density of the growth.",
      [("What is forestry mulching?","It's a clearing method where a rotating mulching head grinds trees and brush into mulch right where they stand. The mulch stays on the ground as a protective, regrowth-suppressing layer."),
       ("How is it different from regular land clearing?","Traditional clearing knocks everything down and hauls or burns it, often disturbing the soil. Mulching grinds vegetation in place with minimal ground disturbance and no debris to remove."),
       ("How much does forestry mulching cost?","Light underbrush can run $1,750&ndash;$2,500 per acre; heavy growth with larger trees runs higher. We quote per acre after seeing the density."),
       ("What size trees can you mulch?","It depends on the machine, but we routinely mulch brush and trees up to several inches in diameter. Larger trees may be removed separately first."),
       ("Does the mulch need to be removed?","No. The mulch is a benefit &mdash; it controls erosion, retains moisture, and slows regrowth. It breaks down naturally over time."),
       ("Is mulching good for thinning a wooded lot?","Yes. Selective mulching is great for opening up a wooded property while keeping the trees you want."),
       ("Will the brush grow back?","The mulch layer slows regrowth, but persistent species can return. For permanent clearing with root removal, full land clearing is the better option."),
       ("Can you mulch trails and fence lines?","Absolutely &mdash; trails, fence lines, and right-of-way mulching are common jobs.")],
      [(FOREST,MULCH,"Forestry mulching"),("1486754735734-325b5831c3ad",FIELD,"Wooded lot")],
      ["local:assets/img/jobs/land-cat265-grapple-burn.jpg",FOREST,"1635350736475-c8cef4b21906","1448375240586-882707db888b"],
      None,
      hero_credit="Forestry mulching in progress &mdash; our Cat 265 with HM316 mulcher head in Middle Tennessee.")

    # SITE PREP
    build_service("site-preparation","Site Preparation",SITEPREP,
      "Building-pad prep and site clearing so your project starts on level, solid ground.",
      ["Before the slab pours or the barn goes up, the ground has to be right. Our site preparation service clears, grades, and compacts your building site so your foundation, driveway, or structure sits on stable, properly drained ground.",
       "We handle clearing and grubbing, rough and finish grading, pad building, gravel base, and drainage so water moves away from your structure instead of toward it. Getting the prep right is what keeps a project from running into expensive problems later.",
       "Whether it's a house pad, a shop, a barn, or a driveway, we'll prepare the site to your builder's specs and leave it ready for the next crew."],
      [("Building pad prep &mdash; residential","$2,500&ndash;$8,000+ typical"),("Building pad prep &mdash; large or complex","$8,000&ndash;$15,000+"),("Rough grading","$1,500&ndash;$5,000 per area"),("Gravel base / driveway prep","quoted per job"),("Drainage / culvert work","quoted per job")],
      ["Site cleared and grubbed","Rough and finish grading to spec","Compacted, stable building pad","Gravel base where required","Drainage routed away from structures","Site left ready for the next crew"],
      "Excavators, skid steers, dozers, and compaction equipment &mdash; whatever the pad and grade require.",
      [("What does site preparation include?","Typically clearing and grubbing, grading, building a compacted pad, adding gravel base, and routing drainage &mdash; everything needed before a foundation or structure goes in."),
       ("How much does building pad prep cost?","Most residential pads run $2,500&ndash;$8,000+. Larger pads or jobs with heavy fill, steep grades, or complex drainage can run $8,000&ndash;$15,000+. We quote after seeing the site and your plans."),
       ("Can you work from my builder's specs?","Yes. Bring us the grade and pad specs and we'll prepare the site to match so your builder can step right in."),
       ("Do you handle drainage and culverts?","Yes. Proper drainage is part of good site prep &mdash; we grade for runoff and install culverts or drains as needed."),
       ("Why does compaction matter?","An improperly compacted pad can settle and crack a foundation. We compact in lifts so your structure sits on stable ground."),
       ("Do you do driveways?","Yes. We prep and grade driveway routes and lay gravel base. Final paving is handled by a paving contractor."),
       ("How long does site prep take?","A typical house pad takes a few days depending on conditions. We'll give you a realistic timeline at the estimate."),
       ("Will my lot need clearing first?","If it's wooded or overgrown, yes &mdash; and we can handle the clearing and the prep in one coordinated job.")],
      [],
      [SITEPREP,SITEPREP,SITEPREP,SITEPREP],
      None)

    # EXCAVATION
    build_service("excavation","Excavation",EXCAV_HERO,
      "Trenching, grading, drainage, and earthwork handled with the right machine and a careful operator.",
      ["When a job needs digging, moving, or shaping earth, we bring the right machine and an operator who knows how to use it. Our excavation service covers trenching for utilities and water lines, grading and leveling, drainage solutions, and foundation digs.",
       "We locate before we dig, work cleanly around existing structures and lines, and backfill and grade so your property is left tidy. Whether you're solving a drainage problem, running a new line, or prepping ground for what comes next, we'll handle it safely.",
       "Tell us what you're trying to accomplish and we'll figure out the most efficient, cost-effective way to get there."],
      [("Trenching (utilities / water line)","$15&ndash;$30 per linear foot"),("Grading / leveling","$1,500&ndash;$5,000 per area"),("Drainage / French drain","quoted per job"),("Foundation dig","quoted per job")],
      ["Underground utilities located before digging","Clean trenching for lines and drainage","Grading and leveling to spec","Drainage routed away from structures","Backfill and final grade included","Site left clean and ready for the next phase"],
      "Excavators, skid steers, and trenchers &mdash; sized to the dig, with careful operators on every machine.",
      [("What kinds of excavation do you do?","Trenching for utilities and water lines, grading and leveling, drainage and French drains, and foundation digs."),
       ("How much does trenching cost?","Most trenching runs $15&ndash;$30 per linear foot depending on depth, soil, and what's being buried. We quote after seeing the run."),
       ("Do you locate utilities before digging?","Yes. We call for locates and work carefully around marked lines &mdash; safety and avoiding damage come first."),
       ("Can you fix a drainage or standing-water problem?","Yes. We diagnose where the water's going, then grade or install drains and culverts to move it away from your structures."),
       
       ("Will you backfill and grade after the work?","Yes. Backfilling and leaving a clean final grade is included unless you specify otherwise."),
       ("Can you dig a foundation or footing?","Yes, to your builder's specs. We coordinate so the next crew can pour right away."),
       ("How do I get a price?","Call, text, or fill out the form. We come out, look at the job, and give you a firm written estimate.")],
      [],
      [EXCAV,EXCAV,EXCAV,EXCAV],
      None,
      real_jobs=[
        ("local:assets/img/jobs/excav-stone-trench-bobcat.jpg","Sewer line trenching and PVC sewer pipe installation for new home construction in the Tors of Avalon, Franklin, TN."),
        ("local:assets/img/jobs/excav-driveway-cut.jpg","Waterline trenching and PEX install for a new home build in Columbia, TN using our Cat 265 Compact Track Loader with Trenching attachment."),
        ("local:assets/img/jobs/excav-utility-trench-tree.jpg","Waterline trenching and PEX install for a new home build in Columbia, TN using our Cat 305 CR Mini Excavator."),
        ("local:assets/img/jobs/excav-trench-horse-fence.jpg","Waterline trenching and PEX install for a new garden in LaVergne, TN using our Cat 265 Compact Track Loader with Trenching attachment."),
      ])

# ============ ABOUT ============
def build_about():
    body=f'''
<section class="hero hero--page" style="{hero_bg(CREW,1600)}">
  <div class="container"><p class="eyebrow" style="color:#F0C99A">Our Story</p>
    <h1>The Claiborne Family Story</h1>
    <p class="hero-sub">A family-owned crew doing honest land work across Middle Tennessee.</p>
    <div class="hero-cta"><a class="btn btn--primary" href="contact.html">Get a Free Quote</a></div></div>
</section>
{trustbar()}
<section class="section"><div class="container" style="max-width:780px">
  <p class="eyebrow">Why We Started</p><h2>Built on Real Work and Respect</h2>
  <p>Claiborne Services started the way a lot of good things do &mdash; with a family that wasn't afraid of hard work and got tired of seeing people overpromised and underserved. We're based in Franklin, but our roots and our customers spread across Middle Tennessee.</p>
  <p>We built this company on a few simple ideas: charge a fair price, do exactly what we say we'll do, and treat every property like it belongs to someone we care about. When you call us, you're talking to the people who actually show up and do the work &mdash; not a call center.</p>
  <p>Being full-service matters to us because it matters to you. Most companies make you hire one crew to take down trees, another to clear the lot, and a third to grade and dig. We do all of it. That means one point of contact, one schedule, and one crew that already knows your property.</p>
  <p>We're licensed, insured, and proud to serve neighbors across Middle Tennessee. Big job or small, we'll give you an honest answer and a fair price.</p>
</div></section>
<section class="section bg-forest"><div class="container"><div class="stats">
  <div><div class="stat-num">Since 2023</div><div class="stat-label">Serving Middle Tennessee</div></div>
  <div><div class="stat-num">500+</div><div class="stat-label">Projects completed</div></div>
  <div><div class="stat-num">4.9&#9733;</div><div class="stat-label">Average Google rating</div></div>
</div></div></section>
<section class="section"><div class="container"><div class="feature">
  <div class="feature-text"><p class="eyebrow">Who Shows Up</p><h2>The Crew &amp; The Equipment</h2>
  <p>The work is done by an experienced crew that takes pride in doing it right &mdash; not a rotating cast of subcontractors. We speak English and Spanish, so communication is never a barrier.</p>
  <p>We bring the right machine for the job: excavators, skid steers, mini skid steers, dozers, forestry mulching heads, stump grinders, dump trailers, and lightweight self-propelled lifts. No oversized rigs tearing up your yard, and no undersized equipment dragging the job out.</p></div>
  <div><img src="{img(DOZER,900)}" alt="Claiborne Services equipment on a job site" loading="lazy" style="border-radius:14px;box-shadow:var(--shadow);height:100%;object-fit:cover"></div>
</div></div></section>
<section class="section bg-alt"><div class="container" style="max-width:780px">
  <p class="eyebrow">Peace of Mind</p><h2>Licensing &amp; Insurance</h2>
  <p>We're insured &mdash; ask us for a certificate before any job. It protects you, it protects our crew, and it's how a real company operates.</p>
</div></section>
<section id="bruno" class="section"><div class="container" style="max-width:1000px">
  <div class="bruno-block">
    <div class="bruno-photo"><img src="assets/img/bruno.jpg" alt="CEO Bruno &mdash; the Claiborne Services brindle English Bulldog mascot in a yellow hardhat" loading="lazy"></div>
    <div class="bruno-text">
      <p class="eyebrow">The Story Behind Our Logo</p>
      <h2 style="margin-bottom:.3em">Meet CEO Bruno</h2>
      <p>Every business needs a logo, and for a while we didn't have one we loved. We went through several designs &mdash; clean fonts, generic trees, the usual look-alike logos every tree service company seems to end up with. None of them felt like us.</p>
      <p>Then we looked across the room at Bruno.</p>
      <p>Bruno is our brindle English Bulldog, and if you live in Dallas Downs you already know him. He's the neighborhood greeter, the front-porch supervisor, and an absolute character. So we took a photo of him, added a yellow hardhat, and put him to work as our official mascot.</p>
      <p>He's been <strong>CEO Bruno</strong> ever since &mdash; and somehow it just fits. Family-owned, a little stubborn, friendly to everyone, and serious about the job.</p>
    </div>
  </div>
</div></section>
<section class="section"><div class="container"><div class="finance-callout" style="border-left-color:var(--brown);background:#F2ECE3;border-color:#d8cab4">
  {icon('home')}<p><strong>The Claiborne Family Tribute Discount.</strong> We offer a 10&ndash;15% discount to households affected by Alzheimer's, lupus, or autism &mdash; named in memory of family members who shaped who we are. <a href="discounts.html">Learn about our discount programs &rarr;</a></p></div></div></section>
{cta_banner()}
'''
    write_page("about.html", page("About Claiborne Services LLC | Family-Owned in Middle Tennessee",
      "The Claiborne family story — a family-owned, insured tree, land clearing, and excavation company serving Middle Tennessee with honest pricing and real work.",
      body, prefix="", head_extra=localbusiness_schema()))

# ============ SERVICE AREA ============
CITY_DATA = {
  "franklin-tn":("Franklin","1503387762-592deb58ef4e","Our home base in Williamson County."),
  "brentwood-tn":("Brentwood","1416879595882-3373a0480b5b","Wooded lots and estate properties."),
  "spring-hill-tn":("Spring Hill","1466692476868-aef1dfb1e735","Growing fast &mdash; we clear and prep new sites."),
  "thompsons-station-tn":("Thompson's Station","1500382017468-9049fed747ef","Rural acreage and homesites."),
  "nolensville-tn":("Nolensville","1448375240586-882707db888b","Hillside lots and tree work."),
  "columbia-tn":("Columbia","1486754735734-325b5831c3ad","Maury County land and farm work."),
  "mt-pleasant-tn":("Mt. Pleasant","1543674892-7d64d45df18b","Affordable land work for every property."),
  "nashville-tn":("Nashville","1530541930197-ff16ac917b0e","Davidson County tree and excavation."),
  "belle-meade-tn":("Belle Meade","1416879595882-3373a0480b5b","Estate properties and mature hardwoods."),
  "forest-hills-tn":("Forest Hills","1502082553048-f009c37129b9","Heavily treed, sloped luxury lots."),
  "oak-hill-tn":("Oak Hill","1473773508845-188df298d2d1","Wooded estate lots and drainage work."),
  "leipers-fork-tn":("Leiper's Fork","1500382017468-9049fed747ef","Equestrian estates and rural acreage."),
  "fairview-tn":("Fairview","1500382017468-9049fed747ef","Rural acreage and forestry mulching."),
  "college-grove-tn":("College Grove","1500382017468-9049fed747ef","Horse farms and rolling country."),
  "triune-tn":("Triune","1486754735734-325b5831c3ad","Crossroads of three counties."),
  "lewisburg-tn":("Lewisburg","1543674892-7d64d45df18b","Marshall County farms and lots."),
  "chapel-hill-tn":("Chapel Hill","1543674892-7d64d45df18b","Rural acreage and pasture work."),
}
# Each county: (name, description, city-page slugs, additional communities served)
COUNTY_GROUPS = [
  ("Williamson County", "Our home county &mdash; Franklin-based and a short drive to every town.",
    ["franklin-tn","brentwood-tn","nolensville-tn","thompsons-station-tn","leipers-fork-tn"],
    ["Arrington","Fairview","College Grove","Triune"]),
  ("Davidson County", "The Nashville area &mdash; from city neighborhoods to the wooded estate enclaves.",
    ["nashville-tn","belle-meade-tn","forest-hills-tn","oak-hill-tn"],
    ["Green Hills","West Meade"]),
  ("Maury County", "Spring Hill south to Mt. Pleasant &mdash; rural acreage, farms, and growing homesites.",
    ["spring-hill-tn","columbia-tn","mt-pleasant-tn"],
    ["Culleoka"]),
  ("Rutherford County", "Murfreesboro and the fast-growing communities just east of Nashville.",
    [], ["Murfreesboro","Smyrna","La Vergne","Eagleville"]),
  ("Wilson County", "Mt. Juliet and Lebanon &mdash; established neighborhoods and rural acreage east of Nashville.",
    [], ["Mt. Juliet","Lebanon"]),
  ("Marshall County", "Lewisburg and the surrounding rural communities south of Maury.",
    [], ["Lewisburg","Chapel Hill","Cornersville"]),
  ("Giles County", "Pulaski and the small towns south toward the Alabama line.",
    [], ["Pulaski","Lynnville"]),
  ("Dickson, Cheatham &amp; West", "Dickson and Kingston Springs &mdash; rural acreage and wooded homesites west of Nashville.",
    [], ["Dickson","Kingston Springs"]),
  ("Bedford, Lawrence, Hickman &amp; Lewis", "The wider rural belt &mdash; we travel for the right job throughout south Middle Tennessee.",
    [], ["Shelbyville","Lawrenceburg","Centerville","Hohenwald"]),
]
NEW_CITIES = {"belle-meade-tn","forest-hills-tn","oak-hill-tn","leipers-fork-tn","fairview-tn","college-grove-tn","triune-tn","lewisburg-tn","chapel-hill-tn"}

def build_service_area():
    groups_html=""
    for cname, cdesc, slugs, extras in COUNTY_GROUPS:
        cards=""
        for slug in slugs:
            name,pid,teaser = CITY_DATA[slug]
            badge = '<span class="badge-new">New</span>' if slug in NEW_CITIES else ""
            url = img(pid,600)
            bg = '' if url.endswith('placeholder-need-photo.jpg') else f"background-image:url('{url}')"
            cards+=f'''<a class="city-card{(' city-card--nophoto' if not bg else '')}" href="service-area/{slug}.html" style="{bg}">{badge}<div class="city-body"><h3>{name}</h3><p>{teaser}</p></div></a>'''
        cards_html = f'<div class="grid grid-4">{cards}</div>' if cards else ''
        extras_html = ''
        if extras:
            chips = "".join(f'<span class="chip chip--town">{t}</span>' for t in extras)
            label = 'Also serving' if slugs else 'Communities we cover'
            extras_html = f'<div class="county-extras"><span class="county-extras-label">{label}:</span> <span class="chip-row">{chips}</span></div>'
        groups_html+=f'''<div class="county-group"><div class="county-head"><h3>{cname}</h3><p class="county-meta">{cdesc}</p></div>{cards_html}{extras_html}</div>'''
    body=f'''
<section class="hero hero--page" style="{hero_bg("1503387762-592deb58ef4e",1600)}">
  <div class="container"><p class="eyebrow" style="color:#F0C99A">Coverage</p><h1>Where We Work in Middle Tennessee</h1>
  <p class="hero-sub">Family-owned, insured, and based in Franklin &mdash; serving 35+ communities across Middle Tennessee.</p>
  <div class="hero-cta"><a class="btn btn--primary" href="contact.html">Get a Free Quote</a><a class="btn btn--ghost" href="tel:{PHONE_TEL}">{icon('phone')}Call {PHONE}</a></div></div>
</section>
{trustbar()}
<section class="section"><div class="container center" style="max-width:820px"><p class="eyebrow">Local Coverage</p><h2>One Crew. One Standard. Middle Tennessee Wide.</h2>
  <p class="lead">From estate properties in Belle Meade to pasture work in Leiper's Fork to acreage out in Lawrenceburg, we bring the same crew, the same equipment, and the same fair pricing to every job. Click any featured town for local work, FAQs, and a map &mdash; or scan the list for the communities we cover.</p></div></section>
<section class="section--tight"><div class="container"><iframe class="map-embed" title="Claiborne Services service area &mdash; Middle Tennessee" loading="lazy" src="https://maps.google.com/maps?cid={GBP_CID}&z=10&output=embed" style="min-height:420px"></iframe></div></section>
<section class="section"><div class="container">{groups_html}</div></section>
<section class="section bg-alt"><div class="container center" style="max-width:720px">
  <p class="eyebrow">Beyond the List</p>
  <h2 style="margin-bottom:.3em">Don't see your town?</h2>
  <p class="lead" style="margin:0 auto 22px">We travel for the right job throughout Middle Tennessee. If your community isn't listed above, call or text us &mdash; we'll let you know if we can make the trip.</p>
  <div class="flex-cta" style="justify-content:center"><a class="btn btn--primary" href="tel:{PHONE_TEL}">{icon('phone')}Call {PHONE}</a><a class="btn btn--outline" href="sms:{PHONE_TEL}">{icon('message')}Text Us</a><a class="btn btn--ghost" href="contact.html">Request a Quote</a></div>
</div></section>
{cta_banner()}
'''
    write_page("service-area.html", page("Service Area | Claiborne Services LLC — Middle Tennessee Coverage",
      "Claiborne Services covers 35+ Middle Tennessee communities across Williamson, Davidson, Maury, Rutherford, Wilson, Marshall, Giles, Dickson, Cheatham, Bedford, Lawrence, Hickman, and Lewis counties — including Franklin, Brentwood, Nashville, Murfreesboro, Mt. Juliet, Columbia, and more.",
      body, prefix="", head_extra=localbusiness_schema()))

# ============ CITY PAGES ============
LEIPERS_ROOTS_HTML = '''
<section class="section"><div class="container" style="max-width:880px">
  <div class="roots-block">
    <p class="eyebrow">Family Roots in Leiper's Fork</p>
    <h2>Fifty Years of Friendship &amp; Land Work</h2>
    <p><strong>Dr. Jon Warren, DVM,</strong> and his wife <strong>Nina</strong> have known the Claiborne family since the 1970s, when Jon became the farm vet for the McDonald Thoroughbred Farm where Shawn grew up. That working friendship turned into a lifelong one.</p>
    <p>For more than thirty years, Shawn and his father James serviced tractors, cut trees, repaired waterlines, and handled whatever else came up on the Warrens' Leiper's Fork farm. One of Shawn's favorite teenage rituals: stopping at <strong>Puckett's</strong> for a tenderloin, egg, and cheese biscuit before heading out to a day's work at the Warrens'. Some traditions are worth keeping.</p>
    <p>Leiper's Fork is also Claiborne country in its own right. Uncles, aunts, cousins, and kin from further down the family line have lived out here over the years &mdash; so when we drive these back roads, we're driving past family history.</p>
    <p>Today we're proud to keep working the same land. Mowing creek banks with our excavator, clearing trails with our forestry mulcher, making a beautiful place even better &mdash; that kind of work, on this kind of ground, never stops being satisfying.</p>
  </div>
</div></section>
'''

FRANKLIN_ROOTS_HTML = '''
<section class="section"><div class="container" style="max-width:880px">
  <div class="roots-block">
    <p class="eyebrow">Franklin Is Home, Too</p>
    <h2>Why Shawn Chose Franklin</h2>
    <p>Franklin is where <strong>Shawn Claiborne</strong> built his own life and his own business. He first lived in Franklin from <strong>2003 to 2006</strong>, in a place near <strong>Jim Warren Park</strong>. He moved back for good in <strong>2014</strong> and has lived in the <strong>Dallas Downs</strong> subdivision ever since.</p>
    <p>Franklin has changed a lot in those twenty-plus years &mdash; new neighborhoods, new businesses, new traffic patterns, new faces. But the things that drew him here haven't. It's still one of the best places in Middle Tennessee to live and raise a family &mdash; safe, friendly, surrounded by good people, and beautiful in every season.</p>
    <p>That's why Claiborne Services is based right here. When we work in Franklin, we're working in our own backyard for our own neighbors. Every job is one we'll see again when we drive past.</p>
  </div>
</div></section>
'''

SPRING_HILL_ROOTS_HTML = '''
<section class="section"><div class="container" style="max-width:880px">
  <div class="roots-block">
    <p class="eyebrow">Family Roots in Spring Hill</p>
    <h2>Weekends &amp; Summers at High Ridge Farms</h2>
    <p>From <strong>1991 to 1994</strong>, Shawn spent most weekends and summers in Spring Hill alongside his older brother, <strong>Darryl</strong>, who worked at <strong>High Ridge Farms</strong>. The two of them put in honest days &mdash; cleaning stalls, mowing pastures, walking horses out to graze, mending fence, and cutting trees back off the line.</p>
    <p>It was the kind of work that doesn't leave you. Long hours in the Tennessee sun, the smell of cut hay, and a job list that never quite finished. By the time Shawn was a teenager, he'd already learned what it meant to show up early, work until it was done, and take care of a property like it was your own.</p>
    <p>That's a big part of why Spring Hill still feels familiar to us &mdash; and why we take Spring Hill jobs personally. The town has grown a lot since the early '90s, but the land work hasn't changed much, and neither has the way we approach it.</p>
  </div>
</div></section>
'''

BRENTWOOD_ROOTS_HTML = '''
<section class="section"><div class="container" style="max-width:880px">
  <div class="roots-block">
    <p class="eyebrow">Brentwood Is Home</p>
    <h2>Where Shawn Grew Up</h2>
    <p>Brentwood isn't just a service area for us &mdash; it's home. <strong>Shawn Claiborne</strong> grew up on the old McDonald Thoroughbred Farm from <strong>1983 to 2003</strong>, on the property that later became the campus of <strong><a href="https://www.curreyingram.org" target="_blank" rel="noopener">Currey Ingram Academy</a></strong>.</p>
    <p>His father, <strong>James Claiborne</strong>, started working that land in 1960 under the previous owner, Duncan McDonald, and moved onto the property in 1965. He never left. When <a href="https://www.curreyingram.org" target="_blank" rel="noopener">Currey Ingram Academy</a> purchased the farm in 1999, James stayed on and continued caring for the grounds until his passing in 2024 &mdash; a 64-year stretch of one man, one piece of Brentwood land, and a quiet kind of devotion you don't see much anymore.</p>
    <p>Some of Shawn's earliest memories are out in that hayfield. Before he was even old enough for kindergarten, he was driving the old <strong>Ford 871 Select-O-Speed tractor</strong> pulling the hay baler and wagon, with James riding the wagon stacking bales behind him. That 35-acre hayfield is the same ground that's now the <strong>soccer field at <a href="https://www.curreyingram.org" target="_blank" rel="noopener">Currey Ingram Academy</a></strong>. Shawn learned to ride a pony there, drive a go-kart, get on a dirt bike, mow grass, and a hundred other things a boy learns when he grows up on a working farm. Every bit of who he is as an operator today traces back to that land.</p>

    <h3 style="margin-top:32px;color:#2C5530">A Brentwood Love Story: Johnson Cove</h3>
    <p>Just up the road on Johnson Chapel Road West, the <strong>Johnson Cove</strong> neighborhood sits on land that once belonged to <strong>Sadie and Tony McClanahan</strong>. Sadie and Tony were Shawn's mother <strong>Cynthia's</strong> aunt and uncle &mdash; Shawn's great aunt and uncle &mdash; and that property is where Shawn's parents first met.</p>
    <p>James was out there helping Sadie and Tony install a waterline and put in new flooring. Cynthia had come down for the weekend to visit her aunt and uncle. The two of them crossed paths on that Brentwood property &mdash; and the rest was history. A whole family, a whole business, traces back to one weekend on one piece of Johnson Chapel Road.</p>
    <h3 style="margin-top:32px;color:#2C5530">Earning His Keep: Aunt Sadie &amp; Ms. Ola</h3>
    <p>Years later, when Shawn was 13, he started spending time at the same property helping <strong>Great Aunt Sadie</strong> &mdash; mowing the yard, weed-eating, watering plants, vacuuming the house, and loading up the garbage and recycling to haul down to the convenience center off Sneed Road. That was the first time Shawn earned his keep working a piece of Brentwood land.</p>
    <p>Shawn also worked for <strong>Ms. Ola McClanahan</strong>, Sadie's sister-in-law, on her farm off Murray Lane &mdash; the land that's now the <strong>Avery subdivision</strong>. Mowing, hauling furniture, loading up trash and recycling, and whatever else needed doing. Two Brentwood properties, two McClanahan households, two pieces of land that have since become neighborhoods &mdash; and one teenager learning that work is what holds a place together. Some of the same instincts Shawn uses on jobs today &mdash; show up, do it right, take care of the place like it's your own &mdash; got their start right there.</p>

    <p style="margin-top:24px">Walking these Brentwood properties today, we feel that history. It shapes how we treat every yard, every tree, and every neighbor we work for here.</p>
    <p style="margin-top:18px"><a class="card-link" href="../discounts.html">Read about the Currey Ingram Academy discount &rarr;</a></p>
  </div>
</div></section>
'''

def build_city(slug, full_intro_paras, faqs, job_ids, extra_html=""):
    name = CITY_DATA[slug][0]
    pfx="../"
    paras="".join(f"<p>{p}</p>" for p in full_intro_paras)
    def _gp(g, w): 
        u = img(g, w)
        # Every non-stock image is local; img() also routes stock ids to a local placeholder. Always prepend pfx on subpages.
        return pfx + u
    thumbs="".join(f'<img src="{_gp(g,500)}" alt="{name} job site" loading="lazy" data-lightbox data-full="{_gp(g,1400)}">' for g in job_ids)
    body=f'''
<section class="hero hero--page" style="{hero_bg(CITY_DATA[slug][1],1600,pfx)}">
  <div class="container"><p class="eyebrow" style="color:#F0C99A">{name}, Tennessee</p>
  <h1>Tree Service, Land Clearing &amp; Excavation in {name}, TN</h1>
  <p class="hero-sub">Full-service land work for {name} homeowners, builders, and landowners.</p>
  <div class="hero-cta"><a class="btn btn--primary" href="{pfx}contact.html">Get a Free Quote</a><a class="btn btn--ghost" href="tel:{PHONE_TEL}">{icon('phone')}Call Now</a></div></div>
</section>
{trustbar()}
<section class="section"><div class="container" style="max-width:800px"><p class="eyebrow">Serving {name}</p><h2>Your Local Land Work Team in {name}</h2>{paras}
  <div class="filter-chips" style="justify-content:flex-start;margin-top:18px">
    <a class="chip" href="{pfx}services/tree-services.html">Tree Services</a>
    <a class="chip" href="{pfx}services/land-clearing.html">Land Clearing</a>
    <a class="chip" href="{pfx}services/forestry-mulching.html">Forestry Mulching</a>
    <a class="chip" href="{pfx}services/site-preparation.html">Site Prep</a>
    <a class="chip" href="{pfx}services/excavation.html">Excavation</a>
  </div></div></section>
{extra_html}
<section class="section bg-alt"><div class="container center"><p class="eyebrow">Recent Work</p><h2>Jobs Near {name}</h2></div>
  <div class="container" style="margin-top:28px"><div class="gallery-grid">{thumbs}</div></div></section>
<section class="section--tight"><div class="container"><iframe class="map-embed" title="{name} TN map" loading="lazy" src="https://www.google.com/maps?q={name.replace(' ','+').replace(chr(39),'')},+TN&output=embed" style="min-height:360px"></iframe></div></section>
<section class="section"><div class="container center"><p class="eyebrow">{name} FAQ</p><h2>Questions from {name} Homeowners</h2></div>
  <div class="container" style="margin-top:32px">{faq_block(faqs)}</div></section>
{cta_banner(pfx)}
<div class="lightbox"><button class="lightbox-close" aria-label="Close">&times;</button><img src="" alt=""></div>
'''
    head = localbusiness_schema() + faq_schema(faqs)
    write_page(f"service-area/{slug}.html", page(
      f"Tree Service, Land Clearing &amp; Excavation in {name}, TN | Claiborne Services",
      f"Family-owned tree service, land clearing, forestry mulching, site prep, and excavation in {name}, Tennessee. Licensed, insured, free quotes.",
      body, prefix=pfx, head_extra=head, mobile_prefix=pfx))

def build_cities():
    build_city("franklin-tn",
      ["Franklin is home for us. As a Franklin-based, family-owned company, we know this area's mix of established neighborhoods, wooded estate lots, and growing acreage on the edges of town. From big shade trees that need careful removal near historic homes to clearing and grading new homesites, we handle it all locally.",
       "Williamson County properties often come with mature hardwoods, rolling terrain, and drainage that needs attention. We work carefully around structures and landscaping, and we keep our pricing fair so the service is accessible to every Franklin household &mdash; not just the high end.",
       "Whether you need a hazardous tree taken down, a lot cleared for a build, or trenching and drainage solved, we're a short drive away and quick to get you an estimate."],
      [("Do you offer tree service in Franklin, TN?","Yes &mdash; Franklin is our home base. We do tree removal, trimming, and stump grinding throughout Franklin and all of Williamson County."),
       ("Can you clear a wooded lot in Franklin for building?","Absolutely. We clear, grub, and grade homesites and acreage across Franklin, then prep the pad to your builder's specs."),
       ("How fast can you get to a Franklin property?","Since we're based here, we usually get to Franklin estimates within a couple of days."),
       ("Do you handle drainage problems in Franklin neighborhoods?","Yes. Standing water and runoff are common on Williamson County lots &mdash; we grade and install drains to move water away from your home."),
       ("Are you licensed and insured to work in Franklin?","Yes. We're insured and we'll provide a certificate on request.")],
      ["1503387762-592deb58ef4e",TREE,LAND,EXCAV],
      extra_html=FRANKLIN_ROOTS_HTML)
    build_city("leipers-fork-tn",
      ["Leiper's Fork is one of the most beautiful places we work &mdash; rolling pasture, creek-cut bottoms, hardwood ridges, equestrian estates, and long winding back roads. It's also a place our family has known well for generations.",
       "We clear overgrown pasture and fence lines, mulch dense brush along creek banks and trails, take down big trees safely around homes and barns, and grade and drain ground for new barns, riding rings, and homesites. We come equipped for big rural jobs and we work cleanly around livestock, fencing, and the kind of mature landscape Leiper's Fork is known for.",
       "Whether you're an established estate or a newer landowner getting your acreage in shape, we're a short drive away from our Franklin base and quick to come give you an honest quote."],
      [("Do you clear pasture and acreage in Leiper's Fork?","Yes. Pasture reclamation, brush clearing, and forestry mulching on rural Leiper's Fork acreage are core jobs for us."),
       ("Can you prep a site for a barn or riding ring?","Yes. We clear, grade, and compact pads for barns, arenas, and homesites, and handle the drainage that rural Williamson County properties need."),
       ("Do you mow creek banks or clear trails on bigger Leiper's Fork properties?","Yes &mdash; one of our favorite jobs. We mow creek banks with our excavator and clear trails with our forestry mulcher so they stay walkable and rideable year-round."),
       ("Do you have local roots in Leiper's Fork?","Yes. Our family has known Leiper's Fork families since the 1970s, and Claiborne kin &mdash; uncles, aunts, cousins &mdash; have lived out here for decades. It's home ground for us."),
       ("How fast can you get to a Leiper's Fork property?","Usually within a couple of days for an estimate. We're a short drive from Franklin.")],
      [FIELD,LAND,FOREST],
      extra_html=LEIPERS_ROOTS_HTML)
    build_city("columbia-tn",
      ["Columbia and the wider Maury County area are a big part of who we serve. There's a lot of farmland, rural acreage, and wooded property out here, and the needs are different from the suburbs &mdash; bigger clearing jobs, fence lines, pasture reclamation, and serious drainage work.",
       "We bring the right equipment for rural Columbia jobs: excavators, mulching heads, and dozers that can handle acreage, not just a backyard. And because we keep our prices fair, Columbia and Mt. Pleasant landowners get the same quality service without a premium-market markup.",
       "From clearing overgrown pasture to digging a new water line or taking down storm-damaged trees, we're glad to make the drive to Maury County and give you an honest estimate."],
      [("Do you serve Columbia, TN?","Yes. Columbia and Maury County are a core part of our service area for tree work, land clearing, mulching, site prep, and excavation."),
       ("Can you clear pasture or farmland near Columbia?","Yes &mdash; pasture reclamation, brush clearing, and fence-line work are common jobs for us in Maury County."),
       ("Is your pricing higher because you're based near Franklin?","No. We keep our pricing fair and consistent for Columbia and Mt. Pleasant customers &mdash; we want our service to be accessible everywhere we work."),
       ("Do you do drainage and trenching in Columbia?","Yes. We handle trenching for water lines, French drains, and grading to fix standing-water problems on rural and residential properties."),
       ("Will you travel out to Mt. Pleasant too?","Yes. We regularly serve Mt. Pleasant and the surrounding Maury County area.")],
      ["1486754735734-325b5831c3ad",LAND,FIELD,FOREST])
    build_city("spring-hill-tn",
      ["Spring Hill is one of the fastest-growing communities in Middle Tennessee, and that growth means a lot of land work &mdash; new homesites being cleared, lots being graded, and trees coming down to make room. We help Spring Hill homeowners and builders get sites ready and keep established properties healthy.",
       "Straddling Williamson and Maury counties, Spring Hill has everything from tight subdivision lots to open acreage. We size our equipment and approach to the property, work cleanly around new construction, and keep pricing fair for a community of growing families.",
       "Need a lot cleared, a pad prepped, a tree removed, or drainage fixed before it becomes a bigger problem? We're close by and quick to get you a quote."],
      [("Do you provide land clearing in Spring Hill?","Yes. With Spring Hill growing so fast, lot clearing and site prep are some of our most common jobs here."),
       ("Can you prep a building pad in Spring Hill?","Yes. We clear, grade, and compact pads to your builder's specs and route drainage so your foundation sits right."),
       ("Do you do tree removal in Spring Hill subdivisions?","Yes. We remove and trim trees carefully in established neighborhoods, working around homes, fences, and lines."),
       ("How quickly can you quote a Spring Hill job?","We usually reach Spring Hill estimates within a couple of days &mdash; call or text to get on the schedule."),
       ("Are you insured to work on new construction sites?","Yes. We're insured and can provide a certificate before working on any site."),
       ("Do you have any history in Spring Hill?","Yes &mdash; from 1991 to 1994, Shawn spent most weekends and summers working at High Ridge Farms in Spring Hill alongside his older brother Darryl. Spring Hill has been part of his life for a long time.")],
      ["1466692476868-aef1dfb1e735",SITEPREP,LAND,EXCAV],
      extra_html=SPRING_HILL_ROOTS_HTML)
    build_city("brentwood-tn",
      ["Brentwood is home for us. Shawn grew up here, on the McDonald Thoroughbred Farm that later became the campus of <a href=\"https://www.curreyingram.org\" target=\"_blank\" rel=\"noopener\">Currey Ingram Academy</a>. That kind of history with a place changes how you treat it. When we work in Brentwood, we're working in the neighborhood we know best.",
       "Brentwood's properties &mdash; wooded estate lots, mature hardwoods, manicured landscapes, larger acreage on the edges &mdash; deserve careful, professional work. We take down big trees safely near homes, thin overgrown areas, and handle grading and drainage on estate-sized lots without tearing up the place.",
       "We keep our service personable and our pricing fair. From a single hazardous tree to clearing and prepping a back acre, Brentwood homeowners can call one Brentwood-rooted crew for all of it."],
      [("Do you remove large trees in Brentwood?","Yes. We specialize in safe removal of large, mature trees near homes and structures &mdash; with careful work, the right equipment, and insurance coverage."),
       ("Can you work on larger Brentwood estate lots?","Definitely. Clearing, mulching, grading, and drainage on estate-sized Brentwood properties are common jobs for us."),
       ("Are you familiar with Brentwood specifically?","Yes &mdash; Shawn grew up here on the McDonald Thoroughbred Farm, now the Currey Ingram Academy campus. Brentwood is home."),
       ("Do you offer a discount for Currey Ingram families?","Yes. Current and former students, parents, and faculty get 10% off &mdash; in honor of Shawn's father, James Claiborne, who worked the campus for 64 years."),
       ("How fast can you get to a Brentwood property?","Usually within a couple of days for an estimate. Brentwood is right next door to our Franklin base.")],
      [FOREST,TREE,LAND],
      extra_html=BRENTWOOD_ROOTS_HTML)

def build_city_stubs():
    # remaining cities as lighter pages (still unique copy)
    stubs={
      "thompsons-station-tn":(["Thompson's Station blends rural acreage with new growth, and we serve both. Whether you're reclaiming overgrown land, clearing a homesite, or solving a drainage issue on a country lot, we bring the right equipment and a fair price.",
         "We're a short drive away and happy to walk your property, talk through options, and give you an honest estimate for tree work, clearing, mulching, site prep, or excavation."],
        [("Do you clear acreage in Thompson's Station?","Yes &mdash; land clearing and forestry mulching on rural Thompson's Station acreage are common jobs for us."),
         ("Can you prep a homesite in Thompson's Station?","Yes. We clear, grade, and prep building pads and handle the drainage that rural lots often need.")],
        [FIELD,LAND,SITEPREP]),
      "nolensville-tn":(["Nolensville's hillside lots and wooded properties often need careful tree work and thoughtful grading. We remove and trim trees on sloped ground, clear lots for building, and solve the drainage challenges that come with hilly terrain.",
        "As a family-owned, insured crew, we treat Nolensville properties with care and keep our pricing fair. One call covers tree, land, and excavation needs."],
        [("Do you do tree service in Nolensville?","Yes. We handle removal, trimming, and stump grinding throughout Nolensville, including tricky hillside removals."),
         ("Can you handle grading on a sloped Nolensville lot?","Yes. Grading and drainage on hilly Nolensville terrain is something we deal with regularly.")],
        [TREE,FOREST,EXCAV]),
      "mt-pleasant-tn":(["Mt. Pleasant and the surrounding Maury County area are very much part of who we serve. We bring full-service land work &mdash; tree removal, clearing, mulching, site prep, and excavation &mdash; at fair, accessible pricing for rural and small-town properties.",
        "We make the drive gladly and treat every Mt. Pleasant job, big or small, with the same care and honesty. Call or text and we'll come give you a straight estimate."],
        [("Do you serve Mt. Pleasant, TN?","Yes. Mt. Pleasant is part of our regular Maury County service area for all five of our services."),
         ("Is your pricing fair for Mt. Pleasant customers?","Yes. We keep pricing consistent and accessible &mdash; no premium-market markup for being based near Franklin.")],
        [FIELD,LAND,FOREST]),
      "nashville-tn":(["We serve Davidson County and the Nashville area for tree service, clearing, and excavation. From removing trees in established Nashville neighborhoods to grading, trenching, and drainage work on residential and small commercial properties, we bring the right machine and a careful operator.",
        "Insured and family-owned, we handle Nashville jobs cleanly and professionally, working around tight access and existing structures with care."],
        [("Do you do tree removal in Nashville?","Yes. We remove and trim trees throughout the Nashville and Davidson County area, working carefully in tight neighborhoods."),
         ("Can you handle excavation and drainage in Nashville?","Yes. Trenching, grading, and drainage are all part of what we do in the Nashville area.")],
        [DOZER,TREE,EXCAV]),
      "belle-meade-tn":(["Belle Meade's estate properties come with mature hardwoods, manicured landscaping, and homes worth protecting. We take down large oaks, hickories, and tulip poplars carefully &mdash; no shortcuts, no damage to gardens, walls, or driveways. For estate-sized lots, we also handle selective thinning, deadwood removal, and drainage work that keeps high-value grounds healthy.",
        "As an insured, family-owned crew, we treat Belle Meade properties with the discretion and care they require. One call covers tree work, clearing, grading, and drainage &mdash; with clean job sites and honest pricing every time."],
        [("Do you do tree work on Belle Meade estates?","Yes. We specialize in safe removal and pruning of large, mature trees near high-value homes, with insurance coverage and meticulous cleanup."),
         ("Can you handle drainage on a large Belle Meade lot?","Yes. Grading, French drains, and runoff control on estate-sized properties are common jobs for us.")],
        [FOREST,TREE,LAND]),
      "forest-hills-tn":(["Forest Hills lives up to its name &mdash; densely wooded, hilly lots with mature canopy and steep grades. We do careful tree removal and trimming on sloped ground, thin out crowded stands to keep the healthy trees thriving, and solve the drainage and erosion challenges that come with hillside properties.",
        "We bring the right equipment for tight access and slope work, and we're insured for jobs around luxury homes. Whether it's a single hazardous tree, storm cleanup, or grading a sloped back lot, we work cleanly and quote honestly."],
        [("Do you remove trees on sloped Forest Hills lots?","Yes. Hillside removals and pruning are routine for us &mdash; we bring the right equipment and experience for sloped, wooded properties."),
         ("Can you fix erosion or drainage on a Forest Hills hillside?","Yes. Grading, drainage routing, and erosion control on hilly Davidson County lots are part of what we do.")],
        [FOGFOREST,TREE,EXCAV]),
      "oak-hill-tn":(["Oak Hill's wooded estate lots share a lot with neighboring Forest Hills &mdash; mature trees, larger parcels, and homes that deserve careful work around them. We handle removals, pruning, lot thinning, and the grading and drainage work that keeps wooded properties from turning into wet, root-bound problems.",
        "Family-owned and insured, we treat Oak Hill jobs with the care a high-end neighborhood expects. One crew, one call &mdash; tree, land, and excavation."],
        [("Do you serve Oak Hill, TN?","Yes. Oak Hill is part of our Davidson County service area for tree work, clearing, grading, and drainage."),
         ("Can you thin a wooded Oak Hill lot without damaging the rest?","Yes. Selective thinning and careful removal around mature trees is one of our specialties.")],
        [FORESTPATH,FOREST,LAND]),
    }
    # ---- Tier 2 city stubs held back for later launch ----
    _tier2_stubs_held = {
      "fairview-tn":(["Fairview sits on the western edge of Williamson County, where rural acreage meets growing residential lots. We do a lot of forestry mulching, lot clearing, and tree work out here &mdash; properties that need real machines and an operator who's comfortable on uneven ground.",
        "We're a short drive from Fairview and happy to make the trip. Whether you're clearing brush off a back acre, dropping a hazardous tree near the house, or grading a building pad, we'll come walk the property and give you an honest estimate."],
        [("Do you do forestry mulching in Fairview?","Yes. Mulching overgrown acreage in Fairview is one of our most common jobs out there &mdash; we leave the ground walkable and the soil better than we found it."),
         ("Can you clear a building lot in Fairview?","Yes. We handle full lot clearing, including stumps, brush, and grading, so your builder can start clean."),
         ("Is Fairview part of your regular service area?","Yes. Fairview is a regular stop for us across Williamson County.")],
        [FIELD,LAND,FOREST]),
      "lewisburg-tn":(["Lewisburg and the surrounding Marshall County area are part of our extended service area. We bring the same crew and the same fair pricing south &mdash; tree removal, land clearing, forestry mulching, site prep, and excavation on rural lots, farms, and small-town properties.",
        "We make the drive gladly. Lewisburg families and farm owners get the same straight-talk estimates and clean work we'd give a Franklin neighbor."],
        [("Do you serve Lewisburg, TN?","Yes. Lewisburg is part of our extended Marshall County service area for all five of our services."),
         ("Can you clear pasture land in Lewisburg?","Yes. Reclaiming overgrown pasture and prepping fields for replanting or fence work is common for us in Marshall County."),
         ("Is there a travel charge to Lewisburg?","No surprise travel fees. We quote the job honestly and the price you see is what you pay.")],
        [FIELD,LAND,EXCAV]),
      "chapel-hill-tn":(["Chapel Hill is a small Marshall County town with big land &mdash; pasture, farmland, and rural acreage that often needs serious clearing or careful tree work. We bring the right equipment for rural jobs: skid steers, mulchers, excavators, and the operator who knows how to use them.",
        "Chapel Hill customers get the same honest estimates and clean job sites we give every neighbor. One crew, one call, covering tree work, clearing, mulching, prep, and excavation."],
        [("Do you do land clearing in Chapel Hill?","Yes. Clearing rural acreage, reclaiming overgrown fields, and prepping land for replanting are all common Chapel Hill jobs."),
         ("Can you grade a driveway or pad in Chapel Hill?","Yes. Grading rural driveways and building pads is part of what we do across Marshall County.")],
        [LAND,FIELD,SITEPREP]),
      "college-grove-tn":(["College Grove is rolling Williamson County country &mdash; horse farms, hayfields, and wooded acreage. We do a lot of clearing, mulching, and tree work out here, and we know the value of leaving a property looking better than we found it.",
        "From a single hazardous tree to clearing an acre for a new pasture, we bring the right machine and a fair price. We're insured for working around horses, fences, and outbuildings, and we treat every College Grove property with the care it deserves."],
        [("Do you do forestry mulching in College Grove?","Yes. Mulching overgrown wood lines and reclaiming pasture is a regular job for us in College Grove."),
         ("Are you insured for working around livestock and outbuildings?","Yes. We're insured and careful around horses, fences, and structures on working farms."),
         ("Do you serve large College Grove acreage?","Yes. We handle multi-acre clearing, mulching, and site prep on College Grove farms and estates.")],
        [FIELD,FOREST,LAND]),
      "triune-tn":(["Triune sits where Williamson County meets Rutherford and Marshall counties &mdash; a crossroads of rural acreage, farmland, and growing residential lots. We cover Triune for tree work, clearing, mulching, site prep, and excavation, and we're close enough to get out there quickly.",
        "Whether you're working a small homestead or a multi-acre property, Triune customers get the same fair pricing and careful work we bring to every job."],
        [("Do you serve Triune, TN?","Yes. Triune is well inside our regular service area &mdash; we're out there for tree work, clearing, mulching, and excavation jobs regularly."),
         ("Can you handle drainage work in Triune?","Yes. Grading, French drains, and runoff routing on rural Triune lots are part of what we do.")],
        [LAND,FIELD,EXCAV]),
    }
    for slug,(paras,faqs,ids) in stubs.items():
        build_city(slug, paras, faqs, ids)

# ============ REVIEWS ============
def build_reviews():
    reviews = GBP_REVIEWS.get("reviews", [])
    # Reviews with comments first, then comment-less ones at the end.
    reviews_sorted = [r for r in reviews if r.get("comment")] + [r for r in reviews if not r.get("comment")]
    cards = "".join(google_review_card(r) for r in reviews_sorted)
    rating = _fmt_rating(GBP_RATING)
    body=f'''
<section class="hero hero--page" style="{hero_bg(TREE,1600)}">
  <div class="container center" style="display:flex;flex-direction:column;align-items:center">
    <p class="eyebrow" style="color:#F0C99A">Real reviews from real neighbors</p>
    <h1 style="margin:.2em 0">{rating} Stars on Google</h1>
    <p class="hero-sub" style="margin:0 auto">Based on {GBP_COUNT} verified Google reviews from across Middle Tennessee.</p>
    <div class="hero-cta" style="justify-content:center;gap:12px;flex-wrap:wrap">
      <a class="btn btn--primary" href="{GBP_WRITE_URL}" target="_blank" rel="noopener">Leave Us a Google Review</a>
      <a class="btn btn--ghost" href="{GBP_MAPS_URI}" target="_blank" rel="noopener">View on Google</a>
    </div>
  </div>
</section>
{trustbar()}
<section class="section">
  <div class="container">
    <div class="reviews-summary">
      {gbp_badge()}
      <p class="reviews-summary-note">Reviews shown below are pulled directly from our <a href="{GBP_MAPS_URI}" target="_blank" rel="noopener">Google Business Profile</a>.</p>
    </div>
    <div class="google-reviews-grid">{cards}</div>
  </div>
</section>
<section class="section bg-alt"><div class="container center" style="max-width:620px">
  <h2>Worked with us?</h2><p class="lead" style="margin:0 auto 22px">We'd be grateful if you'd share your experience on Google. It helps other Middle Tennessee families find us.</p>
  <a class="btn btn--primary" href="{GBP_WRITE_URL}" target="_blank" rel="noopener">Leave a Google Review</a></div></section>
{cta_banner()}
'''
    write_page("reviews.html", page(f"Reviews | Claiborne Services LLC — {rating} Stars on Google",
      f"Read {GBP_COUNT} verified Google reviews for Claiborne Services LLC — {rating} stars. Tree service, land clearing, and excavation customers across Middle Tennessee share their experience.",
      body, prefix="", head_extra=localbusiness_schema()))

# ============ GALLERY ============
def build_gallery():
    # ---- Real-only gallery: every photo here is from an actual Claiborne job site. ----
    # When the customer sends more real photos (tree, land, mulching, site prep), add them here.
    real_jobs=[
      ("local:assets/img/jobs/excav-stone-trench-bobcat.jpg","excavation","Sewer line trenching and PVC sewer pipe installation for new home construction in the Tors of Avalon, Franklin, TN."),
      ("local:assets/img/jobs/excav-driveway-cut.jpg","excavation","Waterline trenching and PEX install for a new home build in Columbia, TN using our Cat 265 Compact Track Loader with Trenching attachment."),
      ("local:assets/img/jobs/excav-utility-trench-tree.jpg","excavation","Waterline trenching and PEX install for a new home build in Columbia, TN using our Cat 305 CR Mini Excavator."),
      ("local:assets/img/jobs/excav-trench-horse-fence.jpg","excavation","Waterline trenching and PEX install for a new garden in LaVergne, TN using our Cat 265 Compact Track Loader with Trenching attachment."),
      ("local:assets/img/jobs/tree-bucket-storm-franklin.jpg","tree","Storm damaged limb removal using our Haulotte 55XA self-propelled articulating boom lift in Franklin, TN."),
      ("local:assets/img/jobs/tree-haulotte-drone-backyard.jpg","tree","Drone view of a backyard tree job in Franklin, TN &mdash; our Haulotte 55XA articulating boom lift giving us the reach to trim a row of overgrown pines to reclaim the yard."),
      ("local:assets/img/jobs/land-cat265-grapple-burn.jpg","land","Lot clearing in progress &mdash; our CAT 265 with grapple rake stacking brush for a controlled burn on a Spring Hill, TN property."),
      ("local:assets/img/jobs/land-cat265-rake-rootball.jpg","land","Our CAT 265 Compact Track Loader with grapple rake about to move a massive log in Franklin, TN."),
    ]
    items=""
    for src, cat, caption in real_jobs:
        u=img(src,1400)
        items+=f'''<figure class="real-job" data-cat="{cat}">
          <img src="{u}" alt="{caption}" loading="lazy" data-lightbox data-full="{u}">
          <figcaption>{caption}</figcaption>
        </figure>'''
    body=f'''
<section class="section" style="padding-top:48px;padding-bottom:24px">
  <div class="container center">
    <p class="eyebrow">Our Work</p>
    <h1 style="margin:.2em 0 .3em">Project Gallery</h1>
    <p class="lead" style="max-width:640px;margin:0 auto">Real photos from actual Claiborne Services job sites &mdash; no stock images. We're adding more as we finish jobs across Middle Tennessee.</p>
  </div>
</section>
{trustbar()}
<section class="section">
  <div class="container">
    <div class="real-jobs-grid">{items}</div>
    <p class="center" style="margin-top:36px;color:var(--muted)">Have a job you'd like quoted? <a href="contact.html">Tell us about it</a> or call <a href="tel:{PHONE_TEL}">{PHONE}</a>.</p>
  </div>
</section>
{cta_banner()}
<div class="lightbox"><button class="lightbox-close" aria-label="Close">&times;</button><img src="" alt=""></div>
'''
    write_page("gallery.html", page("Gallery | Claiborne Services LLC",
      "Real job-site photos from Claiborne Services across Middle Tennessee &mdash; tree work, land clearing, forestry mulching, site prep, and excavation.",
      body, prefix="", head_extra=localbusiness_schema()))

# ============ DISCOUNTS ============
def build_discounts():
    # ---- Expanded full-section discount details ----
    details=[
      {
        "id":"senior",
        "name":"Senior Citizen Discount",
        "pct":"10% off",
        "bg":"",
        "lede":"A straightforward thank-you to the folks who built the neighborhoods we work in every day. If you're 65 or older, you get 10% off your entire job &mdash; no project minimum, no fine print.",
        "who":[
          "Homeowner age 65 or older at the time of the estimate.",
          "Applies to the property owner &mdash; if a family member is paying on a senior's behalf, the discount still applies as long as the senior is the homeowner.",
          "Surviving spouses qualify regardless of age."
        ],
        "covers":[
          "Tree trimming, pruning, removal, and stump grinding.",
          "Land clearing, brush cutting, and forestry mulching.",
          "Excavation, grading, drainage, and driveway work.",
          "Storm cleanup and emergency tree work."
        ],
        "how":"Show a driver's license or any state-issued ID when we come out for the estimate. We'll note it on the quote and the discount carries through to the final invoice. You do not need to ask twice &mdash; once it's on the quote, it's locked in."
      },
      {
        "id":"first-responder",
        "name":"First Responder, Veteran &amp; Military Discount",
        "pct":"10% off",
        "bg":"bg-alt",
        "lede":"One combined program for the people who run toward trouble and the people who served. If you wear a uniform, wore a uniform, or work dispatch &mdash; you qualify. No tier system, no \"select branches only,\" no expiration on service.",
        "who":[
          "<strong>Police officers</strong> &mdash; municipal, county, state, federal, retired, or honorably separated.",
          "<strong>Firefighters</strong> &mdash; career, volunteer, or retired.",
          "<strong>EMS &amp; paramedics</strong> &mdash; ground, air, hospital-based, or private.",
          "<strong>911 dispatchers and telecommunicators</strong> &mdash; the voices on the other end of the worst day of someone's life.",
          "<strong>All branches of the U.S. military</strong> &mdash; Army, Navy, Air Force, Marines, Coast Guard, Space Force, National Guard, and Reserves &mdash; active duty, retired, or honorably discharged veterans.",
          "Spouses of active-duty service members deployed at the time of the estimate.",
          "Gold Star families."
        ],
        "covers":[
          "Every service we offer &mdash; tree work, land clearing, mulching, site prep, and excavation.",
          "Emergency calls and storm response.",
          "Stacks with the senior discount &mdash; if you're a 65+ veteran, you can pick whichever is larger (we won't double-stack to keep it sustainable, but you always get the better of the two)."
        ],
        "how":"Any one of the following at the estimate: an active or retired department ID, a VA ID card, a DD-214, a state driver's license with the veteran designation, or <a href=\"https://www.id.me\" target=\"_blank\" rel=\"noopener\">ID.me</a> verification. We don't keep copies &mdash; we just verify and move on."
      },
      {
        "id":"tribute",
        "name":"Claiborne Family Tribute Discount",
        "pct":"10&ndash;15% off",
        "bg":"",
        "lede":"This is the most personal program we run. It is named in memory of three people who shaped our family &mdash; and it exists for any household walking the same road we have walked.",
        "who":[
          "Households where someone is living with, or caring for someone with, <strong>Alzheimer's disease or another form of dementia</strong>.",
          "Households where someone has been diagnosed with <strong>lupus</strong> (SLE, cutaneous, drug-induced, or neonatal).",
          "Households where someone is on the <strong>autism spectrum</strong> &mdash; any level, any age, verbal or nonverbal.",
          "Primary caregivers count, even if the person they care for lives elsewhere."
        ],
        "covers":[
          "10% off standard jobs.",
          "Up to 15% off larger projects (full lot clearing, multi-day excavation, multi-tree removals) at our discretion &mdash; we'll tell you on the quote.",
          "Priority scheduling for hazardous tree work near a home where someone is medically vulnerable."
        ],
        "how":"<strong>Honor system. No paperwork, no medical documentation, no proof of anything.</strong> Just tell us when we come out for the estimate &mdash; you can say it quietly, you can say it in passing, you can put it in the comments on the contact form. We will quietly apply the discount and we will never ask a follow-up question. <a href=\"#tribute-story\">Read why this program exists \u2192</a>"
      },
      {
        "id":"currey-ingram",
        "name":"Currey Ingram Academy Discount",
        "pct":"10% off",
        "bg":"bg-alt",
        "lede":"For sixty-four years, the Brentwood campus that is now <a href=\"https://www.curreyingram.org\" target=\"_blank\" rel=\"noopener\">Currey Ingram Academy</a> was home to Shawn's father, James Claiborne. This discount is a thank-you to the community that was part of his life &mdash; and ours &mdash; for a quarter of a century.",
        "who":[
          "<strong>Current students</strong> and their parents/guardians.",
          "<strong>Former students (alumni)</strong> &mdash; any graduating class, any years attended.",
          "<strong>Parents and guardians of former students.</strong>",
          "<strong>Current and former faculty and staff</strong> &mdash; teachers, administrators, coaches, and support staff.",
          "Extended family of any of the above who refers us to a Currey Ingram household qualifies for the discount on their own job too."
        ],
        "covers":[
          "All tree, land clearing, and excavation services.",
          "Jobs at both the Currey Ingram-connected household and any second property (rental, in-law residence, family farm).",
          "Stacks with the senior discount the same way the first-responder discount does &mdash; you get whichever is larger."
        ],
        "how":"Just mention it at the estimate &mdash; tell us the connection (student, alum, parent, faculty) and roughly the years. We don't ask for transcripts or employee IDs. <a href=\"#currey-story\">Read why this discount exists \u2192</a>"
      },
    ]
    dd=""
    for d in details:
        who_li="".join(f"<li>{x}</li>" for x in d["who"])
        cov_li="".join(f"<li>{x}</li>" for x in d["covers"])
        bg=f' {d["bg"]}' if d["bg"] else ""
        dd+=f'''<section id="{d["id"]}" class="section{bg}"><div class="container">
          <div class="discount-detail">
            <div class="dd-head"><h2>{d["name"]}</h2><span class="dd-pct">{d["pct"]}</span></div>
            <p class="dd-lede">{d["lede"]}</p>
            <h4>Who qualifies</h4><ul>{who_li}</ul>
            <h4>What it covers</h4><ul>{cov_li}</ul>
            <h4>How to claim it</h4><p style="margin:.3em 0">{d["how"]}</p>
            <div class="dd-foot"><strong>Important:</strong> Discounts apply to labor and equipment time. They don't stack on top of each other &mdash; if you qualify for more than one, we apply whichever is the largest. Mention it at the estimate so it's reflected on your written quote.</div>
          </div>
        </div></section>'''
    body=f'''
<section class="hero hero--page" style="{hero_bg(CREW,1600)}">
  <div class="container"><p class="eyebrow" style="color:#F0C99A">Giving Back</p><h1>Discount Programs for Our Community</h1>
  <p class="hero-sub">We believe good land work should be accessible. These four programs are our way of standing with the people who serve, support, and shaped our community.</p></div>
</section>
{trustbar()}
<section class="section"><div class="container center" style="max-width:760px">
  <p class="eyebrow">Four Programs</p>
  <h2 style="margin-bottom:14px">Pick the one that fits &mdash; jump to it</h2>
  <p class="lead" style="margin:0 auto 20px">Each program below has its own story, who qualifies, what it covers, and how to claim it at the estimate.</p>
  <div class="flex-cta" style="justify-content:center;flex-wrap:wrap;gap:10px">
    <a class="btn btn--ghost" href="#senior">Senior &middot; 10%</a>
    <a class="btn btn--ghost" href="#first-responder">First Responder / Vet / Military &middot; 10%</a>
    <a class="btn btn--ghost" href="#tribute">Claiborne Family Tribute &middot; 10&ndash;15%</a>
    <a class="btn btn--ghost" href="#currey-ingram">Currey Ingram &middot; 10%</a>
  </div>
</div></section>
{dd}
<section id="tribute-story" class="section"><div class="container" style="max-width:820px">
  <p class="eyebrow">In Their Memory</p><h2>The Story Behind the Claiborne Family Tribute Discount</h2>
  <div class="tribute">
    <p><em>This program is named in memory of and in honor of three people who shaped our family:</em></p>
    <p class="person"><strong>Cynthia Claiborne</strong> &mdash; Shawn's mother, who passed in 2020 after a 25-year fight with Alzheimer's disease.</p>
    <p class="person"><strong>James Claiborne</strong> &mdash; Shawn's father, who passed away in 2024 from lupus.</p>
    <p class="person"><strong>Emilio Reyes</strong> &mdash; Shawn's nephew, who lives with nonverbal autism and reminds us every day why patience and respect matter.</p>
    <p style="margin-top:16px"><em>If your household is affected by Alzheimer's, lupus, or autism, just mention it when we come out to give you an estimate. There is no paperwork, no medical documentation, and no proof required. We will quietly apply 10&ndash;15% off the job. That is our family's small way of standing with yours.</em></p>
  </div>
</div></section>
<section id="currey-story" class="section bg-alt"><div class="container" style="max-width:820px">
  <p class="eyebrow">A Place That Shaped Us</p><h2>The Story Behind the Currey Ingram Discount</h2>
  <div class="tribute">
    <p>For sixty-four years, the Brentwood campus that is now <strong><a href="https://www.curreyingram.org" target="_blank" rel="noopener">Currey Ingram Academy</a></strong> was home to Shawn's father, <strong>James Claiborne</strong>.</p>
    <p class="person">James started working on the property in <strong>1960</strong> for its previous owner, Duncan McDonald. He moved onto the land in <strong>1965</strong> and never left &mdash; living there for the rest of his life. When <a href="https://www.curreyingram.org" target="_blank" rel="noopener">Currey Ingram Academy</a> purchased the farm in 1999, James stayed on, working there until his passing in 2024.</p>
    <p class="person">That property &mdash; its trees, its fields, its long driveways &mdash; was the backdrop of Shawn's childhood and the place his father called home for sixty years. The school's students, families, and staff were part of that story for a quarter of a century.</p>
    <p style="margin-top:16px"><em>As a thank-you to the Currey Ingram community that was part of our family's life, we offer <strong>10% off</strong> any job for current and former Currey Ingram students, parents, and faculty. Just mention it when we come out for your estimate &mdash; no paperwork required.</em></p>
  </div>
</div></section>
<section class="section bg-alt"><div class="container center" style="max-width:760px">
  <p class="eyebrow">Organizations We Stand With</p><h2>Learn More &amp; Get Support</h2>
  <p class="lead" style="margin:0 auto 28px">If you or your family are facing one of these conditions, these organizations offer real support.</p>
  <div class="grid grid-3">
    <a class="card" href="https://www.alz.org/tennessee" target="_blank" rel="noopener" style="text-decoration:none"><div class="card-body"><h3>Alzheimer's Association</h3><p>Tennessee Chapter</p><span class="card-link">Visit site &rarr;</span></div></a>
    <a class="card" href="https://www.lupus.org/midsouth" target="_blank" rel="noopener" style="text-decoration:none"><div class="card-body"><h3>Lupus Foundation of America</h3><p>Mid South Chapter</p><span class="card-link">Visit site &rarr;</span></div></a>
    <a class="card" href="https://www.autismtn.org" target="_blank" rel="noopener" style="text-decoration:none"><div class="card-body"><h3>Autism Tennessee</h3><p>Statewide support &amp; resources</p><span class="card-link">Visit site &rarr;</span></div></a>
  </div>
</div></section>
<section class="cta-banner"><div class="container"><h2>Mention Your Discount at the Estimate</h2>
  <p>Just let us know when we come out &mdash; we'll apply it to your quote. No hoops, no hassle.</p>
  <div class="flex-cta" style="justify-content:center"><a class="btn btn--outline" href="contact.html">Get a Free Quote</a><a class="btn btn--ghost" href="tel:{PHONE_TEL}" style="border-color:#fff">{icon('phone')}Call {PHONE}</a></div></div></section>
'''
    write_page("discounts.html", page("Discount Programs | Claiborne Services LLC",
      "Claiborne Services offers four discount programs &mdash; senior, a combined first responder/veteran/military discount, the Claiborne Family Tribute, and the Currey Ingram Academy discount for current and former students, parents, and faculty.",
      body, prefix="", head_extra=localbusiness_schema()))

# ============ TRUSTED PARTNERS ============
def build_partners():
    partners = [
        {"company":"Roman Concrete","contact":"Miguel Roman","phone":"(931) 334-5034","tel":"+19313345034","trade":"Concrete &amp; Flatwork","blurb":"Driveways, slabs, sidewalks, and footings. Miguel's crew does clean, square work and shows up when they say they will &mdash; the kind of guys we'd hire on our own property."},
        {"company":"Roll Out Dumpsters","contact":"Jason Whitman","phone":"(931) 246-5688","tel":"+19312465688","trade":"Dumpster Rental","website":"https://www.rolloutdumpsters.com/","website_label":"rolloutdumpsters.com","blurb":"Roll-off dumpsters for cleanouts, renovations, and big yard projects. Fair pricing, prompt drop-off and pickup, and a straightforward guy to deal with."},
        {"company":"JB Plumbing","contact":"Jonathan Benson","phone":"(731) 225-6246","tel":"+17312256246","trade":"Plumbing","blurb":"Residential and light commercial plumbing &mdash; repairs, water lines, fixtures, and trouble-shooting. Jonathan does honest work at honest prices and stands behind it."},
    ]
    cards = "".join([f'''
  <div class="card">
    <div class="card-body">
      <p class="eyebrow">{p["trade"]}</p>
      <h3 style="margin:6px 0 4px">{p["company"]}</h3>
      <p style="margin:0 0 12px;color:var(--ink-muted)">{p["contact"]}</p>
      <p>{p["blurb"]}</p>
      {(f'<p style="margin:10px 0 0"><a href="' + p["website"] + '" target="_blank" rel="noopener" class="card-link">' + p["website_label"] + ' &rarr;</a></p>') if p.get("website") else ''}
      <div class="flex-cta" style="margin-top:14px">
        <a class="btn btn--primary" href="tel:{p["tel"]}">{icon('phone')}Call {p["phone"]}</a>
        <a class="btn btn--outline" href="sms:{p["tel"]}">{icon('message')}Text</a>
      </div>
    </div>
  </div>''' for p in partners])
    body=f'''
<section class="hero hero--page" style="{hero_bg(CREW,1600)}">
  <div class="container"><p class="eyebrow" style="color:#F0C99A">Who We Recommend</p><h1>Trusted Partners</h1>
  <p class="hero-sub">When a job is outside what we do, we want you in good hands. These are local pros we know, trust, and refer our own customers to.</p></div>
</section>
{trustbar()}
<section class="section"><div class="container" style="max-width:820px;text-align:center">
  <p class="eyebrow">Why This Page Exists</p>
  <h2>Good Work Deserves Good People Around It</h2>
  <p class="lead">We get asked all the time, &ldquo;Do you know a good ___?&rdquo; These are the folks we'd call ourselves. We don't take a cut, and we don't get paid for these referrals &mdash; we just want our customers taken care of.</p>
</div></section>
<section class="section bg-alt"><div class="container"><div class="grid grid-3">{cards}</div></div></section>
<section class="section"><div class="container" style="max-width:760px;text-align:center">
  <p class="eyebrow">A Note on Recommendations</p>
  <h2>Honest Referrals Only</h2>
  <p>We only list people we've worked alongside or hired ourselves. If you have a great experience with one of them, let them know we sent you &mdash; and if anything ever falls short, tell us. We want to know.</p>
</div></section>
<section class="cta-banner"><div class="container"><h2>Need Something We Don't Do? Just Ask.</h2>
  <p>Call or text and we'll point you to the right person &mdash; even if it's not on this list yet.</p>
  <div class="flex-cta" style="justify-content:center"><a class="btn btn--outline" href="tel:{PHONE_TEL}">{icon('phone')}Call {PHONE}</a><a class="btn btn--ghost" href="sms:{PHONE_TEL}" style="border-color:#fff">{icon('message')}Text Us</a></div></div></section>
'''
    write_page("partners.html", page("Trusted Partners | Claiborne Services LLC",
      "Local contractors and tradespeople Claiborne Services recommends to customers across Middle Tennessee &mdash; concrete, dumpster rental, plumbing, and more.",
      body, prefix="", head_extra=localbusiness_schema()))

# ============ CONTACT ============
def build_contact():
    body=f'''
<section class="hero hero--page" style="{hero_bg(EXCAV,1600)}">
  <div class="container"><p class="eyebrow" style="color:#F0C99A">Let's Talk</p><h1>Get in Touch</h1>
  <p class="hero-sub">Call, text, email, or fill out the form. We'll get back to you fast with an honest estimate.</p></div>
</section>
{trustbar()}
<section class="section"><div class="container">
  <div class="flex-cta" style="justify-content:center;margin-bottom:36px">
    <a class="btn btn--forest" href="tel:{PHONE_TEL}">{icon('phone')}Call {PHONE}</a>
    <a class="btn btn--primary" href="sms:{PHONE_TEL}">{icon('message')}Text Us</a>
    <a class="btn btn--outline" href="mailto:{EMAIL}">{icon('mail')}Email</a>
  </div>
  <div class="feature" style="align-items:flex-start">
    <form class="quote-form" novalidate>
      <h2 style="margin-top:0">Request a Free Quote</h2>
      <div class="form-row">
        <div class="field"><label for="name">Name</label><input id="name" name="name" type="text" required></div>
        <div class="field"><label for="phone">Phone</label><input id="phone" name="phone" type="tel" required></div>
      </div>
      <div class="form-row">
        <div class="field"><label for="email">Email</label><input id="email" name="email" type="email"></div>
        <div class="field"><label for="address">Property address</label><input id="address" name="address" type="text"></div>
      </div>
      <div class="form-row">
        <div class="field"><label for="service">Service interest</label><select id="service" name="service"><option>Tree Services</option><option>Land Clearing</option><option>Forestry Mulching</option><option>Site Preparation</option><option>Excavation</option><option>Not sure / multiple</option></select></div>
        <div class="field"><label for="contactpref">Preferred contact</label><select id="contactpref" name="contactpref"><option>Call</option><option>Text</option><option>Email</option></select></div>
      </div>
      <div class="field"><label for="desc">Tell us about the job</label><textarea id="desc" name="desc"></textarea></div>
      <div class="field"><label for="photos">Add photos (optional)</label><input id="photos" name="photos" type="file" multiple accept="image/*"></div>
      <button class="btn btn--primary" type="submit" style="width:100%;justify-content:center">Send My Request</button>
      <p class="form-success" style="display:none;color:var(--forest);font-weight:700;text-align:center;margin:0">Thanks! We've got your request and will reach out shortly.</p>
    </form>
    <div>
      <h3>Hours</h3>
      <p style="display:flex;gap:10px;align-items:center;color:var(--muted)">{icon('clock')} Monday&ndash;Friday, 7:00am&ndash;6:00pm &middot; Closed Saturday &amp; Sunday</p>
      <h3 style="margin-top:24px">Reach Us</h3>
      <ul style="list-style:none;padding:0;margin:0;display:grid;gap:10px">
        <li><a href="tel:{PHONE_TEL}" style="display:flex;gap:10px;align-items:center">{icon('phone')}{PHONE}</a></li>
        <li><a href="sms:{PHONE_TEL}" style="display:flex;gap:10px;align-items:center">{icon('message')}Text us</a></li>
        <li><a href="mailto:{EMAIL}" style="display:flex;gap:10px;align-items:center">{icon('mail')}{EMAIL}</a></li>
        <li style="display:flex;gap:10px;align-items:center;color:var(--muted)">{icon('pin')}Franklin, TN &amp; Middle Tennessee</li>
      </ul>
      <p style="margin-top:18px;color:var(--muted)"><strong>Se habla espa&ntilde;ol.</strong> Call or text and we'll be glad to help in Spanish.</p>
      <iframe class="map-embed" title="Claiborne Services LLC on Google Maps" loading="lazy" src="https://maps.google.com/maps?cid={GBP_CID}&z=11&output=embed" style="min-height:280px;margin-top:18px"></iframe>
      <p style="margin-top:10px;font-size:14px"><a href="{GBP_MAPS_URI}" target="_blank" rel="noopener">View on Google Maps &rarr;</a></p>
    </div>
  </div>
</div></section>
'''
    write_page("contact.html", page("Contact | Claiborne Services LLC — Get a Free Quote",
      "Contact Claiborne Services LLC for a free quote on tree service, land clearing, forestry mulching, site prep, or excavation in Middle Tennessee. Call, text, or email.",
      body, prefix="", head_extra=localbusiness_schema()))

# ============ RUNNER ============
# ============ NEW PAGE BUILDERS (FAQ, Pricing, Financing, Equipment, Insurance, Projects, Blog, Spanish, 404) ============

def build_faq():
    groups = [
      ("Pricing & estimates", [
        ("How much does tree removal cost?",
         "Most residential tree removals in Middle Tennessee fall between $400 and $2,500. Price depends on tree height, trunk diameter, lean, dead vs. live wood, access for equipment, and whether the stump is included. We provide free written estimates so there are no surprises."),
        ("Are estimates really free?",
         "Yes. We come look at the work, ask what you want done, and give you a written number. No fee, no obligation, no pressure."),
        ("Do you charge for travel?",
         "Not within our core service area (Williamson, Maury, Davidson counties and immediate neighbors). Long-distance jobs may include a mobilization line item, and we'll show it on the estimate before you ever agree."),
        ("What forms of payment do you accept?",
         "Cash, check, all major cards, and ACH. We can also set up payment plans through QuickBooks financing for qualified customers."),
        ("Do you require a deposit?",
         "For small jobs, no. For larger land clearing or excavation projects, we typically take a deposit to lock the schedule and cover initial mobilization. We'll explain it on the estimate."),
      ]),
      ("Insurance & licensing", [
        ("Are you insured?",
         "Yes. Claiborne Services LLC is insured. We can send a copy of our certificate of insurance directly to your homeowner's insurance or HOA before we start."),
        ("Are you licensed in Tennessee?",
         "We operate as a registered Tennessee LLC. Tree work and land clearing in Tennessee do not require a contractor's license under the standard residential thresholds, but we hold all required local registrations and carry insurance."),
        ("What happens if something gets damaged?",
         "In the rare event property is damaged, we own it. Take a photo, tell us, and we'll make it right — repair, replace, or pay for it. That's the whole point of being insured."),
      ]),
      ("Equipment & access", [
        ("Will your equipment tear up my yard?",
         "Not if we can help it. We use tracked skid steers with turf-friendly tracks, ground protection mats when conditions are wet, and we plan the path before we drive in. If we expect ruts, we tell you first."),
        ("Can you reach trees in tight backyards?",
         "Usually, yes. Between our articulating boom lift, climbers, and compact skid steers with grapples, we handle most fence-line and backyard removals without needing a crane."),
        ("Do you handle large or hazardous trees?",
         "Yes. Storm-damaged, leaning, hollow, or oversized trees over structures are our wheelhouse. When the situation calls for a crane, we coordinate one."),
      ]),
      ("Timing & scheduling", [
        ("How fast can you come out?",
         "For estimates, usually within a few business days. For storm emergencies, we triage by safety risk — trees on houses and blocking driveways jump the line."),
        ("How long is the wait once I approve the work?",
         "Routine tree work is typically 1–2 weeks out. Larger land clearing and excavation projects depend on weather and the current schedule; we give you a real window before you sign anything."),
        ("Do you work in the rain?",
         "Light rain, often yes. Lightning, high winds, or saturated ground that would damage your yard, no. Safety and your lawn come first."),
      ]),
      ("Specific services", [
        ("What's the difference between tree trimming and tree pruning?",
         "In practice we use them interchangeably for residential work — both mean selective cutting to improve health, shape, or clearance. Pruning emphasizes long-term tree health; trimming often emphasizes appearance or clearance from structures."),
        ("Do you grind the stump after removing a tree?",
         "Stump grinding is a separate line item. Some customers want the stump gone; others want to leave it and plant around it. We'll quote both ways."),
        ("What is forestry mulching?",
         "A tracked machine with a rotating drum chews brush, saplings, and small trees into mulch on the spot. Faster and cleaner than dozing, and leaves a layer of natural ground cover."),
        ("Do you haul off the debris?",
         "By default, yes. If you want to keep the firewood or wood chips, just tell us — we'll stack what you want and haul the rest."),
      ]),
      ("Other", [
        ("Do you offer discounts?",
         "Yes — for first responders, military, teachers, seniors, and repeat customers. See the Discounts page for current offers."),
        ("Do you take on commercial or municipal work?",
         "Yes. We work for builders, property managers, HOAs, and commercial clients. We can provide a W-9, COI, and standard subcontractor paperwork."),
        ("Do you work outside Williamson County?",
         "Yes. We regularly work across Maury, Davidson, Marshall, Hickman, and Rutherford counties, and we'll travel further for larger projects."),
        ("Se habla español?",
         "Sí. Hablamos español. Llame o envíe un mensaje de texto y con gusto le ayudaremos."),
      ]),
    ]
    # Flatten for schema
    all_faqs = [(q,a) for _,items in groups for q,a in items]
    blocks = ""
    for title, items in groups:
        blocks += f'<section class="sec"><div class="container"><h2>{title}</h2>{faq_block(items)}</div></section>'
    body = f'''
<section class="hero hero--inner" style="{hero_bg(FORESTPATH,1800,overlay=True)}">
  <div class="container hero-content">
    <p class="eyebrow">Frequently asked questions</p>
    <h1>Straight answers about tree work, land clearing &amp; excavation</h1>
    <p class="hero-sub">Pricing, insurance, equipment, timing — everything customers ask before they sign. If we missed one, call or text and we'll add it.</p>
    <div class="hero-ctas"><a class="btn btn--primary" href="contact.html">Get a Free Estimate</a><a class="btn btn--ghost" href="tel:{PHONE_TEL}">Call {PHONE}</a></div>
  </div>
</section>
{trustbar()}
{blocks}
<section class="sec"><div class="container">{finance_callout()}</div></section>
{cta_banner()}
'''
    head_extra = faq_schema(all_faqs) + breadcrumb_schema([("Home","index.html"),("FAQs","faq.html")])
    write_page("faq.html", page(
        "FAQs | Claiborne Services LLC",
        "Answers to common questions about tree removal cost, insurance, equipment, scheduling, stump grinding, and land clearing in Middle Tennessee.",
        body, head_extra=head_extra, page_path="faq.html"))


def build_pricing():
    rows = [
      ("Tree trimming / pruning","$750 – $1,250","Most residential trims. Crown raise, deadwood, clearance from house/wires."),
      ("Tree removal (small, &lt;30 ft)","$750 – $1,250","Yard trees, open access, no structures close."),
      ("Tree removal (medium, 30–60 ft)","$950 – $1,800","Most front-yard and backyard hardwoods."),
      ("Tree removal (large, 60 ft+)","$1,500 – $3,500+","Mature oaks, hickories, poplars. Crane sometimes needed."),
      ("Storm-damaged / hazard tree","$1,250 – $4,000+","Leaning, hung up, partially failed, or on structure. Priced by risk."),
      ("Stump grinding (per stump)","$300 – $600+","Depends on diameter and root flare. Multiple stumps get bundled pricing."),
      ("Lot clearing &mdash; light brush (per acre)","$1,500 – $3,000","Light brush, scattered saplings. Open, accessible acreage."),
      ("Lot clearing &mdash; medium (per acre)","$3,000 – $6,000","Brush plus small trees. Some grubbing and haul-off."),
      ("Lot clearing &mdash; heavy (per acre)","$6,000 – $12,000+","Mature trees with stump grubbing. Dense timber priced separately."),
      ("Forestry mulching &mdash; light underbrush (per acre)","$1,750 – $2,500","Light underbrush. Tracked mulcher grinds in place."),
      ("Forestry mulching &mdash; medium density (per acre)","$2,500 – $4,500","Brush plus saplings. Mulch left as ground cover."),
      ("Forestry mulching &mdash; heavy density (per acre)","$4,500 – $8,000+","Heavier growth with larger trees. Slower, denser grind."),
      ("Excavation / grading (per day)","$1,800 – $3,500","Skid steer and/or mini-ex with operator. Materials extra."),
      ("Trenching (per linear foot)","$15 – $30","Utilities, water line, drainage runs. Depth and soil drive cost."),
      ("Driveway prep &amp; gravel","$2,500 – $8,000+","Cut, base, compact, gravel. Length and base depth drive cost."),
      ("Drainage / French drain","$1,500 – $6,000","Per run. Depth, length, and outlet location set the price."),
      ("Building pad &mdash; rough grading (per area)","$1,500 – $5,000","Rough grading and leveling for a defined area."),
      ("Builder pad / site prep (residential)","$2,500 – $8,000+","Clear, grub, rough grade, erosion control. Typical residential pad."),
      ("Builder pad / site prep (large or complex)","$8,000 – $15,000+","Larger pads, heavy fill, complex drainage, or steep grade."),
    ]
    rows_html = "".join(f'<tr><th scope="row">{n}</th><td><strong>{p}</strong></td><td>{d}</td></tr>' for n,p,d in rows)
    factors = [
      ("Access","How close can a truck and skid steer get? Fence lines, slopes, septic fields, narrow gates all add time."),
      ("Size &amp; species","A 50-foot pine and a 50-foot oak don't price the same. Hardwood, lean, and dead wood change the work."),
      ("What's nearby","Trees over houses, decks, fences, sheds, or vehicles take more rigging and time than open-yard work."),
      ("Debris &amp; cleanup","Hauling everything off costs more than chipping in place. We quote both ways if you want."),
      ("Stump &amp; grinding","Removing the tree and grinding the stump are two jobs. Sometimes you want both, sometimes just the tree."),
      ("Ground conditions","Saturated ground can mean mats, smaller equipment, or a reschedule to protect your yard."),
    ]
    factors_html = "".join(f'<div class="feature"><h3>{n}</h3><p>{d}</p></div>' for n,d in factors)
    body = f'''
<section class="hero hero--inner" style="{hero_bg(TREE,1800,overlay=True)}">
  <div class="container hero-content">
    <p class="eyebrow">Pricing guidance</p>
    <h1>What tree work, land clearing, and excavation usually cost in Middle Tennessee</h1>
    <p class="hero-sub">These are honest ranges from real jobs in Franklin, Brentwood, Spring Hill, Columbia, Nashville, and the surrounding area. Every property is different — the only real number is the one on your written estimate.</p>
    <div class="hero-ctas"><a class="btn btn--primary" href="contact.html">Get a Free Estimate</a><a class="btn btn--ghost" href="tel:{PHONE_TEL}">Call {PHONE}</a></div>
  </div>
</section>
{trustbar()}
<section class="sec"><div class="container">
  <h2>Typical price ranges</h2>
  <p class="lede">Ranges below are starting points for residential work in our core service area. We give you a firm written number after looking at the property.</p>
  <div class="table-wrap"><table class="pricing-table"><thead><tr><th>Service</th><th>Typical range</th><th>What drives the price</th></tr></thead><tbody>{rows_html}</tbody></table></div>
</div></section>
<section class="sec sec--alt"><div class="container">
  <h2>What actually moves the price</h2>
  <div class="features-grid">{factors_html}</div>
</div></section>
<section class="sec"><div class="container">
  <h2>How we keep estimates honest</h2>
  <ul class="checklist">
    <li>We come look. No phone-call quotes for jobs that need eyes on them.</li>
    <li>The number is written down — service, scope, debris handling, and total.</li>
    <li>If we find something unexpected, we stop and talk before the meter runs.</li>
    <li>If the job comes in faster than expected, the estimate doesn't change on you — that's not your problem.</li>
  </ul>
  {finance_callout()}
</div></section>
{cta_banner()}
'''
    head_extra = breadcrumb_schema([("Home","index.html"),("Pricing","pricing.html")])
    write_page("pricing.html", page(
        "Pricing Guide | Tree Work, Land Clearing &amp; Excavation Costs",
        "Typical price ranges for tree removal, stump grinding, land clearing, forestry mulching, and excavation work in Franklin, Brentwood, Spring Hill, and Nashville.",
        body, head_extra=head_extra, page_path="pricing.html"))


def build_financing():
    faqs = [
      ("How does QuickBooks financing work?",
       "After we send your estimate, we can include a financing option from QuickBooks. You apply online in a few minutes. If approved, you choose your monthly payment plan, and we get the job on the schedule."),
      ("Will applying hurt my credit?",
       "Pre-qualification typically uses a soft credit check that does not affect your score. A hard pull only happens if you accept the loan offer. Final terms are set by the lender, not by us."),
      ("What's the minimum or maximum amount?",
       "Plans typically work for jobs from about a thousand dollars up through larger land clearing and excavation projects. We can quote with and without financing so you can compare."),
      ("Can I pay it off early?",
       "Most QuickBooks financing plans allow early payoff without penalty. Check the lender's terms before you sign."),
      ("Do you offer in-house payment plans?",
       "For long-time customers and larger projects we sometimes work out a milestone payment schedule directly. Ask and we'll see what fits."),
      ("What if I'm not approved?",
       "We still want to do the work. We accept cards, ACH, and checks, and we can usually structure milestone payments on larger projects."),
    ]
    body = f'''
<section class="hero hero--inner" style="{hero_bg(LAND,1800,overlay=True)}">
  <div class="container hero-content">
    <p class="eyebrow">Financing</p>
    <h1>Pay over time. Get the work done now.</h1>
    <p class="hero-sub">Financing available through QuickBooks. Qualified customers may be able to pay over time with monthly payment options, subject to approval.</p>
    <div class="hero-ctas"><a class="btn btn--primary" href="contact.html">Request an Estimate</a><a class="btn btn--ghost" href="tel:{PHONE_TEL}">Call {PHONE}</a></div>
  </div>
</section>
{trustbar()}
<section class="sec"><div class="container">
  <h2>How it works</h2>
  <div class="steps">
    <div class="step"><span class="step-num">1</span><h3>Free estimate</h3><p>We come out, walk the job, and write you a real number.</p></div>
    <div class="step"><span class="step-num">2</span><h3>Apply online</h3><p>If you'd like to pay over time, we'll include a QuickBooks financing option with your estimate.</p></div>
    <div class="step"><span class="step-num">3</span><h3>Pick your plan</h3><p>Choose the monthly payment that fits your budget, subject to lender approval.</p></div>
    <div class="step"><span class="step-num">4</span><h3>We get to work</h3><p>Once it's set, we put your job on the schedule.</p></div>
  </div>
</div></section>
<section class="sec sec--alt"><div class="container">
  <h2>Who this is good for</h2>
  <ul class="checklist">
    <li>Storm cleanup that can't wait.</li>
    <li>Large land clearing or excavation projects.</li>
    <li>Builder pads, driveways, drainage solves that protect your home.</li>
    <li>Bundling multiple trees and stumps into one job instead of one at a time.</li>
  </ul>
  {finance_callout()}
</div></section>
<section class="sec"><div class="container"><h2>Financing FAQ</h2>{faq_block(faqs)}</div></section>
{cta_banner()}
'''
    head_extra = faq_schema(faqs) + breadcrumb_schema([("Home","index.html"),("Financing","financing.html")])
    write_page("financing.html", page(
        "Financing | Pay Over Time for Tree Work &amp; Land Clearing",
        "Financing available through QuickBooks. Qualified customers may be able to pay over time with monthly payment options, subject to approval.",
        body, head_extra=head_extra, page_path="financing.html"))


def build_equipment():
    items = [
      ("Articulating boom lift", "local:assets/img/jobs/equip-haulotte-55xa-boomlift.jpg", "Our Haulotte 55XA self-propelled articulating boom lift provides access for tree trimming, tree removals, and more."),
      ("Tracked skid steer", "local:assets/img/jobs/equip-skidsteer-cat265-grapple.jpg", "Our CAT 265 Compact Track Loader with numerous attachments moves logs and brush, clears lots, loads debris, grades yards, and more."),
      ("Stump grinder", "local:assets/img/jobs/equip-stumpgrinder-cat265-fae.jpg", "Our CAT 265 Compact Track Loader with FAE Stump Grinder attachment handles small up to oversized hardwoods with ease."),
      ("Mini skid steer", "local:assets/img/jobs/equip-miniskid-kubota-grapple.jpg", "Our Kubota SCL 1000 with Branch Manager rotating grapple fits through gates and tight backyard access where full-size machines can't go. Great for moving brush and backyard hauling without tearing up the lawn."),
      ("Mini excavator", "local:assets/img/jobs/equip-miniexcavator-cat305.jpg", "Our CAT 305 CR Mini Excavator handles drainage, footers, stump excavation in tight spots, and fine grading. Smaller footprint means it works in places a full-size machine can't."),
      ("Forestry mulcher", "local:assets/img/jobs/equip-mulcher-cat265-hm316.jpg", "Our CAT 265 Compact Track Loader with CAT HM316 Mulching head chews brush, saplings, and small trees into mulch right on the ground. Fast, clean, and easy on the soil compared to dozing."),
    ]
    grid = "".join(f'''<article class="eq-card"><div class="eq-img"><img src="{img(pid,1100)}" alt="{n}" loading="lazy"></div><div class="eq-body"><h3>{n}</h3><p>{d}</p></div></article>''' for n,pid,d in items)
    body = f'''
<section class="hero hero--inner" style="{hero_bg(DOZER,1800,overlay=True)}">
  <div class="container hero-content">
    <p class="eyebrow">Equipment</p>
    <h1>The right machine for the job — and an operator who knows it</h1>
    <div class="hero-ctas"><a class="btn btn--primary" href="contact.html">Get a Free Estimate</a><a class="btn btn--ghost" href="tel:{PHONE_TEL}">Call {PHONE}</a></div>
  </div>
</section>
{trustbar()}
<section class="sec"><div class="container">
  <h2>Our equipment</h2>
  <div class="eq-grid">{grid}</div>
</div></section>
<section class="sec sec--alt"><div class="container">
  {finance_callout()}
</div></section>
{cta_banner()}
'''
    head_extra = breadcrumb_schema([("Home","index.html"),("Equipment","equipment.html")])
    write_page("equipment.html", page(
        "Equipment | Articulating Boom Lift, Skid Steers, Stump Grinder &amp; Mulcher",
        "Our fleet for tree service, land clearing, and excavation in Middle Tennessee — articulating boom lift, tracked skid steer, mini skid steer, stump grinder, mini excavator, forestry mulcher, and dump trailer.",
        body, head_extra=head_extra, page_path="equipment.html"))


def build_insurance():
    faqs = [
      ("Are you insured?",
       "Yes. Claiborne Services LLC carries insurance. We can send a copy of our certificate of insurance directly to your homeowner's insurance company, HOA, or property manager before we start work."),
      ("Can I see your COI before the job?",
       "Yes. Just ask. We send it directly to you or to whoever needs it — usually within a business day."),
      ("Are you a registered Tennessee business?",
       "Yes. Claiborne Services LLC is a registered Tennessee LLC operating out of Franklin."),
      ("Why does this matter for a homeowner?",
       "If an uninsured crew damages your house, your fence, your neighbor's car, or themselves — it can become your problem. Hiring someone who carries real insurance keeps you out of it."),
      ("What if you damage something on my property?",
       "Take a photo and tell us. We own it. We'll repair, replace, or pay for it. That's why we carry insurance."),
    ]
    body = f'''
<section class="hero hero--inner" style="{hero_bg(FOGFOREST,1800,overlay=True)}">
  <div class="container hero-content">
    <p class="eyebrow">Licensed &amp; insured</p>
    <h1>Real insurance. Real paperwork. Real accountability.</h1>
    <p class="hero-sub">Most tree-service horror stories start with someone hiring the cheapest truck in the neighborhood. We carry insurance, we send the COI before the job, and if something goes wrong, we own it.</p>
    <div class="hero-ctas"><a class="btn btn--primary" href="contact.html">Request COI</a><a class="btn btn--ghost" href="tel:{PHONE_TEL}">Call {PHONE}</a></div>
  </div>
</section>
{trustbar()}
<section class="sec"><div class="container">
  <h2>What we carry</h2>
  <ul class="checklist">
    <li>Claiborne Services LLC — registered Tennessee LLC.</li>
    <li>Insured for tree service, land clearing, and excavation work.</li>
    <li>Certificate of insurance available on request — we'll send it to you or your insurance company directly.</li>
  </ul>
</div></section>
<section class="sec sec--alt"><div class="container">
  <h2>Why this matters</h2>
  <p>Tree work is heavy, high, and unpredictable. The cost of doing it right — insurance, equipment, training, real crews — is the reason a written quote from us is sometimes a little higher than the truck that showed up unannounced. It's also the reason your property, your neighbors, and your homeowner's policy stay clean if something goes sideways.</p>
  {finance_callout()}
</div></section>
<section class="sec"><div class="container"><h2>Insurance FAQ</h2>{faq_block(faqs)}</div></section>
{cta_banner()}
'''
    head_extra = faq_schema(faqs) + breadcrumb_schema([("Home","index.html"),("Licensed &amp; Insured","insurance.html")])
    write_page("insurance.html", page(
        "Licensed &amp; Insured | Claiborne Services LLC",
        "Claiborne Services LLC is a registered Tennessee LLC and is insured for tree work, land clearing, and excavation. Certificate of insurance available on request.",
        body, head_extra=head_extra, page_path="insurance.html"))


# ============ PROJECTS ============
PROJECTS = [
  ("storm-damaged-oak-franklin","Storm-damaged oak removal in Franklin",
   "After a spring storm dropped a sixty-foot oak across a fence line in West Franklin, the homeowner needed it gone before it pulled the rest of the tree over the garage.",
   "Franklin, TN · Williamson County","1 day",
   ["Bucket truck","Climber + rigging","Tracked skid steer with grapple","Chipper","Dump trailer"],
   TREE,
   [("The situation","A mature oak split halfway up the trunk during a thunderstorm. Half the canopy was already on the fence; the rest was hanging over the garage and the neighbor's pool. The homeowner needed it gone fast, without any of it landing where it shouldn't."),
    ("What we did","Set up rigging from the standing half of the trunk. Took the canopy down in controlled sections directly into the yard. Bucketed the upper trunk in pieces small enough to drop without bouncing. Ground the stump flush so they could re-sod the area."),
    ("Outcome","Tree was down, chipped, and the yard was raked clean before the day was over. Insurance company had the paperwork the next morning. Fence repair came in under what the homeowner had budgeted for the whole job.")]),
  ("brentwood-estate-clearing","Brentwood estate clearing &amp; selective thinning",
   "Two acres of mature woodland behind a Brentwood home needed selective clearing to open up the back of the property without losing the trees that gave it character.",
   "Brentwood, TN · Williamson County","3 days",
   ["Forestry mulcher","Tracked skid steer","Climber + chainsaw","Mini excavator"],
   FOREST,
   [("The situation","Decades of growth had filled the back two acres with privet, honeysuckle, and a tangle of small hardwoods crowding out the mature oaks and hickories. The owners wanted to walk through the woods without a machete and see the back property line for the first time in years."),
    ("What we did","Walked the property with the owners and tagged the trees worth keeping. Mulched the rest with the forestry head — privet, sweetgum, small junk hardwoods, and brush — and left the mulch as natural ground cover. Cleaned up a few hangers and limbed up the keeper trees so the canopy felt taller and lighter."),
    ("Outcome","Two acres of usable woods. The owners walked the back line for the first time in twenty years. We came back the following year to keep growth in check.")]),
  ("spring-hill-builder-pad","Spring Hill builder pad &amp; site prep",
   "A custom builder needed a lot cleared, rough-graded, and ready for the foundation crew on a tight schedule.",
   "Spring Hill, TN · Maury County","5 days",
   ["Forestry mulcher","Mini excavator","Tracked skid steer","Dump trailer","Erosion control"],
   SITEPREP,
   [("The situation","A wooded half-acre lot with a steady slope and a small wet-weather drain crossing one corner. The builder had a footprint, a foundation appointment three weeks out, and erosion control requirements from the county."),
    ("What we did","Cleared and grubbed the footprint plus a working area around it. Established a rough pad with the right fall away from the house. Cut a swale to keep stormwater away from the foundation, set silt fence on the down-slope side, and seeded the disturbed perimeter to hold soil through the build."),
    ("Outcome","Foundation crew showed up to a clean, dry pad with their access road already cut. The county inspector signed off on erosion control on the first walk-through.")]),
  ("columbia-pasture-reclaim","Columbia farm pasture reclaim",
   "A working farm in Maury County needed about ten acres of overgrown pasture turned back into useable grazing.",
   "Columbia, TN · Maury County","4 days",
   ["Forestry mulcher","Tracked skid steer with grapple","Chainsaws","Brush hog"],
   FIELD,
   [("The situation","The back ten acres had been let go for over a decade. Cedar, sweetgum, locust, and blackberry had taken over what used to be open pasture. The owner wanted to bring cattle back on it without years of mowing."),
    ("What we did","Mulched everything up to about eight inches in trunk diameter. Took the bigger cedars and locusts down separately. Stacked the keeper logs where the owner could split firewood. Came back and brush-hogged once the mulch settled."),
    ("Outcome","Ten acres of pasture back in service. Owner reseeded in the fall and was grazing the field by the following spring.")]),
  ("belle-meade-selective-thinning","Belle Meade selective thinning &amp; view restoration",
   "A historic Belle Meade property had lost its long view to the next ridge under twenty years of unmanaged growth. The owners wanted the view back without clear-cutting.",
   "Nashville, TN · Davidson County","2 days",
   ["Climber + rigging","Bucket truck","Tracked skid steer","Chipper"],
   FORESTPATH,
   [("The situation","A row of self-seeded hackberries, mulberries, and a few volunteer pines had filled in along the back property line. The view they bought the house for was completely gone. They didn't want a clear-cut — they wanted thoughtful editing."),
    ("What we did","Walked the line with the owners and ribboned every tree slated to come down. Removed the junk volunteers, limbed up the keepers from below so the canopy felt taller, and selectively thinned the ridge line to frame the view without exposing the property line."),
    ("Outcome","The view came back. The property line still has a tree line. From the back porch, you can't tell anything was removed.")]),
  ("nashville-drainage-solve","Nashville drainage solve &amp; french drain",
   "A Nashville homeowner had a recurring wet spot in the side yard that was killing trees and creeping toward the foundation.",
   "Nashville, TN · Davidson County","2 days",
   ["Mini excavator","Tracked skid steer","Drainage gravel + pipe","Sod"],
   EXCAV,
   [("The situation","Every storm dumped water from two neighbors' downspouts into one corner of the side yard. The grade ran the wrong way, two mature dogwoods were declining, and the water was starting to migrate toward the basement wall."),
    ("What we did","Cut a french drain through the wet zone with a positive outlet to daylight near the back of the property. Re-graded the side yard so surface water flowed into the drain instead of toward the house. Replaced the sod and the homeowner replanted the corner."),
    ("Outcome","Side yard stayed dry through the next wet spring. Foundation stayed dry. Homeowner replanted the corner and stopped losing trees.")]),
]

def build_projects():
    cards = ""
    for slug,title,summary,loc,duration,equip,hero_id,sections in PROJECTS:
        cards += f'''
<article class="project-card">
  <a class="project-card-img" href="projects/{slug}.html"><img src="{img(hero_id,1100)}" alt="{title}" loading="lazy"></a>
  <div class="project-card-body">
    <p class="eyebrow">{loc} · {duration}</p>
    <h3><a href="projects/{slug}.html">{title}</a></h3>
    <p>{summary}</p>
    <a class="more" href="projects/{slug}.html">Read the story →</a>
  </div>
</article>'''
    body = f'''
<section class="hero hero--inner" style="{hero_bg(FIELD,1800,overlay=True)}">
  <div class="container hero-content">
    <p class="eyebrow">Recent projects</p>
    <h1>Real work, on real properties, around Middle Tennessee</h1>
    <p class="hero-sub">Storm cleanup, pasture reclaim, builder pads, drainage solves, selective thinning. The stories below are the kind of work we run almost every week.</p>
    <div class="hero-ctas"><a class="btn btn--primary" href="contact.html">Get a Free Estimate</a><a class="btn btn--ghost" href="gallery.html">More Photos</a></div>
  </div>
</section>
{trustbar()}
<section class="sec"><div class="container">
  <div class="projects-grid">{cards}</div>
</div></section>
{cta_banner()}
'''
    head_extra = breadcrumb_schema([("Home","index.html"),("Projects","projects.html")])
    write_page("projects.html", page(
        "Projects | Recent Tree, Land Clearing &amp; Excavation Work",
        "Recent projects from Claiborne Services LLC — storm-damaged oak removals, estate clearing, builder pad prep, pasture reclaim, selective thinning, and drainage solves across Middle Tennessee.",
        body, head_extra=head_extra, page_path="projects.html"))

    # Individual project detail pages
    os.makedirs("projects", exist_ok=True)
    for slug,title,summary,loc,duration,equip,hero_id,sections in PROJECTS:
        eq_html = "".join(f'<li>{e}</li>' for e in equip)
        sec_html = "".join(f'<section class="prose"><h2>{h}</h2><p>{p}</p></section>' for h,p in sections)
        _hero_url = img(hero_id,1800)
        if isinstance(hero_id,str) and hero_id.startswith('local:'):
            _hero_url = "../" + _hero_url
        pbody = f'''
<section class="hero hero--inner" style="background-image:linear-gradient(rgba(20,30,20,.62),rgba(20,30,20,.62)),url('{_hero_url}')">
  <div class="container hero-content">
    <p class="eyebrow"><a href="../projects.html" style="color:#fff;text-decoration:underline">← All projects</a></p>
    <h1>{title}</h1>
    <p class="hero-sub">{summary}</p>
    <div class="hero-ctas"><a class="btn btn--primary" href="../contact.html">Get a Free Estimate</a><a class="btn btn--ghost" href="tel:{PHONE_TEL}">Call {PHONE}</a></div>
  </div>
</section>
<section class="sec"><div class="container">
  <div class="project-meta">
    <div><strong>Location</strong><br>{loc}</div>
    <div><strong>Duration</strong><br>{duration}</div>
    <div><strong>Equipment used</strong><ul class="project-meta-list">{eq_html}</ul></div>
  </div>
  <div class="project-prose">{sec_html}</div>
  {finance_callout()}
</div></section>
{cta_banner("../")}
'''
        head_extra = breadcrumb_schema([("Home","index.html"),("Projects","projects.html"),(title.replace('&amp;','&'),f"projects/{slug}.html")])
        write_page(f"projects/{slug}.html", page(
            f"{title.replace('&amp;','&')} | Claiborne Services LLC",
            summary,
            pbody, prefix="../", head_extra=head_extra, mobile_prefix="../", page_path=f"projects/{slug}.html"))


# ============ BLOG ============
BLOG_POSTS = [
  ("when-to-remove-vs-trim",
   "When to remove a tree vs. when to just trim it",
   "How to tell whether a tree needs to come down or whether good pruning will save it.",
   "2026-04-08","Tree care",FOREST,
   [("Start with structure, not symptoms",
     "Yellow leaves and dropping limbs are symptoms. The question that matters is whether the tree has a sound structure. A tree with one good central trunk, balanced branching, and live wood through the canopy is almost always worth keeping. A tree with a split crotch, hollow trunk, or major lean over a structure is a different conversation."),
    ("Reasons to trim instead of remove",
     "Most trees that look bad are actually trimmable. Deadwood, crossing branches, a heavy lean toward the house, or a canopy that hasn't been touched in fifteen years can all be addressed with selective pruning. A skilled crew can re-balance a tree so it's safer and healthier without taking it down."),
    ("Reasons to remove",
     "Major trunk cracks. Significant hollow at the base. Heavy lean over a house or driveway combined with shallow roots. Mushroom conks at the base — that's heart rot. Storm damage where more than half the canopy is gone. Species in decline (Bradford pears past about fifteen years are the classic example). When any of these are present, removal is usually the safer, cheaper long-term call."),
    ("A second opinion is worth the call",
     "If you're not sure, ask. We'd rather come out and tell you a tree has another twenty years in it than take down something that didn't need to come down.")]),
  ("storm-damage-checklist",
   "Storm damage checklist: what to do in the first 48 hours",
   "A practical order of operations after a tree comes down on your property.",
   "2026-03-20","Storm response",FOGFOREST,
   [("First, stop and check",
     "Look up before you walk out. Tangled limbs hold tension and can spring loose without warning. If anything is on a power line, treat it as live and call the utility — that's not your job and it's not ours."),
    ("Document everything",
     "Take photos before anything is moved. Wide shots, close-ups, from multiple angles. Your insurance company will want them, and so will we when we estimate."),
    ("Call your insurance company",
     "Open a claim as soon as it's safe. Most carriers want you to mitigate further damage — meaning, get the tree off the roof — and they'll usually cover reasonable removal and patching costs. Get the claim number before the crew arrives."),
    ("Call a tree service that answers the phone",
     "Storm cleanup runs on triage. Trees on houses, blocking driveways, or on power-line right-of-way come first. We answer storm calls quickly and prioritize by safety. We can also send a COI directly to your insurance company before we start."),
    ("What not to do",
     "Don't climb on the tree or the roof. Don't try to chainsaw a tree under tension. Don't accept a quote from a crew that just happened to be in the neighborhood without checking who they actually are.")]),
  ("land-clearing-explained",
   "Land clearing explained: dozing, mulching, and selective clearing",
   "Three very different ways to clear land, and which one fits your property.",
   "2026-03-05","Land clearing",FIELD,
   [("Dozing",
     "A dozer or excavator scrapes everything off — trees, brush, roots, topsoil. Fast and brutal. Good for builder pads where the surface is about to become a slab anyway. Bad if you want to keep any of the trees, the topsoil, or the existing grade."),
    ("Forestry mulching",
     "A tracked machine with a mulching head chews brush, saplings, and small trees into ground cover where they stand. No burn pile. No truckloads of debris to haul. Topsoil and stumps stay in place. Great for pasture reclaim, view corridors, fence-line clearing, and selective lot clearing where you want to keep mature trees."),
    ("Selective clearing",
     "A crew walks the property, tags what stays and what goes, and removes things one at a time with a combination of chainsaws, a skid steer, and a chipper. Slower, but it's the only way to clear land while keeping the character of the property."),
    ("How to choose",
     "Builder pad and you don't care what's on it? Doze it. Pasture or fence line where you want it cleaned up but not stripped? Mulch it. Wooded backyard you want to thin without losing the trees that make it feel like the woods? Selective clearing.")]),
  ("stump-grinding-vs-removal",
   "Stump grinding vs. stump removal: which one do you actually need?",
   "A quick guide to grinding, full removal, and when each makes sense.",
   "2026-02-18","Tree care",SITEPREP,
   [("Stump grinding",
     "The fast, common option. A grinder chews the stump down to six or eight inches below grade. The roots stay in the ground and slowly rot over the next few years. Cheaper than full removal and leaves a hole you can fill with topsoil and re-sod."),
    ("Stump removal",
     "A machine pulls the entire stump and root ball out of the ground. Bigger hole. Bigger cost. The right call when you're planting a new tree in the same spot, or when the stump is in the way of a foundation or hardscape."),
    ("What to ask before you decide",
     "Are you replanting in the same spot? Are you putting a patio or driveway there? Or are you just trying to be able to mow over it? The answer tells you which one fits.")]),
  ("tree-service-pricing-explained",
   "Why two tree estimates can be so far apart",
   "What actually goes into a tree-service price, and how to read a quote.",
   "2026-02-02","Pricing",TREE,
   [("The truck in the neighborhood",
     "Sometimes the cheapest quote is from a crew that's underinsured, has no chipper, and is going to pile your debris at the curb. The price is low because they're not actually paying for the things that protect you."),
    ("The real cost components",
     "Crew time, equipment time, debris hauling, stump grinding, insurance, fuel, and the risk premium of any work over a structure. Add them up and you get a real number."),
    ("How to read a quote",
     "Does it list the scope plainly? Does it say what happens to the debris? Does it include the stump or not? Is it written down? If the answer to any of those is no, you're not really comparing quotes — you're comparing guesses."),
    ("What we put on ours",
     "Service, scope, debris handling, stump included or not, total. If anything changes during the job, we stop and talk before the meter runs.")]),
  ("forestry-mulching-vs-bushhogging",
   "Forestry mulching vs. bush hogging: not the same thing",
   "They both look like clearing. They do very different work.",
   "2026-01-22","Land clearing",FORESTPATH,
   [("Bush hogging",
     "A rotary mower on the back of a tractor. Cuts grass and saplings up to about an inch or two. Great for keeping a field knocked down once it's already cleared."),
    ("Forestry mulching",
     "A tracked machine with a drum that chews material up to about eight inches in diameter into mulch. Handles brush, saplings, small trees, and overgrown undergrowth that a bush hog can't touch."),
    ("Which one fits",
     "If the field has just gotten away from you for a year or two, bush hog it. If it's been let go for five-plus years and there are real trees in there, you need a mulcher first — and then a bush hog the next season to keep it.")]),
  ("prep-site-for-builder",
   "How to prep your lot for the builder",
   "What to clear, grade, and protect before the foundation crew shows up.",
   "2026-01-08","Excavation",SITEPREP,
   [("Start with the survey",
     "Know your property lines, easements, and setbacks before anything moves. The cheapest clearing job is the one you don't do twice because the footprint shifted."),
    ("Clear, grub, then rough grade",
     "Clear the footprint plus a working buffer for trucks and a staging area. Grub the stumps so they don't haunt the foundation. Rough-grade with fall away from the future house."),
    ("Erosion control on day one",
     "Silt fence on the down-slope side, a stabilized construction entrance, and seeded perimeters. The inspector wants to see it. Your neighbors definitely want to see it."),
    ("Talk to the builder before you start",
     "Where do they want the staging area? Where will the porta-john go? Where do they want the dumpster? Getting that right before you clear saves a second mobilization later.")]),
  ("drainage-french-drains-explained",
   "French drains, swales, and dry wells: which one fixes your wet yard?",
   "A practical look at the three most common drainage fixes — and when each one is the right call.",
   "2025-12-15","Drainage",EXCAV,
   [("French drain",
     "A perforated pipe in a gravel trench. Picks up groundwater along its length and carries it to a daylight outlet. Best for yards where water keeps showing up from somewhere — a slope above the house, a neighbor's downspout, or a wet seam in the soil."),
    ("Swale",
     "A shallow grass-lined ditch. Moves surface water from a high spot to a low spot using grade. Cheap, low-maintenance, and the right call if your problem is surface runoff during heavy rain."),
    ("Dry well",
     "A buried gravel pit (or perforated chamber) that holds water and lets it soak in slowly. Good for short downspout runs where there's nowhere to daylight to. Bad as the primary fix for a chronically wet yard."),
    ("How to pick",
     "Stand in the yard during the next hard rain. Watch where the water actually comes from and where it actually goes. The fix is whatever interrupts that path with the least disturbance.")]),
]

def build_blog():
    os.makedirs("blog", exist_ok=True)
    def _bp(g, w):
        u = img(g, w)
        return ("../" + u) if (isinstance(g,str) and g.startswith('local:')) else u
    # Index
    cards = ""
    for slug,title,summary,date,category,hero_id,_ in BLOG_POSTS:
        cards += f'''
<article class="blog-card">
  <a class="blog-card-img" href="blog/{slug}.html"><img src="{_bp(hero_id,1100)}" alt="{title}" loading="lazy"></a>
  <div class="blog-card-body">
    <p class="eyebrow">{category} · {date}</p>
    <h3><a href="blog/{slug}.html">{title}</a></h3>
    <p>{summary}</p>
    <a class="more" href="blog/{slug}.html">Read →</a>
  </div>
</article>'''
    ibody = f'''
<section class="hero hero--inner" style="{hero_bg(FOREST,1800,pfx='../',overlay=True)}">
  <div class="container hero-content">
    <p class="eyebrow">Tips &amp; articles</p>
    <h1>Practical guides to tree work, land clearing, and excavation</h1>
    <p class="hero-sub">No filler. The things customers ask us about every week — how to tell when a tree needs to come down, what to do in the first 48 hours after a storm, and how to compare tree-service quotes that aren't really comparable.</p>
  </div>
</section>
{trustbar()}
<section class="sec"><div class="container">
  <div class="blog-grid">{cards}</div>
</div></section>
{cta_banner()}
'''
    head_extra = breadcrumb_schema([("Home","index.html"),("Tips &amp; Articles","blog/index.html")])
    write_page("blog/index.html", page(
        "Tips &amp; Articles | Tree Care, Land Clearing &amp; Excavation",
        "Practical guides to tree removal, storm cleanup, land clearing, stump grinding, drainage, and site prep from Claiborne Services LLC in Middle Tennessee.",
        ibody, prefix="../", head_extra=head_extra, mobile_prefix="../", page_path="blog/index.html"))

    # Individual posts
    for slug,title,summary,date,category,hero_id,sections in BLOG_POSTS:
        sec_html = "".join(f'<section class="prose"><h2>{h}</h2><p>{p}</p></section>' for h,p in sections)
        _bh = _bp(hero_id,1800)
        pbody = f'''
<section class="hero hero--inner" style="background-image:linear-gradient(rgba(20,30,20,.62),rgba(20,30,20,.62)),url('{_bh}')">
  <div class="container hero-content">
    <p class="eyebrow"><a href="index.html" style="color:#fff;text-decoration:underline">← All articles</a> · {category} · {date}</p>
    <h1>{title}</h1>
    <p class="hero-sub">{summary}</p>
  </div>
</section>
<section class="sec"><div class="container">
  <div class="blog-prose">{sec_html}</div>
  {finance_callout()}
</div></section>
{cta_banner("../")}
'''
        head_extra = breadcrumb_schema([("Home","index.html"),("Tips &amp; Articles","blog/index.html"),(title,f"blog/{slug}.html")])
        write_page(f"blog/{slug}.html", page(
            f"{title} | Claiborne Services LLC",
            summary,
            pbody, prefix="../", head_extra=head_extra, mobile_prefix="../", page_path=f"blog/{slug}.html"))


# ============ SPANISH LANDING ============
def build_spanish():
    os.makedirs("es", exist_ok=True)
    body = f'''
<section class="hero hero--inner" style="{hero_bg(TREE,1800,pfx='../',overlay=True)}">
  <div class="container hero-content">
    <p class="eyebrow">Servicios de árboles, limpieza de terrenos y excavación</p>
    <h1>El equipo de servicio completo de árboles, limpieza de terrenos y excavación en Middle Tennessee</h1>
    <p class="hero-sub">Empresa familiar, con seguro. Atendemos los condados de Williamson, Maury y Davidson — Franklin, Brentwood, Spring Hill, Thompson\'s Station, Nolensville, Columbia, Mt. Pleasant, Nashville y comunidades cercanas. Llame o envíe un mensaje de texto — con gusto le ayudamos en español.</p>
    <div class="hero-ctas"><a class="btn btn--primary" href="../contact.html">Solicitar Cotización Gratuita</a><a class="btn btn--ghost" href="tel:{PHONE_TEL}">Llamar {PHONE}</a></div>
  </div>
</section>
{trustbar()}
<section class="sec"><div class="container">
  <h2>Nuestros servicios</h2>
  <div class="features-grid">
    <div class="feature"><h3>Servicio de árboles</h3><p>Poda, recorte, eliminación y servicio de emergencia por daños de tormenta. Equipo completo y cuadrilla con experiencia.</p></div>
    <div class="feature"><h3>Eliminación de tocones</h3><p>Trituración de tocones de cualquier tamaño. Dejamos el área lista para sembrar grama o jardín.</p></div>
    <div class="feature"><h3>Limpieza de terrenos</h3><p>Limpieza forestal, recuperación de pastos, preparación de lotes, líneas de cerca. Cuidamos sus árboles maduros.</p></div>
    <div class="feature"><h3>Triturado forestal</h3><p>Convertimos maleza, arbustos y árboles pequeños en mantillo en el suelo. Sin pilas para quemar, sin viajes al basurero.</p></div>
    <div class="feature"><h3>Excavación y nivelación</h3><p>Preparación de pads para constructores, accesos, drenajes franceses, nivelación. Equipo pequeño y grande según la obra.</p></div>
    <div class="feature"><h3>Drenaje y soluciones</h3><p>Resolvemos zonas húmedas, agua cerca de la casa, escorrentía. Drenajes franceses, swales, y nivelación correctiva.</p></div>
  </div>
</div></section>
<section class="sec sec--alt"><div class="container">
  <h2>Por qué confiar en nosotros</h2>
  <ul class="checklist">
    <li>Empresa familiar, con base en Franklin, Tennessee.</li>
    <li>Con seguro — enviamos certificado de seguro antes de empezar.</li>
    <li>Cotizaciones gratuitas y por escrito.</li>
    <li>Hablamos español. Llame o envíe un mensaje de texto.</li>
    <li>Financiamiento disponible a través de QuickBooks para clientes calificados.</li>
  </ul>
  <div class="finance-callout">{icon("dollar")}<p><strong>Financiamiento disponible a través de QuickBooks.</strong> Clientes calificados pueden pagar a plazos mensuales, sujeto a aprobación.</p></div>
</div></section>
<section class="sec"><div class="container" style="text-align:center">
  <h2>¿Listo para empezar?</h2>
  <p class="lede">Llame o envíe un mensaje de texto al {PHONE}. Salimos a verlo, le damos un número por escrito, y usted decide.</p>
  <div class="hero-ctas" style="justify-content:center"><a class="btn btn--primary" href="../contact.html">Solicitar Cotización</a><a class="btn btn--ghost" href="tel:{PHONE_TEL}">Llamar {PHONE}</a><a class="btn btn--ghost" href="sms:{PHONE_TEL}">Mensaje de Texto</a></div>
</div></section>
'''
    head_extra = breadcrumb_schema([("Home","index.html"),("Español","es/index.html")])
    write_page("es/index.html", page(
        "Servicios de Árboles, Limpieza de Terrenos y Excavación | Claiborne Services LLC",
        "Empresa familiar de servicio de árboles, limpieza de terrenos y excavación en Middle Tennessee. Con seguro. Hablamos español. Cotización gratis.",
        body, prefix="../", head_extra=head_extra, mobile_prefix="../", page_path="es/index.html", lang="es"))


# ============ 404 ============
def build_404():
    body = f'''
<section class="hero hero--inner hero--404" style="{hero_bg(FOGFOREST,1800,overlay=True)}">
  <div class="container hero-content" style="text-align:center">
    <p class="eyebrow">404</p>
    <h1>Lost in the woods?</h1>
    <p class="hero-sub">That page took a wrong turn. Try one of these instead, or call us — that always works.</p>
    <div class="hero-ctas" style="justify-content:center"><a class="btn btn--primary" href="index.html">Back to Home</a><a class="btn btn--ghost" href="tel:{PHONE_TEL}">Call {PHONE}</a></div>
  </div>
</section>
<section class="sec"><div class="container">
  <h2>Maybe you were looking for</h2>
  <div class="features-grid">
    <div class="feature"><h3><a href="services/tree-service.html">Tree Service</a></h3><p>Trimming, removal, and storm work.</p></div>
    <div class="feature"><h3><a href="services/land-clearing.html">Land Clearing</a></h3><p>Lots, pasture, and selective clearing.</p></div>
    <div class="feature"><h3><a href="services/excavation.html">Excavation</a></h3><p>Pads, drainage, grading, driveways.</p></div>
    <div class="feature"><h3><a href="faq.html">FAQs</a></h3><p>Pricing, insurance, equipment, scheduling.</p></div>
    <div class="feature"><h3><a href="contact.html">Get an Estimate</a></h3><p>Free and written.</p></div>
  </div>
</div></section>
'''
    write_page("404.html", page(
        "Page not found | Claiborne Services LLC",
        "That page took a wrong turn. Head back home, or call us.",
        body, page_path="404.html"))


# ============ SITEMAP + ROBOTS ============
def build_sitemap_and_robots():
    import datetime
    today = datetime.date.today().isoformat()
    urls = []
    # Walk repo and collect .html files
    for root, dirs, files in os.walk("."):
        # skip hidden
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("data","assets")]
        for f in files:
            if not f.endswith(".html"): continue
            if f == "404.html": continue
            rel = os.path.relpath(os.path.join(root, f), ".").replace("\\","/")
            if rel.startswith("./"): rel = rel[2:]
            urls.append(rel)
    urls = sorted(set(urls))
    body = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        loc = f"{SITE_URL}/{u}"
        if u == "index.html": loc = f"{SITE_URL}/"
        prio = "1.0" if u == "index.html" else ("0.8" if "/" not in u else "0.6")
        body += f"  <url><loc>{loc}</loc><lastmod>{today}</lastmod><priority>{prio}</priority></url>\n"
    body += "</urlset>\n"
    with open("sitemap.xml","w",encoding="utf-8") as f: f.write(body)
    robots = f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n"
    with open("robots.txt","w",encoding="utf-8") as f: f.write(robots)
    print(f"sitemap.xml written ({len(urls)} URLs); robots.txt written")


if __name__ == "__main__":
    build_home()
    build_all_services()
    build_about()
    build_service_area()
    build_cities()
    build_city_stubs()
    build_reviews()
    build_gallery()
    build_discounts()
    build_partners()
    build_contact()
    build_faq()
    build_pricing()
    build_financing()
    build_equipment()
    build_insurance()
    # build_projects()  # Tier 2 — held back for user review
    # build_blog()       # Tier 2 — held back for user review
    # build_spanish()    # Tier 2 — held back for native speaker review
    build_404()
    build_sitemap_and_robots()
    print("ALL PAGES BUILT")
