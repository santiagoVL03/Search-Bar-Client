import React from 'react'
import { Charge_results } from '../../hooks/Search'

export default function Search() {
  
  return (
    <div className='container'>
        <h2>
            Search for a video
        </h2>
        <div className='input-group mb-3'>
            <input type="text" className='form-control' id="search-video" placeholder='Search a video' />
            <button onClick={Charge_results} className='btn btn-custom' type='button' id='search-button'>Search</button>
        </div>
    </div>
  )
}
