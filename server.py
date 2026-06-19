# -*- coding: utf-8 -*-
import http.server
import socketserver
import urllib.request
import urllib.parse
import json
import os
import sys
import io

# Force UTF-8 encoding for standard output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

PORT = 5000

HTML_CONTENT = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Buscador de Cédulas — Consultas.ec</title>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #0b0f19;
      --card-bg: rgba(22, 30, 49, 0.7);
      --border-color: rgba(255, 255, 255, 0.08);
      --text: #f3f4f6;
      --text-muted: #9ca3af;
      --accent: #3b82f6;
      --accent-hover: #2563eb;
      --success: #10b981;
      --error: #ef4444;
      --warning: #f59e0b;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Plus Jakarta Sans', sans-serif;
    }

    body {
      background: radial-gradient(circle at top, #1e293b 0%, var(--bg) 100%);
      color: var(--text);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 40px 20px;
    }

    .container {
      width: 100%;
      max-width: 680px;
      display: flex;
      flex-direction: column;
      gap: 24px;
    }

    header {
      text-align: center;
      margin-bottom: 10px;
    }

    header h1 {
      font-size: 2.2rem;
      font-weight: 700;
      background: linear-gradient(to right, #60a5fa, #3b82f6, #1d4ed8);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 8px;
    }

    header p {
      color: var(--text-muted);
      font-size: 0.95rem;
    }

    .card {
      background: var(--card-bg);
      backdrop-filter: blur(16px);
      border: 1px solid var(--border-color);
      border-radius: 24px;
      padding: 28px;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
      transition: border-color 0.3s ease;
    }

    .card:hover {
      border-color: rgba(59, 130, 246, 0.2);
    }

    .form-group {
      display: flex;
      flex-direction: column;
      gap: 8px;
      margin-bottom: 20px;
    }

    label {
      font-size: 0.85rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
    }

    .input-wrapper {
      display: flex;
      gap: 12px;
    }

    input {
      flex: 1;
      background: rgba(17, 24, 39, 0.6);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 14px 16px;
      color: var(--text);
      font-size: 0.95rem;
      transition: all 0.2s ease;
    }

    input:focus {
      outline: none;
      border-color: var(--accent);
      box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
    }

    .btn {
      background: var(--accent);
      color: #ffffff;
      border: none;
      border-radius: 12px;
      padding: 14px 24px;
      font-size: 0.95rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      white-space: nowrap;
    }

    .btn:hover {
      background: var(--accent-hover);
      transform: translateY(-1px);
    }

    .btn:active {
      transform: translateY(1px);
    }

    .btn-secondary {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border-color);
      color: var(--text);
    }

    .btn-secondary:hover {
      background: rgba(255, 255, 255, 0.1);
    }

    .credits-badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 16px;
      border-radius: 9999px;
      font-size: 0.9rem;
      font-weight: 600;
      background: rgba(59, 130, 246, 0.1);
      color: var(--accent);
      border: 1px solid rgba(59, 130, 246, 0.2);
      align-self: flex-start;
      margin-top: 5px;
    }

    .credits-badge.zero {
      background: rgba(239, 68, 68, 0.1);
      color: var(--error);
      border-color: rgba(239, 68, 68, 0.2);
    }

    .info-box {
      background: rgba(59, 130, 246, 0.05);
      border-left: 4px solid var(--accent);
      border-radius: 8px;
      padding: 16px;
      margin-bottom: 24px;
      font-size: 0.88rem;
      line-height: 1.6;
    }

    .info-box ul {
      margin-left: 20px;
      margin-top: 8px;
    }

    .result-section {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .result-title {
      font-size: 1.1rem;
      font-weight: 600;
      color: var(--text);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .candidate-card {
      background: rgba(255, 255, 255, 0.02);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      padding: 16px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      transition: all 0.2s ease;
    }

    .candidate-card:hover {
      background: rgba(255, 255, 255, 0.04);
      border-color: rgba(59, 130, 246, 0.3);
    }

    .candidate-info {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .candidate-name {
      font-weight: 600;
      font-size: 0.95rem;
    }

    .candidate-id {
      font-size: 0.85rem;
      color: var(--text-muted);
      font-family: monospace;
    }

    .copy-btn {
      background: rgba(59, 130, 246, 0.1);
      color: var(--accent);
      border: none;
      padding: 6px 12px;
      border-radius: 8px;
      font-size: 0.8rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
    }

    .copy-btn:hover {
      background: var(--accent);
      color: white;
    }

    .status-msg {
      padding: 12px 16px;
      border-radius: 12px;
      font-size: 0.9rem;
      line-height: 1.5;
    }

    .status-msg.error {
      background: rgba(239, 68, 68, 0.1);
      color: var(--error);
      border: 1px solid rgba(239, 68, 68, 0.2);
    }

    .status-msg.info {
      background: rgba(245, 158, 11, 0.1);
      color: var(--warning);
      border: 1px solid rgba(245, 158, 11, 0.2);
    }

    .hidden {
      display: none;
    }

    .loader {
      display: inline-block;
      width: 20px;
      height: 20px;
      border: 3px solid rgba(255,255,255,0.3);
      border-radius: 50%;
      border-top-color: #fff;
      animation: spin 1s ease-in-out infinite;
      margin-right: 8px;
      vertical-align: middle;
    }

    @keyframes spin {
      to { transform: rotate(360deg); }
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>Buscador de Cédulas</h1>
      <p>Consulta tokens disponibles y busca personas por nombre</p>
    </header>

    <!-- Credenciales -->
    <div class="card">
      <div class="form-group">
        <label for="apiKey">Token de consultas.ec</label>
        <div class="input-wrapper">
          <input type="text" id="apiKey" placeholder="Pega aquí tu token..." value="PLSMEoVc-dH8j9EPQU4V7xkejDA9Ychu-YuZU4ZB0hQ">
          <button class="btn" id="checkCreditsBtn">Verificar Créditos</button>
        </div>
        <div id="creditsBadge" class="credits-badge hidden"></div>
      </div>
    </div>

    <!-- Buscador -->
    <div class="card">
      <div class="info-box">
        <strong>💡 ¿Cómo escribir el nombre?</strong>
        <p>El sistema es flexible pero funciona mucho mejor si ingresas primero el apellido y luego el nombre.</p>
        <ul>
          <li><strong>Búsqueda directa:</strong> <code>Quinto Pinela Melany</code> o <code>Plaza Barzola Julyn</code></li>
          <li><strong>Si no sabes el nombre completo:</strong> Escribe solo el apellido y la inicial del nombre para ver candidatos, ej: <code>Quinto Pinela M</code></li>
        </ul>
      </div>

      <div class="form-group">
        <label for="searchQuery">Nombre de la persona</label>
        <div class="input-wrapper">
          <input type="text" id="searchQuery" placeholder="Ej: Plaza Barzola Julyn...">
          <button class="btn" id="searchBtn">Buscar</button>
        </div>
      </div>

      <div id="resultsWrapper" class="result-section hidden">
        <div class="result-title">
          <span>Resultados de la Búsqueda</span>
          <span id="resultsCount" style="font-size: 0.9rem; color: var(--text-muted);"></span>
        </div>
        <div id="statusMsg" class="status-msg hidden"></div>
        <div id="candidatesList" class="result-section"></div>
      </div>
    </div>
  </div>

  <script>
    const apiKeyInput = document.getElementById('apiKey');
    const checkCreditsBtn = document.getElementById('checkCreditsBtn');
    const creditsBadge = document.getElementById('creditsBadge');

    const searchQueryInput = document.getElementById('searchQuery');
    const searchBtn = document.getElementById('searchBtn');
    const resultsWrapper = document.getElementById('resultsWrapper');
    const statusMsg = document.getElementById('statusMsg');
    const candidatesList = document.getElementById('candidatesList');
    const resultsCount = document.getElementById('resultsCount');

    // Cargar token guardado localmente si existe
    if (localStorage.getItem('saved_token')) {
      apiKeyInput.value = localStorage.getItem('saved_token');
    }

    async function checkCredits() {
      const token = apiKeyInput.value.trim();
      if (!token) {
        alert('Por favor ingresa un token válido');
        return;
      }
      localStorage.setItem('saved_token', token);

      checkCreditsBtn.innerHTML = '<div class="loader"></div> Verificando...';
      checkCreditsBtn.disabled = true;

      try {
        const response = await fetch(`/api/credits?token=${encodeURIComponent(token)}`);
        const data = await response.json();
        
        if (response.ok) {
          const credits = data.credits !== undefined ? data.credits : 0;
          creditsBadge.className = 'credits-badge' + (credits === 0 ? ' zero' : '');
          creditsBadge.innerHTML = `🪙 Créditos restantes: ${credits}`;
          creditsBadge.classList.remove('hidden');
        } else {
          creditsBadge.className = 'credits-badge zero';
          creditsBadge.innerText = '❌ Error al verificar token';
          creditsBadge.classList.remove('hidden');
        }
      } catch (err) {
        creditsBadge.className = 'credits-badge zero';
        creditsBadge.innerText = '❌ Error de red';
        creditsBadge.classList.remove('hidden');
      } finally {
        checkCreditsBtn.innerText = 'Verificar Créditos';
        checkCreditsBtn.disabled = false;
      }
    }

    async function searchPerson() {
      const token = apiKeyInput.value.trim();
      const query = searchQueryInput.value.trim();

      if (!token) {
        alert('Ingresa el token primero');
        return;
      }
      if (!query) {
        alert('Ingresa el nombre a buscar');
        return;
      }

      searchBtn.innerHTML = '<div class="loader"></div> Buscando...';
      searchBtn.disabled = true;
      resultsWrapper.classList.remove('hidden');
      statusMsg.classList.add('hidden');
      candidatesList.innerHTML = '';
      resultsCount.innerText = '';

      try {
        const response = await fetch(`/api/fetchdata?token=${encodeURIComponent(token)}&name=${encodeURIComponent(query)}`);
        const data = await response.json();

        // Actualizar créditos automáticamente en segundo plano
        checkCredits();

        if (response.status === 200 && data.data) {
          resultsCount.innerText = `${data.data.length} encontrado(s)`;
          data.data.forEach(item => {
            addCandidateCard(item.name, item.id);
          });
        } else if (response.status === 409 && data.detail && data.detail.candidates) {
          resultsCount.innerText = `${data.detail.candidates.length} candidato(s) (Múltiples resultados)`;
          statusMsg.className = 'status-msg info';
          statusMsg.innerText = '⚠️ La búsqueda retornó múltiples candidatos. Selecciona el que buscas:';
          statusMsg.classList.remove('hidden');

          data.detail.candidates.forEach(item => {
            addCandidateCard(item.name, item.id);
          });
        } else {
          statusMsg.className = 'status-msg error';
          statusMsg.innerText = data.detail && data.detail.message ? `❌ ${data.detail.message}` : (data.detail ? `❌ ${JSON.stringify(data.detail)}` : '❌ Cédula o nombre no encontrado.');
          statusMsg.classList.remove('hidden');
        }
      } catch (err) {
        statusMsg.className = 'status-msg error';
        statusMsg.innerText = '❌ Error de conexión al servidor local.';
        statusMsg.classList.remove('hidden');
      } finally {
        searchBtn.innerText = 'Buscar';
        searchBtn.disabled = false;
      }
    }

    function addCandidateCard(name, id) {
      const div = document.createElement('div');
      div.className = 'candidate-card';
      div.innerHTML = `
        <div class="candidate-info">
          <span class="candidate-name">${name}</span>
          <span class="candidate-id">Cédula: ${id}</span>
        </div>
        <button class="copy-btn" onclick="copyId('${id}')">Copiar Cédula</button>
      `;
      candidatesList.appendChild(div);
    }

    window.copyId = function(id) {
      navigator.clipboard.writeText(id);
      alert(`¡Cédula ${id} copiada al portapapeles!`);
    }

    checkCreditsBtn.addEventListener('click', checkCredits);
    searchBtn.addEventListener('click', searchPerson);
    searchQueryInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') searchPerson();
    });
  </script>
</body>
</html>
"""

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress noise
        pass

    def do_GET(self):
        url_parsed = urllib.parse.urlparse(self.path)
        
        if url_parsed.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_CONTENT.encode('utf-8'))
            return
            
        elif url_parsed.path == '/api/credits':
            query_params = urllib.parse.parse_qs(url_parsed.query)
            token = query_params.get('token', [''])[0]
            
            target_url = f"https://consultas.ec/credits?token={urllib.parse.quote(token)}"
            try:
                req = urllib.request.Request(target_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as response:
                    res_body = response.read()
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(res_body)
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
            return
            
        elif url_parsed.path == '/api/fetchdata':
            query_params = urllib.parse.parse_qs(url_parsed.query)
            token = query_params.get('token', [''])[0]
            name = query_params.get('name', [''])[0]
            
            target_url = f"https://consultas.ec/fetchdata?name={urllib.parse.quote(name)}"
            try:
                req = urllib.request.Request(
                    target_url, 
                    headers={
                        'User-Agent': 'Mozilla/5.0',
                        'X-Credits-Token': token
                    }
                )
                try:
                    with urllib.request.urlopen(req, timeout=15) as response:
                        res_body = response.read()
                        self.send_response(200)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()
                        self.wfile.write(res_body)
                except urllib.error.HTTPError as http_err:
                    # Capture 404 / 409 payloads directly from the remote API
                    res_body = http_err.read()
                    self.send_response(http_err.code)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(res_body)
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
            return
            
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    print(f"\n========================================================")
    print(f"       SERVIDOR LOCAL — CONSULTAS.EC WEB PROXY")
    print(f"========================================================")
    print(f"  [+] Iniciando servidor en: http://localhost:{PORT}")
    print(f"  [+] Abre este enlace en tu navegador para usar la app.")
    print(f"  [~] Presiona CTRL+C para detener el servidor.")
    print(f"========================================================\n")
    
    # Avoid port in use errors
    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("", PORT), ProxyHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[-] Servidor apagado.")
