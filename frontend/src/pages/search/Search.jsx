import React, { useState } from 'react'
import Results from '../results/Result'
import { useSearch } from '../../hooks/Search'
import Swal from 'sweetalert2'
import 'bootstrap-icons/font/bootstrap-icons.css';

export default function Search() {
  const [searchInput, setSearchInput] = useState('')
  const { loading, error, results, searchVideos } = useSearch()

  const handleSearchWithType = (type) => {
    if (searchInput.trim() === '') {
      Swal.fire({
        icon: 'warning',
        title: 'Empty Search',
        text: 'Please enter a search term.',
        confirmButtonText: 'OK'
      })
      return
    }
    searchVideos(searchInput, type)
  }

  return (
    <div className="container mt-5">
      <h2 className="mb-4 text-center">Search for a video</h2>

      <div className="mb-4">
        <div className="input-group input-group-lg">
          <span className="input-group-text bg-white">
            <i className="bi bi-search"></i>
          </span>
          <input
            type="text"
            className="form-control"
            placeholder="Search a video..."
            value={searchInput}
            onChange={e => setSearchInput(e.target.value)}
            id="search-video"
          />
        </div>
      </div>

      <div className="d-flex justify-content-center gap-3 mb-4">
        <button onClick={() => handleSearchWithType('mr')} className="btn btn-custom">
          Search with MR
        </button>
        <button onClick={() => handleSearchWithType('spark')} className="btn btn-custom">
          Search with Spark
        </button>
      </div>

      {loading && <p className="text-center">Loading results...</p>}
      {error && <p className="text-center text-danger">Error: {error}</p>}
      {results && <Results data={results} />}
    </div>
  );

}
