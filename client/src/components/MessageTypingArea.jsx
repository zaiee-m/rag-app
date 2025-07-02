import React, {useState} from 'react'

function MessageTypingArea({setPrompt, loading}) {
    const [input, setInput] = useState("");

    const handleSubmit = (event) => {
        event.preventDefault()  
       
        const value = {
            "text": event.target[0].value,
            "type": "",
        }
            
        setPrompt(value)
        setInput("");
    }

  return (
    <div className='message-typing-area'>
        <form action="" onSubmit={handleSubmit}>
            <input /*disabled={loading.current}*/ value={input} type="text" placeholder='Type anything...' onChange={(e) => setInput(e.target.value)}/>
            <button>Ask</button>
        </form>
    </div>
  )
}

export default MessageTypingArea
