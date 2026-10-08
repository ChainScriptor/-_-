"""Builds anbit_street_guerrilla.pdf from content_street.py (same design as the other PDFs)."""
from collections import Counter
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether, NextPageTemplate, PageBreak,
                                PageTemplate, Paragraph, Spacer, Table, TableStyle)

from build_aggressive import categories, cover_drawer, label_table, page_drawer
from build_playbook import (CONTENT_W, INK, LAV, LAV_SOFT, MARGIN, PAGE_H, S, TYPE_BG, YEL,
                            section_header, style, type_tag)
from content_street import HOW_TO, IDEAS, KIT, RULES, START_WITH

OUT = Path(__file__).parent / "anbit_street_guerrilla.pdf"

draw_cover = cover_drawer(
    "ΤΟ ΑΠΟΛΥΤΟ GUERRILLA ΤΟΥ ΔΡΟΜΟΥ",
    ["100 τερματισμένες", "ιδέες για", "τον δρόμο"],
    ["Παιχνίδια με γιγάντιο QR, ερωτήσεις για street interviews, προκλήσεις,",
     "σειρές TikTok και μεγάλα stunts. Ο κόσμος σκανάρει, παραγγέλνει",
     "μέσα από την Anbit, κερδίζει, και το βίντεο γράφει μόνο του."],
    ["Σκάναρε. Παράγγειλε.", "Κι αν το έχω στο ψυγειάκι, είναι δικό σου."],
    "Σήμερα γεμάτο. Αύριο; Ο δρόμος αποφασίζει.")
draw_page = page_drawer("Anbit · Το απόλυτο guerrilla του δρόμου")


def numbered_steps(rows, num_w=14 * mm):
    t = Table([[Paragraph(f"<b>{n}</b>", style("n", fontName="Sans-Bold", fontSize=13, leading=15,
                                              alignment=TA_CENTER, textColor=YEL)),
                Paragraph(text, S["cell"])] for n, text in rows],
              colWidths=[num_w, CONTENT_W - num_w])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), INK), ("BACKGROUND", (1, 0), (-1, -1), LAV_SOFT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEBELOW", (0, 0), (-1, -2), 1.5, colors.white),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (1, 0), (-1, -1), 9),
    ]))
    return t


def build():
    items = [i for _, _, group in IDEAS for i in group]
    assert len(items) == 100, len(items)
    kinds = Counter(i[4] for i in items)
    cheap = sum(1 for i in items if i[2] == "€")
    titles = {n: idea[0] for n, idea in enumerate(items, start=1)}

    doc = BaseDocTemplate(str(OUT), pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
                          topMargin=16 * mm, bottomMargin=18 * mm,
                          title="Anbit – Το απόλυτο guerrilla του δρόμου", author="Anbit",
                          subject="100 ιδέες για τον δρόμο: QR παιχνίδια, ερωτήσεις, προκλήσεις, TikTok")
    frame = Frame(MARGIN, 18 * mm, CONTENT_W, PAGE_H - 34 * mm, id="f",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="cover", frames=[frame], onPage=draw_cover),
                          PageTemplate(id="page", frames=[frame], onPage=draw_page)])

    story = [NextPageTemplate("page"), PageBreak()]

    # The signature game
    story += section_header("ΤΟ ΒΑΣΙΚΟ ΠΑΙΧΝΙΔΙ", "«Μάντεψε τι έχω στο ψυγειάκι»",
                            "Το παιχνίδι-σήμα της Anbit στον δρόμο. Οι περισσότερες ιδέες του PDF είναι παραλλαγές του, "
                            "οπότε στήσ' το μία φορά σωστά και θα το ξαναχρησιμοποιείς σε κάθε πλατεία.")
    story.append(numbered_steps(HOW_TO))
    story.append(Spacer(1, 14))
    story.append(KeepTogether([Paragraph("Το κιτ του δρόμου", S["h2"]), Spacer(1, 4),
                               label_table(KIT, label_w=46 * mm)]))
    story.append(Spacer(1, 14))

    stats = Table([[
        Paragraph("<font size=22><b>100</b></font><br/>ιδέες για τον δρόμο", style("a", alignment=TA_CENTER, leading=16)),
        Paragraph(f"<font size=22><b>{kinds['Τερματισμένο']}</b></font><br/>τερματισμένες", style("b", alignment=TA_CENTER, leading=16)),
        Paragraph(f"<font size=22><b>{kinds['Επιθετικό']}</b></font><br/>επιθετικές",
                  style("c", alignment=TA_CENTER, leading=16, textColor=YEL)),
        Paragraph(f"<font size=22><b>{cheap}</b></font><br/>κοστίζουν έως 50€", style("d", alignment=TA_CENTER, leading=16)),
    ]], colWidths=[CONTENT_W / 4] * 4)
    stats.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), LAV), ("BACKGROUND", (1, 0), (1, 0), YEL),
        ("BACKGROUND", (2, 0), (2, 0), INK), ("BACKGROUND", (3, 0), (3, 0), LAV),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 12), ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LINEAFTER", (0, 0), (2, 0), 2, colors.white),
    ]))
    tags = ["Έξυπνο", "Επιθετικό", "Τερματισμένο"]
    legend = Table([[Paragraph("<b>€</b> έως 50€ · <b>€€</b> 50–300€ · <b>€€€</b> 300–1.000€", S["cell"])]
                    + [type_tag(k) for k in tags]],
                   colWidths=[CONTENT_W - 3 * 26 * mm] + [26 * mm] * 3)
    legend.setStyle(TableStyle(
        [("BACKGROUND", (i + 1, 0), (i + 1, 0), TYPE_BG.get(k, LAV)) for i, k in enumerate(tags)]
        + [("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (0, 0), 0),
           ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    story.append(KeepTogether([stats, Spacer(1, 8), legend]))

    # Start with + rules
    story.append(PageBreak())
    story += section_header("ΞΕΚΙΝΑ ΑΠΟ ΑΥΤΑ", "Τα πρώτα 10 που κάνεις",
                            "Φθηνά, γρήγορα στο στήσιμο, και με το καθένα φτιάχνεις 3–5 βίντεο σε ένα απόγευμα.")
    story.append(numbered_steps([(f"#{k}", f"<b>{titles[k]}</b>") for k in START_WITH], num_w=16 * mm))
    story.append(Spacer(1, 16))
    story.append(KeepTogether([Paragraph("Κανόνες του δρόμου", S["h2"]),
                               Paragraph("Τερματισμένο σημαίνει να το θυμάται όλη η πόλη. Δεν σημαίνει πρόστιμο ή σκάνδαλο.", S["small"]),
                               Spacer(1, 6), label_table(RULES, label_w=40 * mm)]))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Δεν είναι νομική συμβουλή. Για άδειες και διαγωνισμούς με δώρα, ρώτα τον δήμο, λογιστή ή δικηγόρο.",
                           S["small"]))

    # Ideas
    story.append(PageBreak())
    story += section_header("ΟΙ 100 ΙΔΕΕΣ", "Ο δρόμος είναι η σκηνή σου",
                            "Κάθε ιδέα έχει hook για το βίντεο και λέει τι χρειάζεσαι για να τη στήσεις. "
                            "Στις ερωτήσεις, το «Twist» είναι αυτό που κάνει το βίντεο να αξίζει.")
    blocks, _ = categories(IDEAS, 1, "Τι χρειάζεσαι")
    story += blocks

    doc.build(story)
    print(f"-> {OUT}  {kinds}  cheap={cheap}")


if __name__ == "__main__":
    build()
