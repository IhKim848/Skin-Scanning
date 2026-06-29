# Skin Scan (피부질환 AI 스캐닝 및 병역판정 정보 제공 서비스)

## 주요 기능
1. **XAI 시각화**
   * 사용자 업로드 이미지를 기반으로 주요 피부 질환을 신속하게 분류합니다.
   * **Grad-CAM** 알고리즘을 적용하여 모델이 진단에 참고한 주요 특징 영역을 히트맵으로 시각화합니다.
2. **병역판정 신체검사 기준 맵핑**
   * AI 추론 결과를 병무청 「검사규칙 별표 3」 데이터와 맵핑하여 예상 등급 및 필요 서류를 안내합니다.
3. **의료물자 조달 확인**
   * 전처리된 방위사업청 오픈데이터를 바탕으로, 해당 질환에 필요한 의약품이 어디에 보급되고 있는지 제공합니다.

## 시스템 아키텍처 및 기술 스택
* **Frontend / UI:** Streamlit
* **AI & Computer Vision:** PyTorch, Torchvision (MobileNetV2 pre-trained), pytorch-grad-cam, PIL
* **Data Processing:** Python, Pandas, JSON
* **Deployment:** Streamlit Community Clou

## 저장소 구조 
```
skin_scanning/
├── app.py                   # 웹 UI 및 통합 컨트롤러
├── data/                    
│   ├── integrated_db.json   # json DB 
│   └── 의약품_조달계약_전처리데이터.xlsx
├── modules/                  
│   └── classifier.py        # XAI 히트맵 생성 파이프라인
├── utils/                   
│   └── data_loader.py       # JSON 데이터 로드 및 맵핑 유틸리티
└── requirements.txt         # 클라우드 배포용 환경 설정
```

## 바로 이용하기
[Skin Scan Site](https://skin-scanning-0626wctjmgncuswadbdwulcpj.streamlit.app/)에서 서비스를 이용하실 수 있습니다.
