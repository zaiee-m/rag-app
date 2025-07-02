import React, {useState} from 'react'

function Results({query, setChoice}) {

  const [showResults, setShowResults] = useState(true);

  const handleClick = (item) => {
    setChoice(item)
    setShowResults(false)
  }

  return (
    <>
      {showResults && query && <div className='results'>
        {query?.map((item, index)=>{
          return <div onClick={()=>handleClick(item)} className="result-item">
              {item.library_name}
            </div>
        })}
      </div>}
    </>
  )
}

export default Results
