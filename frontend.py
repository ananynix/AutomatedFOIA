# frontend.py

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>SYS_FOIA // TERMINAL</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

        /* --- CYBERPUNK COLOR & TEXTURE MANAGEMENT --- */
        :root {
            --neon-cyan: #00ffcc;
            --neon-cyan-dim: rgba(0, 255, 204, 0.2);
            --neon-red: #ff003c;
            --dark-bg: #050505;
            --card-bg: rgba(10, 15, 20, 0.85);
            --grid-color: rgba(0, 255, 204, 0.05);
            --text-main: #e0e0e0;
        }

        * { box-sizing: border-box; }

        body {
            font-family: 'Share Tech Mono', monospace;
            background-color: var(--dark-bg);
            /* The Cyberpunk Blueprint Grid */
            background-image: 
                linear-gradient(var(--grid-color) 1px, transparent 1px),
                linear-gradient(90deg, var(--grid-color) 1px, transparent 1px);
            background-size: 40px 40px;
            color: var(--text-main);
            margin: 0;
            padding: 0;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            text-transform: uppercase;
        }

        /* --- TYPOGRAPHY --- */
        h1, h2, h3 { 
            color: var(--neon-cyan); 
            text-shadow: 0 0 5px var(--neon-cyan-dim);
            margin-top: 0;
            letter-spacing: 2px;
        }
        h1 { font-size: 2rem; text-align: center; border-bottom: 2px solid var(--neon-cyan); padding-bottom: 10px; display: inline-block;}
        h2 { font-size: 1.2rem; margin-bottom: 25px; border-left: 4px solid var(--neon-cyan); padding-left: 10px;}
        p { margin: 0 0 10px 0; }
        
        label { display: block; font-size: 0.85rem; color: var(--neon-cyan); margin-bottom: 8px; opacity: 0.8;}

        /* --- CYBERPUNK INPUTS --- */
        input[type="text"], input[type="number"], textarea {
            width: 100%;
            padding: 12px;
            margin-bottom: 25px;
            background-color: rgba(0, 255, 204, 0.05);
            border: 1px solid #333;
            border-bottom: 2px solid var(--neon-cyan);
            color: var(--neon-cyan);
            font-family: 'Share Tech Mono', monospace;
            font-size: 1rem;
            outline: none;
            transition: all 0.3s;
        }
        input:focus, textarea:focus { 
            background-color: rgba(0, 255, 204, 0.1);
            box-shadow: inset 0 0 10px var(--neon-cyan-dim);
        }
        textarea { resize: vertical; min-height: 100px; }
        input::placeholder, textarea::placeholder { color: rgba(0, 255, 204, 0.3); }

        /* --- CHAMFERED CYBER BUTTONS --- */
        button {
            background-color: var(--neon-cyan);
            color: #000;
            border: none;
            padding: 12px 24px;
            font-family: 'Share Tech Mono', monospace;
            font-size: 1.1rem;
            font-weight: bold;
            cursor: pointer;
            width: 100%;
            position: relative;
            /* Angled cuts on corners */
            clip-path: polygon(15px 0, 100% 0, 100% calc(100% - 15px), calc(100% - 15px) 100%, 0 100%, 0 15px);
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        
        button:hover {
            background-color: #fff;
            box-shadow: 0 0 15px var(--neon-cyan);
        }
        
        button:active { transform: scale(0.98); }

        .btn-red { background-color: var(--neon-red); color: white; }
        .btn-red:hover { background-color: #fff; color: var(--neon-red); box-shadow: 0 0 15px var(--neon-red); }

        .btn-outline { 
            background: transparent; 
            color: var(--neon-cyan); 
            border: 1px solid var(--neon-cyan); 
            clip-path: none; 
            width: auto; 
            padding: 8px 16px;
        }
        .btn-outline:hover { background: var(--neon-cyan); color: #000; }

        /* --- HUD LAYOUT & CARDS --- */
        .view { display: none; width: 100%; max-width: 1300px; margin: 0 auto; padding: 30px; flex-grow: 1; }
        .view.active { display: flex; flex-direction: column; }

        .navbar { display: flex; align-items: center; justify-content: space-between; margin-bottom: 40px; }
        
        .grid-container { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; }
        .grid-container.gov-layout { grid-template-columns: 1.5fr 1fr; }

        /* Cyberpunk Modals with glowing inset borders and top-right telemetry text */
        .card { 
            background-color: var(--card-bg); 
            padding: 30px; 
            border: 1px solid #222;
            position: relative;
            box-shadow: inset 0 0 20px rgba(0,0,0,1);
            clip-path: polygon(0 0, calc(100% - 20px) 0, 100% 20px, 100% 100%, 0 100%);
        }
        
        .card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            border-left: 2px solid var(--neon-cyan);
            border-bottom: 2px solid var(--neon-cyan);
            pointer-events: none;
        }

        .card::after {
            content: 'v001.e1349837956';
            position: absolute;
            top: 5px;
            right: 25px;
            color: var(--neon-cyan);
            font-size: 0.6rem;
            opacity: 0.5;
        }

        /* --- LOBBY SPECIFIC --- */
        #login-view.active { justify-content: center; align-items: center; min-height: 80vh;}
        .lobby-card { width: 500px; text-align: center; }
        .lobby-icon { font-size: 3.5rem; color: var(--neon-cyan); margin-bottom: 10px; text-shadow: 0 0 15px var(--neon-cyan-dim); }
        .lobby-card p { color: #888; margin-bottom: 40px; letter-spacing: 1px;}
        .lobby-card button { margin-bottom: 20px; font-size: 1.2rem; padding: 16px;}

        /* --- DATA TABLES --- */
        .table-container { overflow-x: auto; margin-top: 15px; border: 1px solid #333; background: rgba(0,0,0,0.5);}
        table { width: 100%; border-collapse: collapse; text-align: left; }
        th { color: var(--neon-cyan); padding: 15px; border-bottom: 1px solid var(--neon-cyan); font-weight: normal; background: rgba(0, 255, 204, 0.1);}
        td { padding: 15px; border-bottom: 1px solid #222; vertical-align: middle; }
        tr:hover { background-color: rgba(0, 255, 204, 0.05); }
        
        .badge { padding: 4px 8px; font-size: 0.8rem; letter-spacing: 1px; border: 1px solid; }
        .badge.COMPLETED { color: var(--neon-cyan); border-color: var(--neon-cyan); background: rgba(0,255,204,0.1); }
        .badge.PROCESSING { color: #ffeb3b; border-color: #ffeb3b; background: rgba(255,235,59,0.1); }
        .badge.PENDING { color: var(--neon-red); border-color: var(--neon-red); background: rgba(255,0,60,0.1); }

        /* --- UPLOAD ZONE --- */
        .upload-zone { 
            border: 1px dashed var(--neon-cyan); 
            padding: 40px 20px; 
            text-align: center; 
            margin-bottom: 25px; 
            cursor: pointer; 
            position: relative;
            background: rgba(0, 255, 204, 0.02);
            transition: all 0.3s;
        }
        .upload-zone:hover { background: rgba(0, 255, 204, 0.1); box-shadow: inset 0 0 15px var(--neon-cyan-dim);}
        .upload-zone input[type="file"] { position: absolute; width: 100%; height: 100%; top: 0; left: 0; opacity: 0; cursor: pointer; }
        .upload-text { color: #888; font-size: 0.9rem; margin-top: 15px; }
        .upload-text span { color: var(--neon-cyan); }

        /* --- READOUT TERMINALS --- */
        .screen-reply { 
            margin-top: 20px; 
            padding: 15px; 
            background: rgba(0, 255, 204, 0.1); 
            color: var(--neon-cyan); 
            border-left: 3px solid var(--neon-cyan);
        }
        .screen-reply.error { background: rgba(255, 0, 60, 0.1); color: var(--neon-red); border-color: var(--neon-red); }

        .summary-box { 
            background: #000; 
            padding: 20px; 
            border: 1px solid #333; 
            color: var(--neon-cyan);
            line-height: 1.6; 
            max-height: 300px; 
            overflow-y: auto; 
            white-space: pre-wrap;
            font-size: 0.95rem;
            text-transform: none; /* Keep actual document text readable */
        }

        .spinner { 
            border: 2px solid rgba(0, 255, 204, 0.1); 
            border-top: 2px solid var(--neon-cyan); 
            border-radius: 50%; 
            width: 18px; height: 18px; 
            animation: spin 1s linear infinite; 
            display: inline-block; 
            vertical-align: middle; 
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        
        /* Glitch text effect for main header */
        .glitch-text { position: relative; display: inline-block; }
        .glitch-text::before, .glitch-text::after {
            content: attr(data-text);
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            opacity: 0.8;
        }
        .glitch-text::before { left: 2px; text-shadow: -1px 0 red; clip: rect(24px, 550px, 90px, 0); animation: glitch-anim 2s infinite linear alternate-reverse; }
        .glitch-text::after { left: -2px; text-shadow: -1px 0 blue; clip: rect(85px, 550px, 140px, 0); animation: glitch-anim 2.5s infinite linear alternate-reverse; }
        @keyframes glitch-anim {
            0% { clip: rect(10px, 9999px, 86px, 0); }
            20% { clip: rect(65px, 9999px, 11px, 0); }
            40% { clip: rect(43px, 9999px, 114px, 0); }
            60% { clip: rect(9px, 9999px, 54px, 0); }
            80% { clip: rect(110px, 9999px, 95px, 0); }
            100% { clip: rect(55px, 9999px, 15px, 0); }
        }
    </style>
</head>
<body>

    <div id="login-view" class="view active">
        <div class="card lobby-card">
            <div class="lobby-icon">SYS.REQ</div>
            <h1 class="glitch-text" data-text="FOIA DATALINK">FOIA DATALINK</h1>
            <p>AWAITING AUTHORIZATION...</p>
            <button onclick="showScreen('investigator-view')">INITIALIZE INVESTIGATOR_OS</button>
            <button class="btn-red" onclick="showScreen('government-view'); loadGovRequests();">ACCESS GOV_MAINFRAME</button>
        </div>
    </div>

    <div id="investigator-view" class="view">
        <div class="navbar">
            <button class="btn-outline" onclick="showScreen('login-view')">[X] DISCONNECT</button>
            <div style="font-size: 1.5rem; color: var(--neon-cyan);">INVESTIGATOR_OS // ACTIVE</div>
        </div>
        
        <div class="grid-container">
            <div class="card">
                <h2>>> SUBMIT QUERY</h2>
                
                <label>TARGET AGENCY</label>
                <input type="text" id="agencyInput" placeholder="ENTER AGENCY CODE (e.g., NSA, CIA)">
                
                <label>QUERY PARAMETERS</label>
                <textarea id="topicInput" placeholder="SPECIFY REQUIRED DATA PACKETS..."></textarea>
                
                <button onclick="sendToBossRobot()">TRANSMIT REQUEST</button>
                <div id="invSubmitReply" class="screen-reply" style="display: none;"></div>
            </div>

            <div class="card">
                <h2>>> TELEMETRY READOUT</h2>
                
                <label>TRACKING ID</label>
                <input type="number" id="trackingInput" placeholder="INPUT ID...">
                
                <button onclick="askBossRobot()">PING DATABASE</button>
                
                <div id="invCheckLoading" style="display: none; text-align: center; margin-top: 20px;">
                    <div class="spinner"></div> DECRYPTING CLUSTER...
                </div>
                
                <div id="investigator-result-area" style="display:none; margin-top: 25px;">
                    <h3 id="res-topic" style="color: #fff;"></h3>
                    <p style="margin-bottom: 20px;">STATUS: <span id="res-status" class="badge"></span></p>
                    
                    <label>AI FORENSIC SUMMARY:</label>
                    <div id="res-summary" class="summary-box"></div>
                </div>
            </div>
        </div>
    </div>

    <div id="government-view" class="view">
        <div class="navbar">
            <button class="btn-outline" onclick="showScreen('login-view')">[X] DISCONNECT</button>
            <div style="font-size: 1.5rem; color: var(--neon-red);">GOV_MAINFRAME // ACTIVE</div>
        </div>
        
        <div class="grid-container gov-layout">
            <div class="card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <h2 style="margin: 0;">>> INCOMING SECURE PACKETS</h2>
                    <button class="btn-outline" onclick="loadGovRequests()">[ REFRESH ]</button>
                </div>
                
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>AGENCY</th>
                                <th>TARGET DATA</th>
                                <th>STATUS</th>
                                <th>LINK</th>
                            </tr>
                        </thead>
                        <tbody id="gov-table-body">
                            </tbody>
                    </table>
                </div>
            </div>

            <div class="card">
                <h2>>> UPLOAD SECURE DATA</h2>
                
                <label>TARGET ID</label>
                <input type="number" id="govTrackingInput" placeholder="e.g., 1004">
                
                <label>SELECT DATABLOCK (PDF)</label>
                <div class="upload-zone" id="drop-zone">
                    <input type="file" id="govFileInput" accept="application/pdf" onchange="updateFileName()">
                    <div style="font-size: 2rem; color: var(--neon-cyan);">[+]</div>
                    <div class="upload-text" id="file-name-display">INSERT PDF<br><span>OR CLICK TO BROWSE</span></div>
                </div>
                
                <button class="btn-red" onclick="uploadDocument()">EXECUTE UPLOAD</button>
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
                display.innerHTML = `<span style="color:#fff">>> ${input.files[0].name}</span>`;
            } else {
                display.innerHTML = `INSERT PDF<br><span>OR CLICK TO BROWSE</span>`;
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
                replyBox.innerText = "ERR: INCOMPLETE PARAMETERS.";
                return;
            }

            replyBox.className = 'screen-reply';
            replyBox.style.display = 'block';
            replyBox.innerHTML = '<div class="spinner"></div> TRANSMITTING...';
            
            let response = await fetch(`/submit-request?agency=${agency}&topic=${topic}`, { method: 'POST' });
            let data = await response.json();
            
            replyBox.innerText = `>> TRANSMISSION SUCCESSFUL. ID: ${data.tracking_number}`;
            
            // Clear form
            document.getElementById('agencyInput').value = '';
            document.getElementById('topicInput').value = '';
        }

        async function askBossRobot() {
            let number = document.getElementById('trackingInput').value;
            let resultArea = document.getElementById('investigator-result-area');
            let loadingArea = document.getElementById('invCheckLoading');
            
            if(!number) return;

            resultArea.style.display = 'none'; 
            loadingArea.style.display = 'block';
            
            let response = await fetch(`/check-status/${number}`);
            let data = await response.json();
            
            loadingArea.style.display = 'none';
            
            if (data.error) {
                resultArea.style.display = 'block';
                document.getElementById('res-topic').innerHTML = `<span style="color:var(--neon-red)">ERR: DATA NOT FOUND</span>`;
                document.getElementById('res-summary').innerText = "";
                document.getElementById('res-status').innerText = "NULL";
                document.getElementById('res-status').className = "badge PENDING";
                return;
            }
            
            displayInvestigatorResult(data);
        }

        function displayInvestigatorResult(data) {
            const area = document.getElementById('investigator-result-area');
            area.style.display = 'block';
            
            document.getElementById('res-topic').innerText = data.topic || 'UNKNOWN_TOPIC';
            document.getElementById('res-summary').innerText = data.summary || data.full_document_text || 'AWAITING DATA PROCESSING...';
            
            const statusEl = document.getElementById('res-status');
            const statusStr = data.status || 'PENDING';
            
            let badgeClass = 'PENDING';
            if(statusStr.includes('COMPLETED')) badgeClass = 'COMPLETED';
            if(statusStr.includes('PROCESSING') || statusStr.includes('Wait')) badgeClass = 'PROCESSING';
            
            statusEl.innerText = statusStr.split(' - ')[0];
            statusEl.className = `badge ${badgeClass}`;
        }

        // --- GOVERNMENT CONTROLS ---
        async function loadGovRequests() {
            const tableBody = document.getElementById('gov-table-body');
            tableBody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding: 40px;"><div class="spinner"></div> ACCESSING SECURE DATALINK...</td></tr>';
            
            let response = await fetch('/all-requests');
            let data = await response.json();
            
            tableBody.innerHTML = ''; 
            
            if(data.length === 0) {
                tableBody.innerHTML = '<tr><td colspan="5" style="text-align:center; color:#888">NO ACTIVE REQUESTS.</td></tr>';
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
                        <td style="color:var(--neon-cyan)">${req.agency}</td>
                        <td>${req.topic}</td>
                        <td><span class="badge ${badgeClass}">${statusStr.split(' - ')[0]}</span></td>
                        <td>
                            <button onclick="prepFulfill(${req.tracking_number})" class="btn-outline">SELECT</button>
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
            input.style.backgroundColor = 'rgba(0,255,204,0.2)';
            setTimeout(() => input.style.backgroundColor = 'rgba(0, 255, 204, 0.05)', 500);
        }

        async function uploadDocument() {
            let number = document.getElementById('govTrackingInput').value;
            let fileField = document.getElementById('govFileInput');
            let screen = document.getElementById('govReply');
            
            screen.style.display = 'block';
            screen.className = 'screen-reply error';
            
            if (!number) { screen.innerText = "ERR: ID REQUIRED."; return; }
            if (fileField.files.length === 0) { screen.innerText = "ERR: DATABLOCK (PDF) MISSING."; return; }

            screen.className = 'screen-reply';
            screen.innerHTML = '<div class="spinner"></div> EXECUTING UPLOAD SEQUENCE...';

            let formData = new FormData();
            formData.append("file", fileField.files[0]);

            let response = await fetch(`/upload-response/${number}`, { method: 'POST', body: formData });
            let data = await response.json();
            
            if(data.status && data.status.includes('COMPLETED') || data.message) {
                 screen.innerText = ">> UPLOAD SEQUENCE SUCCESSFUL.";
            } else {
                 screen.className = 'screen-reply error';
                 screen.innerText = "ERR: SEQUENCE FAILED.";
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