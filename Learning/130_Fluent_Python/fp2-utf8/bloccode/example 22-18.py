# Example 22-18. Stacking @property on @cache

    @property
    @cache
    def speakers(self):
        spkr_serials = self.__dict__['speakers']
        fetch = self.__class__.fetch
        return [fetch(f'speaker.{key}') for key in spkr_serials]
