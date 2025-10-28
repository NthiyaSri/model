import React, { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { api } from '../api'

export default function Header() {
  const [q, setQ] = useState('')
  const [suggest, setSuggest] = useState([])
  const navigate = useNavigate()

  useEffect(() => {
    const t = setTimeout(async () => {
      if (!q) { setSuggest([]); return }
      const res = await api.products(`?q=${encodeURIComponent(q)}&limit=5`)
      if (res.ok) setSuggest(await res.json())
    }, 200)
    return () => clearTimeout(t)
  }, [q])

  function onSubmit(e) {
    e.preventDefault()
    navigate(`/search?q=${encodeURIComponent(q)}`)
  }

  return (
    <header className="header">
      <div className="container nav">
        <Link to="/" className="brand">AI Shop</Link>
        <form className="search" onSubmit={onSubmit}>
          <input className="input" placeholder="Search products..." value={q} onChange={e=>setQ(e.target.value)} />
          <button className="btn" type="submit">Search</button>
        </form>
        <div className="flex">
          <Link to="/products">Products</Link>
          <Link to="/cart">Cart</Link>
          <Link to="/login">Login</Link>
          <Link to="/admin">Admin</Link>
        </div>
      </div>
      {suggest.length>0 && (
        <div className="container" style={{position:'relative'}}>
          <div style={{position:'absolute', background:'#fff', border:'1px solid #e5e7eb', borderRadius:6, width:320, padding:8}}>
            {suggest.map(s => <div key={s.id} onClick={()=>navigate(`/products/${s.id}`)} style={{padding:6, cursor:'pointer'}}>{s.title}</div>)}
          </div>
        </div>
      )}
    </header>
  )
}
