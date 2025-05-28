import React, { useState } from 'react'

function Search() {
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

      {/* Mostrar resultados */}
      {results && <Results data={results} />}
    </div>
  )
}

function Results({ data }) {
  const [filterText, setFilterText] = useState('')

  const output = data?.data?.output || {}

  const filteredOutput = Object.entries(output).reduce((acc, [video, objects]) => {
    const filteredObjects = objects.filter(obj =>
      obj.object.toLowerCase().includes(filterText.toLowerCase())
    )
    if (filteredObjects.length > 0) {
      acc[video] = filteredObjects
    }
    return acc
  }, {})

  return (
    <div>
      <input
        type="text"
        placeholder="Filter objects..."
        value={filterText}
        onChange={e => setFilterText(e.target.value)}
        style={{ marginBottom: '20px', padding: '5px' }}
      />
      {Object.keys(filteredOutput).length === 0 ? (
        <p>No results found.</p>
      ) : (
        Object.entries(filteredOutput).map(([video, objects]) => (
          <div key={video} style={{ marginBottom: '30px' }}>
            <h3>{video}</h3>
            <table border="1" cellPadding="5" cellSpacing="0">
              <thead>
                <tr>
                  <th>Object</th>
                  <th>Count</th>
                </tr>
              </thead>
              <tbody>
                {objects.map(({ object, count }, i) => (
                  <tr key={i}>
                    <td>{object}</td>
                    <td>{count}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ))
      )}
    </div>
  )
}

export default Search