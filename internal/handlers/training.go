package handlers

import (
	"net/http"
	"strconv"

	"backend-python/internal/database"
	"backend-python/internal/models"

	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
)

type TrainingHandler struct {
	db *gorm.DB
}

func NewTrainingHandler() *TrainingHandler {
	return &TrainingHandler{
		db: database.GetDB(),
	}
}

// GetTrainings godoc
// @Summary Get all trainings
// @Description Get all trainings with pagination
// @Tags trainings
// @Accept json
// @Produce json
// @Param skip query int false "Skip records" default(0)
// @Param limit query int false "Limit records" default(100)
// @Security ApiKeyAuth
// @Success 200 {array} models.Training
// @Failure 400 {object} map[string]interface{}
// @Failure 401 {object} map[string]interface{}
// @Failure 500 {object} map[string]interface{}
// @Router /trainings [get]
func (h *TrainingHandler) GetTrainings(c *gin.Context) {
	skip, _ := strconv.Atoi(c.DefaultQuery("skip", "0"))
	limit, _ := strconv.Atoi(c.DefaultQuery("limit", "100"))

	if limit > 1000 {
		limit = 1000
	}

	var trainings []models.Training
	if err := h.db.Preload("User").Preload("Professor").Preload("TrainingExercises.Exercise").
		Offset(skip).Limit(limit).Find(&trainings).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to retrieve trainings"})
		return
	}

	c.JSON(http.StatusOK, trainings)
}

// GetTraining godoc
// @Summary Get training by ID
// @Description Get a specific training by ID
// @Tags trainings
// @Accept json
// @Produce json
// @Param id path int true "Training ID"
// @Security ApiKeyAuth
// @Success 200 {object} models.Training
// @Failure 400 {object} map[string]interface{}
// @Failure 401 {object} map[string]interface{}
// @Failure 404 {object} map[string]interface{}
// @Router /trainings/{id} [get]
func (h *TrainingHandler) GetTraining(c *gin.Context) {
	trainingID, err := strconv.ParseUint(c.Param("id"), 10, 32)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid training ID"})
		return
	}

	var training models.Training
	if err := h.db.Preload("User").Preload("Professor").Preload("TrainingExercises.Exercise").
		First(&training, trainingID).Error; err != nil {
		if err == gorm.ErrRecordNotFound {
			c.JSON(http.StatusNotFound, gin.H{"error": "Training not found"})
		} else {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to retrieve training"})
		}
		return
	}

	c.JSON(http.StatusOK, training)
}

// CreateTraining godoc
// @Summary Create a new training
// @Description Create a new training
// @Tags trainings
// @Accept json
// @Produce json
// @Param training body models.TrainingCreate true "Training data"
// @Security ApiKeyAuth
// @Success 201 {object} models.Training
// @Failure 400 {object} map[string]interface{}
// @Failure 401 {object} map[string]interface{}
// @Failure 500 {object} map[string]interface{}
// @Router /trainings [post]
func (h *TrainingHandler) CreateTraining(c *gin.Context) {
	var req models.TrainingCreate
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	userID, exists := c.Get("user_id")
	if !exists {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "User not found in context"})
		return
	}

	// Verify professor exists
	var professor models.Professor
	if err := h.db.First(&professor, req.ProfessorID).Error; err != nil {
		if err == gorm.ErrRecordNotFound {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Professor not found"})
		} else {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to verify professor"})
		}
		return
	}

	// Create training
	training := models.Training{
		Name:        req.Name,
		Description: req.Description,
		UserID:      userID.(uint),
		ProfessorID: req.ProfessorID,
		Repetitions: req.Repetitions,
		Sets:        req.Sets,
	}

	if err := h.db.Create(&training).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to create training"})
		return
	}

	// Load relationships
	if err := h.db.Preload("User").Preload("Professor").First(&training, training.ID).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to load training details"})
		return
	}

	c.JSON(http.StatusCreated, training)
}

