"""Builds anbit_guerrilla_playbook.pdf from content.py."""
from collections import Counter
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Frame, KeepTogether, NextPageTemplate,
                                PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle)

from content import CASES, IDEAS, KPIS, PLAN, RED_LINES, SOURCES

HERE = Path(__file__).parent
OUT = HERE / "anbit_guerrilla_playbook.pdf"

FONT_DIR = "/usr/share/fonts/truetype/liberation"
pdfmetrics.registerFont(TTFont("Sans", f"{FONT_DIR}/LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Bold", f"{FONT_DIR}/LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Italic", f"{FONT_DIR}/LiberationSans-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Sans-BoldItalic", f"{FONT_DIR}/LiberationSans-BoldItalic.ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-Bold", italic="Sans-Italic",
                              boldItalic="Sans-BoldItalic")

# Anbit flyer palette: lavender background, black cards, yellow highlights.
LAV = colors.HexColor("#D4C5F2")
LAV_SOFT = colors.HexColor("#F1ECFB")
LAV_DEEP = colors.HexColor("#6B55C7")
INK = colors.HexColor("#111013")
YEL = colors.HexColor("#FFD45E")
GREY = colors.HexColor("#5E5A6B")
LINE = colors.HexColor("#E3DDF2")

PAGE_W, PAGE_H = A4
MARGIN = 18 * mm
CONTENT_W = PAGE_W - 2 * MARGIN


def style(name, **kw):
    base = dict(fontName="Sans", fontSize=9.5, leading=13.5, textColor=INK)
    base.update(kw)
    return ParagraphStyle(name, **base)


S = {
    "h1": style("h1", fontName="Sans-Bold", fontSize=24, leading=28, spaceAfter=4),
    "h2": style("h2", fontName="Sans-Bold", fontSize=15, leading=19, spaceBefore=4, spaceAfter=2),
    "lead": style("lead", fontSize=11, leading=16, textColor=GREY, spaceAfter=10),
    "body": style("body", spaceAfter=6),
    "small": style("small", fontSize=8.5, leading=11.5, textColor=GREY),
    "kicker": style("kicker", fontName="Sans-Bold", fontSize=8.5, leading=11, textColor=LAV_DEEP),
    "card_title": style("card_title", fontName="Sans-Bold", fontSize=11.5, leading=14, textColor=colors.white),
    "card_meta": style("card_meta", fontName="Sans-Bold", fontSize=8.5, leading=11, textColor=YEL),
    "label": style("label", fontName="Sans-Bold", fontSize=8, leading=11, textColor=LAV_DEEP),
    "cell": style("cell", fontSize=8.8, leading=12),
    "cell_b": style("cell_b", fontName="Sans-Bold", fontSize=9.2, leading=12),
    "num": style("num", fontName="Sans-Bold", fontSize=9.5, leading=12, alignment=TA_CENTER),
    "tag": style("tag", fontName="Sans-Bold", fontSize=7.8, leading=10, alignment=TA_CENTER),
    "th": style("th", fontName="Sans-Bold", fontSize=8, leading=10, textColor=colors.white),
    "quote": style("quote", fontName="Sans-Bold", fontSize=13, leading=18, textColor=colors.white),
}


# ---------- page decorations ----------
def draw_cover(c, doc):
    c.saveState()
    c.setFillColor(LAV)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

    c.setFillColor(INK)
    c.setFont("Sans-Bold", 22)
    c.drawString(MARGIN, PAGE_H - 30 * mm, "Anbit")

    # yellow pill
    pill = "ΜΙΚΡΟ BUDGET · ΜΕΓΑΛΟΣ ΘΟΡΥΒΟΣ"
    c.setFont("Sans-Bold", 9)
    w = c.stringWidth(pill, "Sans-Bold", 9) + 14
    c.setFillColor(YEL)
    c.roundRect(MARGIN, PAGE_H - 62 * mm, w, 7.5 * mm, 3.7 * mm, stroke=0, fill=1)
    c.setFillColor(INK)
    c.drawString(MARGIN + 7, PAGE_H - 62 * mm + 2.6 * mm, pill)

    c.setFont("Sans-Bold", 44)
    for i, line in enumerate(["Guerrilla", "Marketing", "Playbook"]):
        c.drawString(MARGIN, PAGE_H - (82 + i * 17) * mm, line)

    c.setFont("Sans", 13)
    c.setFillColor(GREY)
    sub = ["Οι 20 πιο έξυπνες guerrilla καμπάνιες που απογείωσαν brands στα social,",
           "και 100 νέες ιδέες με μικρό budget για να εκτοξεύσουν την Anbit",
           "σε Αθήνα, Θεσσαλονίκη και όλη την Ελλάδα."]
    for i, line in enumerate(sub):
        c.drawString(MARGIN, PAGE_H - (140 + i * 7) * mm, line)

    # black quote card
    box_h = 46 * mm
    c.setFillColor(INK)
    c.roundRect(MARGIN, 32 * mm, CONTENT_W, box_h, 6 * mm, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Sans-Bold", 15)
    c.drawString(MARGIN + 10 * mm, 32 * mm + box_h - 15 * mm, "Ο πελάτης δεν φεύγει επειδή δεν του άρεσε.")
    c.drawString(MARGIN + 10 * mm, 32 * mm + box_h - 23 * mm, "Φεύγει επειδή δεν είχε λόγο να γυρίσει.")
    c.setFillColor(YEL)
    c.drawString(MARGIN + 10 * mm, 32 * mm + box_h - 35 * mm, "Αυτός ο οδηγός είναι για να του δώσουμε τον λόγο.")

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
    c.drawString(MARGIN, PAGE_H - 4.8 * mm, "Anbit · Guerrilla Marketing Playbook")
    c.setFont("Sans", 8)
    c.setFillColor(GREY)
    c.drawRightString(PAGE_W - MARGIN, 10 * mm, f"{doc.page}")
    c.restoreState()


# ---------- building blocks ----------
def pill(text, bg=YEL, fg=INK):
    t = Table([[Paragraph(text, style("p", fontName="Sans-Bold", fontSize=8, leading=10, textColor=fg))]])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("ROUNDEDCORNERS", [4, 4, 4, 4]),
        ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
    ]))
    t.hAlign = "LEFT"
    return t


