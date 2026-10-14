# Helpers to emit WordprocessingML that matches the UAT template styles.
import re
from xml.sax.saxutils import escape

_bm = [900]
def _next_bm():
    _bm[0] += 1
    return _bm[0]

def runs(text, base_rpr=''):
    """Inline markup: **bold**, *italic*. Returns run XML."""
    out = []
    # tokenise
    pos = 0
    for m in re.finditer(r'==(.+?)==|\*\*(.+?)\*\*|\*(.+?)\*', text):
        if m.start() > pos:
            out.append(_run(text[pos:m.start()], base_rpr))
        if m.group(1) is not None:
            out.append(runs(m.group(1), base_rpr + '<w:highlight w:val="yellow"/>'))
        elif m.group(2) is not None:
            out.append(_run(m.group(2), base_rpr + '<w:b/><w:bCs/>'))
        else:
            out.append(_run(m.group(3), base_rpr + '<w:i/><w:iCs/>'))
        pos = m.end()
    if pos < len(text):
        out.append(_run(text[pos:], base_rpr))
    return ''.join(out)

def _run(t, rpr):
    r = f'<w:rPr>{rpr}</w:rPr>' if rpr else ''
    return f'<w:r>{r}<w:t xml:space="preserve">{escape(t)}</w:t></w:r>'

def p(text, ppr=''):
    pp = f'<w:pPr>{ppr}</w:pPr>' if ppr else ''
    return f'<w:p>{pp}{runs(text)}</w:p>'

def h(level, text):
    style = {1: 'Ttulo1', 2: 'Ttulo2', 3: 'Ttulo3'}[level]
    i = _next_bm()
    return (f'<w:p><w:pPr><w:pStyle w:val="{style}"/></w:pPr>'
            f'<w:bookmarkStart w:id="{i}" w:name="_TocN{i}"/>{runs(text)}'
            f'<w:bookmarkEnd w:id="{i}"/></w:p>')

def bullet(text):
    return ('<w:p><w:pPr><w:pStyle w:val="Prrafodelista"/><w:numPr><w:ilvl w:val="0"/>'
            '<w:numId w:val="14"/></w:numPr><w:ind w:left="567" w:hanging="340"/>'
            f'<w:contextualSpacing w:val="0"/></w:pPr>{runs(text)}</w:p>')

def numbered(n, text):
    # manual numbering with hanging indent (keeps template numbering untouched)
    return (f'<w:p><w:pPr><w:ind w:left="567" w:hanging="340"/></w:pPr>'
            f'{runs(str(n) + ".")}<w:r><w:tab/></w:r>{runs(text)}</w:p>')

def quote(text):
    return p(text, '<w:ind w:left="851" w:right="851"/>')

def caption(kind, text):
    """kind: 'Tabla' | 'Figura'. SEQ field so the template's lists of tables/figures pick it up."""
    jc = 'center' if kind == 'Figura' else 'both'
    i = _next_bm()
    b = '<w:rPr><w:b/><w:bCs/></w:rPr>'
    return (f'<w:p><w:pPr><w:pStyle w:val="Sinespaciado"/><w:keepNext/><w:jc w:val="{jc}"/></w:pPr>'
            f'<w:bookmarkStart w:id="{i}" w:name="_TocC{i}"/>'
            f'<w:r>{b}<w:t xml:space="preserve">{kind} </w:t></w:r>'
            f'<w:r>{b}<w:fldChar w:fldCharType="begin"/></w:r>'
            f'<w:r>{b}<w:instrText xml:space="preserve"> SEQ {kind} \\* ARABIC </w:instrText></w:r>'
            f'<w:r>{b}<w:fldChar w:fldCharType="separate"/></w:r>'
            f'<w:r>{b}<w:t>1</w:t></w:r>'
            f'<w:r>{b}<w:fldChar w:fldCharType="end"/></w:r>'
            f'<w:r>{b}<w:t>.</w:t></w:r>'
            f'{runs(" " + text)}<w:bookmarkEnd w:id="{i}"/></w:p>')

def source(text, center=False):
    jc = '<w:jc w:val="center"/>' if center else ''
    return (f'<w:p><w:pPr><w:pStyle w:val="Sinespaciado"/><w:spacing w:after="240"/>{jc}</w:pPr>'
            f'<w:r><w:rPr><w:b/><w:bCs/></w:rPr><w:t>Fuente:</w:t></w:r>{runs(" " + text)}</w:p>')

def table(headers, rows, widths):
    """widths in DXA; total should be <= 8838 (page 12240 - 2*1701)."""
    border = ('<w:tblBorders><w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
              '<w:bottom w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
              '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="BFBFBF"/></w:tblBorders>')
    tw = sum(widths)
    grid = ''.join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    def cell(txt, w, head=False):
        shade = '<w:shd w:val="clear" w:color="auto" w:fill="D9D9D9"/>' if head else ''
        rpr = '<w:b/><w:bCs/>' if head else ''
        paras = ''.join(
            f'<w:p><w:pPr><w:pStyle w:val="Sinespaciado"/><w:jc w:val="{"center" if head else "left"}"/></w:pPr>{runs(line, rpr)}</w:p>'
            for line in txt.split('\n'))
        return (f'<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/>{shade}</w:tcPr>{paras}</w:tc>')
    x = (f'<w:tbl><w:tblPr><w:tblW w:w="{tw}" w:type="dxa"/><w:jc w:val="center"/>{border}'
         '<w:tblLayout w:type="fixed"/><w:tblCellMar><w:left w:w="85" w:type="dxa"/>'
         '<w:right w:w="85" w:type="dxa"/></w:tblCellMar><w:tblLook w:val="04A0"/></w:tblPr>'
         f'<w:tblGrid>{grid}</w:tblGrid>')
    x += '<w:tr><w:trPr><w:tblHeader/></w:trPr>' + ''.join(cell(t, w, True) for t, w in zip(headers, widths)) + '</w:tr>'
    for r in rows:
        x += '<w:tr><w:trPr><w:cantSplit/></w:trPr>' + ''.join(cell(t, w) for t, w in zip(r, widths)) + '</w:tr>'
    return x + '</w:tbl>'

def reference(text):
    # APA 7: hanging indent 1.27 cm
    return p(text, '<w:ind w:left="720" w:hanging="720"/><w:jc w:val="left"/>')

def image(rid, cx, cy, docpr_id, name):
    return ('<w:p><w:pPr><w:pStyle w:val="Sinespaciado"/><w:keepNext/><w:jc w:val="center"/></w:pPr><w:r><w:rPr><w:noProof/></w:rPr><w:drawing>'
            f'<wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{cx}" cy="{cy}"/>'
            f'<wp:effectExtent l="0" t="0" r="0" b="0"/><wp:docPr id="{docpr_id}" name="{name}"/>'
            '<wp:cNvGraphicFramePr><a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/></wp:cNvGraphicFramePr>'
            '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            f'<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:nvPicPr><pic:cNvPr id="{docpr_id}" name="{name}"/><pic:cNvPicPr/></pic:nvPicPr>'
            f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
            '</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>')

SECT = ('<w:p><w:pPr><w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1701" w:right="1701" '
        'w:bottom="1701" w:left="1701" w:header="567" w:footer="850" w:gutter="0"/><w:cols w:space="708"/>'
        '<w:docGrid w:linePitch="360"/></w:sectPr></w:pPr></w:p>')
