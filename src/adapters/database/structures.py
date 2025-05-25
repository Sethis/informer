from sqlalchemy import BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    def __repr__(self):
        ent = []
        for col in {*self.__table__.columns}:
            ent.append("{0}={1}".format(col.key, getattr(self, col.key)))
        return "<{0}(".format(self.__class__.__name__) + ", ".join(ent) + ")>"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in {*self.__table__.columns}}


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger(), unique=True)

    # This could have been put in a separate table with access levels,
    # but it added too much complexity to this small project.
    is_admin: Mapped[bool] = mapped_column(default=False)


class Information(Base):
    __tablename__ = "information"
    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]
    text: Mapped[str]


class EncodedData(Base):
    __tablename__ = "endoded_data"
    id: Mapped[int] = mapped_column(primary_key=True)
    payload: Mapped[str]
