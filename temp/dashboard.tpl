<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JetScan Control Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(140deg, #f3f7f6fc 0%, #010707c3 100%);
            color: #ffffff;
            min-height: 100vh;
            padding: 10px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }

        .card {
            background: rgba(13, 171, 153, 0.1); 
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            border: 1px solid rgba(108, 174, 113, 0.2);
            transition: all 0.3s ease;
            box-shadow: 0 8px 32px 0 rgba(8, 11, 8, 0.37);
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 45px 0 rgba(99, 125, 119, 0.604);
        }

        .card-header {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        }

        .card-icon {
            width: 24px;
            height: 24px;
            margin-right: 10px;
        }

        .card-title {
            font-size: 1.2em;
            font-weight: 600;
        }

        .status-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 20px;
        }

        .status-item {
            text-align: center;
            padding: 15px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            transition: all 0.3s ease;
        }

        .status-item:hover {
            background: rgba(255, 255, 255, 0.1);
        }

        .status-value {
            font-size: 1.8em;
            font-weight: bold;
            margin-bottom: 5px;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }

        .status-label {
            font-size: 0.9em;
            opacity: 0.8;
        }

        .battery-visual {
            width: 100%;
            height: 40px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            margin: 15px 0;
            position: relative;
            overflow: hidden;
        }

        .battery-fill {
            height: 100%;
            background: linear-gradient(90deg, #ff6b6b 0%, #ffd93d 50%, #6bcf7f 100%);
            border-radius: 20px;
            transition: width 0.5s ease;
            position: relative;
        }

        .battery-text {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-weight: bold;
            color: #000;
            text-shadow: 0 1px 2px rgba(255, 255, 255, 0.5);
        }

        .control-section {
            margin-top: 20px;
        }

        .slider-container {
            margin: 20px 0;
        }

        .slider-label {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            font-weight: 500;
        }

        .slider {
            width: 100%;
            height: 8px;
            border-radius: 5px;
            background: rgba(137, 114, 114, 0.508);
            outline: none;
            -webkit-appearance: none;
            appearance: none;
            transition: all 0.3s ease;
        }

        .slider::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: #ffffff;
            cursor: pointer;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
        }

        .slider::-moz-range-thumb {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: #ffffff;
            cursor: pointer;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
            border: none;
        }

        .btn {
            background: linear-gradient(45deg, #0ea4ce, #37e0d74f);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 25px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
            width: 100%;
            margin-top: 10px;
            box-shadow: 0 4px 15px 0 rgba(102, 126, 234, 0.4);
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px 0 rgba(102, 126, 234, 0.6);
        }

        .btn:active {
            transform: translateY(0);
        }

        .btn.recording {
            background: linear-gradient(45deg, #ff6b6b, #ee5a52);
            box-shadow: 0 4px 15px 0 rgba(255, 107, 107, 0.4);
        }

        .btn.recording:hover {
            box-shadow: 0 8px 25px 0 rgba(255, 107, 107, 0.6);
        }

        .cell-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 10px;
            margin-top: 15px;
        }

        .cell-item {
            background: rgba(255, 255, 255, 0.05);
            padding: 10px;
            border-radius: 8px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .cell-voltage {
            font-size: 1.1em;
            font-weight: bold;
            color: #6bcf7f;
        }

        .imu-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-top: 15px;
        }

        .imu-item {
            background: rgba(255, 255, 255, 0.05);
            padding: 12px;
            border-radius: 8px;
            text-align: center;
        }

        .imu-value {
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 5px;
        }

        .imu-label {
            font-size: 0.8em;
            opacity: 0.8;
        }

        .system-info {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-top: 15px;
        }

        .info-item {
            background: rgba(255, 255, 255, 0.05);
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }

        .refresh-indicator {
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(255, 255, 255, 0.9);
            color: #333;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9em;
            opacity: 0;
            transition: opacity 0.3s ease;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }

        .refresh-indicator.show {
            opacity: 1;
        }

        @media (max-width: 768px) {
            .container {
                grid-template-columns: 1fr;
                gap: 15px;
            }
            
            .status-grid, .imu-grid, .system-info {
                grid-template-columns: 1fr;
            }
        }

        .connection-status {
            position: fixed;
            top: 20px;
            left: 20px;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            transition: all 0.3s ease;
        }

        .connection-status.online {
            background: #6bcf7f;
            color: white;
        }

        .connection-status.offline {
            background: #ff6b6b;
            color: white;
        }

        .recording-status {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 15px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            margin-bottom: 20px;
            border: 2px solid transparent;
            transition: all 0.3s ease;
        }

        .recording-status.active {
            border-color: #ff6b6b;
            background: rgba(255, 107, 107, 0.1);
        }

        .recording-indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #666;
            margin-right: 10px;
            transition: all 0.3s ease;
        }

        .recording-indicator.active {
            background: #ff6b6b;
            animation: pulse 1.5s ease-in-out infinite;
        }

        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }

        .recording-info {
            display: flex;
            flex-direction: column;
            align-items: center;
            flex: 1;
        }

        .recording-duration {
            font-size: 1.4em;
            font-weight: bold;
            margin-bottom: 5px;
        }

        .recording-label {
            font-size: 0.9em;
            opacity: 0.8;
        }
    </style>
