import React, { useState } from 'react'
import { Charge_results } from '../../hooks/Search'

export default function Results({ data }) {
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
