from services import Deepface

model = Deepface()

print(model.detect_face('noface.png'))