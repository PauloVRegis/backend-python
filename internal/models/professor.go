package models

import (
	"time"

	"gorm.io/gorm"
)

type Professor struct {
	ID          uint      `json:"id" gorm:"primaryKey"`
	Name        string    `json:"name" gorm:"not null"`
	Email       string    `json:"email" gorm:"uniqueIndex;not null"`
	Phone       string    `json:"phone,omitempty"`
	Bio         string    `json:"bio,omitempty"`
	Specialties string    `json:"specialties,omitempty"`
	CreatedAt   time.Time `json:"created_at"`
	UpdatedAt   time.Time `json:"updated_at"`
	DeletedAt   gorm.DeletedAt `json:"-" gorm:"index"`

	// Relationships
	Trainings []Training `json:"trainings,omitempty" gorm:"foreignKey:ProfessorID"`
}

type ProfessorCreate struct {
	Name        string `json:"name" binding:"required,min=2,max=100"`
	Email       string `json:"email" binding:"required,email"`
	Phone       string `json:"phone,omitempty"`
	Bio         string `json:"bio,omitempty"`
	Specialties string `json:"specialties,omitempty"`
}

type ProfessorUpdate struct {
	Name        string `json:"name,omitempty" binding:"omitempty,min=2,max=100"`
	Email       string `json:"email,omitempty" binding:"omitempty,email"`
	Phone       string `json:"phone,omitempty"`
	Bio         string `json:"bio,omitempty"`
	Specialties string `json:"specialties,omitempty"`
}

// BeforeCreate is a GORM hook
func (p *Professor) BeforeCreate(tx *gorm.DB) error {
	p.CreatedAt = time.Now()
	p.UpdatedAt = time.Now()
	return nil
}

// BeforeUpdate is a GORM hook
func (p *Professor) BeforeUpdate(tx *gorm.DB) error {
	p.UpdatedAt = time.Now()
	return nil
}
