
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

        page_size = 11.0*inch

        ###
        ### PAGE 1 - the Letter
        ###

        logo_path = settings.STATIC_ROOT + 'reports/logo.png'
        drawing = Image(logo_path, 2.68*inch*0.66, 1.0*inch*0.66)
        drawing.drawOn(pdf, 0.75*inch, page_size-1.0*inch)

        letter_style = ParagraphStyle(name="letter_text",
                                      fontName="Courier")

        data['letter_url'] = settings.LETTER_URL

        letter_text = render_to_string('violations_letter.tmpl', data)
        letter_text = letter_text.replace('\n', '<br></br>')


        letter = Paragraph(letter_text, letter_style)

        aw = 5.5*inch
        ah = 8.5*inch
        w,h = letter.wrap(aw, ah)
        if (w <= aw) and (h <= ah):
            letter.drawOn(pdf, 1.5*inch, (page_size-h+2.0*inch)/2.0)
        else:
            pdf.drawString(1.5*inch, 5.0*inch, 'Could not render the letter because the page is too small.')

        pdf.showPage()

        ###
        ### PAGE 2 - The Violation Report
        ###

        text_width = 6.5*inch
        text_height = 9.0*inch
        top_line = page_size - 1.0*inch # 1 inch margin at top

        header_style = ParagraphStyle(name="header_text",
                                      fontName="Times-Roman")

        header_text = "<para align=center><b>SAFEWATER ATHENS - VIOLATIONS REPORT</b><br></br>Prepared for %s on %s<p></p></para>"

        ## FIXME date --vvvv
        header_text = header_text % (data.get('name'), 'March 15, 2013')
        header = Paragraph(header_text, header_style)
        w, h = header.wrap(text_width, text_height)
        top_line = top_line - h
        header.drawOn(pdf, (8.5*inch - w) / 2.0, top_line)
        top_line = top_line - 0.5 * inch

        vio_style = ParagraphStyle(name='violation_text', fontName="Courier")

        vio_intro_text = "The EPA has reported the following violations for your public water supply:<br></br><br></br><seqreset id='report'>"
        vio_intro = Paragraph(vio_intro_text, vio_style)
        w, h = vio_intro.wrap(text_width, text_height)
        top_line = top_line - h
        vio_intro.drawOn(pdf, (8.5*inch - w) / 2.0, top_line)
        top_line = top_line - 0.5 * inch

        for report in data.get('reports', []):

            vio_text = render_to_string('violations_listing.tmpl', report)
            vio_text = vio_text.replace('\n', '<br></br>')

            vio = Paragraph(vio_text, vio_style)

            vio_width, vio_height = vio.wrap(aw, ah)
            top_line = top_line - vio_height

            # If it won't fit on the page, then put it on the next one
            #
            if top_line < 1.0:
                pdf.showPage()
                top_line = page_size - 1.0*inch # 1 inch margin at top
                w, h = header.wrap(text_width, text_height)
                top_line = top_line - h
                header.drawOn(pdf, (8.5*inch - w) / 2.0, top_line)
                top_line = top_line - 0.5 * inch - vio_height

            vio.drawOn(pdf, 1.0*inch, top_line)

        pdf.showPage()

        ###
        ### PAGE 3 - The Table
        ###
