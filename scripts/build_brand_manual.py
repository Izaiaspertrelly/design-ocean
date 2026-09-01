from pathlib import Path
import math
import textwrap

from PIL import Image, ImageOps
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "manual" / "Manual-da-Marca-Ocean-Health.pdf"
TMP = ROOT / "tmp" / "pdfs"
TMP.mkdir(parents=True, exist_ok=True)

W, H = landscape(A4)

OCEAN = HexColor("#4800EF")
DEEP = HexColor("#200077")
CURRENT = HexColor("#00DBF9")
SKY = HexColor("#EFFBFF")
INK = HexColor("#15192D")
MUTED = HexColor("#484F64")
LINE = HexColor("#D4DAEC")
WHITE = HexColor("#FFFFFF")
SUCCESS = HexColor("#008745")

FONT_DIR = ROOT / "assets" / "fonts"
pdfmetrics.registerFont(TTFont("Gabarito", str(FONT_DIR / "Gabarito-Bold.ttf")))
pdfmetrics.registerFont(TTFont("GabaritoX", str(FONT_DIR / "Gabarito-ExtraBold.ttf")))
pdfmetrics.registerFont(TTFont("Albert", str(FONT_DIR / "AlbertSans-Regular.ttf")))
pdfmetrics.registerFont(TTFont("AlbertSemi", str(FONT_DIR / "AlbertSans-SemiBold.ttf")))
pdfmetrics.registerFont(TTFont("AlbertBold", str(FONT_DIR / "AlbertSans-Bold.ttf")))

LOGO_PRIMARY = ROOT / "assets" / "logos" / "ocean-health-primary.png"
LOGO_WHITE = ROOT / "assets" / "logos" / "ocean-health-white.png"
IMG_HERO = ROOT / "assets" / "photography" / "familia-hero.png"
IMG_HUMAN = ROOT / "assets" / "photography" / "pessoas-cuidado.png"
IMG_BUSINESS = ROOT / "assets" / "photography" / "equipe-empresas.png"
IMG_INST = ROOT / "assets" / "photography" / "institucional-ocean.png"
IMG_LOGIN = ROOT / "assets" / "photography" / "familia-login.png"
IMG_APP = ROOT / "assets" / "app" / "ocean-app-cutout.png"


def safe_alpha(c, fill=None, stroke=None):
    if fill is not None and hasattr(c, "setFillAlpha"):
        c.setFillAlpha(fill)
    if stroke is not None and hasattr(c, "setStrokeAlpha"):
        c.setStrokeAlpha(stroke)


def reset_alpha(c):
    safe_alpha(c, 1, 1)


def crop_image(path, width, height, focus=(0.5, 0.5)):
    key = f"{Path(path).stem}-{int(width)}x{int(height)}-{int(focus[0]*100)}-{int(focus[1]*100)}.jpg"
    target = TMP / key
    if not target.exists():
        with Image.open(path) as im:
            im = im.convert("RGB")
            out = ImageOps.fit(
                im,
                (max(2, int(width * 2)), max(2, int(height * 2))),
                method=Image.Resampling.LANCZOS,
                centering=focus,
            )
            out.save(target, quality=91, optimize=True)
    return target


def image_cover(c, path, x, y, w, h, focus=(0.5, 0.5), radius=0):
    img = crop_image(path, w, h, focus)
    c.saveState()
    if radius:
        p = c.beginPath()
        p.roundRect(x, y, w, h, radius)
        c.clipPath(p, stroke=0, fill=0)
    c.drawImage(str(img), x, y, w, h, preserveAspectRatio=False, mask="auto")
    c.restoreState()


