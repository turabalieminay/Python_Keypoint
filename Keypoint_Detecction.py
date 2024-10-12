import cv2
import numpy as np
from ultralytics import YOLO

# Resim ve model dosya yolları (Spyder ortamında yerel dosya yollarını kullanın)
img_path = "test.jpg"  # Resim dosyanızın yolunu buraya ekleyin
model_path = "yolov8n-pose.pt"  # Pose model dosyanızın yolunu buraya ekleyin

# Resmi yükle
img = cv2.imread(img_path)

# YOLO modelini yükle (Pose modelini kullanıyoruz)
model = YOLO(model_path)

# Model ile tespit yap
results = model.predict(source=img, save=False, save_txt=False)[0]

# Tüm tespit edilen nesneleri çiz
for result in results:
    # Bounding box'ları al
    boxes = result.boxes.xyxy.cpu().numpy().astype(int)
    scores = result.boxes.conf.cpu().numpy()  # Güven skorları
    class_ids = result.boxes.cls.cpu().numpy().astype(int)  # Sınıf ID'leri
    class_names = model.names  # Modeldeki sınıf isimleri (örn: person)

    for box, score, class_id in zip(boxes, scores, class_ids):
        (xmin, ymin, xmax, ymax) = box

        # Sınıf ismi ve güven skorunu ekleyelim
        class_name = class_names[class_id]
        label = f"{class_name}: {score:.2f}"
        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)  # Yeşil dikdörtgen
        cv2.putText(img, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)  # Kırmızı yazı

    # Keypoint'leri al
    keypoints = np.array(result.keypoints.xy.cpu(), dtype="int")

    # Her keypoint'in (x, y) koordinatlarını kullanarak mavi küçük daireler çizelim
    for point in keypoints[0]:
        cv2.circle(img, (point[0], point[1]), 5, (255, 0, 0), -1)  # Küçük mavi daireler

# İşlenmiş resmi ekranda göster
cv2.imshow("Pose Detection", img)

# Ekranda resmi kapatmak için bir tuşa basmayı bekle
cv2.waitKey(0)
cv2.destroyAllWindows()
