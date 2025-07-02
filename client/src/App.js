import Home from './pages/Home'
import Chat from './pages/Chat'
import { createBrowserRouter,
  RouterProvider } from "react-router";

import "./style.scss"
import { Component } from 'react';

function App() {
  const router = createBrowserRouter([
    { 
      path: "/", 
      Component: Home, 
    },
    {
      path: "/chat",
      Component: Chat
    }
  ]);

  return (
    // Your App component MUST return JSX
    <RouterProvider router={router} />
  );
}

export default App;
