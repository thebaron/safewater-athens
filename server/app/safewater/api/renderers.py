
import tempfile
import logging

from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm, inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Image

from rest_framework import renderers
from svglib.svglib import svg2rlg

from django.conf import settings
from django.template.loader import render_to_string


class HALJSONRenderer(renderers.JSONRenderer):
    """
    Adds HAL-style output
    """
    media_type = 'application/json'
    format = 'json'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render `obj` into HAL-embellished JSON.
        """
        hal = { 'data' : data }

        renderer_context = renderer_context or {}
        hal['_links'] = renderer_context.get('links', {})
        hal['_embedded'] = renderer_context.get('embedded', {})

        return super(HALJSONRenderer, self).render(hal, accepted_media_type, renderer_context)


class PDFRenderer(renderers.BaseRenderer):
    """
    Renders a PDF report!
    """

    media_type = 'application/pdf'
    format = 'pdf'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render an object into a PDF document.
        """

        from safewater.api.v1.viewsets import PublicWaterSourceViewSet

        tmpPDF = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        pdf = canvas.Canvas(tmpPDF)

        if (isinstance(renderer_context.get('view', None), PublicWaterSourceViewSet)):
            self.doPWSPDF(pdf, data, renderer_context)
        else:
            pdf.drawString(100, 100, 'This report is not available in PDF format!')
            pdf.showPage()

        pdf.save()
        tmpPDF.seek(0)
        return tmpPDF.read()

    def doPWSPDF(self, pdf, data, context):

        pageSize = 11.0*inch

        ###
        ### PAGE 1 - the Letter
        ###

        logo_path = settings.STATIC_ROOT + 'reports/logo.png'
        drawing = Image(logo_path, 2.68*inch*0.66, 1.0*inch*0.66)
        drawing.drawOn(pdf, 0.75*inch, pageSize-1.0*inch)

        letter_text = render_to_string('violations_letter.tmpl', data)
        letter_text = letter_text.replace('\n', '<br></br>')

        letter_style = ParagraphStyle(name="letter_text",
                                      fontName="Courier")

        letter = Paragraph(letter_text, letter_style)

        aw = 5.5*inch
        ah = 8.5*inch
        w,h = letter.wrap(aw, ah)
        if (w <= aw) and (h <= ah):
            letter.drawOn(pdf, 1.5*inch, (pageSize-h+2.0*inch)/2.0)
        else:
            pdf.drawString(1.5*inch, 5.0*inch, 'Could not render the letter because the page is too small.')

        pdf.showPage()

        ###
        ### PAGE 2 - The Violation Report
        ###

        textWidth = 6.5*inch
        textHeight = 9.0*inch
        topLine = pageSize - 1.0*inch # 1 inch margin at top

        headerStyle = ParagraphStyle(name="HeaderText", fontName="Times-Roman")

        header_text = "<para align=center><b>SAFEWATER ATHENS - VIOLATIONS REPORT</b><br></br>Prepared for %s on %s<p></p></para>"

        header_text = header_text % (data.get('name'), 'March 15, 2013')
        header = Paragraph(header_text, headerStyle)
        w, h = header.wrap(textWidth, textHeight)
        topLine = topLine - h
        header.drawOn(pdf, (8.5*inch - w) / 2.0, topLine)

        topLine = topLine - 0.5 * inch

        vios = render_to_string('violations_listing.tmpl', data)
        vios = vios.replace('\n', '<br></br>')

        letterStyle = ParagraphStyle(name="LetterText", fontName="Courier")

        letter = Paragraph(vios, letterStyle)

        w, h = letter.wrap(aw, ah)
        topLine = topLine - h
        letter.drawOn(pdf, 1.0*inch, topLine)

        pdf.showPage()

        ###
        ### PAGE 3 - The Table
        ###
