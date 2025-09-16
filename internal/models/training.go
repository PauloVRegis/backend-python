package models

import (
	"time"

	"gorm.io/gorm"
)

type Training struct {
	ID           uint      `json:"id" gorm:"primaryKey"`
	Name         string    `json:"name" gorm:"not null;index"`
	Description  string    `json:"description"`
	UserID       uint      `json:"user_id" gorm:"not null"`
	ProfessorID  uint      `json:"professor_id" gorm:"not null"`
	Repetitions  int       `json:"repetitions"`
	Sets         int       `json:"sets"`
	CreatedAt    time.Time `json:"created_at"`
	UpdatedAt    time.Time `json:"updated_at"`
	DeletedAt    gorm.DeletedAt `json:"-" gorm:"index"`

	// Relationships
	User                  User                   `json:"user,omitempty" gorm:"foreignKey:UserID"`
	Professor             Professor              `json:"professor,omitempty" gorm:"foreignKey:ProfessorID"`
	TrainingRegistrations []TrainingRegistration `json:"training_registrations,omitempty" gorm:"foreignKey:TrainingID"`
	TrainingExercises     []TrainingExercise     `json:"training_exercises,omitempty" gorm:"foreignKey:TrainingID"`
}

type TrainingExercise struct {
	ID          uint `json:"id" gorm:"primaryKey"`
	TrainingID  uint `json:"training_id" gorm:"not null"`
	ExerciseID  uint `json:"exercise_id" gorm:"not null"`
	Repetitions int  `json:"repetitions"`
	Sets        int  `json:"sets"`

	// Relationships
	Training Training `json:"training,omitempty" gorm:"foreignKey:TrainingID"`
	Exercise Exercise `json:"exercise,omitempty" gorm:"foreignKey:ExerciseID"`
}

type TrainingRegistration struct {
	ID          uint      `json:"id" gorm:"primaryKey"`
	UserID      uint      `json:"user_id" gorm:"not null"`
	TrainingID  uint      `json:"training_id" gorm:"not null"`
	Date        time.Time `json:"date"`
	Completed   bool      `json:"completed" gorm:"default:false"`
	CreatedAt   time.Time `json:"created_at"`
	UpdatedAt   time.Time `json:"updated_at"`
	DeletedAt   gorm.DeletedAt `json:"-" gorm:"index"`

	// Relationships
	User     User     `json:"user,omitempty" gorm:"foreignKey:UserID"`
	Training Training `json:"training,omitempty" gorm:"foreignKey:TrainingID"`
}

type TrainingCreate struct {
	Name        string `json:"name" binding:"required,min=2,max=100"`
	Description string `json:"description,omitempty"`
	ProfessorID uint   `json:"professor_id" binding:"required"`
	Repetitions int    `json:"repetitions,omitempty"`
	Sets        int    `json:"sets,omitempty"`
}

type TrainingUpdate struct {
	Name        string `json:"name,omitempty" binding:"omitempty,min=2,max=100"`
	Description string `json:"description,omitempty"`
	ProfessorID uint   `json:"professor_id,omitempty"`
	Repetitions int    `json:"repetitions,omitempty"`
	Sets        int    `json:"sets,omitempty"`
}

type TrainingExerciseCreate struct {
	ExerciseID  uint `json:"exercise_id" binding:"required"`
	Repetitions int  `json:"repetitions,omitempty"`
	Sets        int  `json:"sets,omitempty"`
}

// BeforeCreate is a GORM hook
func (t *Training) BeforeCreate(tx *gorm.DB) error {
	t.CreatedAt = time.Now()
	t.UpdatedAt = time.Now()
	return nil
}

// BeforeUpdate is a GORM hook
func (t *Training) BeforeUpdate(tx *gorm.DB) error {
	t.UpdatedAt = time.Now()
	return nil
}

// BeforeCreate is a GORM hook for TrainingRegistration
func (tr *TrainingRegistration) BeforeCreate(tx *gorm.DB) error {
	tr.CreatedAt = time.Now()
	tr.UpdatedAt = time.Now()
	return nil
}

// BeforeUpdate is a GORM hook for TrainingRegistration
func (tr *TrainingRegistration) BeforeUpdate(tx *gorm.DB) error {
	tr.UpdatedAt = time.Now()
	return nil
}
