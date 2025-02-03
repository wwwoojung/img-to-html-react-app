import React, { useState } from "react";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [htmlResult, setHtmlResult] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // 파일 선택 시 호출되는 핸들러
  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  // 폼 제출 시, 파일을 백엔드로 전송하는 핸들러
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!selectedFile) {
      setError("이미지 파일을 선택해 주세요.");
      return;
    }

    setError("");
    setLoading(true);
    setHtmlResult("");

    // FormData 객체에 파일과 추가 데이터를 담습니다.
    const formData = new FormData();
    formData.append("image", selectedFile);

    try {
      // 백엔드 API 엔드포인트에 POST 요청 (포트 번호를 3000으로 변경)
      const response = await fetch("http://localhost:3000/api/process-image", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`서버 에러: ${response.status}`);
      }

      const data = await response.json();
      // 백엔드가 { result: "생성된 HTML 코드" } 형식으로 응답한다고 가정합니다.
      setHtmlResult(data.result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ margin: "2rem", fontFamily: "Arial, sans-serif" }}>
      <h1>디자인 이미지 → HTML 변환기</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          style={{ marginBottom: "1rem" }}
        />
        <br />
        <button type="submit" disabled={loading}>
          {loading ? "처리 중..." : "이미지 변환하기"}
        </button>
      </form>

      {error && (
        <div style={{ color: "red", marginTop: "1rem" }}>에러: {error}</div>
      )}

      {htmlResult && (
        <div style={{ marginTop: "2rem" }}>
          <h2>생성된 HTML</h2>
          <pre
            style={{
              background: "#f8f8f8",
              padding: "1rem",
              border: "1px solid #ddd",
              whiteSpace: "pre-wrap",
            }}
          >
            {htmlResult}
          </pre>
        </div>
      )}
    </div>
  );
}

export default App;
