package handlers

import (
	"net/http"
	"strconv"

	"backend-python/internal/auth"
	"backend-python/internal/database"
	"backend-python/internal/models"

	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
)

type UserHandler struct {
	db *gorm.DB
}

func NewUserHandler() *UserHandler {
	return &UserHandler{
		db: database.GetDB(),
	}
}

// GetUsers godoc
// @Summary Get all users
// @Description Get all users with pagination
// @Tags users
// @Accept json
// @Produce json
// @Param skip query int false "Skip records" default(0)
// @Param limit query int false "Limit records" default(100)
// @Security ApiKeyAuth
// @Success 200 {array} models.UserResponse
// @Failure 400 {object} map[string]interface{}
// @Failure 401 {object} map[string]interface{}
// @Failure 500 {object} map[string]interface{}
// @Router /users [get]
func (h *UserHandler) GetUsers(c *gin.Context) {
	skip, _ := strconv.Atoi(c.DefaultQuery("skip", "0"))
	limit, _ := strconv.Atoi(c.DefaultQuery("limit", "100"))

	if limit > 1000 {
		limit = 1000
	}

	var users []models.User
	if err := h.db.Offset(skip).Limit(limit).Find(&users).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to retrieve users"})
		return
	}

	// Convert to response format
	var response []models.UserResponse
	for _, user := range users {
		response = append(response, models.UserResponse{
			ID:        user.ID,
			Email:     user.Email,
			Name:      user.Name,
			CreatedAt: user.CreatedAt,
		})
	}

	c.JSON(http.StatusOK, response)
}

// GetUser godoc
// @Summary Get user by ID
// @Description Get a specific user by ID
// @Tags users
// @Accept json
// @Produce json
// @Param id path int true "User ID"
// @Security ApiKeyAuth
// @Success 200 {object} models.UserResponse
// @Failure 400 {object} map[string]interface{}
// @Failure 401 {object} map[string]interface{}
// @Failure 404 {object} map[string]interface{}
// @Router /users/{id} [get]
func (h *UserHandler) GetUser(c *gin.Context) {
	userID, err := strconv.ParseUint(c.Param("id"), 10, 32)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid user ID"})
		return
	}

	var user models.User
	if err := h.db.First(&user, userID).Error; err != nil {
		if err == gorm.ErrRecordNotFound {
			c.JSON(http.StatusNotFound, gin.H{"error": "User not found"})
		} else {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to retrieve user"})
		}
		return
	}

	response := models.UserResponse{
		ID:        user.ID,
		Email:     user.Email,
		Name:      user.Name,
		CreatedAt: user.CreatedAt,
	}

	c.JSON(http.StatusOK, response)
}

// CreateUser godoc
// @Summary Create a new user
// @Description Create a new user with email and password
// @Tags users
// @Accept json
// @Produce json
// @Param user body models.UserCreate true "User data"
// @Success 201 {object} models.UserResponse
// @Failure 400 {object} map[string]interface{}
// @Failure 409 {object} map[string]interface{}
// @Failure 500 {object} map[string]interface{}
// @Router /users [post]
func (h *UserHandler) CreateUser(c *gin.Context) {
	var req models.UserCreate
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Check if user already exists
	var existingUser models.User
	if err := h.db.Where("email = ?", req.Email).First(&existingUser).Error; err == nil {
		c.JSON(http.StatusConflict, gin.H{"error": "User with this email already exists"})
		return
	}

	// Hash password
	hashedPassword, err := auth.HashPassword(req.Password)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to hash password"})
		return
	}

	// Create user
	user := models.User{
		Email:        req.Email,
		Name:         req.Name,
		PasswordHash: hashedPassword,
	}

	if err := h.db.Create(&user).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to create user"})
		return
	}

	response := models.UserResponse{
		ID:        user.ID,
		Email:     user.Email,
		Name:      user.Name,
		CreatedAt: user.CreatedAt,
	}

	c.JSON(http.StatusCreated, response)
}

// UpdateUser godoc
// @Summary Update user
// @Description Update user information
// @Tags users
// @Accept json
// @Produce json
// @Param id path int true "User ID"
// @Param user body models.UserUpdate true "User data"
// @Security ApiKeyAuth
// @Success 200 {object} models.UserResponse
// @Failure 400 {object} map[string]interface{}
// @Failure 401 {object} map[string]interface{}
// @Failure 403 {object} map[string]interface{}
// @Failure 404 {object} map[string]interface{}
// @Router /users/{id} [put]
func (h *UserHandler) UpdateUser(c *gin.Context) {
	userID, err := strconv.ParseUint(c.Param("id"), 10, 32)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid user ID"})
		return
	}

	// Check if user can update this profile
	currentUserID, exists := c.Get("user_id")
	if !exists || currentUserID != uint(userID) {
		c.JSON(http.StatusForbidden, gin.H{"error": "You can only update your own profile"})
		return
	}

	var req models.UserUpdate
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	var user models.User
	if err := h.db.First(&user, userID).Error; err != nil {
		if err == gorm.ErrRecordNotFound {
			c.JSON(http.StatusNotFound, gin.H{"error": "User not found"})
		} else {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to retrieve user"})
		}
		return
	}

	// Update fields if provided
	if req.Email != "" {
		// Check if email is already taken by another user
		var existingUser models.User
		if err := h.db.Where("email = ? AND id != ?", req.Email, userID).First(&existingUser).Error; err == nil {
			c.JSON(http.StatusConflict, gin.H{"error": "Email already taken"})
			return
		}
		user.Email = req.Email
	}
	if req.Name != "" {
		user.Name = req.Name
	}

	if err := h.db.Save(&user).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to update user"})
		return
	}

	response := models.UserResponse{
		ID:        user.ID,
		Email:     user.Email,
		Name:      user.Name,
		CreatedAt: user.CreatedAt,
	}

	c.JSON(http.StatusOK, response)
}

// DeleteUser godoc
// @Summary Delete user
// @Description Delete a user account
// @Tags users
// @Accept json
// @Produce json
// @Param id path int true "User ID"
// @Security ApiKeyAuth
// @Success 204
// @Failure 400 {object} map[string]interface{}
// @Failure 401 {object} map[string]interface{}
// @Failure 403 {object} map[string]interface{}
// @Failure 404 {object} map[string]interface{}
// @Router /users/{id} [delete]
func (h *UserHandler) DeleteUser(c *gin.Context) {
	userID, err := strconv.ParseUint(c.Param("id"), 10, 32)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid user ID"})
		return
	}

	// Check if user can delete this profile
	currentUserID, exists := c.Get("user_id")
	if !exists || currentUserID != uint(userID) {
		c.JSON(http.StatusForbidden, gin.H{"error": "You can only delete your own profile"})
		return
	}

	var user models.User
	if err := h.db.First(&user, userID).Error; err != nil {
		if err == gorm.ErrRecordNotFound {
			c.JSON(http.StatusNotFound, gin.H{"error": "User not found"})
		} else {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to retrieve user"})
		}
		return
	}

	if err := h.db.Delete(&user).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to delete user"})
		return
	}

	c.Status(http.StatusNoContent)
}
