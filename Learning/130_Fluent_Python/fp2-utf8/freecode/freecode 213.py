    def is_published(self, obj):
        return obj.publish_date is not None
    is_published.short_description = 'Is Published?'
