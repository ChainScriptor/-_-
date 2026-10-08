"""Builds anbit_100_aggressive_ideas.pdf from content_aggressive.py (same design as the playbook)."""
from collections import Counter
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Frame, KeepTogether, NextPageTemplate,
                                PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle)

from build_playbook import (CONTENT_W, GREY, INK, LAV, LAV_SOFT, LINE, MARGIN, PAGE_H, PAGE_W, S, YEL,
                            ideas_table, section_header, style, type_tag)
from content_aggressive import FOUNDER_RULES, HOOKS, OTHER, RED_LINES, TIKTOK, TIKTOK_PLAN

OUT = Path(__file__).parent / "anbit_100_aggressive_ideas.pdf"
HEADER = "Anbit · 100 έξυπνες & επιθετικές ιδέες"


def draw_cover(c, doc):
    c.saveState()
    c.setFillColor(LAV)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    c.setFillColor(INK)
    c.setFont("Sans-Bold", 22)
    c.drawString(MARGIN, PAGE_H - 30 * mm, "Anbit")

    pill_text = "ΕΚΔΟΣΗ ΙΔΡΥΤΗ · TIKTOK FIRST"
    c.setFont("Sans-Bold", 9)
    w = c.stringWidth(pill_text, "Sans-Bold", 9) + 14
    c.setFillColor(YEL)
    c.roundRect(MARGIN, PAGE_H - 62 * mm, w, 7.5 * mm, 3.7 * mm, stroke=0, fill=1)
    c.setFillColor(INK)
    c.drawString(MARGIN + 7, PAGE_H - 62 * mm + 2.6 * mm, pill_text)

    c.setFont("Sans-Bold", 44)
    for i, line in enumerate(["100 έξυπνες", "& επιθετικές", "ιδέες"]):
        c.drawString(MARGIN, PAGE_H - (82 + i * 17) * mm, line)

    c.setFont("Sans", 13)
    c.setFillColor(GREY)
    for i, line in enumerate(["50 ιδέες για TikTok που κάνεις εσύ, ως ιδρυτής, μπροστά στην κάμερα,",
                              "και 50 ακόμα για δρόμο, πωλήσεις, PR και growth.",
                              "Όλες καινούργιες, όλες με μικρό budget."]):
        c.drawString(MARGIN, PAGE_H - (140 + i * 7) * mm, line)

    box_h = 46 * mm
    c.setFillColor(INK)
    c.roundRect(MARGIN, 32 * mm, CONTENT_W, box_h, 6 * mm, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Sans-Bold", 15)
    c.drawString(MARGIN + 10 * mm, 32 * mm + box_h - 15 * mm, "Το TikTok δεν θέλει διαφημίσεις.")
    c.drawString(MARGIN + 10 * mm, 32 * mm + box_h - 23 * mm, "Θέλει εσένα, τα «όχι» σου και τις νίκες σου.")
    c.setFillColor(YEL)
    c.drawString(MARGIN + 10 * mm, 32 * mm + box_h - 35 * mm, "Σήμερα γεμάτο. Αύριο; Θα το δουν όλοι.")

    c.setFillColor(INK)
    c.setFont("Sans", 9)
    c.drawString(MARGIN, 18 * mm, "anbit.gr · Οκτώβριος 2026")
    c.restoreState()


def draw_page(c, doc):
    c.saveState()
    c.setFillColor(LAV)
    c.rect(0, PAGE_H - 7 * mm, PAGE_W, 7 * mm, stroke=0, fill=1)
    c.setFont("Sans-Bold", 8)
    c.setFillColor(INK)
    c.drawString(MARGIN, PAGE_H - 4.8 * mm, HEADER)
    c.setFont("Sans", 8)
    c.setFillColor(GREY)
    c.drawRightString(PAGE_W - MARGIN, 10 * mm, f"{doc.page}")
    c.restoreState()


def label_table(rows, label_w=46 * mm):
    t = Table([[Paragraph(f"<b>{a}</b>", S["cell"]), Paragraph(b, S["cell"])] for a, b in rows],
              colWidths=[label_w, CONTENT_W - label_w])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (0, -1), YEL),
        ("LINEBELOW", (0, 0), (-1, -2), 0.5, LINE),
        ("BOX", (0, 0), (-1, -1), 0.6, INK),
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def categories(groups, start, col4):
    out, n = [], start
    for i, (cat, sub, ideas) in enumerate(groups, start=1):
        out += [CondPageBreak(60 * mm), Spacer(1, 4),
                Paragraph(f"ΚΑΤΗΓΟΡΙΑ {i} · ΙΔΕΕΣ {n}–{n + len(ideas) - 1}", S["kicker"]),
                Paragraph(cat, S["h2"]), Paragraph(sub, S["small"]), Spacer(1, 6),
                ideas_table(n, ideas, col4=col4), Spacer(1, 14)]
        n += len(ideas)
    return out, n