// UpdateTraining godoc
// @Summary Update training
// @Description Update training information
// @Tags trainings
// @Accept json
// @Produce json
// @Param id path int true "Training ID"
// @Param training body models.TrainingUpdate true "Training data"
// @Security ApiKeyAuth
// @Success 200 {object} models.Training
// @Failure 400 {object} map[string]interface{}
// @Failure 401 {object} map[string]interface{}
// @Failure 403 {object} map[string]interface{}
// @Failure 404 {object} map[string]interface{}
// @Router /trainings/{id} [put]
func (h *TrainingHandler) UpdateTraining(c *gin.Context) {
	trainingID, err := strconv.ParseUint(c.Param("id"), 10, 32)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid training ID"})
		return
	}

	userID, exists := c.Get("user_id")
	if !exists {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "User not found in context"})
		return
	}

	var req models.TrainingUpdate
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	var training models.Training
	if err := h.db.First(&training, trainingID).Error; err != nil {
		if err == gorm.ErrRecordNotFound {
			c.JSON(http.StatusNotFound, gin.H{"error": "Training not found"})
		} else {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to retrieve training"})
		}
		return
	}

	// Check if user owns this training
	if training.UserID != userID.(uint) {
		c.JSON(http.StatusForbidden, gin.H{"error": "You can only update your own trainings"})
		return
	}

	// Update fields if provided
	if req.Name != "" {
		training.Name = req.Name
	}
	if req.Description != "" {
		training.Description = req.Description
	}
	if req.ProfessorID != 0 {
		// Verify professor exists
		var professor models.Professor
		if err := h.db.First(&professor, req.ProfessorID).Error; err != nil {
			if err == gorm.ErrRecordNotFound {
				c.JSON(http.StatusBadRequest, gin.H{"error": "Professor not found"})
			} else {
				c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to verify professor"})
			}
			return
		}
		training.ProfessorID = req.ProfessorID
	}
	if req.Repetitions != 0 {
		training.Repetitions = req.Repetitions
	}
	if req.Sets != 0 {
		training.Sets = req.Sets
	}

	if err := h.db.Save(&training).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to update training"})
		return
	}

	// Load relationships
	if err := h.db.Preload("User").Preload("Professor").Preload("TrainingExercises.Exercise").
		First(&training, training.ID).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to load training details"})
		return
	}

	c.JSON(http.StatusOK, training)
}

// DeleteTraining godoc
// @Summary Delete training
// @Description Delete a training
// @Tags trainings
// @Accept json
// @Produce json
// @Param id path int true "Training ID"
// @Security ApiKeyAuth
// @Success 204
// @Failure 400 {object} map[string]interface{}
// @Failure 401 {object} map[string]interface{}
// @Failure 403 {object} map[string]interface{}
// @Failure 404 {object} map[string]interface{}
// @Router /trainings/{id} [delete]
func (h *TrainingHandler) DeleteTraining(c *gin.Context) {
	trainingID, err := strconv.ParseUint(c.Param("id"), 10, 32)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid training ID"})
		return
	}

	userID, exists := c.Get("user_id")
	if !exists {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "User not found in context"})
		return
	}

	var training models.Training
	if err := h.db.First(&training, trainingID).Error; err != nil {
		if err == gorm.ErrRecordNotFound {
			c.JSON(http.StatusNotFound, gin.H{"error": "Training not found"})
		} else {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to retrieve training"})
		}
		return
	}

	// Check if user owns this training
	if training.UserID != userID.(uint) {
		c.JSON(http.StatusForbidden, gin.H{"error": "You can only delete your own trainings"})
		return
	}

	if err := h.db.Delete(&training).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to delete training"})
		return
	}

	c.Status(http.StatusNoContent)
}

// AddExerciseToTraining godoc
// @Summary Add exercise to training
// @Description Add an exercise to a training
// @Tags trainings
// @Accept json
// @Produce json
// @Param id path int true "Training ID"
// @Param exercise body models.TrainingExerciseCreate true "Exercise data"
// @Security ApiKeyAuth
// @Success 201 {object} models.TrainingExercise
// @Failure 400 {object} map[string]interface{}
// @Failure 401 {object} map[string]interface{}
// @Failure 403 {object} map[string]interface{}
// @Failure 404 {object} map[string]interface{}
// @Router /trainings/{id}/exercises [post]
func (h *TrainingHandler) AddExerciseToTraining(c *gin.Context) {
	trainingID, err := strconv.ParseUint(c.Param("id"), 10, 32)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid training ID"})
		return
	}

	userID, exists := c.Get("user_id")
	if !exists {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "User not found in context"})
		return
	}

	var req models.TrainingExerciseCreate
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Verify training exists and user owns it
	var training models.Training
	if err := h.db.First(&training, trainingID).Error; err != nil {
		if err == gorm.ErrRecordNotFound {
			c.JSON(http.StatusNotFound, gin.H{"error": "Training not found"})
		} else {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to retrieve training"})
		}
		return
	}

	if training.UserID != userID.(uint) {
		c.JSON(http.StatusForbidden, gin.H{"error": "You can only modify your own trainings"})
		return
	}

	// Verify exercise exists
	var exercise models.Exercise
	if err := h.db.First(&exercise, req.ExerciseID).Error; err != nil {
		if err == gorm.ErrRecordNotFound {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Exercise not found"})
		} else {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to verify exercise"})
		}
		return
	}

	// Create training exercise
	trainingExercise := models.TrainingExercise{
		TrainingID:  uint(trainingID),
		ExerciseID:  req.ExerciseID,
		Repetitions: req.Repetitions,
		Sets:        req.Sets,
	}

	if err := h.db.Create(&trainingExercise).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to add exercise to training"})
		return
	}

	// Load relationships
	if err := h.db.Preload("Training").Preload("Exercise").First(&trainingExercise, trainingExercise.ID).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to load exercise details"})
		return
	}

	c.JSON(http.StatusCreated, trainingExercise)
}
