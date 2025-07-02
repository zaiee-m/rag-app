import React, {useState} from 'react'
import Search from '../components/Search'
import Results from '../components/Results'
import Options from '../components/Options'


function Home() {

  const [query, setQuery] = useState() 
  const [choice, setChoice] = useState() 

  return (
    <div className="home">
      <div className='home-container'>
        <Search setQuery={setQuery}/>
        <Results query={query} setChoice={setChoice}/>
        <Options choice={choice}/>
      </div>
    </div>
  )
}

export default Home
