import React, { useState } from 'react'
import Results from '../results/Result'
import { useSearch } from '../../hooks/useSearch'
import Swal from 'sweetalert2'

export default function Search() {
  const [searchInput, setSearchInput] = useState('')
  const { loading, error, results, searchVideos } = useSearch()

  const handleSearch = () => {
    if (searchInput.trim() === '') {
      Swal.fire({
        icon: 'warning',
        title: 'Empty Search',
        text: 'Please enter a search term.',
        confirmButtonText: 'OK'
      })
      return
    }
    searchVideos(searchInput)
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
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}
      {results && <Results data={results} />}
    </div>
  )
}
