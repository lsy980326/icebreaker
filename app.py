from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template_string
from ice_breaker import ice_break_with
import os

load_dotenv()

app = Flask(__name__)

# HTML 템플릿
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ice Breaker - GitHub 프로필 분석</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 300;
        }
        
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .form-section {
            padding: 40px 30px;
        }
        
        .input-group {
            margin-bottom: 30px;
        }
        
        .input-group label {
            display: block;
            margin-bottom: 10px;
            font-weight: 600;
            color: #333;
            font-size: 1.1em;
        }
        
        .input-group input {
            width: 100%;
            padding: 15px 20px;
            border: 2px solid #e1e5e9;
            border-radius: 10px;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        
        .input-group input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 40px;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .result {
            display: none;
            padding: 30px;
            background: #f8f9fa;
            border-radius: 15px;
            margin-top: 20px;
        }
        
        .profile-section {
            display: flex;
            align-items: center;
            margin-bottom: 30px;
            padding: 20px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        }
        
        .profile-image {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            margin-right: 20px;
            border: 3px solid #667eea;
        }
        
        .profile-info h3 {
            color: #333;
            margin-bottom: 5px;
            font-size: 1.3em;
        }
        
        .profile-info p {
            color: #666;
            font-size: 1em;
        }
        
        .summary-section {
            background: white;
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        }
        
        .summary-section h4 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.2em;
            border-bottom: 2px solid #e1e5e9;
            padding-bottom: 10px;
        }
        
        .summary-section p {
            line-height: 1.6;
            color: #555;
            margin-bottom: 15px;
        }
        
        .facts-list {
            list-style: none;
            padding-left: 0;
        }
        
        .facts-list li {
            background: #f8f9fa;
            padding: 10px 15px;
            margin-bottom: 10px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        
        .error {
            background: #ffe6e6;
            color: #d63031;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            border-left: 4px solid #d63031;
        }
        
        .github-link {
            display: inline-block;
            background: #333;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 8px;
            margin-top: 10px;
            transition: all 0.3s ease;
        }
        
        .github-link:hover {
            background: #555;
            transform: translateY(-2px);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧊 Ice Breaker</h1>
            <p>GitHub 프로필을 분석하여 흥미로운 정보를 찾아보세요!</p>
        </div>
        
        <div class="form-section">
            <form id="iceBreakerForm">
                <div class="input-group">
                    <label for="name">이름 또는 GitHub 사용자명을 입력하세요:</label>
                    <input type="text" id="name" name="name" placeholder="예: lsy980326 또는 Lee Sang Yeop" required>
                </div>
                <button type="submit" class="btn" id="submitBtn">분석 시작하기</button>
            </form>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>GitHub 프로필을 분석하고 있습니다...</p>
            </div>
            
            <div class="result" id="result">
                <!-- 결과가 여기에 표시됩니다 -->
            </div>
        </div>
    </div>

    <script>
        document.getElementById('iceBreakerForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const name = document.getElementById('name').value;
            const submitBtn = document.getElementById('submitBtn');
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');
            
            // UI 상태 변경
            submitBtn.disabled = true;
            submitBtn.textContent = '분석 중...';
            loading.style.display = 'block';
            result.style.display = 'none';
            
            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ name: name })
                });
                
                const data = await response.json();
                
                if (data.error) {
                    result.innerHTML = `<div class="error">오류: ${data.error}</div>`;
                } else {
                    displayResult(data);
                }
                
            } catch (error) {
                result.innerHTML = `<div class="error">네트워크 오류가 발생했습니다: ${error.message}</div>`;
            } finally {
                // UI 상태 복원
                submitBtn.disabled = false;
                submitBtn.textContent = '분석 시작하기';
                loading.style.display = 'none';
                result.style.display = 'block';
            }
        });
        
        function displayResult(data) {
            const result = document.getElementById('result');
            
            let factsHtml = '';
            if (data.summary.interesting_facts) {
                factsHtml = '<ul class="facts-list">';
                data.summary.interesting_facts.forEach(fact => {
                    factsHtml += `<li>${fact}</li>`;
                });
                factsHtml += '</ul>';
            }
            
            result.innerHTML = `
                <div class="profile-section">
                    <img src="${data.image_url}" alt="Profile" class="profile-image" onerror="this.src='https://via.placeholder.com/80x80/667eea/ffffff?text=GitHub'">
                    <div class="profile-info">
                        <h3>${data.summary.name || 'GitHub 사용자'}</h3>
                        <p>프로필 분석 완료</p>
                    </div>
                </div>
                
                <div class="summary-section">
                    <h4>📋 요약</h4>
                    <p>${data.summary.summary || '요약 정보가 없습니다.'}</p>
                </div>
                
                <div class="summary-section">
                    <h4>✨ 흥미로운 사실</h4>
                    ${factsHtml || '<p>흥미로운 사실이 없습니다.</p>'}
                </div>
                
                <div class="summary-section">
                    <h4>💡 개선점 및 칭찬</h4>
                    <p>${data.summary.areas_for_improvement || '개선점이 없습니다.'}</p>
                </div>
            `;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """메인 페이지"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/analyze', methods=['POST'])
def analyze():
    """GitHub 프로필 분석 API"""
    try:
        data = request.get_json()
        name = data.get('name')
        
        if not name:
            return jsonify({'error': '이름을 입력해주세요.'}), 400
        
        # Ice Breaker 실행
        summary, image_url = ice_break_with(name)
        
        return jsonify({
            'summary': {
                'name': summary.name,
                'summary': summary.summary,
                'interesting_facts': summary.interesting_facts,
                'areas_for_improvement': summary.areas_for_improvement
            },
            'image_url': image_url
        })
        
    except Exception as e:
        return jsonify({'error': f'분석 중 오류가 발생했습니다: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)