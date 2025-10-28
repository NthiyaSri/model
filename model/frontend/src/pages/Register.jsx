import React, { useState } from 'react'
import { api } from '../api'
import { useNavigate } from 'react-router-dom'

export default function Register(){
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [name, setName] = useState('')
  const [error, setError] = useState('')
  const navigate = useNavigate()

  async function submit(e){
    e.preventDefault()
    const r = await api.register({ email, password, name })
    if (r.ok) navigate('/login')
    else setError((await r.json()).error || 'Registration failed')
  }

  return (
    <div className="container">
      <h1>Register</h1>
      <form className="form" onSubmit={submit}>
        <input className="input" placeholder="Name" value={name} onChange={e=>setName(e.target.value)} />
        <input className="input" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
        <input className="input" placeholder="Password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
        <button className="btn">Register</button>
      </form>
      {error && <div className="mt" style={{color:'crimson'}}>{error}</div>}
    </div>
  )
}
