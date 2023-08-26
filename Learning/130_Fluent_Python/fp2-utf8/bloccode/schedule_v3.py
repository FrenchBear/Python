# Example 22-14. schedule_v3.py: the speakers property

    @property
    def speakers(self):
        spkr_serials = self.__dict__['speakers']
        fetch = self.__class__.fetch
        return [fetch(f'speaker.{key}') for key in spkr_serials]