def image_contain(c, path, x, y, w, h):
    with Image.open(path) as im:
        iw, ih = im.size
    scale = min(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    c.drawImage(str(path), x + (w - dw) / 2, y + (h - dh) / 2, dw, dh, preserveAspectRatio=True, mask="auto")


def wrapped_lines(text, font, size, max_width):
    words = text.split()
    lines, current = [], ""
    for word in words:
        test = word if not current else f"{current} {word}"
        if pdfmetrics.stringWidth(test, font, size) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def paragraph(c, text, x, y, w, size=11, leading=None, color=MUTED, font="Albert", max_lines=None):
    if leading is None:
        leading = size * 1.42
    c.setFont(font, size)
    c.setFillColor(color)
    lines = []
    for block in text.split("\n"):
        if not block:
            lines.append("")
        else:
            lines.extend(wrapped_lines(block, font, size, w))
    if max_lines:
        lines = lines[:max_lines]
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def title(c, text, x, y, w, size=42, color=INK, font="GabaritoX", leading=None):
    if leading is None:
        leading = size * 0.98
    c.setFont(font, size)
    c.setFillColor(color)
    for line in wrapped_lines(text, font, size, w):
        c.drawString(x, y, line)
        y -= leading
    return y


def label(c, text, x, y, color=OCEAN):
    c.setFont("AlbertBold", 9)
    c.setFillColor(color)
    c.drawString(x, y, text.upper())


def current_stroke(c, x, y, w, h, color=CURRENT, width=14, rotate=0):
    c.saveState()
    c.translate(x + w / 2, y + h / 2)
    c.rotate(rotate)
    c.translate(-w / 2, -h / 2)
    p = c.beginPath()
    p.moveTo(0.02 * w, 0.57 * h)
    p.curveTo(0.18 * w, 0.12 * h, 0.38 * w, 0.09 * h, 0.55 * w, 0.42 * h)
    p.curveTo(0.68 * w, 0.69 * h, 0.78 * w, 0.72 * h, 0.86 * w, 0.41 * h)
    p.curveTo(0.92 * w, 0.17 * h, 0.91 * w, 0.07 * h, 0.86 * w, 0.18 * h)
    p.curveTo(0.80 * w, 0.31 * h, 0.82 * w, 0.66 * h, 0.90 * w, 0.76 * h)
    p.curveTo(0.94 * w, 0.82 * h, 0.97 * w, 0.66 * h, 0.99 * w, 0.53 * h)
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.setLineCap(1)
    c.setLineJoin(1)
    c.drawPath(p, stroke=1, fill=0)
    c.restoreState()


def card(c, x, y, w, h, fill=WHITE, radius=14, stroke=None):
    c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke)
        c.roundRect(x, y, w, h, radius, fill=1, stroke=1)
    else:
        c.roundRect(x, y, w, h, radius, fill=1, stroke=0)


def page_number(c, n, section, dark=False):
    color = Color(1, 1, 1, alpha=0.55) if dark else MUTED
    c.setFillColor(color)
    c.setFont("AlbertSemi", 8)
    c.drawString(42, 24, f"OCEAN HEALTH  /  {section.upper()}")
    c.drawRightString(W - 42, 24, f"{n:02d}")


def logo(c, path, x, y, w):
    with Image.open(path) as im:
        iw, ih = im.size
    h = w * ih / iw
    c.drawImage(str(path), x, y, w, h, preserveAspectRatio=True, mask="auto")
    return h


def rule(c, x, y, w, color=LINE, width=1):
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(x, y, x + w, y)


def bullet(c, text, x, y, w, accent=CURRENT, color=INK, size=10.5):
    c.setFillColor(accent)
    c.circle(x + 4, y + 3, 3, fill=1, stroke=0)
    return paragraph(c, text, x + 18, y + 7, w - 18, size=size, leading=size * 1.35, color=color)


def new_page(c, bg=WHITE):
    c.setFillColor(bg)
    c.rect(0, 0, W, H, fill=1, stroke=0)


