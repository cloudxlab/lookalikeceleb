import face_recognition
import os
import numpy as np

def load_images(known_images_dir):
    known_encodings = []
    known_images = []

    for file in os.listdir(known_images_dir):
        print("Loading ", file)
        filename = os.fsdecode(file)
        image = face_recognition.load_image_file(os.path.join(known_images_dir, filename))
        # print(image.shape)
        
        enc = face_recognition.face_encodings(image)
        if len(enc) > 0:
            known_encodings.append(enc[0])
            known_images.append(filename)
        else:
            print("Face not found in ", file)
    return (known_encodings, known_images)

def cosine_closest(known_encodings, img):
    cs = np.array(known_encodings).dot(np.array(img))
    return cs.argmax()

def calculate_face_distance(known_encodings, unknown_img_path, cutoff=0.5, num_results=4):
    # Load a test image and get encondings for it
    image_to_test = face_recognition.load_image_file(unknown_img_path)
    image_to_test_encoding = face_recognition.face_encodings(image_to_test)[0]

    # See how far apart the test image is from the known faces
    face_distances = face_recognition.face_distance(known_encodings, image_to_test_encoding)
    return (unknown_img_path, known_images[face_distances.argmin()])

known_encodings, known_images = load_images("images")

print(calculate_face_distance(known_encodings, "sandeep.jpg"))
print(calculate_face_distance(known_encodings, "sandeep1.jpg"))
print(calculate_face_distance(known_encodings, "abhinav.jpeg"))
print(calculate_face_distance(known_encodings, "akode.jpeg"))
print(calculate_face_distance(known_encodings, "aswath.jpeg"))