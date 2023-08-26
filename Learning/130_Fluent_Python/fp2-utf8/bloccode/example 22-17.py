# Example 22-17. Simple use of a @cached_property

    @cached_property
    def venue(self):
        key = f'venue.{self.venue_serial}'
        return self.__class__.fetch(key)
