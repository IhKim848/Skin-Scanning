import streamlit as st
from PIL import Image
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.classifier import SkinDiseaseClassifier
from utils.data_loader import MedicalDataLinker

st.set_page_config(page_title="군 장병 피부질환 스캐닝", layout="wide", page_icon="🪖")

@st.cache_resource
def load_systems():
    classifier = SkinDiseaseClassifier()
    linker = MedicalDataLinker()
    return classifier, linker

classifier, linker = load_systems()

def main():
    st.title("군 장병 피부질환 스캐닝 시스템")
    st.markdown("병무청 신체등급 판정 기준과 방위사업청 의료물자 조달 데이터를 통합 안내합니다.")
    
    st.divider()

    uploaded_file = st.file_uploader("피부 환부 사진을 업로드하세요 (jpg, png)", type=['jpg', 'jpeg', 'png'])

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert('RGB')

        with st.spinner("AI 모델이 환부 특징을 분석하고 있습니다..."):
            pred_idx, cam_image = classifier.predict_and_explain(image)
        
        categories = ["진균_감염", "세균_감염", "피부염_습진"]
        predicted_category = categories[pred_idx % 3] 

        col1, col2 = st.columns([1, 1.2])

        with col1:
            st.subheader("AI 분석 결과 (Grad-CAM)")
            
            # 원본 및 히트맵 이미지 탭으로 구분
            tab1, tab2 = st.tabs(["AI 집중 분석 영역", "원본 이미지"])
            with tab1:
                st.image(cam_image, caption="붉은색 영역이 AI가 진단에 주요하게 참고한 부위입니다.", use_container_width=True)
            with tab2:
                st.image(image, caption="업로드된 원본 이미지", use_container_width=True)
                
            st.success(f"**분석 결과:** {predicted_category.replace('_', ' ')} 패턴이 감지되었습니다.")

        with col2:
            disease_name, mma_data, dapa_data = linker.get_info_by_diagnosis(predicted_category)

            st.subheader("병무청 신체등급 판정 기준")
            if mma_data:
                st.info(f"**분류:** {mma_data['분류']}")
                st.warning(f"**판정 기준:** {mma_data['판정기준']}")
                st.error(f"**필요 서류:** {mma_data.get('필요서류', '안내된 서류 없음')}")
            else:
                st.write("해당 기준을 찾을 수 없습니다.")

            st.divider()

            st.subheader("방위사업청 의약품 조달 현황")
            st.caption(f"군 입대 후 {disease_name} 관리를 위해 부대에 보급되고 있는 의료물자 내역입니다.")
            
            if dapa_data:
                df = pd.DataFrame(dapa_data)
                display_cols = ['계약체결일자', '계약명', '수요기관명', '대표업체명']
                
                existing_cols = [col for col in display_cols if col in df.columns]
                display_df = df[existing_cols].copy()

                st.dataframe(display_df, use_container_width=True, hide_index=True)
            else:
                st.info("해당 질환에 매핑된 최근 조달 내역이 없습니다.")

if __name__ == "__main__":
    main()