</head>
<body>
    <div class="connection-status" id="connectionStatus">● Online</div>
    <div class="refresh-indicator" id="refreshIndicator">Updating...</div>

    <div class="container">
        <!-- Battery Management Card -->
        <div class="card">
            <div class="card-header">
                <svg class="card-icon" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M15.67 4H14V2h-4v2H8.33C7.6 4 7 4.6 7 5.33v15.33C7 21.4 7.6 22 8.33 22h7.33c.74 0 1.34-.6 1.34-1.33V5.33C17 4.6 16.4 4 15.67 4z"/>
                </svg>
                <span class="card-title">Battery Management</span>
            </div>
            
            <div class="status-grid">
                <div class="status-item">
                    <div class="status-value" id="totalVoltage">{{ total_voltage }}V</div>
                    <div class="status-label">Total Voltage</div>
                </div>
                <div class="status-item">
                    <div class="status-value" id="chargePercent">{{ charge_percent }}%</div>
                    <div class="status-label">Charge Level</div>
                </div>
            </div>

            <div class="battery-visual">
                <div class="battery-fill" id="batteryFill" style="width: {{ charge_percent }}%"></div>
                <div class="battery-text" id="batteryText">{{ charge_percent }}%</div>
            </div>

            <div class="status-item">
                <div class="status-value" id="chargerStatus">{{ charger_status }}</div>
                <div class="status-label">Charger Status</div>
            </div>

            <!--<div class="cell-grid">
                % for i in range(len(cell_voltages)) :
                <div class="cell-item">
                    <div class="cell-voltage">{{ cell_voltages[i] }}</div>
                    <div class="status-label">Cell {{ i+1 }} (mV)</div>
                </div>
                % end 
            </div>-->
        </div>

        <!-- Video Recording Card -->
        <div class="card">
            <div class="card-header">
                <svg class="card-icon" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M17,10.5V7A1,1 0 0,0 16,6H4A1,1 0 0,0 3,7V17A1,1 0 0,0 4,18H16A1,1 0 0,0 17,17V13.5L21,17.5V6.5L17,10.5Z"/>
                </svg>
                <span class="card-title">Video Recording</span>
            </div>

            <div class="recording-status" id="recordingStatus">
                <div class="recording-indicator" id="recordingIndicator"></div>
                <div class="recording-info">
                    <div class="recording-duration" id="recordingDuration">00:00:00</div>
                    <div class="recording-label" id="recordingLabel">Not Recording</div>
                </div>
            </div>

            <div class="status-grid">
                <div class="status-item">
                    <div class="status-value" id="videoQuality">1080p</div>
                    <div class="status-label">Video Quality</div>
                </div>
                <div class="status-item">
                    <div class="status-value" id="storageUsed">--</div>
                    <div class="status-label">Storage Used (GB)</div>
                </div>
            </div>

            <div class="control-section">
                <button class="btn" id="recordingBtn" onclick="toggleRecording()">Start Recording</button>
            </div>
        </div>

        <!-- LED Control Card -->
        <div class="card">
            <div class="card-header">
                <svg class="card-icon" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M9,21C9,21.5 9.4,22 10,22H14C14.6,22 15,21.5 15,21V20H9V21M12,2A7,7 0 0,0 5,9C5,11.38 6.19,13.47 8,14.74V17A1,1 0 0,0 9,18H15A1,1 0 0,0 16,17V14.74C17.81,13.47 19,11.38 19,9A7,7 0 0,0 12,2Z"/>
                </svg>
                <span class="card-title">LED Control</span>
            </div>

            <div class="control-section">
                <div class="slider-container">
                    <div class="slider-label">
                        <span>Brightness</span>
                        <span id="brightnessValue">{{ brightness }}%</span>
                    </div>
                    <input type="range" id="brightnessSlider" class="slider" min="0" max="100" value="{{ brightness }}">
                </div>
                <button class="btn" onclick="setBrightness()">Apply Brightness</button>
            </div>
        </div>

        <!-- IMU Sensor Card -->
        <div class="card">
            <div class="card-header">
                <svg class="card-icon" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4M11,6V8L10,9V11H8V13H10V15L11,16V18H13V16L14,15V13H16V11H14V9L13,8V6H11Z"/>
                </svg>
                <span class="card-title">IMU Orientation</span>
            </div>

            <div class="status-grid">
                <div class="status-item">
                    <div class="status-value" id="pitch">{{ pitch }}°</div>
                    <div class="status-label">Pitch</div>
                </div>
                <div class="status-item">
                    <div class="status-value" id="roll">{{ roll }}°</div>
                    <div class="status-label">Roll</div>
                </div>
            </div>

            <div class="imu-grid">
                <div class="imu-item">
                    <div class="imu-value" id="accelX">{{ accel[0] }}</div>
                    <div class="imu-label">Accel X (g)</div>
                </div>
                <div class="imu-item">
                    <div class="imu-value" id="accelY">{{ accel[1] }}</div>
                    <div class="imu-label">Accel Y (g)</div>
                </div>
                <div class="imu-item">
                    <div class="imu-value" id="accelZ">{{ accel[2] }}</div>
                    <div class="imu-label">Accel Z (g)</div>
                </div>
                <div class="imu-item">
                    <div class="imu-value" id="gyroX">{{ gyro[0] }}</div>
                    <div class="imu-label">Gyro X (°/s)</div>
                </div>
                <div class="imu-item">
                    <div class="imu-value" id="gyroY">{{ gyro[1] }}</div>
                    <div class="imu-label">Gyro Y (°/s)</div>
                </div>
                <div class="imu-item">
                    <div class="imu-value" id="gyroZ">{{ gyro[2] }}</div>
                    <div class="imu-label">Gyro Z (°/s)</div>
                </div>
            </div>
        </div>

        <!-- System Information Card -->
        <div class="card">
            <div class="card-header">
                <svg class="card-icon" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M4,6H20V16H4M20,18A2,2 0 0,0 22,16V6C22,4.89 21.1,4 20,4H4C2.89,4 2,4.89 2,6V16A2,2 0 0,0 4,18H0V20H24V18H20Z"/>
                </svg>
                <span class="card-title">System Status</span>
            </div>

            <div class="system-info">
                <div class="info-item">
                    <div class="status-value" id="uptime">--</div>
                    <div class="status-label">Uptime (hours)</div>
                </div>
                <div class="info-item">
                    <div class="status-value" id="storage">--</div>
                    <div class="status-label">Free Storage (GB)</div>
                </div>
                <div class="info-item">
                    <div class="status-value" id="temperature">23°C</div>
                    <div class="status-label">CPU Temperature</div>
                </div>
                <div class="info-item">
                    <div class="status-value" id="currentTime">--</div>
                    <div class="status-label">Current Time</div>
                </div>
            </div>

            <button class="btn" onclick="rebootSystem()">Reboot System</button>
        </div>
    </div>

    <script>
        let isOnline = true;
        let isRecording = false;
        let recordingStartTime = null;
        let recordingTimer = null;
        
        // Update brightness display
        const brightnessSlider = document.getElementById('brightnessSlider');
        const brightnessValue = document.getElementById('brightnessValue');
        
        brightnessSlider.addEventListener('input', function() {
            brightnessValue.textContent = this.value + '%';
        });

        // Set brightness function
        function setBrightness() {
            const brightness = brightnessSlider.value;
            showRefreshIndicator();
            
            fetch('/set_pwm', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `brightness=${brightness}`
            })
            .then(response => {
                if (response.ok) {
                    updateConnectionStatus(true);
                } else {
                    throw new Error('Network response was not ok');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                updateConnectionStatus(false);
            });
        }

        // Toggle recording function
        function toggleRecording() {
            showRefreshIndicator();
            
            const endpoint = isRecording ? '/stop_recording' : '/start_recording';
            
            fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Network response was not ok');
                }
            })
            .then(data => {
                updateRecordingStatus(data.recording, data.duration || 0);
                updateConnectionStatus(true);
            })
            .catch(error => {
                console.error('Error:', error);
                updateConnectionStatus(false);
            });
        }

        // Update recording status
        function updateRecordingStatus(recording, duration = 0) {
            isRecording = recording;
            const recordingStatus = document.getElementById('recordingStatus');
            const recordingIndicator = document.getElementById('recordingIndicator');
            const recordingBtn = document.getElementById('recordingBtn');
            const recordingLabel = document.getElementById('recordingLabel');
            
            if (recording) {
                recordingStatus.classList.add('active');
                recordingIndicator.classList.add('active');
                recordingBtn.classList.add('recording');
                recordingBtn.textContent = 'Stop Recording';
                recordingLabel.textContent = 'Recording Active';
                
                // Start timer
                recordingStartTime = Date.now() - (duration * 1000);
                startRecordingTimer();
            } else {
                recordingStatus.classList.remove('active');
                recordingIndicator.classList.remove('active');
                recordingBtn.classList.remove('recording');
                recordingBtn.textContent = 'Start Recording';
                recordingLabel.textContent = 'Not Recording';
                
                // Stop timer
                stopRecordingTimer();
                document.getElementById('recordingDuration').textContent = '00:00:00';
            }
        }

        // Start recording timer
        function startRecordingTimer() {
            if (recordingTimer) clearInterval(recordingTimer);
            
            recordingTimer = setInterval(() => {
                if (recordingStartTime) {
                    const elapsed = Math.floor((Date.now() - recordingStartTime) / 1000);
                    const hours = Math.floor(elapsed / 3600);
                    const minutes = Math.floor((elapsed % 3600) / 60);
                    const seconds = elapsed % 60;
                    
                    const timeString = 
                        String(hours).padStart(2, '0') + ':' +
                        String(minutes).padStart(2, '0') + ':' +
                        String(seconds).padStart(2, '0');
                    
                    document.getElementById('recordingDuration').textContent = timeString;
                }
            }, 1000);
        }

        // Stop recording timer
        function stopRecordingTimer() {
            if (recordingTimer) {
                clearInterval(recordingTimer);
                recordingTimer = null;
            }
        }

        // Reboot system function
        function rebootSystem() {
            if (confirm('Are you sure you want to reboot the system?')) {
                showRefreshIndicator();
                fetch('/reboot', { method: 'POST' })
                .then(response => {
                    if (response.ok) {
                        alert('System reboot initiated. Please wait...');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    updateConnectionStatus(false);
                });
            }
        }

        // Show refresh indicator
        function showRefreshIndicator() {
            const indicator = document.getElementById('refreshIndicator');
            indicator.classList.add('show');
            setTimeout(() => {
                indicator.classList.remove('show');
            }, 2000);
        }

        // Update connection status
        function updateConnectionStatus(online) {
            const status = document.getElementById('connectionStatus');
            isOnline = online;
            
            if (online) {
                status.className = 'connection-status online';
                status.textContent = '● Online';
            } else {
                status.className = 'connection-status offline';
                status.textContent = '● Offline';
            }
        }

        // Auto-refresh data every 5 seconds
        function refreshData() {
            if (!isOnline) return;
            
            showRefreshIndicator();
            
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    // Update battery info
                    document.getElementById('totalVoltage').textContent = data.total_voltage + 'V';
                    document.getElementById('chargePercent').textContent = data.charge_percent + '%';
                    document.getElementById('chargerStatus').textContent = data.charger_status;
                    
                    // Update battery visual
                    const batteryFill = document.getElementById('batteryFill');
                    const batteryText = document.getElementById('batteryText');
                    batteryFill.style.width = data.charge_percent + '%';
                    batteryText.textContent = data.charge_percent + '%';
                    
                    // Update recording status
                    if (data.recording !== undefined) {
                        updateRecordingStatus(data.recording, data.recording_duration || 0);
                    }
                    
                    // Update video info
                    if (data.video_quality) {
                        document.getElementById('videoQuality').textContent = data.video_quality;
                    }
                    if (data.storage_used !== undefined) {
                        document.getElementById('storageUsed').textContent = data.storage_used.toFixed(1);
                    }
                    
                    // Update IMU data
                    document.getElementById('pitch').textContent = data.pitch + '°';
                    document.getElementById('roll').textContent = data.roll + '°';
                    document.getElementById('accelX').textContent = data.accel[0];
                    document.getElementById('accelY').textContent = data.accel[1];
                    document.getElementById('accelZ').textContent = data.accel[2];
                    document.getElementById('gyroX').textContent = data.gyro[0];
                    document.getElementById('gyroY').textContent = data.gyro[1];
                    document.getElementById('gyroZ').textContent = data.gyro[2];
                    
                    // Update system info
                    document.getElementById('uptime').textContent = data.uptime;
                    document.getElementById('storage').textContent = data.free_storage;
                    document.getElementById('temperature').textContent = data.temperature;
                    document.getElementById('currentTime').textContent = data.current_time;
                    
                    updateConnectionStatus(true);
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                    updateConnectionStatus(false);
                });
        }

        // Start auto-refresh
        setInterval(refreshData, 5000);
        
        // Initial data load
        refreshData();

        // Update current time every second
        function updateTime() {
            const now = new Date();
            const timeString = now.toLocaleTimeString();
            if (document.getElementById('currentTime')) {
                document.getElementById('currentTime').textContent = timeString;
            }
        }
        
        setInterval(updateTime, 1000);
        updateTime();
    </script>
</body>
</html>
