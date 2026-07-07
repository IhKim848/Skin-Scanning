import React, { useState } from 'react';
import './App.css';

function App() {
  
  const [selectedFile, setSelectedFile] = useState(null); // 실제 이미지 파일
  const [previewUrl, setPreviewUrl] = useState(null);     // 화면에 보여줄 미리보기 URL
  const [isLoading, setIsLoading] = useState(false);      // 로딩 상태
  const [result, setResult] = useState(null);             // 백엔드에서 받은 결과 데이터
  const [error, setError] = useState(null);               // 에러 메시지

 
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file)); 
      setResult(null); 
      setError(null);
    }
  };

  const handleSubmit = async () => {
    if (!selectedFile) {
      alert("피부 환부 사진을 먼저 업로드해주세요!");
      return;
    }

    setIsLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      // fast API 주소로 POST 요청
      const response = await fetch("http://127.0.0.1:8000/api/predict", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("서버에서 응답을 가져오는데 실패했습니다.");
      }

      const data = await response.json();
      
      if (data.status === "success") {
        setResult(data.result);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false); 
    }
  };

  return (
    <div className="App" style={{ maxWidth: '800px', margin: '0 auto', padding: '20px', fontFamily: 'sans-serif' }}>
      
      {/* 타이틀 */}
      <header style={{ textAlign: 'center', marginBottom: '30px' }}>
        <h1>🪖 Skin Scanning</h1>
        <p>AI 기반 피부질환 신체등급 및 조달약품 확인 시스템</p>
      </header>

      {/* 업로드 영역 */}
      <section style={{ border: '2px dashed #ccc', padding: '20px', textAlign: 'center', borderRadius: '10px' }}>
        <input 
          type="file" 
          accept="image/*" 
          onChange={handleFileChange} 
          style={{ marginBottom: '15px' }}
        />
        
        {previewUrl && (
          <div>
            <img 
              src={previewUrl} 
              alt="업로드 미리보기" 
              style={{ maxWidth: '100%', maxHeight: '300px', borderRadius: '8px' }} 
            />
          </div>
        )}

        <button 
          onClick={handleSubmit} 
          disabled={!selectedFile || isLoading}
          style={{ 
            marginTop: '20px', 
            padding: '10px 20px', 
            fontSize: '16px', 
            backgroundColor: isLoading ? '#999' : '#0066cc', 
            color: 'white', 
            border: 'none', 
            borderRadius: '5px', 
            cursor: isLoading ? 'not-allowed' : 'pointer'
          }}
        >
          {isLoading ? "AI 분석 중입니다..." : "AI 진단 시작하기"}
        </button>
      </section>

      {/* 에러 메시지 영역 */}
      {error && (
        <div style={{ color: 'red', marginTop: '20px', textAlign: 'center' }}>
           에러 발생: {error}
        </div>
      )}

      {/* 결과 출력 영역 */}
      {result && (
        <section style={{ marginTop: '40px' }}>
          <h2 style={{ borderBottom: '2px solid #333', paddingBottom: '10px' }}>📋 AI 판독 결과</h2>
          
          <div style={{ display: 'flex', gap: '20px', marginTop: '20px' }}>
            {/* 질환 정보 및 히트맵 */}
            <div style={{ flex: 1, backgroundColor: '#f9f9f9', padding: '15px', borderRadius: '8px' }}>
              <h3>1. 질환 분석 (XAI)</h3>
              <p><strong>진단 카테고리:</strong> {result.disease_category}</p>
              <p><strong>상세 질환명:</strong> {result.disease_name}</p>
              {result.heatmap_image_base64 && (
                <div style={{ marginTop: '10px' }}>
                  <p style={{ fontSize: '12px', color: '#666' }}>* AI가 질환을 판단한 주요 근거 영역(히트맵)입니다.</p>
                  <img 
                    src={`data:image/jpeg;base64,${result.heatmap_image_base64}`} 
                    alt="Grad-CAM Heatmap" 
                    style={{ width: '100%', borderRadius: '8px' }}
                  />
                </div>
              )}
            </div>

            {/* 공공데이터 */}
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '20px' }}>
              {/* 병무청 데이터 */}
              <div style={{ backgroundColor: '#eef2ff', padding: '15px', borderRadius: '8px' }}>
                <h3 style={{ color: '#3730a3', marginTop: 0 }}>2. 병역판정 신체검사 기준</h3>
                <p><strong>질환 분류:</strong> {result.mma_data?.분류 || "정보 없음"}</p>
                <p><strong>예상 신체등급:</strong> {result.mma_data?.판정기준 || "정보 없음"}</p>
                <p><strong>필요 서류:</strong> {result.mma_data?.필요서류 || "정보 없음"}</p>
              </div>

              {/* 방위사업청 데이터 */}
              <div style={{ backgroundColor: '#f0fdf4', padding: '15px', borderRadius: '8px' }}>
                <h3 style={{ color: '#166534', marginTop: 0 }}>3. 군부대 의료물자 조달 현황</h3>
                {result.dapa_data && result.dapa_data.length > 0 ? (
                  <ul style={{ paddingLeft: '20px', margin: 0, fontSize: '14px', color: '#333' }}>
                    {result.dapa_data.map((item, index) => (
                      <li key={index} style={{ marginBottom: '10px' }}>
                        <strong>{item.계약명}</strong><br/>
                        <span style={{ color: '#666', fontSize: '12px' }}>계약기간: {item.계약기간}</span>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p>조달 정보 없음</p>
                )}
              </div>
            </div>
          </div>
        </section>
      )}
    </div>
  );
}

export default App;