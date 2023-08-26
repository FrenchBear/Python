    @dataclass
    class HackerClubMember:
        .name: str
        .guests: list = field(default_factory=list)
        .handle: str = ''

        all_handles = set()
