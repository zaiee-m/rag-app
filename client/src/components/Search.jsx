import React, { useState } from 'react'
import searchIcon from '../img/search.svg'
import FileUploader from './FileUploader'

function Search({setQuery}) {

  const [library, setLibrary] = useState({})

    const searchDataBase = async (name) => {
      try{
        const response = await fetch(`/search?name=${name}`)
        const data = await response.json();
        setQuery(data)
      }
      catch(err){
        console.log(err)
      }
    }
    
    
    const handleKey = async (event) => {
      let debounceTimer;
      const value = event.target.value;
      setLibrary(value);
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        searchDataBase(value);
      }, 300);
    }


  return (
    <div className='search-form'>
      <div className='form'>
        <input type="text" placeholder='Search..' onChange={handleKey}/>
        <button type="submit">
          <img src={searchIcon} alt="" />
        </button>
        <FileUploader/>
      </div>
    </div>
  )
}

export default Search