def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=(W, H), pageCompression=1)
    c.setTitle("Manual da Marca Ocean Health")
    c.setAuthor("Ocean Health")
    c.setSubject("Sistema de identidade visual e orientacoes para produção de marca")
    c.setKeywords("Ocean Health, manual de marca, identidade visual, brand guidelines")

    # 01 - Cover
    new_page(c, DEEP)
    image_cover(c, IMG_HERO, W * 0.49, 0, W * 0.51, H, focus=(0.66, 0.5))
    c.saveState()
    safe_alpha(c, fill=0.88)
    c.setFillColor(OCEAN)
    c.rect(W * 0.42, 0, W * 0.17, H, fill=1, stroke=0)
    reset_alpha(c)
    c.restoreState()
    c.setFillColor(DEEP)
    c.setStrokeColor(DEEP)
    p = c.beginPath()
    p.moveTo(W * 0.42, 0)
    p.lineTo(W * 0.58, 0)
    p.curveTo(W * 0.48, H * 0.25, W * 0.56, H * 0.76, W * 0.43, H)
    p.lineTo(0, H)
    p.lineTo(0, 0)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    logo(c, LOGO_WHITE, 52, H - 118, 205)
    label(c, "Sistema de identidade", 54, H - 174, CURRENT)
    title(c, "Manual da marca", 52, H - 218, W * 0.39, size=55, color=WHITE)
    paragraph(c, "Uma identidade humana, clara e conectada para transformar o cuidado em movimento.", 54, 132, 300, size=14, leading=20, color=WHITE)
    c.setFont("AlbertSemi", 9)
    c.setFillColor(CURRENT)
    c.drawString(54, 66, "VERSÃO 1.0  /  SETEMBRO 2026")
    current_stroke(c, 365, -22, 500, 130, width=17, rotate=-3)
    page_number(c, 1, "Capa", dark=True)
    c.showPage()

    # 02 - Essence
    new_page(c, WHITE)
    image_cover(c, IMG_HUMAN, 0, 0, W * 0.44, H, focus=(0.52, 0.42))
    current_stroke(c, -45, 7, 470, 110, width=16, rotate=2)
    label(c, "01 / Essência", W * 0.49, H - 72)
    y = title(c, "Cuidado que acompanha a vida.", W * 0.49, H - 120, W * 0.43, size=48, color=INK)
    y -= 18
    paragraph(c, "Ocean Health existe para reduzir a distância entre a pessoa e a saúde: menos labirinto, menos burocracia e mais clareza sobre o próximo passo.", W * 0.49, y, W * 0.42, size=13, leading=19, color=MUTED)
    card(c, W * 0.49, 84, W * 0.42, 132, SKY, 14)
    label(c, "Promessa", W * 0.52, 183)
    paragraph(c, "Transformar o acesso à saúde em uma experiência clara, próxima e confiável para pessoas, famílias e empresas.", W * 0.52, 154, W * 0.35, size=13, leading=18, color=INK)
    page_number(c, 2, "Essência")
    c.showPage()

    # 03 - Strategy
    new_page(c, DEEP)
    label(c, "02 / Plataforma de marca", 52, H - 64, CURRENT)
    title(c, "Humana. Clara. Conectada. Segura.", 52, H - 112, 730, size=47, color=WHITE)
    pillars = [
        ("01", "Humana", "Pessoas antes de funcionalidades, números ou protocolos."),
        ("02", "Clara", "Informação direta, escolhas comparáveis e próximo passo visível."),
        ("03", "Conectada", "Digital quando simplifica; atendimento humano quando importa."),
        ("04", "Segura", "Linguagem responsável, visual consistente e compromissos verificáveis."),
    ]
    x0, gap, cw = 52, 16, 173
    for i, (num, head, body) in enumerate(pillars):
        x = x0 + i * (cw + gap)
        card(c, x, 168, cw, 225, fill=Color(1, 1, 1, alpha=0.09), radius=10)
        c.setFont("AlbertBold", 10)
        c.setFillColor(CURRENT)
        c.drawString(x + 20, 360, num)
        c.setFont("Gabarito", 25)
        c.setFillColor(WHITE)
        c.drawString(x + 20, 306, head)
        paragraph(c, body, x + 20, 268, cw - 40, size=10.5, leading=15, color=Color(1, 1, 1, alpha=0.72))
    current_stroke(c, 470, 44, 410, 100, width=12, rotate=-2)
    page_number(c, 3, "Plataforma de marca", dark=True)
    c.showPage()

    # 04 - Voice
    new_page(c, SKY)
    label(c, "03 / Voz", 52, H - 64)
    title(c, "Próxima sem infantilizar. Clara sem simplificar demais.", 52, H - 108, 730, size=42, color=INK)
    cols = [
        ("SOMOS", ["Diretos", "Acolhedores", "Responsáveis", "Otimistas"]),
        ("FAZEMOS", ["Falamos com você", "Usamos voz ativa", "Explicamos uma ideia por vez", "Mostramos o próximo passo"]),
        ("EVITAMOS", ["Juridiquês", "Superlativos vazios", "Siglas sem contexto", "Promessas absolutas"]),
    ]
    x0, y0, cw = 52, 300, 226
    for i, (head, items) in enumerate(cols):
        x = x0 + i * 247
        c.setFont("AlbertBold", 9)
        c.setFillColor(OCEAN if i < 2 else MUTED)
        c.drawString(x, y0 + 84, head)
        rule(c, x, y0 + 68, cw, OCEAN if i < 2 else LINE, 2)
        yy = y0 + 42
        for item in items:
            yy = bullet(c, item, x, yy, cw, accent=CURRENT if i < 2 else LINE, color=INK)
            yy -= 9
    card(c, 52, 76, 352, 132, WHITE, 12)
    label(c, "Preferir", 76, 178, SUCCESS)
    paragraph(c, "“Encontre atendimento perto de você.”", 76, 146, 302, size=14, leading=19, color=INK, font="AlbertSemi")
    card(c, 432, 76, 358, 132, WHITE, 12)
    label(c, "Evitar", 456, 178, MUTED)
    paragraph(c, "“Consulte nossa ampla rede assistencial credenciada.”", 456, 146, 308, size=14, leading=19, color=INK, font="AlbertSemi")
    page_number(c, 4, "Voz")
    c.showPage()

    # 05 - Logo system
    new_page(c, WHITE)
    label(c, "04 / Logotipo", 52, H - 64)
    title(c, "Duas versões. Uma marca consistente.", 52, H - 106, 730, size=42)
    card(c, 52, 214, 350, 246, SKY, 14)
    logo(c, LOGO_PRIMARY, 96, 314, 260)
    label(c, "Primária / fundos claros", 82, 246)
    card(c, 430, 214, 360, 246, DEEP, 14)
    logo(c, LOGO_WHITE, 477, 314, 266)
    label(c, "Branca transparente / fundos escuros", 460, 246, CURRENT)
    rule(c, 52, 174, 738, LINE)
    c.setFont("Gabarito", 18)
    c.setFillColor(INK)
    c.drawString(52, 136, "Área de proteção")
    paragraph(c, "Preserve no mínimo 2x em todos os lados, onde x é a altura das letras de HEALTH.", 52, 109, 350, size=10.5, color=MUTED)
    c.setFont("Gabarito", 18)
    c.setFillColor(INK)
    c.drawString(430, 136, "Tamanho mínimo")
    paragraph(c, "Digital: 132 px de largura. Impressão: 32 mm. Sempre validar a leitura de HEALTH.", 430, 109, 350, size=10.5, color=MUTED)
    page_number(c, 5, "Logotipo")
    c.showPage()

    # 06 - Logo mistakes
    new_page(c, OCEAN)
    label(c, "05 / Proteção da marca", 52, H - 64, CURRENT)
    title(c, "O logo nunca precisa de uma caixa branca sobre o azul.", 52, H - 108, 720, size=43, color=WHITE)
    # Correct
    c.setFont("AlbertBold", 10)
    c.setFillColor(CURRENT)
    c.drawString(52, 384, "CORRETO")
    logo(c, LOGO_WHITE, 58, 270, 282)
    c.setFont("AlbertSemi", 11)
    c.setFillColor(WHITE)
    c.drawString(58, 234, "Logo branco com transparência real")
    # Incorrect mock backing
    c.setFont("AlbertBold", 10)
    c.setFillColor(WHITE)
    c.drawString(450, 384, "INCORRETO")
    card(c, 450, 263, 296, 102, WHITE, 7)
    logo(c, LOGO_PRIMARY, 480, 284, 236)
    c.setStrokeColor(CURRENT)
    c.setLineWidth(5)
    c.line(456, 356, 740, 270)
    c.line(740, 356, 456, 270)
    c.setFont("AlbertSemi", 11)
    c.setFillColor(WHITE)
    c.drawString(450, 234, "Não adicionar placa ou retângulo branco")
    items = ["Não distorcer", "Não recolorir", "Não aplicar sombra ou 3D", "Não usar screenshot", "Não invadir a área de proteção"]
    yy = 158
    for i, item in enumerate(items):
        x = 52 + (i % 3) * 248
        y = yy - (i // 3) * 50
        bullet(c, item, x, y, 220, accent=CURRENT, color=WHITE, size=10.5)
    page_number(c, 6, "Proteção da marca", dark=True)
    c.showPage()

    # 07 - Color
    new_page(c, WHITE)
    label(c, "06 / Cor", 52, H - 64)
    title(c, "Azul com coragem. Ciano com intenção.", 52, H - 108, 730, size=43)
    swatches = [
        ("OCEAN 700", "#4800EF", OCEAN, WHITE),
        ("OCEAN 900", "#200077", DEEP, WHITE),
        ("CURRENT", "#00DBF9", CURRENT, DEEP),
        ("SKY 050", "#EFFBFF", SKY, INK),
        ("INK", "#15192D", INK, WHITE),
        ("MUTED", "#484F64", MUTED, WHITE),
        ("LINE", "#D4DAEC", LINE, INK),
        ("WHITE", "#FFFFFF", WHITE, INK),
    ]
    sw, sh, gap = 174, 112, 10
    for i, (name, hx, fill, txt) in enumerate(swatches):
        col, row = i % 4, i // 4
        x = 52 + col * (sw + gap)
        y = 300 - row * (sh + 16)
        c.setFillColor(fill)
        c.setStrokeColor(LINE)
        c.roundRect(x, y, sw, sh, 10, fill=1, stroke=1 if fill == WHITE else 0)
        c.setFillColor(txt)
        c.setFont("AlbertBold", 9)
        c.drawString(x + 14, y + 26, name)
        c.setFont("Albert", 9)
        c.drawRightString(x + sw - 14, y + 26, hx)
    c.setFont("AlbertSemi", 11)
    c.setFillColor(INK)
    c.drawString(52, 100, "Proporção recomendada")
    c.setFillColor(OCEAN)
    c.roundRect(203, 86, 240, 25, 5, fill=1, stroke=0)
    c.setFillColor(DEEP)
    c.roundRect(443, 86, 120, 25, 0, fill=1, stroke=0)
    c.setFillColor(CURRENT)
    c.roundRect(563, 86, 62, 25, 0, fill=1, stroke=0)
    c.setFillColor(SKY)
    c.roundRect(625, 86, 165, 25, 5, fill=1, stroke=0)
    page_number(c, 7, "Cor")
    c.showPage()

    # 08 - Typography
    new_page(c, SKY)
    label(c, "07 / Tipografia", 52, H - 64)
    title(c, "Gabarito traz calor. Albert Sans traz clareza.", 52, H - 108, 730, size=42)
    c.setFillColor(OCEAN)
    c.setFont("GabaritoX", 72)
    c.drawString(52, 330, "Cuidar muda tudo.")
    c.setFont("Albert", 14)
    c.setFillColor(MUTED)
    c.drawString(54, 296, "Gabarito ExtraBold / títulos, números e manifestos")
    rule(c, 52, 266, 738, LINE)
    c.setFont("Albert", 25)
    c.setFillColor(INK)
    c.drawString(52, 216, "Saúde simples, humana e conectada.")
    c.setFont("Albert", 11)
    c.setFillColor(MUTED)
    c.drawString(54, 188, "Albert Sans Regular / corpo, interface, navegação e informação funcional")
    sizes = [("HERO", "72-96", 24), ("H2", "48-76", 20), ("H3", "24-38", 16), ("CORPO", "15-20", 12), ("UI", "13-16", 10)]
    x = 52
    for name, spec, fs in sizes:
        c.setFont("AlbertBold", 8)
        c.setFillColor(OCEAN)
        c.drawString(x, 118, name)
        c.setFont("Gabarito", fs)
        c.setFillColor(INK)
        c.drawString(x, 87, spec)
        x += 145
    page_number(c, 8, "Tipografia")
    c.showPage()

    # 09 - Current gesture
    new_page(c, DEEP)
    label(c, "08 / Corrente Ocean", 52, H - 64, CURRENT)
    title(c, "Um gesto contínuo, cursivo e assimétrico.", 52, H - 108, 720, size=44, color=WHITE)
    current_stroke(c, 35, 218, 770, 170, color=CURRENT, width=20, rotate=-1)
    paragraph(c, "A corrente leva o movimento do wordmark para a composição. Ela parece desenhada à mão, atravessa a cena e conduz o olhar. Nunca é um círculo geométrico perfeito.", 52, 182, 620, size=12, leading=18, color=Color(1, 1, 1, alpha=0.76))
    rules = ["Uma corrente dominante por peça", "Pontas e encontros arredondados", "Espessura de 1,2% a 2,2% da largura", "Nunca cruzar rosto, logo ou texto"]
    yy = 112
    for i, item in enumerate(rules):
        x = 52 + (i % 2) * 370
        y = yy - (i // 2) * 38
        bullet(c, item, x, y, 330, accent=CURRENT, color=WHITE, size=10)
    page_number(c, 9, "Corrente Ocean", dark=True)
    c.showPage()

    # 10 - Photography
    new_page(c, WHITE)
    label(c, "09 / Fotografia", 52, H - 64)
    title(c, "Pessoas antes de procedimentos.", 52, H - 108, 730, size=45)
    image_cover(c, IMG_HERO, 52, 190, 330, 260, focus=(0.70, 0.48), radius=12)
    image_cover(c, IMG_BUSINESS, 401, 190, 190, 260, focus=(0.48, 0.48), radius=12)
    image_cover(c, IMG_INST, 610, 190, 180, 260, focus=(0.62, 0.48), radius=12)
    current_stroke(c, 40, 142, 560, 88, width=11, rotate=1)
    good = "Luz natural, expressões autênticas, diversidade brasileira, figurino neutro e área negativa planejada."
    bad = "Evitar estetoscópio sem contexto, sorriso de banco de imagens, anatomia artificial, hologramas e filtro azul sobre pele."
    label(c, "Direção", 52, 112, SUCCESS)
    paragraph(c, good, 52, 89, 330, size=10.5, leading=15, color=INK)
    label(c, "Não usar", 430, 112, MUTED)
    paragraph(c, bad, 430, 89, 360, size=10.5, leading=15, color=INK)
    page_number(c, 10, "Fotografia")
    c.showPage()

    # 11 - Layout
    new_page(c, SKY)
    label(c, "10 / Layout", 52, H - 64)
    title(c, "Uma decisão por tela. Uma hierarquia que respira.", 52, H - 108, 730, size=42)
    # Abstract website composition
    card(c, 52, 130, 480, 300, WHITE, 12, stroke=LINE)
    c.setFillColor(OCEAN)
    c.roundRect(52, 130, 480, 300, 12, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.roundRect(76, 392, 100, 12, 5, fill=1, stroke=0)
    c.roundRect(76, 337, 245, 28, 5, fill=1, stroke=0)
    c.roundRect(76, 296, 195, 28, 5, fill=1, stroke=0)
    safe_alpha(c, fill=0.7)
    c.roundRect(76, 255, 220, 9, 4, fill=1, stroke=0)
    c.roundRect(76, 236, 180, 9, 4, fill=1, stroke=0)
    reset_alpha(c)
    c.setFillColor(WHITE)
    c.roundRect(76, 176, 130, 42, 10, fill=1, stroke=0)
    image_cover(c, IMG_HERO, 325, 130, 207, 300, focus=(0.70, 0.48), radius=0)
    current_stroke(c, 270, 120, 292, 74, width=9, rotate=-2)
    principles = [
        ("01", "Mensagem dominante", "Título, apoio e próximo passo sem competição."),
        ("02", "Cor como superfície", "Ocean ocupa áreas inteiras; Current indica movimento."),
        ("03", "Cards com função", "Usar somente para comparação, formulário ou tarefa."),
        ("04", "Grade consistente", "1280 px, 12 colunas, base de 8 px e margens generosas."),
    ]
    yy = 392
    for num, head, body in principles:
        c.setFont("AlbertBold", 8)
        c.setFillColor(CURRENT)
        c.drawString(574, yy, num)
        c.setFont("Gabarito", 16)
        c.setFillColor(INK)
        c.drawString(607, yy - 2, head)
        paragraph(c, body, 607, yy - 23, 180, size=8.5, leading=12, color=MUTED)
        yy -= 72
    page_number(c, 11, "Layout")
    c.showPage()

    # 12 - Digital
    new_page(c, DEEP)
    label(c, "11 / Produto digital", 52, H - 64, CURRENT)
    title(c, "Resolver a saúde. Continuar a vida.", 52, H - 108, 450, size=43, color=WHITE)
    paragraph(c, "O portal e o aplicativo devem parecer completos, confiáveis e diretos. A interface existe para resolver tarefas, não para exibir tecnologia.", 52, 398, 355, size=12, leading=18, color=Color(1, 1, 1, alpha=0.73))
    tasks = ["Carteirinha digital", "Consultas", "Rede credenciada", "Telemedicina", "Reembolso"]
    yy = 316
    for t in tasks:
        yy = bullet(c, t, 52, yy, 300, accent=CURRENT, color=WHITE, size=10.5)
        yy -= 10
    c.saveState()
    safe_alpha(c, fill=0.08)
    c.setFillColor(CURRENT)
    c.circle(646, 286, 245, fill=1, stroke=0)
    reset_alpha(c)
    c.restoreState()
    image_contain(c, IMG_APP, 410, 36, 410, 520)
    c.setFont("AlbertSemi", 9)
    c.setFillColor(CURRENT)
    c.drawString(52, 72, "APARELHO INTEIRO  /  FUNDO TRANSPARENTE  /  SEM HALO  /  DADOS FICTÍCIOS")
    page_number(c, 12, "Produto digital", dark=True)
    c.showPage()

    # 13 - Applications
    new_page(c, WHITE)
    label(c, "12 / Aplicações", 52, H - 64)
    title(c, "A identidade muda de escala, não de comportamento.", 52, H - 108, 730, size=42)
    cards = [
        (52, "Papelaria", "Branco, logo primário, verso Ocean e corrente atravessando bordas."),
        (300, "Apresentações", "Uma conclusão por slide, títulos grandes e dados verificáveis."),
        (548, "Ambientes", "Logo branco aplicado diretamente em parede Ocean, sem placa branca."),
    ]
    for x, head, body in cards:
        card(c, x, 162, 222, 278, SKY, 12)
        c.setFillColor(DEEP)
        c.roundRect(x + 20, 320, 182, 86, 8, fill=1, stroke=0)
        logo(c, LOGO_WHITE, x + 45, 342, 132)
        current_stroke(c, x + 8, 276, 210, 65, width=7, rotate=-2)
        c.setFont("Gabarito", 21)
        c.setFillColor(INK)
        c.drawString(x + 20, 244, head)
        paragraph(c, body, x + 20, 216, 180, size=9.5, leading=14, color=MUTED)
    paragraph(c, "Mockup demonstra contexto. O arquivo de produção deve ser entregue separadamente, com medidas, sangria, cores e acabamento.", 52, 108, 738, size=11, leading=16, color=INK, font="AlbertSemi")
    page_number(c, 13, "Aplicações")
    c.showPage()

    # 14 - Accessibility and responsibility
    new_page(c, SKY)
    label(c, "13 / Acessibilidade e responsabilidade", 52, H - 64)
    title(c, "Clareza também é cuidado.", 52, H - 108, 730, size=46)
    blocks = [
        ("4.5:1", "Contraste mínimo para texto normal", OCEAN),
        ("44 px", "Alvo mínimo de toque", DEEP),
        ("AA", "Meta WCAG 2.2", CURRENT),
    ]
    for i, (big, body, fill) in enumerate(blocks):
        x = 52 + i * 247
        card(c, x, 280, 226, 150, fill, 12)
        c.setFillColor(WHITE if fill != CURRENT else DEEP)
        c.setFont("GabaritoX", 38)
        c.drawString(x + 22, 354, big)
        paragraph(c, body, x + 22, 322, 182, size=9.5, leading=13, color=WHITE if fill != CURRENT else DEEP)
    checks = [
        "Foco visível e navegação por teclado",
        "Texto alternativo que descreve a cena",
        "Movimento reduzido quando solicitado",
        "Não depender somente de cor para estado",
        "Validar preço, rede, carência, cobertura e ANS",
        "Usar apenas dados fictícios em protótipos",
    ]
    yy = 222
    for i, item in enumerate(checks):
        x = 52 + (i % 2) * 370
        y = yy - (i // 2) * 44
        bullet(c, item, x, y, 330, accent=CURRENT, color=INK, size=10)
    page_number(c, 14, "Acessibilidade")
    c.showPage()

    # 15 - Agent workflow
    new_page(c, WHITE)
    label(c, "14 / Agente de design", 52, H - 64)
    title(c, "Do briefing à entrega, sem perder a marca.", 52, H - 108, 730, size=43)
    steps = [
        ("01", "Entender", "Objetivo, público, canal, mensagem e restrições."),
        ("02", "Direcionar", "Escrever a ideia visual em uma frase."),
        ("03", "Selecionar", "Logo, foto, corrente e tokens oficiais."),
        ("04", "Compor", "Hierarquia primeiro; cor e gesto com intenção."),
        ("05", "Validar", "Checklist binário, contraste e conformidade."),
        ("06", "Entregar", "Editável, exportações, fontes e relatório."),
    ]
    for i, (num, head, body) in enumerate(steps):
        col, row = i % 3, i // 3
        x = 52 + col * 247
        y = 276 - row * 150
        c.setFont("AlbertBold", 9)
        c.setFillColor(CURRENT)
        c.drawString(x, y + 118, num)
        rule(c, x, y + 104, 220, LINE)
        c.setFont("Gabarito", 22)
        c.setFillColor(INK)
        c.drawString(x, y + 70, head)
        paragraph(c, body, x, y + 42, 215, size=9.5, leading=14, color=MUTED)
    c.setFillColor(OCEAN)
    c.roundRect(52, 69, 738, 44, 10, fill=1, stroke=0)
    c.setFont("AlbertBold", 10)
    c.setFillColor(WHITE)
    c.drawCentredString(W / 2, 86, "Se não parece inequivocamente Ocean Health, ainda não está pronto.")
    page_number(c, 15, "Agente de design")
    c.showPage()

    # 16 - Closing checklist
    new_page(c, OCEAN)
    logo(c, LOGO_WHITE, 52, H - 112, 188)
    label(c, "Checklist essencial", 52, H - 170, CURRENT)
    title(c, "Antes de publicar, confirme.", 52, H - 212, 650, size=47, color=WHITE)
    checklist = [
        "Logo correto e com transparência real",
        "Corrente cursiva, assimétrica e intencional",
        "Fotografia humana e corte seguro",
        "Mensagem dominante e próximo passo claro",
        "Contraste, tipografia e tamanhos acessíveis",
        "Informações comerciais e regulatórias validadas",
        "Editável, exportações e fontes organizados",
    ]
    yy = 306
    for i, item in enumerate(checklist):
        x = 52 + (i % 2) * 372
        y = yy - (i // 2) * 50
        c.setStrokeColor(CURRENT)
        c.setLineWidth(2)
        c.roundRect(x, y - 3, 14, 14, 3, fill=0, stroke=1)
        paragraph(c, item, x + 26, y + 8, 315, size=10.5, leading=15, color=WHITE)
    current_stroke(c, 430, 42, 430, 100, width=14, rotate=-2)
    c.setFont("AlbertSemi", 9)
    c.setFillColor(CURRENT)
    c.drawString(52, 64, "FONTE DE VERDADE: MANUAL + TOKENS + ASSETS APROVADOS")
    page_number(c, 16, "Checklist", dark=True)
    c.showPage()

    c.save()
    print(OUT)


if __name__ == "__main__":
    build()
