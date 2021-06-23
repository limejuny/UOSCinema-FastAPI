from sqlalchemy import CHAR, Column, DateTime, ForeignKey, Integer, VARCHAR, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import Session

from app.database.conn import db

Base = declarative_base()
metadata = Base.metadata


class BaseMixin:
    # id = Column(Integer, primary_key=True, index=True)

    def __init__(self):
        self._q = None
        self._session = None
        self.served = None

    def all_columns(self):
        return [c for c in self.__table__.columns if c.primary_key is False]

    # def __hash__(self):
    #     return hash(self.id)

    @classmethod
    def create(cls, session: Session, auto_commit=False, **kwargs):
        """
        :param session:
        :param auto_commit: 자동 커밋 여부
        :param kwargs: 적재할 데이터
        :return:
        """
        obj = cls()
        for col in obj.all_columns():
            col_name = col.name
            if col_name in kwargs:
                setattr(obj, col_name, kwargs.get(col_name))
        session.add(obj)
        session.flush()
        if auto_commit:
            session.commit()
        return obj

    @classmethod
    def get(cls, session: Session = None, **kwargs):
        """
        :param session:
        :param kwargs:
        :return
        """
        s = next(db.session()) if not session else session
        query = s.query(cls)
        for key, val in kwargs.items():
            col = getattr(cls, key)
            query = query.filter(col == val)

        if query.count() > 1:
            raise Exception(
                "Only one row is supposed to be returned, but got more than one."
            )
        result = query.first()
        if not session:
            s.close()
        return result

    @classmethod
    def filter(cls, session: Session = None, **kwargs):
        """
        :param session:
        :param kwargs:
        :return:
        """
        cond = []
        for key, val in kwargs.items():
            key = key.split("__")
            if len(key) > 2:
                raise Exception("No 2 more dunders")
            col = getattr(cls, key[0])
            if len(key) == 1:
                cond.append((col == val))
            elif len(key) == 2:
                if key[1] == 'gt':
                    cond.append((col > val))
                elif key[1] == 'gte':
                    cond.append((col >= val))
                elif key[1] == 'lt':
                    cond.append((col < val))
                elif key[1] == 'lte':
                    cond.append((col <= val))
                elif key[1] == 'in':
                    cond.append((col.in_(val)))
            obj = cls()
            if session:
                obj._session = session
                obj.served = True
            else:
                obj._session = next(db.session())
                obj.served = False
            query = obj._session.query(cls)
            query = query.filter(*cond)
            obj._q = query
            return obj

        @classmethod
        def cls_attr(cls, col_name=None):
            if col_name:
                col = getattr(cls, col_name)
                return col
            else:
                return cls

        def order_by(self, *args: str):
            for a in args:
                if a.startswith("-"):
                    col_name = a[1:]
                    is_asc = False
                else:
                    col_name = a
                    is_asc = True
                col = self.cls_attr(col_name)
                self._q = self._q.order_by(
                    col.asc()) if is_asc else self._q.order_by(col.desc())
            return self

        def update(self, auto_commit: bool = False, **kwargs):
            qs = self._q.update(kwargs)
            # get_id = self.id
            ret = None

            self._session.flush()
            if qs > 0:
                ret = self._q.first()
            if auto_commit:
                self._session.commit()
            return ret

        def first(self):
            result = self._q.first()
            self.close()
            return result

        def count(self):
            result = self._q.count()
            self.close()
            return result

        def close(self):
            if not self.served:
                self._session.close()
            else:
                self._session.flush()


class CustomerType(Base, BaseMixin):
    __tablename__ = 'customer_type'

    customer_type_id = Column(Integer, primary_key=True)
    customer_type_name = Column(VARCHAR(15), nullable=False)


class Movie(Base, BaseMixin):
    __tablename__ = 'movie'

    movie_id = Column(Integer, primary_key=True)
    movie_name = Column(VARCHAR(60), nullable=False)
    movie_time = Column(DateTime)
    movie_desc = Column(VARCHAR(4000))
    movie_distr = Column(VARCHAR(60))
    movie_release = Column(DateTime, index=True)
    movie_gen = Column(VARCHAR(60))
    show_total_count = Column(Integer,
                              nullable=False,
                              server_default=text("0  "))
    directors = Column(VARCHAR(60))
    actors = Column(VARCHAR(300))
    poster_url = Column(VARCHAR(500))
    movie_grade = Column(CHAR(2))


