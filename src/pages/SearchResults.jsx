import React, { useEffect, useState } from 'react'
import { useLocation } from 'react-router-dom'
import { api } from '../api'
import ProductCard from '../components/ProductCard'

export default function SearchResults(){
  const { search } = useLocation()
  const params = new URLSearchParams(search)
  const q = params.get('q') || ''
  const [items, setItems] = useState([])

  useEffect(()=>{
    api.products(`?q=${encodeURIComponent(q)}`).then(async r => { if (r.ok) setItems(await r.json()) })
  }, [q])

  return (
    <div className="container">
      <h1>Search: {q}</h1>
      <div className="grid mt">{items.map(p => <ProductCard key={p.id} p={p} />)}</div>
    </div>
  )
}
