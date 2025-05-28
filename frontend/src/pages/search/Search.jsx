import React, { useState } from 'react'
import Results from '../results/Result'

export default function Search() {
  const [searchInput, setSearchInput] = useState('')
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSearch = () => {
    if (searchInput.trim() === '') {
      alert('Please enter a search term')
      return
    }

    setLoading(true)
    setError(null)

    const url = `http://localhost:5000/api/v1/search/?word=${searchInput}`

    fetch(url)
      .then(res => {
        if (!res.ok) throw new Error('Network response was not ok')
        return res.json()
      })
      .then(data => {
        setResults(data)
        setLoading(false)
      })
      .catch(err => {
        setError(err.message)
        setLoading(false)
      })
  }

  return (
    <div className='container'>
      <h2>Search for a video</h2>
      <div className='input-group mb-3'>
        <input
          type="text"
          className='form-control'
          placeholder='Search a video'
          value={searchInput}
          onChange={e => setSearchInput(e.target.value)}
          id="search-video"
        />
        <button onClick={handleSearch} className='btn btn-custom' type='button'>
          Search
        </button>
      </div>

      {loading && <p>Loading results...</p>}
      {error && <p style={{color: 'red'}}>Error: {error}</p>}

      {results && <Results data={results} />}
    </div>
  )
}
