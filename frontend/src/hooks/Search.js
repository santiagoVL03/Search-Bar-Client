import { useState } from 'react'
import { fetchSearchResults, fetchSearchResultsSpark } from '../services/Api'

export function useSearch() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [results, setResults] = useState(null)

  const searchVideos = async (query, type) => {
    setLoading(true)
    setError(null)

    try {
      if (type === 'spark') {
        const data = await fetchSearchResultsSpark(query)
        setResults(data)
      } else if (type === 'mr') {
        const data = await fetchSearchResults(query)
        setResults(data)
      } else {
        throw new Error('You must specify a search type (mr or spark)')
      }
    } catch (err) {
      setError(err.message || 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  return { loading, error, results, searchVideos }
}
