package models

import (
	"time"

	"gorm.io/gorm"
)

type Exercise struct {
	ID          uint      `json:"id" gorm:"primaryKey"`
	Name        string    `json:"name" gorm:"not null;index"`
	Description string    `json:"description"`
	MuscleGroup string    `json:"muscle_group"`
	Equipment   string    `json:"equipment,omitempty"`
	Difficulty  string    `json:"difficulty,omitempty"` // beginner, intermediate, advanced
	Instructions string   `json:"instructions,omitempty"`
	ImageURL    string    `json:"image_url,omitempty"`
	VideoURL    string    `json:"video_url,omitempty"`
	CreatedAt   time.Time `json:"created_at"`
	UpdatedAt   time.Time `json:"updated_at"`
	DeletedAt   gorm.DeletedAt `json:"-" gorm:"index"`

	// Relationships
	TrainingExercises []TrainingExercise `json:"training_exercises,omitempty" gorm:"foreignKey:ExerciseID"`
}

type ExerciseCreate struct {
	Name         string `json:"name" binding:"required,min=2,max=100"`
	Description  string `json:"description,omitempty"`
	MuscleGroup  string `json:"muscle_group" binding:"required"`
	Equipment    string `json:"equipment,omitempty"`
	Difficulty   string `json:"difficulty,omitempty" binding:"omitempty,oneof=beginner intermediate advanced"`
	Instructions string `json:"instructions,omitempty"`
	ImageURL     string `json:"image_url,omitempty" binding:"omitempty,url"`
	VideoURL     string `json:"video_url,omitempty" binding:"omitempty,url"`
}

type ExerciseUpdate struct {
	Name         string `json:"name,omitempty" binding:"omitempty,min=2,max=100"`
	Description  string `json:"description,omitempty"`
	MuscleGroup  string `json:"muscle_group,omitempty"`
	Equipment    string `json:"equipment,omitempty"`
	Difficulty   string `json:"difficulty,omitempty" binding:"omitempty,oneof=beginner intermediate advanced"`
	Instructions string `json:"instructions,omitempty"`
	ImageURL     string `json:"image_url,omitempty" binding:"omitempty,url"`
	VideoURL     string `json:"video_url,omitempty" binding:"omitempty,url"`
}

// BeforeCreate is a GORM hook
func (e *Exercise) BeforeCreate(tx *gorm.DB) error {
	e.CreatedAt = time.Now()
	e.UpdatedAt = time.Now()
	return nil
}

// BeforeUpdate is a GORM hook
func (e *Exercise) BeforeUpdate(tx *gorm.DB) error {
	e.UpdatedAt = time.Now()
	return nil
}
