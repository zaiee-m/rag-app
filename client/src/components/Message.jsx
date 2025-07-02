import React from 'react'
import ReactMarkdown from 'react-markdown';

function Message({prompt}) {
  return (
    <div className={`message ${prompt?.type}`}>
       <div className="content">
        <ReactMarkdown>  
        {prompt?.text}
      </ReactMarkdown>
    </div> 
    </div>
  )
}

export default Message
