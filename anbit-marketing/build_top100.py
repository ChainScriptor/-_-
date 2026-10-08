"""Builds anbit_top100_crowd_ideas.pdf from content_top100.py (same design as the other PDFs)."""
from collections import Counter
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether, NextPageTemplate, PageBreak,
                                PageTemplate, Paragraph, Spacer, Table, TableStyle)

from build_aggressive import categories, cover_drawer, label_table, page_drawer
from build_playbook import CONTENT_W, INK, LAV, LAV_SOFT, MARGIN, PAGE_H, S, TYPE_BG, YEL, section_header, style, type_tag
from build_street import numbered_steps
from content_top100 import CRITERIA, IDEAS, RULES, TOP10

OUT = Path(__file__).parent / "anbit_top100_crowd_ideas.pdf"

draw_cover = cover_drawer(
    "TOP 100 · ΤΕΡΜΑΤΙΣΜΕΝΕΣ ΙΔΕΕΣ",
    ["100 ιδέες", "που μαζεύουν", "κόσμο"],
    ["100 διαφορετικά concepts, όχι παραλλαγές του ίδιου: θέαμα, θέατρο δρόμου,",
     "κοινωνικά πειράματα, χιούμορ, τεχνολογία, μυστήριο, συγκίνηση, ρεκόρ,",
     "κόντρες και η πόλη ως σκηνικό. Για Αθήνα, Θεσσαλονίκη και κάθε πόλη."],
    ["Ο κόσμος δεν σταματάει για διαφημίσεις.", "Σταματάει για κάτι που δεν έχει ξαναδεί."],
    "Σήμερα γεμάτο. Αύριο; Όλη η πόλη θα μιλάει.")
draw_page = page_drawer("Anbit · Top 100 ιδέες που μαζεύουν κόσμο")


def build():
    items = [i for _, _, group in IDEAS for i in group]
    assert len(items) == 100, len(items)
    assert all(len(group) == 10 for _, _, group in IDEAS)
    kinds = Counter(i[4] for i in items)
    pulls = Counter(i[3] for i in items)
    titles = {n: idea[0] for n, idea in enumerate(items, start=1)}

    doc = BaseDocTemplate(str(OUT), pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
                          topMargin=16 * mm, bottomMargin=18 * mm,
                          title="Anbit – Top 100 ιδέες που μαζεύουν κόσμο", author="Anbit",
                          subject="100 διαφορετικές guerrilla ιδέες για την Anbit")
    frame = Frame(MARGIN, 18 * mm, CONTENT_W, PAGE_H - 34 * mm, id="f",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="cover", frames=[frame], onPage=draw_cover),
                          PageTemplate(id="page", frames=[frame], onPage=draw_page)])

    story = [NextPageTemplate("page"), PageBreak()]
    story += section_header("ΠΩΣ ΔΙΑΛΕΞΑ ΤΑ 100", "Τέσσερα κριτήρια, 100 ιδέες",
                            "Κάθε ιδέα πέρασε από τέσσερα φίλτρα. Όπου στηρίζεται σε γνωστή καμπάνια, το γράφει κάτω από την ιδέα.")
    story.append(label_table(CRITERIA, label_w=40 * mm))
    story.append(Spacer(1, 14))

    pull_rows = sorted(pulls.items(), key=lambda kv: -kv[1])
    cells = [Paragraph(f"<b>{n}</b>&nbsp; {k}", S["cell"]) for k, n in pull_rows]
    while len(cells) % 4:
        cells.append(Paragraph("", S["cell"]))
    grid = Table([cells[i:i + 4] for i in range(0, len(cells), 4)], colWidths=[CONTENT_W / 4] * 4)
    grid.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LAV_SOFT), ("GRID", (0, 0), (-1, -1), 2, colors.white),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(KeepTogether([Paragraph("Γιατί τραβάνε κόσμο", S["h2"]),
                               Paragraph("Η στήλη «Γιατί τραβάει» λέει τι κάνει τον κόσμο να σταματήσει σε κάθε ιδέα.", S["small"]),
                               Spacer(1, 6), grid]))
    story.append(Spacer(1, 14))

    stats = Table([[
        Paragraph("<font size=22><b>100</b></font><br/>διαφορετικά concepts", style("a", alignment=TA_CENTER, leading=16)),
        Paragraph(f"<font size=22><b>{kinds['Τερματισμένο']}</b></font><br/>τερματισμένες", style("b", alignment=TA_CENTER, leading=16)),
        Paragraph(f"<font size=22><b>{kinds['Επιθετικό']}</b></font><br/>επιθετικές",
                  style("c", alignment=TA_CENTER, leading=16, textColor=YEL)),
        Paragraph(f"<font size=22><b>{len(pulls)}</b></font><br/>λόγοι που τραβάνε κόσμο", style("d", alignment=TA_CENTER, leading=16)),
    ]], colWidths=[CONTENT_W / 4] * 4)
    stats.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), LAV), ("BACKGROUND", (1, 0), (1, 0), YEL),
        ("BACKGROUND", (2, 0), (2, 0), INK), ("BACKGROUND", (3, 0), (3, 0), LAV),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 12), ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LINEAFTER", (0, 0), (2, 0), 2, colors.white),
    ]))
    tags = ["Έξυπνο", "Επιθετικό", "Τερματισμένο"]
    legend = Table([[Paragraph("<b>€</b> έως 50€ · <b>€€</b> 50–300€ · <b>€€€</b> 300–1.000€+", S["cell"])]
                    + [type_tag(k) for k in tags]],
                   colWidths=[CONTENT_W - 3 * 26 * mm] + [26 * mm] * 3)
    legend.setStyle(TableStyle(
        [("BACKGROUND", (i + 1, 0), (i + 1, 0), TYPE_BG.get(k, LAV)) for i, k in enumerate(tags)]
        + [("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (0, 0), 0),
           ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    story.append(KeepTogether([stats, Spacer(1, 8), legend]))

    story.append(PageBreak())
    story += section_header("ΑΝ ΚΑΝΕΙΣ ΜΟΝΟ 10", "Τα 10 που θα έκανα πρώτα",
                            "Φθηνά ή μεσαίου κόστους, γρήγορα στο στήσιμο, και το καθένα μαζεύει κόσμο από μόνο του.")
    story.append(numbered_steps([(f"#{k}", f"<b>{titles[k]}</b>") for k in TOP10], num_w=16 * mm))
    story.append(Spacer(1, 16))
    story.append(KeepTogether([Paragraph("Κανόνες για να μείνει τερματισμένο και όχι προβληματικό", S["h2"]),
                               Spacer(1, 6), label_table(RULES, label_w=36 * mm)]))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Δεν είναι νομική συμβουλή. Για άδειες, διαγωνισμούς με δώρα και δικαιώματα, ρώτα τον δήμο, λογιστή ή δικηγόρο.",
                           S["small"]))

    story.append(PageBreak())
    story += section_header("ΟΙ 100 ΙΔΕΕΣ", "10 κατηγορίες, 100 διαφορετικοί τρόποι να σταματήσεις την πόλη",
                            "Κάθε ιδέα έχει hook για το βίντεο. Όπου μια ιδέα στηρίζεται σε πραγματική καμπάνια, γράφει από ποια.")
    blocks, _ = categories(IDEAS, 1, "Γιατί τραβάει")
    story += blocks

    doc.build(story)
    print(f"-> {OUT}  {kinds}  pulls={dict(pulls)}")


if __name__ == "__main__":
    build()
