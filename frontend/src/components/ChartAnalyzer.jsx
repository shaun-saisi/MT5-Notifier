import React, { useState, useCallback, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import './ChartAnalyzer.css';

const ChartAnalyzer = ({ onAnalysisStart, onAnalysisComplete, onError, loading }) => {
  const [files, setFiles] = useState([]);
  const [tradeDuration, setTradeDuration] = useState('24-72');
  const [riskReward, setRiskReward] = useState('1:3');
  const [previews, setPreviews] = useState([]);
  const [ollamaStatus, setOllamaStatus] = useState(null);
  const [availableModels, setAvailableModels] = useState([]);

  // Check Ollama status on load
  useEffect(() => {
    checkOllamaStatus();
  }, []);

  const checkOllamaStatus = async () => {
    try {
      const response = await axios.get('http://localhost:5000/health');
      setOllamaStatus(response.data.ollama_status);
      
      // Fetch available models
      const modelsResponse = await axios.get('http://localhost:5000/models');
      if (modelsResponse.data.models) {
        setAvailableModels(modelsResponse.data.models.map(m => m.name));
      }
    } catch (error) {
      setOllamaStatus('offline');
    }
  };

  const onDrop = useCallback((acceptedFiles) => {
    // Sort files by timeframe priority
    const priority = { 'W1': 1, 'D1': 2, 'H4': 3, 'H1': 4, 'M30': 5, 'M15': 6, 'MS': 7 };
    const getPriority = (filename) => {
      for (const [key, value] of Object.entries(priority)) {
        if (filename.toUpperCase().includes(key)) return value;
      }
      return 99;
    };
    
    const sortedFiles = [...acceptedFiles].sort((a, b) => getPriority(a.name) - getPriority(b.name));
    setFiles(sortedFiles);
    
    // Create preview URLs
    const newPreviews = sortedFiles.map(file => ({
      file,
      preview: URL.createObjectURL(file)
    }));
    
    // Clean up old previews
    previews.forEach(preview => URL.revokeObjectURL(preview.preview));
    setPreviews(newPreviews);
  }, [previews]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/png': ['.png'],
      'image/jpeg': ['.jpg', '.jpeg'],
      'image/webp': ['.webp']
    },
    maxFiles: 10
  });

  const handleSubmit = async () => {
    if (files.length === 0) {
      onError('Please upload at least one chart screenshot');
      return;
    }

    if (ollamaStatus !== 'online') {
      onError('Ollama is not running. Please start Ollama first:\nollama serve');
      return;
    }

    onAnalysisStart();

    const formData = new FormData();
    files.forEach(file => {
      formData.append('charts', file);
    });
    formData.append('trade_duration', tradeDuration);
    formData.append('risk_reward_ratio', riskReward);

    try {
      const response = await axios.post('http://localhost:5000/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        timeout: 180000 // 180 seconds for vision model
      });

      if (response.data.success) {
        onAnalysisComplete(response.data.analysis);
      } else {
        onError(response.data.error || 'Analysis failed');
      }
    } catch (err) {
      console.error('Error:', err);
      if (err.code === 'ECONNREFUSED') {
        onError('Cannot connect to backend. Start Flask: python app.py');
      } else if (err.message.includes('timeout')) {
        onError('Analysis timeout - try with fewer or smaller images');
      } else {
        onError(err.response?.data?.error || err.message || 'Failed to analyze charts');
      }
    }
  };

  const removeFile = (index) => {
    const newFiles = [...files];
    newFiles.splice(index, 1);
    setFiles(newFiles);
    
    const newPreviews = [...previews];
    URL.revokeObjectURL(newPreviews[index].preview);
    newPreviews.splice(index, 1);
    setPreviews(newPreviews);
  };

  return (
    <div className="chart-analyzer">
      <div className={`ollama-status ${ollamaStatus === 'online' ? 'online' : 'offline'}`}>
        {ollamaStatus === 'online' ? (
          <span>✅ Ollama Running | Model: qwen3-vl:4b</span>
        ) : ollamaStatus === 'offline' ? (
          <span>❌ Ollama Not Running - Run: <code>ollama serve</code></span>
        ) : (
          <span>🔄 Checking Ollama Status...</span>
        )}
      </div>

      <div className="upload-section">
        <h2>📸 Upload Chart Screenshots</h2>
        <div {...getRootProps()} className={`dropzone ${isDragActive ? 'active' : ''}`}>
          <input {...getInputProps()} />
          {isDragActive ? (
            <p>📥 Drop your charts here...</p>
          ) : (
            <p>📤 Drag & drop chart screenshots here, or click to select</p>
          )}
          <small>Supports PNG, JPG, WEBP | Recommended: W1, D1, H4, H1, M30</small>
        </div>

        {previews.length > 0 && (
          <div className="preview-grid">
            <div className="preview-header">
              <h3>📊 Uploaded Charts ({previews.length})</h3>
              <button onClick={() => {
                setFiles([]);
                previews.forEach(p => URL.revokeObjectURL(p.preview));
                setPreviews([]);
              }} className="clear-btn">Clear All</button>
            </div>
            <div className="preview-container">
              {previews.map((preview, index) => (
                <div key={index} className="preview-item">
                  <img src={preview.preview} alt={`Chart ${index + 1}`} />
                  <button onClick={() => removeFile(index)} className="remove-btn" title="Remove">✖</button>
                  <div className="preview-info">
                    <span className="timeframe-badge">
                      {preview.file.name.match(/MN|W1|D1|H4|H1|M30|M15|MS/)?.[0] || '???'}
                    </span>
                    <span className="filename" title={preview.file.name}>
                      {preview.file.name.substring(0, 25)}...
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      <div className="settings-section">
        <h2>⚙️ Trading Parameters</h2>
        <div className="param-group">
          <label>
            Trade Duration:
            <select value={tradeDuration} onChange={(e) => setTradeDuration(e.target.value)}>
              <option value="4-8">4-8 hours (Intraday)</option>
              <option value="24-72">24-72 hours (Swing Trade)</option>
              <option value="48-96">48-96 hours (Position Trade)</option>
            </select>
          </label>

          <label>
            Risk-Reward Ratio:
            <select value={riskReward} onChange={(e) => setRiskReward(e.target.value)}>
              <option value="1:2">1:2 (Moderate)</option>
              <option value="1:3">1:3 (Conservative - Recommended)</option>
              <option value="1:4">1:4 (Aggressive)</option>
            </select>
          </label>
        </div>

        <button 
          onClick={handleSubmit} 
          disabled={loading || files.length === 0 || ollamaStatus !== 'online'}
          className={`analyze-btn ${loading ? 'loading' : ''}`}
        >
          {loading ? (
            <>
              <span className="spinner"></span>
              Analyzing {files.length} charts with Qwen3-VL...
            </>
          ) : (
            `🔍 Analyze ${files.length} Chart${files.length !== 1 ? 's' : ''}`
          )}
        </button>

        <div className="tips">
          <h4>💡 Tips for Best Results:</h4>
          <ul>
            <li>Include at least <strong>3 timeframes</strong> (W1 + D1 + H4 recommended)</li>
            <li>Ensure <strong>price scales and candlesticks</strong> are clearly visible</li>
            <li>Take screenshots with <strong>timeframe labels visible</strong> (W1, D1, H4, etc.)</li>
            <li>Make sure <strong>Ollama is running</strong>: <code>ollama run qwen3-vl:4b</code></li>
            <li>The AI will ONLY trade clear trends, never sideways markets</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default ChartAnalyzer;