import cv2
from deepface import DeepFace

def detect_deepfake(video_path):
    # Load the pre-trained face detection model from OpenCV
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        # Read a frame from the video
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Check if faces are present in the frame
        if len(faces) > 0:
            # Crop the detected face(s) and use DeepFace for verification
            for (x, y, w, h) in faces:
                face = frame[y:y+h, x:x+w]
                try:
                    result = DeepFace.verify(
                        img1_path=face,
                        img2_path=r"E:\python\referanceimage.jpg",
                        detector_backend='opencv',
                        model_name="Facenet"
                    )
                    # The 'verified' field indicates if the content is likely manipulated
                    if result.get("verified", False):
                        print("This video may contain deepfake")
                    else:
                        print("No deepfake detected.")
                except Exception as e:
                    print("Error:", str(e))

        # Display the frame
        cv2.imshow('Frame', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close all windows
    cap.release()
    cv2.destroyAllWindows()


# Replace with your actual video path
video_path = r"E:\python\video_name.mp4"
detect_deepfake(video_path)
