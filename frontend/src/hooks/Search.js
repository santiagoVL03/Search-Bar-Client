import { useState } from 'react'
import { fetchSearchResults } from '../services/Api'

export function useSearch() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [results, setResults] = useState(null)

  const searchVideos = async (query) => {
    setLoading(true)
    setError(null)

    try {
      const data = await fetchSearchResults(query)
      setResults(data)
    } catch (err) {
      setError(err.message || 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  return { loading, error, results, searchVideos }
}
