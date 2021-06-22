from datetime import datetime
from pydantic import BaseModel


class CustomerType(BaseModel):
    customer_type_id: int
    customer_type_name: str


class Movie(BaseModel):
    # movie_id:int
    movie_name: str
    movie_time: datetime
    movie_desc: str
    movie_distr: str
    movie_release: datetime
    movie_gen: str
    show_total_count: int
    directors: str
    actors: str
    poster_url: str
    movie_grade: str


class Pay(BaseModel):
    pay_id: int
    pay_type: int
    pay_state: int
    pay_price: int
    pay_aprv_num: int
    pay_date: datetime


class TheaterType(BaseModel):
    theater_type_id: int
    theater_type_name: str


class Usr(BaseModel):
    usr_id: str
    usr_name: str
    usr_email: str
    usr_password: str
    usr_point: int
    usr_type: int


class Fee(BaseModel):
    theater_type_id: int
    customer_type_id: int
    movie_fee: int


class Theater(BaseModel):
    theater_id: int
    theater_type_id: int
    theater_row: int
    theater_col: int
    theater_cap: int
    theater_name: str


class Seat(BaseModel):
    seat_id: int
    seat_row: int
    seat_col: int
    theater_id: int
    seat_type: int


class Show(BaseModel):
    show_id: int
    theater_id: int
    show_start_time: datetime
    show_count: int
    movie_id: int


class Ticket(BaseModel):
    ticket_id: int
    ticket_state: int
    pay_id: int
    seat_id: int
    usr_id: str
    show_id: int
    customer_type_id: int
