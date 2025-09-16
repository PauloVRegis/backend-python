package models

import (
	"time"

	"gorm.io/gorm"
)

type User struct {
	ID           uint      `json:"id" gorm:"primaryKey"`
	Email        string    `json:"email" gorm:"uniqueIndex;not null"`
	Name         string    `json:"name" gorm:"not null"`
	PasswordHash string    `json:"-" gorm:"not null"`
	CreatedAt    time.Time `json:"created_at"`
	UpdatedAt    time.Time `json:"updated_at"`
	DeletedAt    gorm.DeletedAt `json:"-" gorm:"index"`

	// Relationships
	Trainings             []Training             `json:"trainings,omitempty" gorm:"foreignKey:UserID"`
	TrainingRegistrations []TrainingRegistration `json:"training_registrations,omitempty" gorm:"foreignKey:UserID"`
}

type UserCreate struct {
	Email    string `json:"email" binding:"required,email"`
	Name     string `json:"name" binding:"required,min=2,max=100"`
	Password string `json:"password" binding:"required,min=6"`
}

type UserUpdate struct {
	Email string `json:"email,omitempty" binding:"omitempty,email"`
	Name  string `json:"name,omitempty" binding:"omitempty,min=2,max=100"`
}

type UserResponse struct {
	ID        uint      `json:"id"`
	Email     string    `json:"email"`
	Name      string    `json:"name"`
	CreatedAt time.Time `json:"created_at"`
}

type LoginRequest struct {
	Email    string `json:"email" binding:"required,email"`
	Password string `json:"password" binding:"required"`
}

type LoginResponse struct {
	AccessToken string       `json:"access_token"`
	TokenType   string       `json:"token_type"`
	ExpiresIn   int          `json:"expires_in"`
	User        UserResponse `json:"user"`
}

// BeforeCreate is a GORM hook
func (u *User) BeforeCreate(tx *gorm.DB) error {
	u.CreatedAt = time.Now()
	u.UpdatedAt = time.Now()
	return nil
}

// BeforeUpdate is a GORM hook
func (u *User) BeforeUpdate(tx *gorm.DB) error {
	u.UpdatedAt = time.Now()
	return nil
}
