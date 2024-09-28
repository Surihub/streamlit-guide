import streamlit as st
from PIL import Image
import torch
from torchvision import models, transforms

# 1. 페이지 제목 설정
st.title("🤖 이미지 분류 AI")

# 2. 그림 파일 제출하기 섹션
st.subheader("어떤 사진인지 제가 판단해볼게요.")
uploaded_file = st.file_uploader("그림 파일을 업로드하세요(jpg, jpeg, png 확장자만 가능합니다.)", type=["jpg", "jpeg", "png"])

# 3. 이미지 분류를 위한 함수 정의
def predict_image(image):
    # 이미지가 RGB가 아닌 경우 변환
    if image.mode != "RGB":
        image = image.convert("RGB")
    
    # 이미지 전처리
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    
    img_tensor = preprocess(image).unsqueeze(0)
    
    # Pretrained ResNet 모델 로드
    model = models.resnet18(pretrained=True)
    model.eval()
    
    # 이미지 분류 실행
    with torch.no_grad():
        outputs = model(img_tensor)
    
    # 결과 처리
    _, predicted = outputs.max(1)
    
    # 클래스 이름 로드
    labels = open("data/imagenet_classes.txt").read().splitlines()
    predicted_label = labels[predicted.item()]
    
    return predicted_label

# 4. 파일 업로드 후 처리
if uploaded_file is not None:
    # 업로드한 파일 이름 출력
    st.write("업로드한 파일 이름:", uploaded_file.name)
    
    # 업로드한 이미지 미리보기
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드한 이미지", use_column_width=True)
    
    # 이미지 분류 실행
    label = predict_image(image)
    st.write(f"# 예측 결과 : {label}")
else:
    st.warning("이미지를 업로드하세요.")
