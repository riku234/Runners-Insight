import React, { useState, useEffect } from 'react'
import './App.css'

interface AnalysisResult {
  analysis_id: string
  timestamp: string
  features: {
    cadence: number
    stride_length: number
    landing_angle: number
    vertical_oscillation: number
    ground_contact_time: number
  }
  video_quality: string
  processing_status: string
}

interface AdviceResult {
  advice_id: string
  generated_at: string
  user_features: Record<string, number>
  advice_text: string
  relevant_keywords: string[]
  confidence_score: number
  llm_model: string
}

function App() {
  const [apiStatus, setApiStatus] = useState<string>('未確認')
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null)
  const [advice, setAdvice] = useState<AdviceResult | null>(null)
  const [loading, setLoading] = useState<boolean>(false)
  const [selectedVideo, setSelectedVideo] = useState<File | null>(null)
  const [videoPreview, setVideoPreview] = useState<string | null>(null)
  const [errorMessage, setErrorMessage] = useState<string>('')

  const API_BASE = 'http://127.0.0.1:8000/api'

  const checkApiHealth = async () => {
    try {
      setErrorMessage('')
      const response = await fetch(`${API_BASE}/health/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        mode: 'cors',  // CORSモードを明示的に指定
        credentials: 'include',  // クレデンシャルを含める
      })
      if (response.ok) {
        const data = await response.json()
        setApiStatus('✅ 正常')
        console.log('API Health Check:', data)
      } else {
        setApiStatus('❌ エラー')
        setErrorMessage(`APIエラー: ${response.status} ${response.statusText}`)
      }
    } catch (error) {
      setApiStatus('❌ 接続失敗')
      if (error instanceof TypeError && error.message.includes('CORS')) {
        setErrorMessage(`CORS エラー: クロスオリジンリクエストが拒否されました`)
      } else if (error instanceof TypeError && error.message.includes('Failed to fetch')) {
        setErrorMessage(`接続エラー: バックエンドサーバーに接続できません (${API_BASE})`)
      } else {
        setErrorMessage(`接続エラー: ${error}`)
      }
      console.error('API接続エラー:', error)
    }
  }

  const handleVideoUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      // 動画ファイルの検証
      if (!file.type.startsWith('video/')) {
        setErrorMessage('動画ファイルを選択してください')
        return
      }
      
      // ファイルサイズ制限 (100MB)
      if (file.size > 100 * 1024 * 1024) {
        setErrorMessage('ファイルサイズは100MB以下にしてください')
        return
      }

      setSelectedVideo(file)
      setErrorMessage('')
      
      // プレビュー用のURL作成
      const previewUrl = URL.createObjectURL(file)
      setVideoPreview(previewUrl)
    }
  }

  const runMockAnalysis = async () => {
    setLoading(true)
    setErrorMessage('')
    try {
      const response = await fetch(`${API_BASE}/analysis/mock/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        mode: 'cors',
        credentials: 'include',
      })
      if (response.ok) {
        const data = await response.json()
        setAnalysisResult(data)
        console.log('Analysis Result:', data)
      } else {
        setErrorMessage(`分析エラー: ${response.status} ${response.statusText}`)
        console.error('分析データの取得に失敗しました')
      }
    } catch (error) {
      setErrorMessage(`分析接続エラー: ${error}`)
      console.error('API接続エラー:', error)
    } finally {
      setLoading(false)
    }
  }

  const runVideoAnalysis = async () => {
    if (!selectedVideo) {
      setErrorMessage('動画ファイルを選択してください')
      return
    }

    setLoading(true)
    setErrorMessage('')
    
    try {
      // Step 1: 動画ファイルをアップロード
      const formData = new FormData()
      formData.append('video', selectedVideo)
      
      const uploadResponse = await fetch(`${API_BASE}/videos/upload/`, {
        method: 'POST',
        body: formData  // Content-Typeヘッダーは自動設定される
      })
      
      if (!uploadResponse.ok) {
        throw new Error(`Upload failed: ${uploadResponse.status}`)
      }
      
      const uploadData = await uploadResponse.json()
      console.log('Video uploaded:', uploadData)
      
      // Step 2: アップロードされた動画を解析
      const analysisResponse = await fetch(`${API_BASE}/videos/analyze/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          video_id: uploadData.video_id
        })
      })
      
      if (analysisResponse.ok) {
        const analysisData = await analysisResponse.json()
        // API仕様に合わせてデータ構造を調整
        const formattedResult = {
          analysis_id: analysisData.analysis_id,
          timestamp: analysisData.analysis_timestamp,
          features: analysisData.features,
          video_quality: 'high', // デフォルト値
          processing_status: analysisData.status
        }
        setAnalysisResult(formattedResult)
        console.log('Video Analysis Result:', analysisData)
      } else {
        throw new Error(`Analysis failed: ${analysisResponse.status}`)
      }
      
    } catch (error) {
      setErrorMessage(`動画分析エラー: ${error}`)
      console.error('動画分析エラー:', error)
    } finally {
      setLoading(false)
    }
  }

  const generateAdvice = async () => {
    if (!analysisResult) {
      setErrorMessage('先に分析を実行してください')
      return
    }

    setLoading(true)
    setErrorMessage('')
    try {
      const response = await fetch(`${API_BASE}/advice/generate/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        mode: 'cors',
        credentials: 'include',
        body: JSON.stringify({
          features: analysisResult.features
        })
      })

      if (response.ok) {
        const data = await response.json()
        setAdvice(data)
        console.log('Advice Generated:', data)
      } else {
        setErrorMessage(`アドバイス生成エラー: ${response.status} ${response.statusText}`)
        console.error('アドバイス生成に失敗しました')
      }
    } catch (error) {
      setErrorMessage(`アドバイス生成接続エラー: ${error}`)
      console.error('API接続エラー:', error)
    } finally {
      setLoading(false)
    }
  }

  const clearData = () => {
    setSelectedVideo(null)
    setVideoPreview(null)
    setAnalysisResult(null)
    setAdvice(null)
    setErrorMessage('')
  }

  useEffect(() => {
    checkApiHealth()
  }, [])

  // プレビューURLのクリーンアップ
  useEffect(() => {
    return () => {
      if (videoPreview) {
        URL.revokeObjectURL(videoPreview)
      }
    }
  }, [videoPreview])

  return (
    <div className="app">
      <header className="app-header">
        <h1>🏃‍♂️ Runners' Insight</h1>
        <p>ランニングフォーム解析・AIアドバイスシステム</p>
      </header>

      <main className="app-main">
        {errorMessage && (
          <div className="error-banner">
            <h3>⚠️ エラー</h3>
            <p>{errorMessage}</p>
            <button onClick={() => setErrorMessage('')} className="btn-secondary">
              閉じる
            </button>
          </div>
        )}

        <section className="status-section">
          <h2>📊 システム状態</h2>
          <div className="status-card">
            <p><strong>API状態:</strong> {apiStatus}</p>
            <button onClick={checkApiHealth} className="btn-secondary">
              再確認
            </button>
          </div>
        </section>

        <section className="upload-section">
          <h2>🎥 動画アップロード</h2>
          <div className="upload-card">
            <div className="video-upload-area">
              <input
                type="file"
                accept="video/*"
                onChange={handleVideoUpload}
                className="video-input"
                id="video-upload"
              />
              <label htmlFor="video-upload" className="upload-label">
                {selectedVideo ? selectedVideo.name : '動画ファイルを選択'}
              </label>
            </div>
            
            {videoPreview && (
              <div className="video-preview">
                <h4>プレビュー:</h4>
                <video 
                  src={videoPreview} 
                  controls 
                  className="preview-video"
                  width="300"
                  height="200"
                />
                <div className="video-info">
                  <p><strong>ファイル名:</strong> {selectedVideo?.name}</p>
                  <p><strong>サイズ:</strong> {(selectedVideo?.size || 0 / (1024 * 1024)).toFixed(2)} MB</p>
                </div>
              </div>
            )}

            <div className="upload-actions">
              <button 
                onClick={runVideoAnalysis} 
                disabled={loading || !selectedVideo}
                className="btn-primary"
              >
                {loading ? '分析中...' : '動画分析実行'}
              </button>
              <button 
                onClick={clearData} 
                className="btn-secondary"
              >
                リセット
              </button>
            </div>
          </div>
        </section>

        <section className="analysis-section">
          <h2>🧪 モック分析（テスト用）</h2>
          <div className="analysis-card">
            <p className="section-description">
              動画がない場合のテスト用モック分析です
            </p>
            <button 
              onClick={runMockAnalysis} 
              disabled={loading}
              className="btn-secondary"
            >
              {loading ? '分析中...' : 'モック分析実行'}
            </button>

            {analysisResult && (
              <div className="result-display">
                <h3>📈 解析結果</h3>
                <div className="features-grid">
                  <div className="feature-item">
                    <label>ピッチ</label>
                    <span>{analysisResult.features.cadence} 歩/分</span>
                  </div>
                  <div className="feature-item">
                    <label>ストライド長</label>
                    <span>{analysisResult.features.stride_length} cm</span>
                  </div>
                  <div className="feature-item">
                    <label>着地角度</label>
                    <span>{analysisResult.features.landing_angle}°</span>
                  </div>
                  <div className="feature-item">
                    <label>上下動</label>
                    <span>{analysisResult.features.vertical_oscillation} cm</span>
                  </div>
                  <div className="feature-item">
                    <label>接地時間</label>
                    <span>{analysisResult.features.ground_contact_time} ms</span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </section>

        <section className="advice-section">
          <h2>🤖 AIアドバイス生成</h2>
          <div className="advice-card">
            <button 
              onClick={generateAdvice} 
              disabled={loading || !analysisResult}
              className="btn-primary"
            >
              {loading ? 'アドバイス生成中...' : 'アドバイス生成'}
            </button>

            {advice && (
              <div className="advice-display">
                <div className="advice-meta">
                  <h3>💡 パーソナライズドアドバイス</h3>
                  <p className="confidence">信頼度: {(advice.confidence_score * 100).toFixed(1)}%</p>
                </div>
                <div className="advice-content">
                  <pre>{advice.advice_text}</pre>
                </div>
                <div className="advice-keywords">
                  <h4>関連キーワード:</h4>
                  <div className="keywords">
                    {advice.relevant_keywords.map((keyword, index) => (
                      <span key={index} className="keyword-tag">{keyword}</span>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        </section>
      </main>

      <footer className="app-footer">
        <p>&copy; 2025 Runners' Insight - ランニングパフォーマンス向上支援システム</p>
      </footer>
    </div>
  )
}

export default App
