from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Boolean, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Creature(Base):
    __tablename__ = 'creature'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(5000))
    unique_number = Column(Integer, unique=True, nullable=False)
    owner_id = Column(Integer, ForeignKey('client.id'), nullable=False)
    image_url = Column(String(500), nullable=True)
    QR_code_url = Column(String(500), nullable=True)
    #created_at = Column(DateTime, default=func.now())
    created_at = Column(DateTime, server_default=func.now())

    owner = relationship('Client', back_populates='creatures')

    def __repr__(self):
        return f'<Creature id={self.id}, name={self.name}, unique_number={self.unique_number}>'

class Client(Base):
    __tablename__ = 'client'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(120), nullable=False)
    birthdate = Column(Date, nullable=True)
    created_at = Column(DateTime, default=func.now())

    creatures = relationship('Creature', back_populates='owner')
    books = relationship("Book", back_populates="client")

    __table_args__ = (Index('ix_client_id', 'id'),)

    def __repr__(self):
        return f'<Client id={self.id}, name={self.name}>'

class Wheel(Base):
    __tablename__ = 'wheel'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    numero = Column(Integer, unique=True, nullable=False)
    created_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f'<Wheel id={self.id}, numero={self.numero}>'

class Book(Base):
    __tablename__ = 'book'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    client_id = Column(Integer, ForeignKey('client.id'), nullable=False)
    scene_count = Column(Integer, default=20)
    completion_status = Column(Boolean, default=False)
    is_paid = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())

    client = relationship("Client", back_populates="books")
    scenes = relationship("Scene", back_populates="book")

    __table_args__ = (Index('ix_book_id', 'id'),)

    def __repr__(self):
        return f'<Book id={self.id}, title={self.title}>'

class Scene(Base):
    __tablename__ = 'scene'
    
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('book.id'), nullable=False)
    paragraph = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    scene_number = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now())

    book = relationship("Book", back_populates="scenes")

    __table_args__ = (Index('ix_scene_id', 'id'),)

    def __repr__(self):
        return f'<Scene id={self.id}, book={self.book_id}>'
