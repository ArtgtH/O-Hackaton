package authHandlers

type (
	SignUpRequest struct {
		Email    string `json:"email"`
		Password string `json:"password"`
	}

	SignInRequest struct {
		Email    string `json:"email"`
		Password string `json:"password"`
	}

	SignInResponse struct {
		JWTToken string `json:"jwt_token"`
	}

	CheckUserRequest struct {
		Email string `json:"email"`
	}
)