class Pay(Base, BaseMixin):
    __tablename__ = 'pay'

    pay_id = Column(Integer, primary_key=True)
    pay_type = Column(Integer, nullable=False, server_default=text("1  "))
    pay_state = Column(Integer, nullable=False, server_default=text("1  "))
    pay_price = Column(Integer)
    pay_aprv_num = Column(Integer)
    pay_date = Column(DateTime)


class TheaterType(Base, BaseMixin):
    __tablename__ = 'theater_type'

    theater_type_id = Column(Integer, primary_key=True)
    theater_type_name = Column(VARCHAR(30), nullable=False)


class Usr(Base, BaseMixin):
    __tablename__ = 'usr'

    usr_id = Column(VARCHAR(16), primary_key=True)
    usr_name = Column(VARCHAR(30), nullable=False)
    usr_email = Column(VARCHAR(50), nullable=False, index=True)
    usr_password = Column(CHAR(64), nullable=False)
    usr_point = Column(Integer, server_default=text("0  "))
    usr_type = Column(Integer, nullable=False, server_default=text("1  "))


class Fee(Base, BaseMixin):
    __tablename__ = 'fee'

    theater_type_id = Column(ForeignKey('theater_type.theater_type_id'),
                             primary_key=True,
                             nullable=False)
    customer_type_id = Column(ForeignKey('customer_type.customer_type_id'),
                              primary_key=True,
                              nullable=False)
    movie_fee = Column(Integer, nullable=False)

    customer_type = relationship('CustomerType')
    theater_type = relationship('TheaterType')


class Theater(Base, BaseMixin):
    __tablename__ = 'theater'

    theater_id = Column(Integer, primary_key=True)
    theater_type_id = Column(ForeignKey('theater_type.theater_type_id'),
                             nullable=False,
                             server_default=text("1  "))
    theater_row = Column(Integer, nullable=False, server_default=text("16  "))
    theater_col = Column(Integer, nullable=False, server_default=text("24  "))
    theater_cap = Column(Integer, nullable=False)
    theater_name = Column(VARCHAR(30))

    theater_type = relationship('TheaterType')


class Seat(Base, BaseMixin):
    __tablename__ = 'seat'

    seat_id = Column(Integer, primary_key=True)
    seat_row = Column(Integer, nullable=False)
    seat_col = Column(Integer, nullable=False)
    theater_id = Column(ForeignKey('theater.theater_id'), nullable=False)
    seat_type = Column(Integer, server_default=text("1  "))

    theater = relationship('Theater')


class Show(Base, BaseMixin):
    __tablename__ = 'show'

    show_id = Column(Integer, primary_key=True)
    theater_id = Column(ForeignKey('theater.theater_id'), nullable=False)
    show_start_time = Column(DateTime, nullable=False, index=True)
    show_count = Column(Integer, nullable=False)
    movie_id = Column(ForeignKey('movie.movie_id'), nullable=False, index=True)

    movie = relationship('Movie')
    theater = relationship('Theater')


class Ticket(Base, BaseMixin):
    __tablename__ = 'ticket'

    ticket_id = Column(Integer, primary_key=True)
    ticket_state = Column(Integer, nullable=False, server_default=text("1  "))
    pay_id = Column(ForeignKey('pay.pay_id'), nullable=False, index=True)
    seat_id = Column(ForeignKey('seat.seat_id'), nullable=False, index=True)
    usr_id = Column(ForeignKey('usr.usr_id'), nullable=False, index=True)
    show_id = Column(ForeignKey('show.show_id'), nullable=False, index=True)
    customer_type_id = Column(ForeignKey('customer_type.customer_type_id'),
                              nullable=False)

    customer_type = relationship('CustomerType')
    pay = relationship('Pay')
    seat = relationship('Seat')
    show = relationship('Show')
    usr = relationship('Usr')
