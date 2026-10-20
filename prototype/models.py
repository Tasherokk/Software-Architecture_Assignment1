from dataclasses import dataclass, asdict


@dataclass
class Reader:
    id: int
    name: str
    email: str

    def to_dict(self):
        return asdict(self)


@dataclass
class Book:
    id: int
    title: str
    author: str
    available: bool = True

    def to_dict(self):
        return asdict(self)


@dataclass
class Loan:
    id: int
    reader_id: int
    book_id: int

    def to_dict(self):
        return asdict(self)
