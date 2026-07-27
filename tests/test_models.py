"""Tests for data models."""

from mcp_server_linkedin.models.linkedin import (
    LinkedInProfile,
    MediaUploadInfo,
    PostResult,
)


class TestLinkedInProfile:
    """Tests for LinkedInProfile model."""

    def test_from_api_response(self, sample_profile_response: dict) -> None:
        profile = LinkedInProfile.from_api_response(sample_profile_response)
        assert profile.sub == "abc123def"
        assert profile.name == "Jane Developer"
        assert profile.email == "jane@example.com"
        assert profile.picture == "https://media.linkedin.com/photo.jpg"

    def test_person_urn(self) -> None:
        profile = LinkedInProfile(sub="xyz789", name="Test", email="t@t.com")
        assert profile.person_urn == "urn:li:person:xyz789"

    def test_format_display_with_picture(self) -> None:
        profile = LinkedInProfile(
            sub="abc", name="Alice", email="a@b.com", picture="https://img.url"
        )
        display = profile.format_display()
        assert "Alice" in display
        assert "a@b.com" in display
        assert "urn:li:person:abc" in display
        assert "https://img.url" in display

    def test_format_display_without_picture(self) -> None:
        profile = LinkedInProfile(sub="abc", name="Alice", email="a@b.com")
        display = profile.format_display()
        assert "Picture" not in display

    def test_from_api_response_missing_optional_fields(self) -> None:
        data = {"sub": "id1", "name": "Bob", "email": "bob@test.com"}
        profile = LinkedInProfile.from_api_response(data)
        assert profile.picture is None

    def test_frozen_immutability(self) -> None:
        profile = LinkedInProfile(sub="abc", name="Test", email="t@t.com")
        try:
            profile.name = "Changed"  # type: ignore[misc]
            assert False, "Should have raised FrozenInstanceError"
        except AttributeError:
            pass


class TestMediaUploadInfo:
    """Tests for MediaUploadInfo model."""

    def test_from_api_response(self, sample_register_upload_response: dict) -> None:
        info = MediaUploadInfo.from_api_response(sample_register_upload_response)
        assert info.upload_url == "https://api.linkedin.com/mediaUpload/xxx/upload"
        assert info.asset_urn == "urn:li:digitalmediaAsset:D123456"

    def test_frozen_immutability(self) -> None:
        info = MediaUploadInfo(upload_url="https://x.com", asset_urn="urn:test")
        try:
            info.upload_url = "changed"  # type: ignore[misc]
            assert False, "Should have raised FrozenInstanceError"
        except AttributeError:
            pass


class TestPostResult:
    """Tests for PostResult model."""

    def test_from_api_response(self, sample_post_response: dict) -> None:
        result = PostResult.from_api_response(sample_post_response)
        assert result.post_id == "urn:li:ugcPost:7654321"
        assert result.post_urn == "urn:li:ugcPost:7654321"

    def test_from_api_response_missing_id(self) -> None:
        result = PostResult.from_api_response({})
        assert result.post_id == "unknown"
