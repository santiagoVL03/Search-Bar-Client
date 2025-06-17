import React from 'react';

export default function Results({ data }) {
  const output = data?.data?.output || {};

  return (
    <div className="mt-4">
      <h3 className="mb-4 text-center">Search Results</h3>

      {Object.entries(output).length === 0 && (
        <p className="text-center text-muted">No results found.</p>
      )}

      {Object.entries(output).sort((a, b) => b[1].views - a[1].views).map(([video, info]) => (
        <div key={video} className="card mb-4 shadow-sm">
          <div className="card-header d-flex justify-content-between align-items-center">
            <div>
              <h5 className="mb-1">{video}</h5>
              <small className="text-muted">Views: {info.views}</small>
            </div>
            <a
              className="btn btn-sm btn-custom"
              href={`http://localhost:5000/api/v1/video/${video}`}
              target="_blank"
              rel="noopener noreferrer"
            >
              <i className="bi bi-play-circle me-1"></i>
              Watch Video
            </a>
          </div>

          <div className="card-body">
            <div className="table-responsive">
              <table className="table table-striped table-bordered mb-0">
                <thead className="table-dark">
                  <tr>
                    <th>Object</th>
                    <th>Count</th>
                  </tr>
                </thead>
                <tbody>
                  {info.objects.map(({ object, count }, i) => (
                    <tr key={i}>
                      <td>{object}</td>
                      <td>{count}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
