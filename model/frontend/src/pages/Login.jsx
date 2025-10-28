import React, { useState } from 'react'
import { api } from '../api'
import { useNavigate } from 'react-router-dom'

export default function Login(){
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const navigate = useNavigate()

  async function submit(e){
    e.preventDefault()
    const { res, json } = await api.login({ email, password })
    if (res.ok) navigate('/')
    else setError(json.error || 'Login failed')
  }

  return (
    <div className="container">
      <h1>Login</h1>
      <form className="form" onSubmit={submit}>
        <input className="input" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
        <input className="input" placeholder="Password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
        <button className="btn">Login</button>
      </form>
      {error && <div className="mt" style={{color:'crimson'}}>{error}</div>}
    </div>
  )
}
