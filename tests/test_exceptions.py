"""Tests for exception hierarchy."""

from mcp_server_linkedin.exceptions import (
    AuthenticationError,
    ConfigurationError,
    LinkedInAPIError,
    LinkedInMCPError,
    MediaUploadError,
    ValidationError,
)


class TestExceptionHierarchy:
    """Verify exception inheritance and attributes."""

    def test_all_inherit_from_base(self) -> None:
        assert issubclass(AuthenticationError, LinkedInMCPError)
        assert issubclass(ConfigurationError, LinkedInMCPError)
        assert issubclass(LinkedInAPIError, LinkedInMCPError)
        assert issubclass(MediaUploadError, LinkedInMCPError)
        assert issubclass(ValidationError, LinkedInMCPError)

    def test_authentication_error_default_message(self) -> None:
        err = AuthenticationError()
        assert "Not authenticated" in str(err)

    def test_configuration_error(self) -> None:
        err = ConfigurationError("Missing CLIENT_ID")
        assert "Missing CLIENT_ID" in str(err)

    def test_linkedin_api_error_attributes(self) -> None:
        err = LinkedInAPIError(
            "Failed to post", status_code=403, detail="Forbidden"
        )
        assert err.status_code == 403
        assert err.detail == "Forbidden"
        assert "403" in str(err)
        assert "Forbidden" in str(err)

    def test_linkedin_api_error_no_status(self) -> None:
        err = LinkedInAPIError("Something broke")
        assert err.status_code is None
        assert "Something broke" in str(err)

    def test_media_upload_error(self) -> None:
        err = MediaUploadError("File too large")
        assert "File too large" in str(err)

    def test_validation_error(self) -> None:
        err = ValidationError("Text cannot be empty")
        assert "Text cannot be empty" in str(err)
