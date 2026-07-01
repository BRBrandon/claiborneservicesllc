# Image Sources — Claiborne Services LLC Website

All imagery is sourced from **Pexels** and **Unsplash** (both free-to-use, no attribution required).
Every URL below was verified to return HTTP 200 and visually confirmed for relevant subject matter
(heavy equipment, tree work, land clearing, forestry, fields, trenching/excavation, forest scenes).

## Delivery
- Pexels: `https://images.pexels.com/photos/{ID}/pexels-photo-{ID}.jpeg?auto=compress&cs=tinysrgb&w={W}`
- Unsplash: `https://images.unsplash.com/photo-{ID}?auto=format&fit=crop&q=70&w={W}`
- All non-hero images use `loading="lazy"`. Heroes are CSS background images.

## Pexels photos used (primary equipment / crew / land / forest)
| ID | Subject | Usage |
|----|---------|-------|
| 1078884 | Orange excavator on a job site | Homepage hero, excavation, gallery |
| 585419 | Worker carrying log / timber on site | Tree services, crew action, gallery |
| 1216589 | Two workers in hard hats | Crew / about |
| 1029243 | Tall tree | Tree services |
| 96715 | Cleared field at sunrise | Land clearing |
| 440731 | Green field | Land clearing |
| 167698 | Sunlit forest | Forestry mulching, gallery |
| 2219024 | Cement / site work | Site preparation |
| 2310904 | Industrial pipes / trenching | Excavation, utilities |
| 2058134 | Hands over site plans | Site preparation / planning |
| 531844 | Large oak tree | Gallery (tree) |
| 259280 | Forest road | Gallery (mulching) |
| 57903 | Green rolling field | Gallery (land) |
| 1632790 | Large tree at sunset | Gallery (tree) |
| 142497 | Mossy tree trunk | Gallery (tree) |

## Unsplash photos used (forest / field scenery)
| ID | Subject |
|----|---------|
| 1416879595882-3373a0480b5b | Forest canopy |
| 1473773508845-188df298d2d1 | Forest path / floor |
| 1502082553048-f009c37129b9 | Foggy forest |
| 1500382017468-9049fed747ef | Golden field |
| 1486754735734-325b5831c3ad | Field rows |

## QA
- 67 unique image URLs across the site; all verified HTTP 200 (zero broken links).
- Browser render check (Playwright): no broken `<img>` elements beyond the empty lightbox placeholder (expected — populated on click).
