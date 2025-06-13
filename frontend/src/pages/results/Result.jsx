import React from 'react'
import { Charge_results } from '../../hooks/Search'

export default function Results({ data }) {
  const output = data?.data?.output || {}

  const filteredOutput = Object.entries(output).reduce((acc, [video, objects]) => {
    const filteredObjects = objects.filter(obj =>
      obj.object.toLowerCase()
    )
    if (filteredObjects.length > 0) {
      acc[video] = filteredObjects
    }
    return acc
  }, {})

  return (
    <div>
      {
        Object.entries(filteredOutput).map(([video, objects]) => (
          <div key={video} style={{ marginBottom: '30px' }}>
            <h3>{video}</h3>
            <table border="1" cellPadding="5" cellSpacing="0">
              <thead>
                <tr>
                  <th>Object</th>
                  <th>Count</th>
                  <th>Video</th>
                </tr>
              </thead>
              <tbody>
                {objects.map(({ object, count }, i) => (
                  <tr key={i}>
                    <td>{object}</td>
                    <td>{count}</td>
                    <td>
                      <a
                        className="btn btn-dark"
                        href={`http://localhost:5000/api/v1/video/${video}`} target="_blank" rel="noopener noreferrer">
                        Watch Video
                      </a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )
        )}
    </div>
  )
}
