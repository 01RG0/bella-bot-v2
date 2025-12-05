import { useState, useEffect } from 'react'

export function useBot() {
  const [status, setStatus] = useState('offline')

  useEffect(() => {
    // Fetch bot status
  }, [])

  return { status }
}