def section_header(kicker, title, lead=None):
    parts = [pill(kicker), Spacer(1, 6), Paragraph(title, S["h1"])]
    if lead:
        parts.append(Paragraph(lead, S["lead"]))
    return parts


def case_card(i, case):
    """Black title bar on top of a label/text body table."""
    title, meta, did, result, lesson = case
    head = Table([[Paragraph(f"{i:02d}  ·  {title}", S["card_title"]),
                   Paragraph(meta, style("m", fontName="Sans-Bold", fontSize=8.5, leading=14,
                                         textColor=YEL, alignment=2))]],
                 colWidths=[CONTENT_W * 0.70, CONTENT_W * 0.30])
    head.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), INK),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("ROUNDEDCORNERS", [6, 6, 0, 0]),
    ]))
    label_w = 27 * mm
    body = Table([
        [Paragraph("ΤΙ ΕΚΑΝΑΝ", S["label"]), Paragraph(did, S["cell"])],
        [Paragraph("ΑΠΟΤΕΛΕΣΜΑ", S["label"]), Paragraph(result, S["cell"])],
        [Paragraph("ΓΙΑ ΤΗΝ ANBIT", style("l2", fontName="Sans-Bold", fontSize=8, leading=11, textColor=INK)),
         Paragraph(f"<b>{lesson}</b>", S["cell"])],
    ], colWidths=[label_w, CONTENT_W - label_w])
    body.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 2), (-1, 2), YEL),
        ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, LINE),
        ("BOX", (0, 0), (-1, -1), 0.6, INK),
        ("ROUNDEDCORNERS", [0, 0, 6, 6]),
    ]))
    return KeepTogether([head, body, Spacer(1, 9)])


def type_tag(kind):
    if kind == "Επιθετικό":
        return Paragraph(kind, style("ta", fontName="Sans-Bold", fontSize=7.8, leading=10,
                                     alignment=TA_CENTER, textColor=YEL))
    return Paragraph(kind, S["tag"])


