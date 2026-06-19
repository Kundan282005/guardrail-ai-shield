import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css' // YEH LINE ZAROORI HAI TAILWIND KE LIYE
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)