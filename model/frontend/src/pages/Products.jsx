import React, { useEffect, useState } from 'react'
import { api } from '../api'
import ProductCard from '../components/ProductCard'

export default function Products(){
  const [items, setItems] = useState([])
  const [q, setQ] = useState('')
  const [min, setMin] = useState('')
  const [max, setMax] = useState('')

  async function load() {
    const params = new URLSearchParams()
    if (q) params.set('q', q)
    if (min) params.set('min_price', min)
    if (max) params.set('max_price', max)
    const r = await api.products(`?${params.toString()}`)
    if (r.ok) setItems(await r.json())
  }
  useEffect(()=>{ load() },[])

  return (
    <div className="container">
      <h1>Products</h1>
      <div className="row">
        <input className="input" placeholder="Search" value={q} onChange={e=>setQ(e.target.value)} />
        <input className="input" placeholder="Min" value={min} onChange={e=>setMin(e.target.value)} />
        <input className="input" placeholder="Max" value={max} onChange={e=>setMax(e.target.value)} />
        <button className="btn" onClick={load}>Filter</button>
      </div>
      <div className="grid mt">{items.map(p => <ProductCard key={p.id} p={p} />)}</div>
    </div>
  )
}
