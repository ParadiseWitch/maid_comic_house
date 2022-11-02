import { Route, Routes } from 'react-router-dom'
import './App.css'
import Comic from './pages/comic'
import Home from './pages/home'
import Login from './pages/login'
import Chapter from './pages/chapter'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/comic" element={<Comic />} />
      <Route path="/chapter" element={<Chapter />} />
    </Routes>
  )
}

export default App
