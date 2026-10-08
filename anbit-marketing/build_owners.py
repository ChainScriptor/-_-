"""Builds anbit_100_owner_approaches.pdf from content_owners.py (same design as the other PDFs)."""
from collections import Counter
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether, NextPageTemplate, PageBreak,
                                PageTemplate, Paragraph, Spacer, Table, TableStyle)

from build_aggressive import categories, cover_drawer, label_table, page_drawer
from build_playbook import CONTENT_W, INK, LAV, LAV_SOFT, LINE, MARGIN, PAGE_H, S, YEL, section_header, style, type_tag
from content_owners import APPROACHES, RULES, VISIT_SCRIPT

OUT = Path(__file__).parent / "anbit_100_owner_approaches.pdf"

draw_cover = cover_drawer(
    "ΠΩΛΗΣΕΙΣ ΣΤΑ ΜΑΓΑΖΙΑ · B2B",
    ["100 τρόποι", "να πείσεις", "τον ιδιοκτήτη"],
    ["Προσεγγίσεις σαν τον «μυστικό πελάτη», με έτοιμη ατάκα για την καθεμία:",
     "από την έρευνα πριν την πόρτα μέχρι το κλείσιμο και την πρώτη μέρα.",
     "Όλες καινούργιες, όλες για να τις δοκιμάσεις από αύριο."],
    ["«3η φορά αυτή την εβδομάδα.", "Με την Anbit θα το ξέρατε.»"],
    "Δεν πουλάς σύστημα. Πουλάς θαμώνες.")
draw_page = page_drawer("Anbit · 100 προσεγγίσεις καταστηματάρχη")


def build():
    items = [i for _, _, group in APPROACHES for i in group]
    assert len(items) == 100, len(items)
    kinds = Counter(i[4] for i in items)
    cheap = sum(1 for i in items if i[2] == "€")

    doc = BaseDocTemplate(str(OUT), pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
                          topMargin=16 * mm, bottomMargin=18 * mm,
                          title="Anbit – 100 προσεγγίσεις καταστηματάρχη", author="Anbit",
                          subject="100 τρόποι προσέγγισης ιδιοκτητών καταστημάτων εστίασης")
    frame = Frame(MARGIN, 18 * mm, CONTENT_W, PAGE_H - 34 * mm, id="f",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="cover", frames=[frame], onPage=draw_cover),
                          PageTemplate(id="page", frames=[frame], onPage=draw_page)])

    story = [NextPageTemplate("page"), PageBreak()]
    story += section_header("ΠΡΙΝ ΒΓΕΙΣ ΣΤΟΝ ΔΡΟΜΟ", "7 κανόνες για κάθε επίσκεψη",
                            "Ο ιδιοκτήτης ακούει δέκα πωλητές τον μήνα. Θυμάται μόνο αυτόν που ήξερε το μαγαζί του, "
                            "σεβάστηκε τον χρόνο του και του άφησε κάτι.")
    story.append(label_table(RULES, label_w=44 * mm))
    story.append(Spacer(1, 14))

    script_rows = [[Paragraph(f"<b>{t}</b>", style("t", fontName="Sans-Bold", fontSize=11, leading=13,
                                                 alignment=TA_CENTER, textColor=YEL)),
                    Paragraph(f"<b>{step}</b>", S["cell"]), Paragraph(what, S["cell"])]
                   for t, step, what in VISIT_SCRIPT]
    script = Table(script_rows, colWidths=[18 * mm, 26 * mm, CONTENT_W - 44 * mm])
    script.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), INK), ("BACKGROUND", (1, 0), (-1, -1), LAV_SOFT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEBELOW", (0, 0), (-1, -2), 1.5, colors.white),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (1, 0), (-1, -1), 8),
    ]))
    story.append(KeepTogether([
        Paragraph("Η επίσκεψη των 5 λεπτών", S["h2"]),
        Paragraph("Ο σκελετός κάθε συνάντησης. Τα νούμερα δείχνουν ποιες προσεγγίσεις ταιριάζουν σε κάθε βήμα.", S["small"]),
        Spacer(1, 6), script]))
    story.append(Spacer(1, 14))

    stats = Table([[
        Paragraph("<font size=22><b>100</b></font><br/>προσεγγίσεις", style("a", alignment=TA_CENTER, leading=16)),
        Paragraph("<font size=22><b>100</b></font><br/>έτοιμες ατάκες", style("b", alignment=TA_CENTER, leading=16)),
        Paragraph(f"<font size=22><b>{kinds['Επιθετικό']}</b></font><br/>επιθετικές",
                  style("c", alignment=TA_CENTER, leading=16, textColor=YEL)),
        Paragraph(f"<font size=22><b>{cheap}</b></font><br/>κοστίζουν έως 50€", style("d", alignment=TA_CENTER, leading=16)),
    ]], colWidths=[CONTENT_W / 4] * 4)
    stats.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (1, 0), LAV), ("BACKGROUND", (2, 0), (2, 0), INK),
        ("BACKGROUND", (3, 0), (3, 0), YEL), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 12), ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LINEAFTER", (0, 0), (2, 0), 2, colors.white),
    ]))
    legend = Table([[
        Paragraph("<b>Πότε:</b> Πριν · 1η επίσκεψη · Follow-up · Κλείσιμο · Μετά το ναι", S["cell"]),
        type_tag("Έξυπνο"), type_tag("Επιθετικό"),
    ]], colWidths=[CONTENT_W - 2 * 24 * mm, 24 * mm, 24 * mm])
    legend.setStyle(TableStyle([
        ("BACKGROUND", (1, 0), (1, 0), LAV), ("BACKGROUND", (2, 0), (2, 0), INK),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (0, 0), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LINEABOVE", (0, 0), (-1, 0), 0.5, LINE),
    ]))
    story.append(KeepTogether([stats, Spacer(1, 8), legend]))

    story.append(PageBreak())
    story += section_header("ΟΙ 100 ΠΡΟΣΕΓΓΙΣΕΙΣ", "Από την πόρτα μέχρι το «ναι»",
                            "Κάθε προσέγγιση έχει μια έτοιμη ατάκα. Προσάρμοσέ την στη φωνή σου και χρησιμοποίησε μόνο "
                            "αληθινά νούμερα και αληθινά ονόματα. Η στήλη «Πότε» λέει σε ποιο σημείο της πώλησης ταιριάζει.")
    blocks, _ = categories(APPROACHES, 1, "Πότε")
    story += blocks

    doc.build(story)
    print(f"-> {OUT}  {kinds}  cheap={cheap}")


if __name__ == "__main__":
    build()