def build():
    tiktok = [i for _, _, ideas in TIKTOK for i in ideas]
    other = [i for _, _, ideas in OTHER for i in ideas]
    assert len(tiktok) == 50 and len(other) == 50, (len(tiktok), len(other))
    kinds = Counter(i[4] for i in tiktok + other)
    cheap = sum(1 for i in tiktok + other if i[2] == "€")
    titles = {n: idea[0] for n, idea in enumerate(tiktok, start=1)}

    doc = BaseDocTemplate(str(OUT), pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
                          topMargin=16 * mm, bottomMargin=18 * mm,
                          title="Anbit – 100 έξυπνες & επιθετικές ιδέες", author="Anbit",
                          subject="50 ιδέες TikTok για τον ιδρυτή και 50 επιθετικές ιδέες growth")
    frame = Frame(MARGIN, 18 * mm, CONTENT_W, PAGE_H - 34 * mm, id="f",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="cover", frames=[frame], onPage=draw_cover),
                          PageTemplate(id="page", frames=[frame], onPage=draw_page)])

    story = [NextPageTemplate("page"), PageBreak()]

    # Founder rules
    story += section_header("ΠΡΙΝ ΠΑΤΗΣΕΙΣ REC", "Οι 11 κανόνες του ιδρυτή στο TikTok",
                            "Το πιο φθηνό και πιο δυνατό marketing της Anbit είσαι εσύ: ένας ιδρυτής που πάει "
                            "πόρτα-πόρτα και το δείχνει. Οι ιδέες 1–50 είναι γραμμένες για να τις γυρίσεις εσύ.")
    story.append(label_table(FOUNDER_RULES))
    story.append(Spacer(1, 12))

    hook_cells = [[Paragraph(f"<b>{HOOKS[i]}</b>", S["cell"]),
                   Paragraph(f"<b>{HOOKS[i + 1]}</b>", S["cell"])] for i in range(0, len(HOOKS), 2)]
    hooks = Table(hook_cells, colWidths=[CONTENT_W / 2] * 2)
    hooks.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LAV_SOFT),
        ("GRID", (0, 0), (-1, -1), 2, colors.white),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(KeepTogether([Paragraph("8 hooks για όταν κολλήσεις", S["h2"]), Spacer(1, 4), hooks]))
    story.append(Spacer(1, 12))

    stats = Table([[
        Paragraph("<font size=22><b>50</b></font><br/>TikTok ιδρυτή", style("a", alignment=TA_CENTER, leading=16)),
        Paragraph("<font size=22><b>50</b></font><br/>δρόμος · πωλήσεις · PR · growth",
                  style("b", alignment=TA_CENTER, leading=16)),
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
        Paragraph("<b>€</b> έως 50€ · <b>€€</b> 50–300€ · <b>€€€</b> 300–1.000€", S["cell"]),
        type_tag("Έξυπνο"), type_tag("Επιθετικό"),
    ]], colWidths=[CONTENT_W - 2 * 24 * mm, 24 * mm, 24 * mm])
    legend.setStyle(TableStyle([
        ("BACKGROUND", (1, 0), (1, 0), LAV), ("BACKGROUND", (2, 0), (2, 0), INK),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (0, 0), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(KeepTogether([stats, Spacer(1, 8), legend]))

    # Part 1: TikTok
    story.append(PageBreak())
    story += section_header("ΜΕΡΟΣ 1 · ΙΔΕΕΣ 1–50", "TikTok: τι κάνεις εσύ, ως ιδρυτής",
                            "Κάθε ιδέα έχει έτοιμο hook για τα πρώτα δευτερόλεπτα. Τα hooks είναι παραδείγματα: "
                            "προσάρμοσέ τα στην αληθινή σου ιστορία και στα δικά σου νούμερα. Η στήλη «Format» λέει τι είδους βίντεο είναι.")
    blocks, nxt = categories(TIKTOK, 1, "Format")
    story += blocks

    # 30-day plan
    story.append(CondPageBreak(110 * mm))
    story.append(Spacer(1, 6))
    story += section_header("ΤΟ ΠΡΩΤΟ 30ΗΜΕΡΟ", "Τι ανεβάζεις κάθε εβδομάδα",
                            "Η σειρά #1 «Μέρα 1 από 100» τρέχει κάθε μέρα. Γύρω της, 5 βίντεο την εβδομάδα από την παρακάτω λίστα.")
    week_cells = []
    for title, nums in TIKTOK_PLAN:
        inner = [Paragraph(f"<b>{title}</b>", style("wt", fontName="Sans-Bold", fontSize=9.5, leading=12,
                                                    textColor=colors.white))]
        inner += [Paragraph(f"<b>#{k}</b>&nbsp;&nbsp;{titles[k]}", S["cell"]) for k in nums]
        week_cells.append(inner)
    col_w = CONTENT_W / 2
    grid = []
    for r in range(0, len(week_cells), 2):
        pair = week_cells[r:r + 2]
        t_pair = []
        for inner in pair:
            t = Table([[p] for p in inner], colWidths=[col_w - 6])
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), INK), ("BACKGROUND", (0, 1), (-1, -1), LAV_SOFT),
                ("LEFTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4), ("TOPPADDING", (0, 0), (-1, 0), 6),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 6), ("BOX", (0, 0), (-1, -1), 0.6, INK),
            ]))
            t_pair.append(t)
        grid.append(t_pair)
    gt = Table(grid, colWidths=[col_w, col_w])
    gt.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                            ("RIGHTPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
    story.append(gt)

    # Part 2: other
    story.append(PageBreak())
    story += section_header("ΜΕΡΟΣ 2 · ΙΔΕΕΣ 51–100", "Δρόμος, πωλήσεις, PR & growth",
                            "Ό,τι δεν είναι TikTok: guerrilla μέσα και έξω από τα μαγαζιά, πωλήσεις κομάντο, "
                            "stunts για τα ΜΜΕ και μηχανισμοί που μεγαλώνουν το δίκτυο μόνοι τους.")
    blocks, _ = categories(OTHER, nxt, "Για ποιους")
    story += blocks

    # Red lines
    story.append(CondPageBreak(80 * mm))
    story.append(Spacer(1, 6))
    story += section_header("ΚΟΚΚΙΝΕΣ ΓΡΑΜΜΕΣ", "Επιθετικό, αλλά καθαρό",
                            "Όσο πιο επιθετική η ιδέα, τόσο πιο προσεκτική η εκτέλεση.")
    story.append(label_table(RED_LINES))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Δεν είναι νομική συμβουλή. Για συγκριτικές διαφημίσεις και δρώμενα σε δημόσιο χώρο, "
                           "ρώτα πρώτα δικηγόρο ή τον δήμο.", S["small"]))

    doc.build(story)
    print(f"-> {OUT}  {kinds}  cheap={cheap}")


if __name__ == "__main__":
    build()
