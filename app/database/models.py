from sqlalchemy import CHAR, Column, DateTime, ForeignKey, Integer, VARCHAR, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class CustomerType(Base):
    __tablename__ = 'customer_type'

    customer_type_id = Column(Integer, primary_key=True)
    customer_type_name = Column(VARCHAR(15), nullable=False)


class Movie(Base):
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


class Pay(Base):
    __tablename__ = 'pay'

    pay_id = Column(Integer, primary_key=True)
    pay_type = Column(Integer, nullable=False, server_default=text("1  "))
    pay_state = Column(Integer, nullable=False, server_default=text("1  "))
    pay_price = Column(Integer)
    pay_aprv_num = Column(Integer)
    pay_date = Column(DateTime)


class TheaterType(Base):
    __tablename__ = 'theater_type'

    theater_type_id = Column(Integer, primary_key=True)
    theater_type_name = Column(VARCHAR(30), nullable=False)


class Usr(Base):
    __tablename__ = 'usr'

    usr_id = Column(VARCHAR(16), primary_key=True)
    usr_name = Column(VARCHAR(30), nullable=False)
    usr_email = Column(VARCHAR(50), nullable=False, index=True)
    usr_password = Column(CHAR(64), nullable=False)
    usr_point = Column(Integer, server_default=text("0  "))
    usr_type = Column(Integer, nullable=False, server_default=text("1  "))


class Fee(Base):
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


class Theater(Base):
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


class Seat(Base):
    __tablename__ = 'seat'

    seat_id = Column(Integer, primary_key=True)
    seat_row = Column(Integer, nullable=False)
    seat_col = Column(Integer, nullable=False)
    theater_id = Column(ForeignKey('theater.theater_id'), nullable=False)
    seat_type = Column(Integer, server_default=text("1  "))

    theater = relationship('Theater')


class Show(Base):
    __tablename__ = 'show'

    show_id = Column(Integer, primary_key=True)
    theater_id = Column(ForeignKey('theater.theater_id'), nullable=False)
    show_start_time = Column(DateTime, nullable=False, index=True)
    show_count = Column(Integer, nullable=False)
    movie_id = Column(ForeignKey('movie.movie_id'), nullable=False, index=True)

    movie = relationship('Movie')
    theater = relationship('Theater')


class Ticket(Base):
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
