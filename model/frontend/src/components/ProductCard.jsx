import React from 'react'
import { Link } from 'react-router-dom'

export default function ProductCard({ p }) {
  return (
    <div className="card">
      <img src={p.image_url || 'https://via.placeholder.com/400x300?text=Product'} alt={p.title} />
      <div className="p">
        <div style={{fontWeight:600}}>{p.title}</div>
        <div>${p.price?.toFixed(2)}</div>
        <div className="mt"><Link className="btn" to={`/products/${p.id}`}>View</Link></div>
      </div>
    </div>
  )
}
