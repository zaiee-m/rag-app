import React, {useState, useEffect, useRef} from 'react'
import Message from './Message'

function MessageArea({prompt, response}) {
  const messagesEndRef = useRef(null)
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    if (prompt?.text) {
      setMessages(prev => [...prev, prompt]); // add new message to array
    }
  }, [prompt]);

  useEffect(() => {
    if (response?.text) {
      setMessages(prev => [...prev, response]); // add new message to array
    }
  }, [response]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className='message-area'>
    {messages.map((msg, index) => (
        <Message key={index} prompt={msg} /> 
    ))}
        <div ref={messagesEndRef}></div>
    </div>
  )
}

export default MessageArea
