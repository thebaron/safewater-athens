
import tempfile
import logging

from rest_framework import renderers

from reportlab.pdfgen import canvas


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

        hal = data.copy()
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

        tmpPDF = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        pdf = canvas.Canvas(tmpPDF)
        pdf.drawString(100, 100, 'Hello, world!')

        pdf.showPage()
        pdf.save()

        tmpPDF.seek(0)

        return tmpPDF.read()

