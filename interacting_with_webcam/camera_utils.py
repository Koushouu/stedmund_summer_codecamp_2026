import sys
import cv2


def open_camera(index=0, fallback_video=None, width=640, height=480):
    """
    Open a webcam and return the VideoCapture object.

    index          : which camera to use (0 is usually the built-in one)
    fallback_video : path to a video file to use if no webcam is found
    width, height  : requested frame size (the camera may ignore this)

    Raises SystemExit with a friendly message if nothing can be opened.
    """
    # On macOS, AVFoundation is the reliable backend.
    if sys.platform == "darwin":
        cap = cv2.VideoCapture(index, cv2.CAP_AVFOUNDATION)
    else:
        cap = cv2.VideoCapture(index)

    if cap.isOpened():
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        return cap

    # Webcam failed. Try the fallback video file.
    if fallback_video is not None:
        cap = cv2.VideoCapture(fallback_video)
        if cap.isOpened():
            print(f"[camera_utils] No webcam found. Using video file: {fallback_video}")
            return cap

    raise SystemExit(
        "\n[camera_utils] Could not open a camera.\n"
        "  - Is another app (Zoom, Teams, WeChat) already using it?\n"
        "  - On macOS: System Settings > Privacy & Security > Camera,\n"
        "    and allow your terminal / VS Code.\n"
        "  - Try open_camera(index=1) if you have an external camera.\n"
        "  - Or ask your instructor for the fallback video file.\n"
    )


def read_frame(cap, mirror=True):
    """
    Read one frame. Returns None when the stream ends.

    mirror=True flips the image left-right so it behaves like a mirror.
    This matters a lot for hand tracking: without it, moving your hand
    right makes the image move left, which feels wrong.
    """
    ok, frame = cap.read()
    if not ok:
        return None
    if mirror:
        frame = cv2.flip(frame, 1)
    return frame


def show_fps(frame, fps):
    """Draw the frames-per-second counter in the top-left corner."""
    cv2.putText(
        frame, f"{fps:.1f} FPS", (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2
    )
    return frame


def cleanup(cap):
    """Always call this at the end, or your camera light stays on."""
    cap.release()
    cv2.destroyAllWindows()