package handlers

import (
	"net/http"
	"strconv"

	"backend-python/internal/database"
	"backend-python/internal/models"

	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
)

type ExerciseHandler struct {
	db *gorm.DB
}

func NewExerciseHandler() *ExerciseHandler {
	return &ExerciseHandler{
		db: database.GetDB(),
	}
}

// GetExercises godoc
// @Summary Get all exercises
// @Description Get all exercises with pagination and optional filtering
// @Tags exercises
// @Accept json
// @Produce json
// @Param skip query int false "Skip records" default(0)
// @Param limit query int false "Limit records" default(100)
// @Param muscle_group query string false "Filter by muscle group"
// @Param difficulty query string false "Filter by difficulty"
// @Success 200 {array} models.Exercise
// @Failure 400 {object} map[string]interface{}
// @Failure 500 {object} map[string]interface{}
// @Router /exercises [get]
func (h *ExerciseHandler) GetExercises(c *gin.Context) {
	skip, _ := strconv.Atoi(c.DefaultQuery("skip", "0"))
	limit, _ := strconv.Atoi(c.DefaultQuery("limit", "100"))
	muscleGroup := c.Query("muscle_group")
	difficulty := c.Query("difficulty")

	if limit > 1000 {
		limit = 1000
	}

	query := h.db.Offset(skip).Limit(limit)

	// Apply filters
	if muscleGroup != "" {
		query = query.Where("muscle_group = ?", muscleGroup)
	}
	if difficulty != "" {
		query = query.Where("difficulty = ?", difficulty)
	}

	var exercises []models.Exercise
	if err := query.Find(&exercises).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to retrieve exercises"})
		return
	}

	c.JSON(http.StatusOK, exercises)
}

// GetExercise godoc
// @Summary Get exercise by ID
// @Description Get a specific exercise by ID
// @Tags exercises
// @Accept json
// @Produce json
// @Param id path int true "Exercise ID"
// @Success 200 {object} models.Exercise
// @Failure 400 {object} map[string]interface{}
// @Failure 404 {object} map[string]interface{}
// @Router /exercises/{id} [get]
func (h *ExerciseHandler) GetExercise(c *gin.Context) {
	exerciseID, err := strconv.ParseUint(c.Param("id"), 10, 32)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid exercise ID"})
		return
	}

	var exercise models.Exercise
	if err := h.db.First(&exercise, exerciseID).Error; err != nil {
		if err == gorm.ErrRecordNotFound {
			c.JSON(http.StatusNotFound, gin.H{"error": "Exercise not found"})
		} else {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to retrieve exercise"})
		}
		return
	}

	c.JSON(http.StatusOK, exercise)
}

// CreateExercise godoc
// @Summary Create a new exercise
// @Description Create a new exercise
// @Tags exercises
// @Accept json
// @Produce json
// @Param exercise body models.ExerciseCreate true "Exercise data"
// @Security ApiKeyAuth
// @Success 201 {object} models.Exercise
// @Failure 400 {object} map[string]interface{}
// @Failure 401 {object} map[string]interface{}
// @Failure 500 {object} map[string]interface{}
// @Router /exercises [post]
func (h *ExerciseHandler) CreateExercise(c *gin.Context) {
	var req models.ExerciseCreate
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Create exercise
	exercise := models.Exercise{
		Name:         req.Name,
		Description:  req.Description,
		MuscleGroup:  req.MuscleGroup,
		Equipment:    req.Equipment,
		Difficulty:   req.Difficulty,
		Instructions: req.Instructions,
		ImageURL:     req.ImageURL,
		VideoURL:     req.VideoURL,
	}

	if err := h.db.Create(&exercise).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to create exercise"})
		return
	}

	c.JSON(http.StatusCreated, exercise)
}

// UpdateExercise godoc
// @Summary Update exercise
// @Description Update exercise information
// @Tags exercises
// @Accept json
// @Produce json
// @Param id path int true "Exercise ID"
// @Param exercise body models.ExerciseUpdate true "Exercise data"
// @Security ApiKeyAuth
// @Success 200 {object} models.Exercise
// @Failure 400 {object} map[string]interface{}
// @Failure 401 {object} map[string]interface{}
// @Failure 404 {object} map[string]interface{}
// @Router /exercises/{id} [put]
func (h *ExerciseHandler) UpdateExercise(c *gin.Context) {
	exerciseID, err := strconv.ParseUint(c.Param("id"), 10, 32)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid exercise ID"})
		return
	}

	var req models.ExerciseUpdate
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	var exercise models.Exercise
	if err := h.db.First(&exercise, exerciseID).Error; err != nil {
		if err == gorm.ErrRecordNotFound {
			c.JSON(http.StatusNotFound, gin.H{"error": "Exercise not found"})
		} else {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to retrieve exercise"})
		}
		return
	}

	// Update fields if provided
	if req.Name != "" {
		exercise.Name = req.Name
	}
	if req.Description != "" {
		exercise.Description = req.Description
	}
	if req.MuscleGroup != "" {
		exercise.MuscleGroup = req.MuscleGroup
	}
	if req.Equipment != "" {
		exercise.Equipment = req.Equipment
	}
	if req.Difficulty != "" {
		exercise.Difficulty = req.Difficulty
	}
	if req.Instructions != "" {
		exercise.Instructions = req.Instructions
	}
	if req.ImageURL != "" {
		exercise.ImageURL = req.ImageURL
	}
	if req.VideoURL != "" {
		exercise.VideoURL = req.VideoURL
	}

	if err := h.db.Save(&exercise).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to update exercise"})
		return
	}

	c.JSON(http.StatusOK, exercise)
}

// DeleteExercise godoc
// @Summary Delete exercise
// @Description Delete an exercise
// @Tags exercises
// @Accept json
// @Produce json
// @Param id path int true "Exercise ID"
// @Security ApiKeyAuth
// @Success 204
// @Failure 400 {object} map[string]interface{}
// @Failure 401 {object} map[string]interface{}
// @Failure 404 {object} map[string]interface{}
// @Router /exercises/{id} [delete]
func (h *ExerciseHandler) DeleteExercise(c *gin.Context) {
	exerciseID, err := strconv.ParseUint(c.Param("id"), 10, 32)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid exercise ID"})
		return
	}

	var exercise models.Exercise
	if err := h.db.First(&exercise, exerciseID).Error; err != nil {
		if err == gorm.ErrRecordNotFound {
			c.JSON(http.StatusNotFound, gin.H{"error": "Exercise not found"})
		} else {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to retrieve exercise"})
		}
		return
	}

	if err := h.db.Delete(&exercise).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to delete exercise"})
		return
	}

	c.Status(http.StatusNoContent)
}

// GetMuscleGroups godoc
// @Summary Get all muscle groups
// @Description Get a list of all available muscle groups
// @Tags exercises
// @Accept json
// @Produce json
// @Success 200 {array} string
// @Failure 500 {object} map[string]interface{}
// @Router /exercises/muscle-groups [get]
func (h *ExerciseHandler) GetMuscleGroups(c *gin.Context) {
	var muscleGroups []string
	if err := h.db.Model(&models.Exercise{}).Distinct("muscle_group").
		Where("muscle_group != ''").Pluck("muscle_group", &muscleGroups).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to retrieve muscle groups"})
		return
	}

	c.JSON(http.StatusOK, muscleGroups)
}
