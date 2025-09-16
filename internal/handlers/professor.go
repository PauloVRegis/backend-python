package handlers

import (
	"net/http"
	"strconv"

	"backend-python/internal/database"
	"backend-python/internal/models"

	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
)

type ProfessorHandler struct {
	db *gorm.DB
}

func NewProfessorHandler() *ProfessorHandler {
	return &ProfessorHandler{
		db: database.GetDB(),
	}
}

// GetProfessors godoc
// @Summary Get all professors
// @Description Get all professors with pagination
// @Tags professors
// @Accept json
// @Produce json
// @Param skip query int false "Skip records" default(0)
// @Param limit query int false "Limit records" default(100)
// @Success 200 {array} models.Professor
// @Failure 400 {object} map[string]interface{}
// @Failure 500 {object} map[string]interface{}
// @Router /professors [get]
func (h *ProfessorHandler) GetProfessors(c *gin.Context) {
	skip, _ := strconv.Atoi(c.DefaultQuery("skip", "0"))
	limit, _ := strconv.Atoi(c.DefaultQuery("limit", "100"))

	if limit > 1000 {
		limit = 1000
	}

	var professors []models.Professor
	if err := h.db.Offset(skip).Limit(limit).Find(&professors).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to retrieve professors"})
		return
	}

	c.JSON(http.StatusOK, professors)
}

// GetProfessor godoc
// @Summary Get professor by ID
// @Description Get a specific professor by ID
// @Tags professors
// @Accept json
// @Produce json
// @Param id path int true "Professor ID"
// @Success 200 {object} models.Professor
// @Failure 400 {object} map[string]interface{}
// @Failure 404 {object} map[string]interface{}
// @Router /professors/{id} [get]
func (h *ProfessorHandler) GetProfessor(c *gin.Context) {
	professorID, err := strconv.ParseUint(c.Param("id"), 10, 32)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid professor ID"})
		return
	}

	var professor models.Professor
	if err := h.db.Preload("Trainings").First(&professor, professorID).Error; err != nil {
		if err == gorm.ErrRecordNotFound {
			c.JSON(http.StatusNotFound, gin.H{"error": "Professor not found"})
		} else {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to retrieve professor"})
		}
		return
	}

	c.JSON(http.StatusOK, professor)
}

// CreateProfessor godoc
// @Summary Create a new professor
// @Description Create a new professor
// @Tags professors
// @Accept json
// @Produce json
// @Param professor body models.ProfessorCreate true "Professor data"
// @Security ApiKeyAuth
// @Success 201 {object} models.Professor
// @Failure 400 {object} map[string]interface{}
// @Failure 401 {object} map[string]interface{}
// @Failure 409 {object} map[string]interface{}
// @Failure 500 {object} map[string]interface{}
// @Router /professors [post]
func (h *ProfessorHandler) CreateProfessor(c *gin.Context) {
	var req models.ProfessorCreate
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Check if professor with this email already exists
	var existingProfessor models.Professor
	if err := h.db.Where("email = ?", req.Email).First(&existingProfessor).Error; err == nil {
		c.JSON(http.StatusConflict, gin.H{"error": "Professor with this email already exists"})
		return
	}

	// Create professor
	professor := models.Professor{
		Name:        req.Name,
		Email:       req.Email,
		Phone:       req.Phone,
		Bio:         req.Bio,
		Specialties: req.Specialties,
	}

	if err := h.db.Create(&professor).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to create professor"})
		return
	}

	c.JSON(http.StatusCreated, professor)
}

// UpdateProfessor godoc
// @Summary Update professor
// @Description Update professor information
// @Tags professors
// @Accept json
// @Produce json
// @Param id path int true "Professor ID"
// @Param professor body models.ProfessorUpdate true "Professor data"
// @Security ApiKeyAuth
// @Success 200 {object} models.Professor
// @Failure 400 {object} map[string]interface{}
// @Failure 401 {object} map[string]interface{}
// @Failure 404 {object} map[string]interface{}
// @Failure 409 {object} map[string]interface{}
// @Router /professors/{id} [put]
func (h *ProfessorHandler) UpdateProfessor(c *gin.Context) {
	professorID, err := strconv.ParseUint(c.Param("id"), 10, 32)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid professor ID"})
		return
	}

	var req models.ProfessorUpdate
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	var professor models.Professor
	if err := h.db.First(&professor, professorID).Error; err != nil {
		if err == gorm.ErrRecordNotFound {
			c.JSON(http.StatusNotFound, gin.H{"error": "Professor not found"})
		} else {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to retrieve professor"})
		}
		return
	}

	// Update fields if provided
	if req.Name != "" {
		professor.Name = req.Name
	}
	if req.Email != "" {
		// Check if email is already taken by another professor
		var existingProfessor models.Professor
		if err := h.db.Where("email = ? AND id != ?", req.Email, professorID).First(&existingProfessor).Error; err == nil {
			c.JSON(http.StatusConflict, gin.H{"error": "Email already taken"})
			return
		}
		professor.Email = req.Email
	}
	if req.Phone != "" {
		professor.Phone = req.Phone
	}
	if req.Bio != "" {
		professor.Bio = req.Bio
	}
	if req.Specialties != "" {
		professor.Specialties = req.Specialties
	}

	if err := h.db.Save(&professor).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to update professor"})
		return
	}

	c.JSON(http.StatusOK, professor)
}

// DeleteProfessor godoc
// @Summary Delete professor
// @Description Delete a professor
// @Tags professors
// @Accept json
// @Produce json
// @Param id path int true "Professor ID"
// @Security ApiKeyAuth
// @Success 204
// @Failure 400 {object} map[string]interface{}
// @Failure 401 {object} map[string]interface{}
// @Failure 404 {object} map[string]interface{}
// @Router /professors/{id} [delete]
func (h *ProfessorHandler) DeleteProfessor(c *gin.Context) {
	professorID, err := strconv.ParseUint(c.Param("id"), 10, 32)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid professor ID"})
		return
	}

	var professor models.Professor
	if err := h.db.First(&professor, professorID).Error; err != nil {
		if err == gorm.ErrRecordNotFound {
			c.JSON(http.StatusNotFound, gin.H{"error": "Professor not found"})
		} else {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to retrieve professor"})
		}
		return
	}

	if err := h.db.Delete(&professor).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to delete professor"})
		return
	}

	c.Status(http.StatusNoContent)
}
