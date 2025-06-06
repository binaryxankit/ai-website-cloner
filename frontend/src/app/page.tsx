'use client';

import { useState } from 'react';
import styles from './page.module.css';

export default function Home() {
  const [url, setUrl] = useState('');
  const [clonedHtml, setClonedHtml] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [scale, setScale] = useState(1);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setClonedHtml('');
    setScale(1);

    try {
      const response = await fetch('http://localhost:8000/clone', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });

      if (!response.ok) {
        throw new Error('Failed to clone website');
      }

      const data = await response.json();
      setClonedHtml(data.html);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleScale = (newScale: number) => {
    setScale(newScale);
  };

  return (
    <main className={styles.main}>
      <div className={styles.container}>
        <h1 className={styles.title}>Website Cloner</h1>
        <p className={styles.description}>
          Enter a website URL to create a pixel-perfect clone
        </p>

        <form onSubmit={handleSubmit} className={styles.form}>
          <input
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="Enter website URL (e.g., https://example.com)"
            required
            className={styles.input}
          />
          <button
            type="submit"
            disabled={loading}
            className={styles.button}
            suppressHydrationWarning
          >
            {loading ? (
              <>
                <span className={styles.loadingSpinner} />
                Cloning...
              </>
            ) : (
              'Clone Website'
            )}
          </button>
        </form>

        {error && (
          <div className={styles.error}>
            {error}
          </div>
        )}

        {clonedHtml && (
          <div className={styles.preview}>
            <h2>
              Preview
              <div className={styles.previewControls}>
                <button onClick={() => handleScale(0.5)} suppressHydrationWarning>50%</button>
                <button onClick={() => handleScale(0.75)} suppressHydrationWarning>75%</button>
                <button onClick={() => handleScale(1)} suppressHydrationWarning>100%</button>
                <button onClick={() => handleScale(1.25)} suppressHydrationWarning>125%</button>
                <button onClick={() => handleScale(1.5)} suppressHydrationWarning>150%</button>
        </div>
            </h2>
            <div 
              className={styles.previewFrame}
              style={{
                transform: `scale(${scale})`,
                transformOrigin: 'top left',
                width: `${100 / scale}%`,
                minHeight: `${100 / scale}%`,
                maxWidth: '100%',
                overflow: 'auto',
              }}
        >
              <div 
                style={{
                  width: '100%',
                  minWidth: '100%',
                  height: 'auto',
                }}
                dangerouslySetInnerHTML={{ __html: clonedHtml }}
          />
            </div>
          </div>
        )}
    </div>
    </main>
  );
}
