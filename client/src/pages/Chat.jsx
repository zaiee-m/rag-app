import React, { useEffect, useState, useRef} from 'react'
import MessageArea from '../components/MessageArea'
import MessageTypingArea from '../components/MessageTypingArea'
import { GoogleGenAI,
        createUserContent,
        createPartFromUri,
 } from "@google/genai";
 import {useLocation, useNavigate} from 'react-router'


function Chat() {
    const [currPrompt, setCurrPrompt] = useState(null);
    const [aiResponse, setAiResponse] = useState(null);
    const chatRef = useRef(null);
    const loadingRef = useRef(true)
    const hasInitialized = useRef(false);
    const location = useLocation()
    const navigate = useNavigate()
    const [library, setLibrary] = useState(null)

  useEffect(() => {
    if (hasInitialized.current) return;
    hasInitialized.current = true;

    /*
      chat page is only acessible through the options component.
      fromHome and contents objects are passed through navigate's state parameter

        fromHome signifies wether user was redirected from home or they tried to direly access
        the page through /chat url which should be blocked as in such cases we do not know what library docs to
        use for rag

        contentes:{
          library: text
        }
    */ 

    let state = location.state;
    if(!state?.fromHome){
      navigate("/")
      return
    }

    setLibrary(state?.content.library)

    const ai = new GoogleGenAI({
        apiKey: "AIzaSyASrRbXgfB83hypSjL38ciJPzMrN7SzOUw",
    });
    
    async function initializeChat() {
      try {

       

       chatRef.current = await ai.chats.create({
            model: "gemini-2.0-flash",
            config:{
              systemInstruction: ""
            }
        });

        console.log("Chat initialized sucessfully")

      } catch (error) {
        console.error("Failed to initialize chat:", error);
      }
      setTimeout(() => {
        loadingRef.current = false;
      }, 2000);
      
    }

    initializeChat()

  }, []);


  useEffect(() => {
    if (!currPrompt?.text || !chatRef.current) return;
    
    async function sendMessage() {
      let response = null;
      try{
        response = await fetch("/chat" , {
          method: "POST",

          body: JSON.stringify({
            "library": library,
            "query": currPrompt.text
          }),

          headers: {
            "Content-type": "application/json; charset=UTF-8"
          }
        })

        if(!response.ok){
          const content = await response.json()
          console.log("Response was not OK: "+ content)
          return 
        }
      }
      catch(error){
        console.log("Something went wrong in the fetch request: " + error)
      }

      try{
        let extraInformation = await response.json()
        console.log(extraInformation)

        let Parts = [];

        for(const txt of extraInformation['text']){
          Parts.push({text: txt})
        }
        Parts.push({text:`Question: ${currPrompt.text}`})

        console.log(Parts)

        response = await chatRef.current.sendMessage({
            message: {
                parts:Parts
              }
            
        });
        const text = response.text;

        setAiResponse({
          text: text,
          type: "ai",
        }); 

      } catch (error) {
        console.error("Error sending message:", error);

        setAiResponse({
          text: "**Sorry, I encountered an error. Please try again.**",
          type: "ai",
        });

      }
    }

    sendMessage();
  }, [currPrompt]);


  return (
    <div className='chat'>
        <div className="chat-container">
            <MessageArea prompt={currPrompt} response={aiResponse} />
            <MessageTypingArea setPrompt={setCurrPrompt} loading={loadingRef}/>
        </div>
    </div>
  )
}

export default Chat
