import React from 'react'
import './css/layout.css'

export default function Layout({ children }) {
  return (
    <div className="d-flex flex-column min-vh-100 custom-layer">
      {/* Header fijo arriba */}
      <header className="navbar navbar-dark bg-dark text-white px-4">
        <span>Just Another Search Bar</span>
      </header>

      {/* Main centrado vertical y horizontalmente */}
      <main className="flex-grow-1 d-flex justify-content-center align-items-center">
        <div className="w-100" style={{ maxWidth: '600px' }}>
          {children}
        </div>
      </main>

      {/* Footer fijo abajo */}
      <footer className="bg-light text-center text-muted py-3 border-top mt-auto">
        <small>&copy; 2025 Search App</small>
      </footer>
    </div>
  )
}
