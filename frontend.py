html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Automated FOIA Mailroom</title>
        <style>
            /* --- GLOBAL STYLES --- */
            :root {
                --bg-main: #0b1120;
                --bg-card: #1e293b;
                --bg-input: #334155;
                --border-color: #475569;
                --text-main: #f8fafc;
                --text-muted: #94a3b8;
                --accent-blue: #3b82f6;
                --accent-blue-hover: #2563eb;
                --accent-green: #10b981;
                --accent-green-hover: #059669;
                --badge-green: #05c46b;
                --badge-yellow: #f59e0b;
                --badge-red: #ef4444;
            }

            * { box-sizing: border-box; }

            body {
                font-family: 'Inter', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                background-color: var(--bg-main);
                color: var(--text-main);
                margin: 0;
                padding: 0;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
            }

            /* --- TYPOGRAPHY & BASIC ELEMENTS --- */
            h1, h2, h3, h4 { margin-top: 0; }
            h1 { font-size: 1.5rem; text-align: center; font-weight: 600; }
            h2 { font-size: 1.25rem; margin-bottom: 20px; font-weight: 600; }
            p { margin: 0 0 10px 0; }
            
            label { display: block; font-size: 0.875rem; color: var(--text-muted); margin-bottom: 8px; font-weight: 500;}

            input[type="text"], input[type="number"], textarea {
                width: 100%;
                padding: 12px 16px;
                margin-bottom: 20px;
                background-color: var(--bg-input);
                border: 1px solid var(--border-color);
                border-radius: 8px;
                color: var(--text-main);
                font-size: 0.95rem;
                outline: none;
                transition: border-color 0.2s;
            }
            input:focus, textarea:focus { border-color: var(--accent-blue); }
            textarea { resize: vertical; min-height: 100px; }
            input::placeholder, textarea::placeholder { color: #64748b; }

            button {
                padding: 12px 24px;
                border: none;
                border-radius: 8px;
                font-weight: 600;
                font-size: 0.95rem;
                cursor: pointer;
                transition: background-color 0.2s, transform 0.1s;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
                width: 100%;
            }
            button:active { transform: scale(0.98); }
            
            .btn-blue { background-color: var(--accent-blue); color: white; }
            .btn-blue:hover { background-color: var(--accent-blue-hover); }
            
            .btn-green { background-color: var(--accent-green); color: white; }
            .btn-green:hover { background-color: var(--accent-green-hover); }

            .btn-outline { background: transparent; border: 1px solid var(--border-color); color: var(--text-main); padding: 6px 16px; font-size: 0.85rem;}
            .btn-outline:hover { background: var(--bg-input); }

            .btn-back { background: transparent; color: var(--text-muted); width: auto; padding: 8px 0; }
            .btn-back:hover { color: var(--text-main); background: transparent; }

            /* --- LAYOUTS --- */
            .view { display: none; width: 100%; max-width: 1200px; margin: 0 auto; padding: 20px; flex-grow: 1; }
            .view.active { display: flex; flex-direction: column; }

            .navbar { display: flex; align-items: center; justify-content: space-between; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 1px solid var(--border-color); }
            .navbar-center { position: absolute; left: 50%; transform: translateX(-50%); display: flex; align-items: center; gap: 10px; font-size: 1.25rem; font-weight: 600;}
            
            .grid-container { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
            .grid-container.gov-layout { grid-template-columns: 1.5fr 1fr; }

            .card { background-color: var(--bg-card); border-radius: 12px; padding: 30px; border: 1px solid var(--border-color); box-shadow: 0 10px 25px rgba(0,0,0,0.2); }

            /* --- LOBBY SPECIFIC --- */
            #login-view.active { justify-content: center; align-items: center; }
            .lobby-card { width: 400px; text-align: center; }
            .lobby-icon { font-size: 3rem; margin-bottom: 15px; color: var(--accent-blue); }
            .lobby-card h1 { margin-bottom: 5px; }
            .lobby-card p { color: var(--text-muted); margin-bottom: 30px; }
            .lobby-card button { margin-bottom: 15px; font-size: 1.05rem; padding: 14px;}

            /* --- TABLE SPECIFIC --- */
            .table-container { overflow-x: auto; margin-top: 15px; }
            table { width: 100%; border-collapse: collapse; text-align: left; font-size: 0.9rem; }
            th { color: var(--text-muted); padding: 12px 15px; border-bottom: 1px solid var(--border-color); font-weight: 500; }
            td { padding: 16px 15px; border-bottom: 1px solid #2a384e; vertical-align: middle; }
            
            .badge { padding: 6px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: bold; letter-spacing: 0.5px; }
            .badge.COMPLETED { background-color: rgba(5, 196, 107, 0.2); color: var(--badge-green); border: 1px solid rgba(5, 196, 107, 0.3); }
            .badge.PROCESSING { background-color: rgba(245, 158, 11, 0.2); color: var(--badge-yellow); border: 1px solid rgba(245, 158, 11, 0.3); }
            .badge.PENDING { background-color: rgba(239, 68, 68, 0.2); color: var(--badge-red); border: 1px solid rgba(239, 68, 68, 0.3); }

            /* --- FILE UPLOAD ZONE --- */
            .upload-zone { border: 2px dashed var(--border-color); border-radius: 8px; padding: 40px 20px; text-align: center; margin-bottom: 20px; cursor: pointer; transition: background 0.2s, border-color 0.2s; position: relative;}
            .upload-zone:hover { background: var(--bg-input); border-color: var(--accent-blue); }
            .upload-zone input[type="file"] { position: absolute; width: 100%; height: 100%; top: 0; left: 0; opacity: 0; cursor: pointer; }
            .upload-icon { font-size: 2rem; color: var(--text-muted); margin-bottom: 10px; }
            .upload-text { color: var(--text-muted); font-size: 0.9rem; }
            .upload-text span { color: var(--accent-blue); font-weight: 500; }

            /* --- HELPERS & ALERTS --- */
            .info-box { background: rgba(255, 255, 255, 0.03); border: 1px solid var(--border-color); border-radius: 8px; padding: 15px; margin-top: 20px; font-size: 0.85rem; color: var(--text-muted); }
            .info-box ul { margin: 10px 0 0 0; padding-left: 20px; }
            .info-box li { margin-bottom: 5px; }
            
            .screen-reply { margin-top: 15px; padding: 12px; border-radius: 8px; background: rgba(16, 185, 129, 0.1); color: var(--accent-green); font-size: 0.9rem; text-align: center; border: 1px solid rgba(16, 185, 129, 0.2);}
            .screen-reply.error { background: rgba(239, 68, 68, 0.1); color: var(--badge-red); border-color: rgba(239, 68, 68, 0.2); }

            .summary-box { background: var(--bg-input); padding: 15px; border-radius: 8px; border-left: 4px solid var(--accent-blue); line-height: 1.6; max-height: 300px; overflow-y: auto; white-space: pre-wrap; font-size: 0.9rem;}

            .spinner { border: 3px solid rgba(255, 255, 255, 0.1); border-top: 3px solid var(--accent-blue); border-radius: 50%; width: 16px; height: 16px; animation: spin 1s linear infinite; display: inline-block; vertical-align: middle; margin-right: 8px; }
            @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
            
            .header-action { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;}
            .header-action h2 { margin-bottom: 0; }
        </style>
    </head>
    <body>

        <div id="login-view" class="view active">
            <div class="card lobby-card">
                <div class="lobby-icon">🏢</div>
                <h1>Automated FOIA Mailroom</h1>
                <p>Who are you?</p>
                <button class="btn-blue" onclick="showScreen('investigator-view')">🕵️‍♂️ I am an Investigator</button>
                <button class="btn-green" onclick="showScreen('government-view'); loadGovRequests();">🏛️ I am the Government</button>
            </div>
        </div>

        <div id="investigator-view" class="view">
            <div class="navbar">
                <button class="btn-back" onclick="showScreen('login-view')">← Back to Lobby</button>
                <div class="navbar-center">🕵️‍♂️ Investigator Desk</div>
                <div style="width: 100px;"></div> </div>
            
            <div class="grid-container">
                <div class="card">
                    <h2>Submit Request</h2>
                    
                    <label>Agency Name</label>
                    <input type="text" id="agencyInput" placeholder="e.g., FBI, CIA, EPA">
                    
                    <label>What records do you need?</label>
                    <textarea id="topicInput" placeholder="Describe the documents you're requesting..."></textarea>
                    
                    <button class="btn-blue" onclick="sendToBossRobot()">Send Request</button>
                    <div id="invSubmitReply" class="screen-reply" style="display: none;"></div>
                </div>

                <div class="card">
                    <h2>Check Status & Read Summary</h2>
                    
                    <label>Tracking Number</label>
                    <input type="number" id="trackingInput" placeholder="e.g., 1001">
                    
                    <button class="btn-blue" onclick="askBossRobot()">Check Clipboard</button>
                    
                    <div id="invCheckLoading" style="display: none; text-align: center; margin-top: 20px; color: var(--text-muted);">
                        <div class="spinner"></div> Checking the Giant Clipboard...
                    </div>
                    
                    <div id="investigator-hint-area" class="info-box">
                        Try these tracking numbers once submitted:
                        <ul id="hint-list">
                            <li>Check back here after requesting a document.</li>
                        </ul>
                    </div>
                    
                    <div id="investigator-result-area" style="display:none; margin-top: 25px;">
                        <h3 id="res-topic" style="color: var(--text-main); margin-bottom: 8px; font-size: 1.1rem;"></h3>
                        <p style="margin-bottom: 20px;"><span id="res-status" class="badge"></span></p>
                        
                        <label>Parsed Summary:</label>
                        <div id="res-summary" class="summary-box"></div>
                    </div>
                </div>
            </div>
        </div>

        <div id="government-view" class="view">
            <div class="navbar">
                <button class="btn-back" onclick="showScreen('login-view')">← Back to Lobby</button>
                <div class="navbar-center">🏛️ Government Desk</div>
                <div style="width: 100px;"></div>
            </div>
            
            <div class="grid-container gov-layout">
                <div class="card">
                    <div class="header-action">
                        <h2>Incoming Requests</h2>
                        <button class="btn-outline" style="width: auto;" onclick="loadGovRequests()">↻ Refresh</button>
                    </div>
                    
                    <div class="table-container">
                        <table>
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Agency</th>
                                    <th>Topic</th>
                                    <th>Status</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody id="gov-table-body">
                                </tbody>
                        </table>
                    </div>
                </div>

                <div class="card">
                    <h2>Fulfill Request</h2>
                    
                    <label>Tracking Number to fulfill</label>
                    <input type="number" id="govTrackingInput" placeholder="e.g., 1004">
                    
                    <label>Upload Document (PDF)</label>
                    <div class="upload-zone" id="drop-zone">
                        <input type="file" id="govFileInput" accept="application/pdf" onchange="updateFileName()">
                        <div class="upload-icon">↑</div>
                        <div class="upload-text" id="file-name-display">Drag & drop PDF here<br><span>or click to browse</span></div>
                    </div>
                    
                    <button class="btn-green" onclick="uploadDocument()">↑ Upload & Fulfill</button>
                    <div id="govReply" class="screen-reply" style="display: none;"></div>
                </div>
            </div>
        </div>

        <script>
            // --- UI LOGIC ---
            function showScreen(screenId) {
                document.querySelectorAll('.view').forEach(el => el.classList.remove('active'));
                document.getElementById(screenId).classList.add('active');
            }

            function updateFileName() {
                const input = document.getElementById('govFileInput');
                const display = document.getElementById('file-name-display');
                if (input.files && input.files.length > 0) {
                    display.innerHTML = `<span style="color:var(--accent-green)">📄 ${input.files[0].name}</span>`;
                } else {
                    display.innerHTML = `Drag & drop PDF here<br><span>or click to browse</span>`;
                }
            }

            // --- INVESTIGATOR CONTROLS ---
            async function sendToBossRobot() {
                let agency = document.getElementById('agencyInput').value;
                let topic = document.getElementById('topicInput').value;
                let replyBox = document.getElementById('invSubmitReply');
                
                if(!agency || !topic) {
                    replyBox.className = 'screen-reply error';
                    replyBox.style.display = 'block';
                    replyBox.innerText = "Please fill out both fields.";
                    return;
                }

                replyBox.className = 'screen-reply';
                replyBox.style.display = 'block';
                replyBox.innerHTML = '<div class="spinner"></div> Submitting...';
                
                let response = await fetch(`/submit-request?agency=${agency}&topic=${topic}`, { method: 'POST' });
                let data = await response.json();
                
                replyBox.innerText = `✅ Success! Tracking Number: ${data.tracking_number}`;
                
                // Clear form
                document.getElementById('agencyInput').value = '';
                document.getElementById('topicInput').value = '';
            }

            async function askBossRobot() {
                let number = document.getElementById('trackingInput').value;
                let resultArea = document.getElementById('investigator-result-area');
                let hintArea = document.getElementById('investigator-hint-area');
                let loadingArea = document.getElementById('invCheckLoading');
                
                if(!number) return;

                resultArea.style.display = 'none'; 
                hintArea.style.display = 'none';
                loadingArea.style.display = 'block';
                
                let response = await fetch(`/check-status/${number}`);
                let data = await response.json();
                
                loadingArea.style.display = 'none';
                
                if (data.error) {
                    hintArea.style.display = 'block';
                    hintArea.innerHTML = `<span style="color:var(--badge-red)">${data.error}</span>`;
                    return;
                }
                
                displayInvestigatorResult(data);
            }

            function displayInvestigatorResult(data) {
                const area = document.getElementById('investigator-result-area');
                area.style.display = 'block';
                
                document.getElementById('res-topic').innerText = data.topic || 'Unknown Topic';
                document.getElementById('res-summary').innerText = data.summary || data.full_document_text || 'No summary available yet.';
                
                const statusEl = document.getElementById('res-status');
                const statusStr = data.status || 'PENDING';
                
                let badgeClass = 'PENDING';
                if(statusStr.includes('COMPLETED')) badgeClass = 'COMPLETED';
                if(statusStr.includes('PROCESSING') || statusStr.includes('Wait')) badgeClass = 'PROCESSING';
                
                statusEl.innerText = statusStr;
                statusEl.className = `badge ${badgeClass}`;
            }

            // --- GOVERNMENT CONTROLS ---
            async function loadGovRequests() {
                const tableBody = document.getElementById('gov-table-body');
                tableBody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding: 40px;"><div class="spinner"></div> Fetching requests...</td></tr>';
                
                let response = await fetch('/all-requests');
                let data = await response.json();
                
                tableBody.innerHTML = ''; 
                
                if(data.length === 0) {
                    tableBody.innerHTML = '<tr><td colspan="5" style="text-align:center; color:var(--text-muted)">No active requests found.</td></tr>';
                    return;
                }

                data.forEach(req => {
                    const statusStr = req.status || 'PENDING';
                    let badgeClass = 'PENDING';
                    if(statusStr.includes('COMPLETED')) badgeClass = 'COMPLETED';
                    if(statusStr.includes('PROCESSING') || statusStr.includes('Wait')) badgeClass = 'PROCESSING';
                    
                    const row = `
                        <tr>
                            <td>${req.tracking_number}</td>
                            <td>${req.agency}</td>
                            <td>${req.topic}</td>
                            <td><span class="badge ${badgeClass}">${statusStr.split(' - ')[0]}</span></td>
                            <td>
                                <button onclick="prepFulfill(${req.tracking_number})" class="btn-outline">Select</button>
                            </td>
                        </tr>
                    `;
                    tableBody.insertAdjacentHTML('beforeend', row);
                });
            }

            function prepFulfill(id) {
                let input = document.getElementById('govTrackingInput');
                input.value = id;
                input.scrollIntoView({ behavior: 'smooth' });
                input.style.borderColor = 'var(--accent-blue)';
                setTimeout(() => input.style.borderColor = 'var(--border-color)', 1000);
            }

            async function uploadDocument() {
                let number = document.getElementById('govTrackingInput').value;
                let fileField = document.getElementById('govFileInput');
                let screen = document.getElementById('govReply');
                
                screen.style.display = 'block';
                screen.className = 'screen-reply error';
                
                if (!number) { screen.innerText = "Please enter a tracking number."; return; }
                if (fileField.files.length === 0) { screen.innerText = "Please select a PDF file."; return; }

                screen.className = 'screen-reply';
                screen.innerHTML = '<div class="spinner"></div> Processing document...';

                let formData = new FormData();
                formData.append("file", fileField.files[0]);

                let response = await fetch(`/upload-response/${number}`, { method: 'POST', body: formData });
                let data = await response.json();
                
                if(data.status && data.status.includes('COMPLETED') || data.message) {
                     screen.innerText = "✅ Upload initialized successfully!";
                } else {
                     screen.className = 'screen-reply error';
                     screen.innerText = "Failed to upload.";
                }
                
                // Clear inputs
                fileField.value = '';
                document.getElementById('govTrackingInput').value = '';
                updateFileName();
                loadGovRequests();
            }
        </script>
    </body>
    </html>
    """