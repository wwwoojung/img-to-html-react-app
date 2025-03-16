from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from tool_2 import MultiModal  # MultiModal 클래스가 정의된 파일
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일에서 환경변수를 로드

# 모델 및 MultiModal 인스턴스 생성 (프롬프트는 필요에 맞게 수정)
model = ChatOpenAI(model="gpt-4o", temperature=0)
memory = ConversationBufferMemory(memory_key="chat_history")
multi_modal = MultiModal(
    model=model,
    system_prompt="You are a professional front-end developer specializing in converting design mockups into clean, accessible, and responsive HTML. Your primary task is to accurately publish the layout and structure of the provided design image as HTML while adhering to specific publishing rules.",
)


file_path = "Group 4157.jpg"
response = multi_modal.stream(
    image_url=file_path,
    user_prompt="Here are the specific publishing rules you must follow: 1. Image Handling: Identify the dimensions (width and height) of all images in the design. Replace actual images with placeholders (gray background) matching the dimensions. Use the <img> tag for placeholders, setting the src attribute to an empty string (src='') and the alt attribute to 'image'. 2. Links and Buttons: Identify all interactive elements, such as <a> tags and buttons. Use the <a> tag for links, including placeholder href='#' if the URL is not specified. Use the <button> tag for buttons, and include their respective labels. 3. Layout Preservation: Preserve the layout and spacing of all elements based on the design. Ensure all elements, including images and interactive components, are aligned properly and styled with CSS for accurate positioning. 4. Output Format: Provide clean and semantic HTML5 with inline CSS styles for layout demonstration. Ensure the code is responsive by using percentage-based widths or other flexible units where appropriate. Avoid using JavaScript; the focus is on HTML and CSS. Here is an example input design image. Generate the HTML structure accordingly.",
)
