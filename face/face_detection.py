import cv2
import time
import face.face_const as fc


def validate_face(face, minial_size):
    if face[2] * face[3] >= minial_size:
        return True
    else:
        return False


def detect_face_haar(frame, minial_size, classifier="default"):
    """Detect faces from a frame
        works for front face without rotation
        return a frame of faces with rectangle emphasized
    """
    # print("===========", fc.classifier_dict[classifier])
    face_cascade = cv2.CascadeClassifier(fc.classifier_dict[classifier])
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(120, 120))
    # print("==========faces:", faces)
    valid_faces = [face for face in faces if validate_face(face, minial_size)]
    for (x, y, w, h) in valid_faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    # print("==========valid_faces:", valid_faces)
    return valid_faces


def detect_eyes_haar(frame, eye_classifier, face_classifier="default"):
    eye_cascade = cv2.CascadeClassifier(fc.classifier_dict[eye_classifier])
    faces = detect_face_haar(frame, face_classifier)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rois = [gray[y:y+h, x:x+w] for (x, y, w, h) in faces]
    eye_groups = [eye_cascade.detectMultiScale(roi, 1.03, 5, minSize=(40, 40)) for roi in rois]
    for i in range(len(faces)):
        x, y, w, h = faces[i]
        for eye in eye_groups[i]:
            ex, ey, ew, eh = eye
            cv2.circle(frame, (int(x + ex + ew / 2), int(y + ey + eh / 2)), max(ew, eh), (0, 0, 255))
    return


if __name__ == '__main__':
    # t0 = time.time()
    frame_path = r".\face_pictures\grammar-devotional.jpg"
    frame = cv2.imread(frame_path)
    detect_face_haar(frame, minial_size=9000, classifier="default")
    # detect_face_haar(frame, minial_size=900, classifier="alt_tree")
    # detect_eyes_haar(frame, "eye")
    cv2.imshow("frame", frame)
    cv2.waitKey(0)




