import face_recognition
import os


class PhotoAnalyses:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image_with_face = []
        self.abstract_images = []
        self.people_without_main_person = 0
        self.coincidences = -1  # because 1 image will be compare with itself
        self.people_with_main_person = 0

    def return_image_with_one_face(self):
        """
        divide image to categories
        """
        for i in os.listdir(self.image_path):
            image = face_recognition.load_image_file(self.image_path + i)
            face_locations = face_recognition.face_locations(image)

            if len(face_locations) >= 1:
                self.image_with_face.append(i)
            else:
                self.abstract_images.append(i)

    def definition_main_person(self):
        """
        definition main person on images
        """

        for i in self.image_with_face:
            temp = -1
            image = face_recognition.load_image_file(self.image_path + i)
            known_encoding = face_recognition.face_encodings(image)[0]
            # print(i)
            for k in self.image_with_face:
                unknown_image = face_recognition.load_image_file(self.image_path + k)
                # print(k)
                unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
                results = face_recognition.compare_faces([known_encoding], unknown_encoding)
                temp += 1 if results == [True] else 0
                if self.coincidences < temp:
                    self.coincidences = temp
                    self.people_without_main_person = len(os.listdir(self.image_path)) - self.coincidences
                    if len(unknown_encoding) >= 2 and results == [True]:
                        self.people_with_main_person = + 1

    def show_results(self):
        self.return_image_with_one_face()
        self.definition_main_person()

        print("Количество фотографий где есть пользователь: {}".format(self.coincidences))
        print("Количество фотографий пользователя с другими людьми: {}".format(self.people_with_main_person))
        print("Фотографии других людей, без пользователя: {}".format(self.people_without_main_person))
        print("Абстрактные фотографии: {}".format(len(self.abstract_images)))


temp = PhotoAnalyses('./images/')
a = temp.show_results()
