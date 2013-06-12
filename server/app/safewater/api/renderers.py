from rest_framework import renderers


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
