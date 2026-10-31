import re
import streamlit as st
import markdown

st.set_page_config(page_title="수능 모의고사 시험지 자동 생성기", layout="wide")

def parse_math_markdown(md_text):
    if "## Ⅱ. [정답 및 상세 해설]" in md_text:
        problem_part = md_text.split("## Ⅱ. [정답 및 상세 해설]")[0]
    else:
        problem_part = md_text

    raw_questions = re.split(r'(?=^### \d+\.)', problem_part, flags=re.M)
    
    parsed_items = []
    for q_text in raw_questions:
        q_text = q_text.strip()
        if not q_text or q_text.startswith("# "):
            continue
        html_item = markdown.markdown(q_text, extensions=['fenced_code', 'tables'])
        parsed_items.append(f'<div class="question-card">{html_item}</div>')

    return "".join(parsed_items)

st.title("📐 수능 모의고사 B4 2단 시험지 자동 생성기")
st.caption("제미나이 노트북 마크다운(.md)을 입력하면 브라우저 인쇄(Ctrl+P)를 통해 B4 2단 수능 시험지로 완벽하게 출력할 수 있는 뷰어를 생성합니다.")

uploaded_file = st.file_uploader("제미나이 노트북 문제 마크다운(.md) 파일 업로드", type=["md", "txt"])

if uploaded_file is not None:
    raw_md = uploaded_file.read().decode("utf-8")
    st.success("파일 파싱 완료!")
    
    parsed_html = parse_math_markdown(raw_md)
    
    # B4 2단 인쇄 최적화 HTML 뷰어 렌더링
    exam_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
      @media print {{
        @page {{ size: b4 portrait; margin: 15mm; }}
        body {{ -webkit-print-color-adjust: exact; }}
        .no-print {{ display: none; }}
      }}
      body {{
        font-family: "함초롬바탕", "Batang", serif;
        font-size: 10.5pt;
        line-height: 1.6;
        color: #000;
        background: #fff;
        margin: 0;
        padding: 20px;
      }}
      .exam-header {{
        text-align: center;
        border-bottom: 2px solid #000;
        padding-bottom: 8px;
        margin-bottom: 20px;
      }}
      .exam-header h1 {{
        font-size: 18pt;
        margin: 0;
      }}
      .exam-grid {{
        column-count: 2;
        column-gap: 12mm;
        column-rule: 1px solid #777;
      }}
      .question-card {{
        break-inside: avoid;
        page-break-inside: avoid;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 0.5px dashed #ccc;
      }}
      .question-card h3 {{
        font-size: 11pt;
        margin: 0 0 6px 0;
        background-color: #f8f9fa;
        padding: 4px;
        border-left: 3px solid #000;
      }}
    </style>
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    </head>
    <body>
      <div class="exam-header">
        <h1>2026학년도 수능 대비 수학 영역 모의고사</h1>
      </div>
      <div class="exam-grid">
        {parsed_html}
      </div>
    </body>
    </html>
    """
    
    st.markdown("### 👁️ B4 2단 시험지 미리보기 및 인쇄")
    st.info("💡 브라우저의 인쇄 기능(Ctrl+P 또는 Cmd+P)을 이용하여 **용지 규격을 B4로 설정**하시면 텍스트 밀림 없는 완벽한 수능 시험지가 출력됩니다.")
    
    # HTML 컴포넌트로 화면에 직접 렌더링
    st.components.v1.html(exam_html, height=800, scrolling=True)
