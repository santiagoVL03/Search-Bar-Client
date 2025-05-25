import React from 'react'

export default function Search() {
  return (
    <div className='container'>
        <h2>
            Search a video
        </h2>
        <div className='input-group mb-3'>
            <input type="text" className='form-control' id="search-video" placeholder='Search a video' />
        </div>
    </div>
  )
}
