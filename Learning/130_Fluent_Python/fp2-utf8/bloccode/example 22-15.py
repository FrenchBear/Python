# Example 22-15. Custom caching logic using hasattr disables key-sharing optimization

    @property
    def speakers(self):
        if not hasattr(self, '__speaker_objs'):
            spkr_serials = self.__dict__['speakers']
            fetch = self.__class__.fetch
            self.__speaker_objs = [fetch(f'speaker.{key}') for key in spkr_serials]
        return self.__speaker_objs
