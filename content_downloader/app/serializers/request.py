from marshmallow import Schema, fields, validates, ValidationError


class Content2chRequestValidateSchema(Schema):
    _patterns = ('https://2ch', 'res', 'html')

    threadUrl = fields.Str(required=True, example='https://2ch.hk/pr/res/1512752.html')

    @validates("threadUrl")
    def validate_thread_url(self, value):
        patterns = value.split('.')
        patterns[1] = value.split('/')[-2]
        if not tuple(patterns) == self._patterns:
            raise ValidationError(f"'{value}' does not look like 2ch thread url.")


class Content2chThreadObjectSchema(Schema):
    _json = '.json'

    thread_url_json = fields.Method("jsonify_url")
    thread_name = fields.Method("get_thread_name")


    def jsonify_url(self, obj):
        return '.'.join(obj['threadUrl'].split('.')[:-1]) + self._json

    def get_thread_name(self, obj):
        return obj['threadUrl'].split('/')[-1].split('.')[0]


content_2ch_request_validate_schema = Content2chRequestValidateSchema()
content_2ch_thread_object_schema = Content2chThreadObjectSchema()