def ideas_table(start_no, ideas, col4="Για ποιους"):
    widths = [10 * mm, CONTENT_W - 10 * mm - 15 * mm - 22 * mm - 21 * mm, 15 * mm, 22 * mm, 21 * mm]
    rows = [[Paragraph("#", S["th"]), Paragraph("Ιδέα", S["th"]), Paragraph("Κόστος", S["th"]),
             Paragraph(col4, S["th"]), Paragraph("Τύπος", S["th"])]]
    st = [
        ("BACKGROUND", (0, 0), (-1, 0), INK),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("VALIGN", (0, 0), (-1, 0), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (0, -1), 1), ("RIGHTPADDING", (0, 0), (0, -1), 1),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 1), (-1, -1), 0.5, LINE),
        ("BOX", (0, 0), (-1, -1), 0.6, INK),
    ]
    for k, (title, desc, budget, who, kind) in enumerate(ideas):
        r = k + 1
        n = start_no + k
        rows.append([
            Paragraph(str(n), S["num"]),
            Paragraph(f"<b>{title}</b><br/>{desc}", S["cell"]),
            Paragraph(budget, S["num"]),
            Paragraph(who, style("w", fontSize=8.3, leading=11)),
            type_tag(kind),
        ])
        if kind == "Επιθετικό":
            st.append(("BACKGROUND", (4, r), (4, r), INK))
        else:
            st.append(("BACKGROUND", (4, r), (4, r), LAV))
        st.append(("BACKGROUND", (0, r), (0, r), YEL))
        if r % 2 == 0:
            st.append(("BACKGROUND", (1, r), (3, r), LAV_SOFT))
    t = Table(rows, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle(st))
    return t


def bullet_list(items, st=None):
    st = st or S["body"]
    return [Paragraph(f"<font color='#6B55C7'><b>→</b></font>&nbsp;&nbsp;{it}", st) for it in items]


