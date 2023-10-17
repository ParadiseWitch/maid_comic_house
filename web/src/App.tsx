import { Route, Routes } from 'react-router-dom'
import './App.css'
import Comic from './pages/comic'
import Subscribe from './pages/subscribe'
import Discover from './pages/discover'
import User from './pages/user'
import Login from './pages/login'
import Chapter from './pages/chapter'
import Regist from './pages/regist'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Subscribe />} />
      <Route path="/subscribe" element={<Subscribe />} />
      <Route path="/discover" element={<Discover />} />
      <Route path="/user" element={<User />} />
      <Route path="/login" element={<Login />} />
      <Route path="/regist" element={<Regist />} />
      <Route path="/comic" element={<Comic />} />
      <Route path="/chapter" element={<Chapter />} />
    </Routes>
  )
}

export default App
