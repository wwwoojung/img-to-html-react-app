from flask import Flask, request, jsonify
from flask_cors import CORS
from tool import MultiModal  # 앞서 작성한 MultiModal 클래스가 정의된 파일
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일에서 환경변수를 로드

app = Flask(__name__)
CORS(app)

# 모델 및 MultiModal 인스턴스 생성 (프롬프트는 필요에 맞게 수정)
model = ChatOpenAI(model="gpt-4o", temperature=0)
memory = ConversationBufferMemory(memory_key="chat_history")
multi_modal = MultiModal(
    model=model,
    system_prompt="You are a professional front-end developer specializing in converting design mockups into clean, accessible, and responsive HTML. Your primary task is to accurately publish the layout and structure of the provided design image as HTML while adhering to specific publishing rules."
)

@app.route('/api/process-image', methods=['POST'])
def process_image():
    if 'image' not in request.files or 'prompt' not in request.form:
        return jsonify({'error': '이미지와 프롬프트를 제공해야 합니다.'}), 400
    
    image_file = request.files['image']
    prompt_text = request.form['prompt']

    # ✅ 기본 HTML 변환을 위한 프롬프트 (사용자 입력과 결합)
    base_prompt = """
        Convert this design image into a structured HTML page with inline CSS for layout demonstration.
        Follow these rules strictly:
        1. **Image Handling**: Identify the dimensions (width and height) of all images in the design.
           Replace actual images with placeholders (gray background) matching the dimensions.
           Use the `<img>` tag for placeholders, setting `src=""` and `alt="image"`.
        2. **Links and Buttons**: Identify all interactive elements like `<a>` tags and buttons.
           Use `<a>` tags for links, including placeholder `href="#"` if the URL is not specified.
           Use the `<button>` tag for buttons, and ensure they are correctly labeled.
        3. **Layout Preservation**: Preserve the layout and spacing of all elements based on the design.
           Ensure all elements, including images and interactive components, are aligned properly and styled with CSS.
        4. **Output Format**: Provide clean and semantic HTML5 with inline CSS styles for layout demonstration.
    """

    # ✅ 사용자 입력 프롬프트와 기본 프롬프트 결합
    final_prompt = f"{base_prompt}\n\nUser Instructions:\n{prompt_text}"
    
    # 임시 저장 경로 (폴더가 없으면 생성)
    temp_dir = "./temp"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, image_file.filename)
    image_file.save(file_path)
    
    try:
        # MultiModal.invoke를 통해 HTML 결과 생성
        result = multi_modal.invoke(
            image_url=file_path,
            user_prompt=final_prompt
        )
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # 임시 파일 삭제
        os.remove(file_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
    



    