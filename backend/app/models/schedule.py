from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Time, Date, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    name = Column(String(100), nullable=False)
    capacity = Column(Integer)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    organization = relationship("Organization", back_populates="rooms")
    schedule = relationship("Schedule", back_populates="room")

    def __repr__(self):
        return f"<Room {self.name}>"


class Schedule(Base):
    __tablename__ = "schedule"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lesson_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    lesson_type = Column(String(50), default="regular")  # regular, exam, open_lesson
    is_cancelled = Column(Boolean, default=False)
    cancelled_reason = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    group = relationship("Group", back_populates="schedule")
    room = relationship("Room", back_populates="schedule")
    teacher = relationship("User", foreign_keys=[teacher_id])
    attendance = relationship("LessonAttendance", back_populates="schedule")

    def __repr__(self):
        return f"<Schedule {self.lesson_date} {self.start_time}>"


class LessonAttendance(Base):
    __tablename__ = "lesson_attendance"

    id = Column(Integer, primary_key=True, index=True)
    schedule_id = Column(Integer, ForeignKey("schedule.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    status = Column(String(20), default="absent")  # present, absent, late, excused
    notes = Column(Text)
    marked_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    schedule = relationship("Schedule", back_populates="attendance")
    student = relationship("Student", back_populates="lessons_attended")

    def __repr__(self):
        return f"<LessonAttendance {self.student_id} - {self.status}>"
