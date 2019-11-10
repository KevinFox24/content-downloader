from marshmallow import Schema, fields, validates, ValidationError


class Content2chRequestSchema(Schema):
    _patterns = ('https://2ch', 'res', 'html')

    threadUrl = fields.Str(required=True, example='https://2ch.hk/pr/res/1512752.html')

    @validates("threadUrl")
    def validate_thread_url(self, value):
        patterns = value.split('.')
        patterns[1] = value.split('/')[-2]
        if not tuple(patterns) == self._patterns:
            raise ValidationError(f"'{value}' does not look like 2ch thread url.")


content_2ch_request_schema = Content2chRequestSchema()
