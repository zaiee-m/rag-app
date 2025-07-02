import React, { useEffect, useState, Form } from 'react'
import linkIcon from '../img/link.svg'
import aiIcon from '../img/chatbot.svg'
import clipboardIcon from '../img/clipboard.svg'
import {useNavigate} from 'react-router'

function Options({choice}) {

  /*
    choice object is the option chosen out of the displayed results on searching database.
    choice has attributes, .library_name, .official_docs_URL, and .docs_file_URL
  */

  const [doc, setDoc] = useState()
  const [copied, setCopied] = useState(false);

  const navigate = useNavigate();

useEffect(() => {
  const fetchDoc = async () => {
    if (!choice?.library_name) return; // Don't fetch if no choice selected
    
    try {
      const response = await fetch(`/docs?filename=${choice.library_name}`);
      if (!response.ok) throw new Error('Network response was not ok');
      const text = await response.text();
      setDoc(text);
    } catch (error) {
      console.error('Error fetching document:', error);
      setDoc(''); // Clear doc on error
    }
  };

  fetchDoc();
}, [choice]);

  const handleClick = async (event) => {
    try{
      await navigator.clipboard.writeText(doc);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000); 
    }catch(err){
      console.log(err)
    }
  }

  const handleNavigate = () => {
      navigate("/chat", {
        state: {
          fromHome: true,
          content: {
            library: choice.library_name,
          }
        },
      });
  }

  return (
    <>
    {choice && <div className='options'>
      <div className='item'>
        <a href={choice?.official_docs_URL}>Official Docs</a>
        <img src={linkIcon} alt="" />
      </div>
      <div className='item'>
        <span onClick={handleNavigate}>
          Chat with AI
        </span>
        <img src={aiIcon} alt="" />
      </div>
      <div className='item'>
        <span onClick={handleClick}>
          {copied ? '✓ Copied!' : 'Copy Docs to Clipboard'}
        </span>
        <img src={clipboardIcon} alt="" />
      </div>
    </div>}
    </>
  )
}

export default Options