# ---------- story ----------
def build():
    doc = BaseDocTemplate(str(OUT), pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
                          topMargin=16 * mm, bottomMargin=18 * mm,
                          title="Anbit – Guerrilla Marketing Playbook", author="Anbit",
                          subject="Guerrilla marketing: 20 καμπάνιες και 100 ιδέες για την Anbit")
    frame = Frame(MARGIN, 18 * mm, CONTENT_W, PAGE_H - 34 * mm, id="f", leftPadding=0, rightPadding=0,
                  topPadding=0, bottomPadding=0)
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[frame], onPage=draw_cover),
        PageTemplate(id="page", frames=[frame], onPage=draw_page),
    ])

    all_ideas = [idea for _, _, ideas in IDEAS for idea in ideas]
    assert len(all_ideas) == 100, len(all_ideas)
    kinds = Counter(i[4] for i in all_ideas)
    budgets = Counter(i[2] for i in all_ideas)
    titles = {n: idea[0] for n, idea in enumerate(all_ideas, start=1)}

    story = [NextPageTemplate("page"), PageBreak()]

    # --- How to use ---
    story += section_header("ΠΩΣ ΝΑ ΤΟ ΔΙΑΒΑΣΕΙΣ", "Πριν ξεκινήσεις",
                            "Guerrilla marketing σημαίνει: λίγα χρήματα, μία απλή και απρόσμενη ιδέα, "
                            "και κάτι που ο κόσμος θέλει να φωτογραφίσει, να συζητήσει και να μοιραστεί.")
    story.append(Paragraph(
        "Η Anbit πουλάει σε <b>δύο κοινά ταυτόχρονα</b>: στα <b>μαγαζιά</b>, που πληρώνουν "
        "(1ος μήνας 0€, μετά Café 29€ ή Resto 49€ τον μήνα), και στους <b>πελάτες</b>, που πρέπει να σκανάρουν και να ξαναγυρίσουν. "
        "Κάθε ιδέα σε αυτόν τον οδηγό στοχεύει στο ένα ή και στα δύο κοινά.", S["body"]))
    story.append(Spacer(1, 6))

    legend = Table([
        [Paragraph("<b>Μέρος 1</b>", S["cell"]),
         Paragraph("20 καμπάνιες που άλλαξαν τα δεδομένα: τι έκαναν, τι πέτυχαν και τι μπορεί να πάρει η Anbit από αυτές.", S["cell"])],
        [Paragraph("<b>Μέρος 2</b>", S["cell"]),
         Paragraph("100 νέες ιδέες σε 8 κατηγορίες, με κόστος, κοινό και τύπο για την καθεμία.", S["cell"])],
        [Paragraph("<b>Μέρος 3</b>", S["cell"]),
         Paragraph("Πλάνο 90 ημερών: ποιες ιδέες να κάνεις πρώτες και τι να μετράς.", S["cell"])],
        [Paragraph("<b>Μέρος 4</b>", S["cell"]),
         Paragraph("Κόκκινες γραμμές: πώς κάνεις επιθετικό marketing χωρίς πρόστιμα και χωρίς να χαλάσεις το όνομά σου.", S["cell"])],
    ], colWidths=[24 * mm, CONTENT_W - 24 * mm])
    legend.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -2), 0.5, LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ]))
    story += [legend, Spacer(1, 14)]

    story.append(Paragraph("Τα σύμβολα στις 100 ιδέες", S["h2"]))
    sym = Table([
        [Paragraph("<b>€</b>", S["num"]), Paragraph("έως 50€", S["cell"]),
         Paragraph("<b>€€</b>", S["num"]), Paragraph("50–300€", S["cell"]),
         Paragraph("<b>€€€</b>", S["num"]), Paragraph("300–1.000€", S["cell"])],
        [type_tag("Κανονικό"), Paragraph("Ασφαλές, χτίζει brand σταθερά.", S["cell"]),
         type_tag("Επιθετικό"), Paragraph("Προκαλεί, συγκρίνει, κάνει θόρυβο. Νόμιμο, αλλά θέλει προσοχή.", S["cell"]),
         Paragraph("", S["cell"]), Paragraph("", S["cell"])],
    ], colWidths=[18 * mm, 30 * mm, 22 * mm, 52 * mm, 16 * mm, CONTENT_W - 138 * mm])
    sym.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BACKGROUND", (0, 0), (0, 0), YEL), ("BACKGROUND", (2, 0), (2, 0), YEL), ("BACKGROUND", (4, 0), (4, 0), YEL),
        ("BACKGROUND", (0, 1), (0, 1), LAV), ("BACKGROUND", (2, 1), (2, 1), INK),
        ("SPAN", (3, 1), (5, 1)),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story += [sym, Spacer(1, 14)]

    stats = Table([[
        Paragraph(f"<font size=22><b>100</b></font><br/>ιδέες", style("s1", alignment=TA_CENTER, leading=16)),
        Paragraph(f"<font size=22><b>{kinds['Κανονικό']}</b></font><br/>κανονικές", style("s2", alignment=TA_CENTER, leading=16)),
        Paragraph(f"<font size=22><b>{kinds['Επιθετικό']}</b></font><br/>επιθετικές",
                  style("s3", alignment=TA_CENTER, leading=16, textColor=YEL)),
        Paragraph(f"<font size=22><b>{budgets['€']}</b></font><br/>κοστίζουν έως 50€", style("s4", alignment=TA_CENTER, leading=16)),
    ]], colWidths=[CONTENT_W / 4] * 4)
    stats.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (1, 0), LAV), ("BACKGROUND", (2, 0), (2, 0), INK), ("BACKGROUND", (3, 0), (3, 0), YEL),
        ("TOPPADDING", (0, 0), (-1, -1), 12), ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LINEAFTER", (0, 0), (2, 0), 2, colors.white),
    ]))
    story.append(stats)

    # --- Part 1 ---
    story.append(PageBreak())
    story += section_header("ΜΕΡΟΣ 1", "Οι 20 πιο έξυπνες guerrilla καμπάνιες",
                            "Κοινό τους χαρακτηριστικό: σχεδόν μηδενικό κόστος σε διαφήμιση, μία ιδέα που χωράει σε μία πρόταση, "
                            "και η διάδοση έγινε από τον ίδιο τον κόσμο στα social. Τα νούμερα είναι όπως τα δημοσίευσαν "
                            "οι εταιρείες και τα επαγγελματικά μέσα (πηγές στο τέλος).")
    for i, case in enumerate(CASES, start=1):
        story.append(case_card(i, case))

    # --- Part 2 ---
    story.append(CondPageBreak(140 * mm))
    story.append(Spacer(1, 12))
    story += section_header("ΜΕΡΟΣ 2", "100 ιδέες για να εκτοξεύσεις την Anbit",
                            "Όλες είναι σχεδιασμένες για μικρό budget και για τις γειτονιές της Αθήνας και της Θεσσαλονίκης, "
                            "αλλά δουλεύουν σε κάθε ελληνική πόλη. Τα νούμερα των ιδεών αντιστοιχούν σε όσα αναφέρονται στο Μέρος 1 και στο πλάνο 90 ημερών.")
    n = 1
    for c_idx, (cat, sub, ideas) in enumerate(IDEAS, start=1):
        block = [CondPageBreak(60 * mm), Spacer(1, 4),
                 Paragraph(f"ΚΑΤΗΓΟΡΙΑ {c_idx} · ΙΔΕΕΣ {n}–{n + len(ideas) - 1}", S["kicker"]),
                 Paragraph(cat, S["h2"]), Paragraph(sub, S["small"]), Spacer(1, 6),
                 ideas_table(n, ideas), Spacer(1, 14)]
        story += block
        n += len(ideas)

    # --- Part 3 ---
    story.append(PageBreak())
    story += section_header("ΜΕΡΟΣ 3", "Πλάνο 90 ημερών",
                            "Μην τα κάνεις όλα μαζί. Ξεκίνα από ιδέες που φέρνουν συνεργάτες, μετά φέρε κίνηση στα μαγαζιά τους, "
                            "και μόνο τότε κάνε θόρυβο. Ο θόρυβος χωρίς μαγαζιά στον χάρτη πάει χαμένος.")
    for title, budget, goal, nums in PLAN:
        head = Table([[Paragraph(title, S["card_title"]),
                       Paragraph(f"Budget {budget}", style("b", fontName="Sans-Bold", fontSize=9, leading=14,
                                                            textColor=YEL, alignment=2))]],
                     colWidths=[CONTENT_W * 0.7, CONTENT_W * 0.3])
        head.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), INK), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9),
            ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("ROUNDEDCORNERS", [6, 6, 0, 0]),
        ]))
        items = [Paragraph(f"<i>{goal}</i>", S["cell"])]
        items += [Paragraph(f"<b>#{k}</b>&nbsp;&nbsp;{titles[k]}", S["cell"]) for k in nums]
        body = Table([[it] for it in items], colWidths=[CONTENT_W])
        body.setStyle(TableStyle([
            ("BOX", (0, 0), (-1, -1), 0.6, INK), ("BACKGROUND", (0, 0), (-1, 0), LAV_SOFT),
            ("LEFTPADDING", (0, 0), (-1, -1), 9), ("TOPPADDING", (0, 0), (-1, -1), 3.5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5), ("TOPPADDING", (0, 0), (-1, 0), 6),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 6), ("ROUNDEDCORNERS", [0, 0, 6, 6]),
        ]))
        story.append(KeepTogether([head, body, Spacer(1, 10)]))

    story.append(Paragraph("Τι να μετράς κάθε εβδομάδα", S["h2"]))
    story += bullet_list(KPIS)

    # --- Part 4 ---
    story.append(CondPageBreak(90 * mm))
    story.append(Spacer(1, 10))
    story += section_header("ΜΕΡΟΣ 4", "Κόκκινες γραμμές",
                            "Επιθετικό δεν σημαίνει παράνομο. Ένα πρόστιμο ή ένα σκάνδαλο κοστίζει περισσότερο από όσο φέρνει "
                            "οποιαδήποτε καμπάνια.")
    rl = Table([[Paragraph(f"<b>{t}</b>", S["cell"]), Paragraph(d, S["cell"])] for t, d in RED_LINES],
               colWidths=[42 * mm, CONTENT_W - 42 * mm])
    rl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (0, -1), YEL),
        ("LINEBELOW", (0, 0), (-1, -2), 0.5, LINE),
        ("BOX", (0, 0), (-1, -1), 0.6, INK),
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.append(rl)
    story.append(Spacer(1, 8))
    story.append(Paragraph("Δεν είναι νομική συμβουλή. Για συγκριτικές διαφημίσεις και δρώμενα σε δημόσιο χώρο, "
                           "ρώτα πρώτα δικηγόρο ή τον δήμο.", S["small"]))

    # --- Sources ---
    story.append(CondPageBreak(60 * mm))
    story.append(Spacer(1, 14))
    story.append(Paragraph("Πηγές για τα νούμερα του Μέρους 1", S["h2"]))
    story.append(Paragraph("Τα αποτελέσματα των καμπανιών είναι κυρίως νούμερα που δημοσίευσαν οι ίδιες οι εταιρείες "
                           "και τα γραφεία τους, και όπου οι πηγές διαφωνούν αναφέρεται το πιο συντηρητικό νούμερο. "
                           "Για τις υπόλοιπες καμπάνιες τα στοιχεία είναι ευρέως γνωστά στον κλάδο.", S["small"]))
    story.append(Spacer(1, 4))
    for name, src in SOURCES:
        story.append(Paragraph(f"<b>{name}:</b> {src}", S["small"]))

    doc.build(story)
    print(f"-> {OUT}  ({kinds}, {budgets})")


if __name__ == "__main__":
    build()
