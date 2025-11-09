# test_complex_app.py
# -------------------------------------------------------------
# These tests check how the Flask app handles image uploads.
# They send real POST requests to the /prediction route and
# replace the heavy model functions with simple fake ones.
# One test checks the "happy" (success) path, and the other
# checks the "sad" (error) path.
# -------------------------------------------------------------

import io
import pytest
from app import app as flask_app
import app as app_module  # lets us patch preprocess_img and predict_result


@pytest.fixture()
def app():
    # Enable Flask test mode
    flask_app.config.update({"TESTING": True})
    yield flask_app

@pytest.fixture()
def client(app):
    # Create a test client to send fake HTTP requests
    return app.test_client()

@pytest.fixture()
def sample_png_bytes():
    # Tiny "fake" PNG file, enough for testing file uploads
    return b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR" + b"\x00" * 40


# -------------------- Helper Function --------------------
def _post_image(client, img_bytes):
    """Send a fake image file to the /prediction route."""
    data = {"file": (io.BytesIO(img_bytes), "hand.png")}
    res = client.post("/prediction", data=data, content_type="multipart/form-data")
    return res


# -------------------- Test 1: Happy Path --------------------
def test_predict_happy_path(client, sample_png_bytes, monkeypatch):
    """Test that a valid image upload returns a prediction."""

    # This fake function replaces preprocess_img().
    # It checks that some data is read and then returns a simple value.
    def fake_preprocess_img(stream):
        data = stream.read()
        assert len(data) > 0  # proves the file reached this stage
        return "IMG"

    # This fake function replaces predict_result().
    # It takes the fake "processed" image and returns a fixed prediction.
    def fake_predict_result(img):
        assert img == "IMG"
        return "digit-3"

    # Replace the real functions in the app with our fake ones
    monkeypatch.setattr(app_module, "preprocess_img", fake_preprocess_img)
    monkeypatch.setattr(app_module, "predict_result", fake_predict_result)

    # Send a POST request with the fake image
    res = _post_image(client, sample_png_bytes)

    # Check that the response is OK (status 200)
    # and that it includes our fake prediction text.
    assert res.status_code == 200
    text = res.get_data(as_text=True)
    assert "digit-3" in text or "predictions" in text


# -------------------- Test 2: Sad Path --------------------
def test_predict_sad_path_invalid_image(client, monkeypatch):
    """Test that an invalid image shows an error message."""

    # Create a fake error type to simulate a bad image
    class UnsupportedImageError(ValueError):
        pass

    # This fake preprocess function always raises an error
    def fake_preprocess_img_raises(_stream):
        raise UnsupportedImageError("Unsupported or corrupted image")

    # Patch only preprocess_img to raise the error
    monkeypatch.setattr(app_module, "preprocess_img", fake_preprocess_img_raises)

    # Send a bad "image" (just plain text bytes)
    bad_bytes = b"not-an-image"
    res = _post_image(client, bad_bytes)

    # The app catches the error and renders an error page
    assert res.status_code == 200  # Flask still returns 200 for error template
    text = res.get_data(as_text=True)
    assert "File cannot be processed." in text or "err" in text
