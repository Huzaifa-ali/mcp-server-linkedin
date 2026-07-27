"""Shared test fixtures."""

import pytest


@pytest.fixture
def sample_profile_response() -> dict:
    """Sample LinkedIn userinfo API response."""
    return {
        "sub": "abc123def",
        "name": "Jane Developer",
        "email": "jane@example.com",
        "picture": "https://media.linkedin.com/photo.jpg",
    }


@pytest.fixture
def sample_post_response() -> dict:
    """Sample UGC post creation response."""
    return {
        "id": "urn:li:ugcPost:7654321",
    }


@pytest.fixture
def sample_register_upload_response() -> dict:
    """Sample register-upload API response."""
    return {
        "value": {
            "uploadMechanism": {
                "com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest": {
                    "uploadUrl": "https://api.linkedin.com/mediaUpload/xxx/upload"
                }
            },
            "asset": "urn:li:digitalmediaAsset:D123456",
        }
    }
