import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Search from './pages/search/Search'
import Layout from './components/Layout'
import './css/general.css'


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={
          <Layout>
            <Home />
          </Layout>
        } />
        <Route path="/search" element={
          <Layout>
            <Search />
          </Layout>
        } />
      </Routes>
    </Router>
  )
}

function Home() {
  return (
    <div className="container text-center">
      <h1>Welcome to the Search App</h1>
      <a href="/search" className="btn btn-lg mt-3 btn-custom">
        <span>Search a video</span>
      </a>
    </div>
  )
}

export default App
