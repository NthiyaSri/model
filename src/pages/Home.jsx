import React, { useEffect, useState } from 'react'
import { api } from '../api'
import ProductCard from '../components/ProductCard'

export default function Home() {
  const [featured, setFeatured] = useState([])
  const [recs, setRecs] = useState([])

  useEffect(() => {
    api.products('?limit=8').then(async r => { if (r.ok) setFeatured(await r.json()) })
    api.aiRecommendations().then(async r => { if (r.ok) setRecs(await r.json()) })
  }, [])

  return (
    <div className="container">
      <section style={{padding:'2rem 0'}}>
        <h1>Discover your next favorite product</h1>
        <p>AI-enhanced descriptions and recommendations to help you decide.</p>
      </section>
      <section>
        <h2>Featured</h2>
        <div className="grid">{featured.map(p => <ProductCard key={p.id} p={p} />)}</div>
      </section>
      <section className="mt">
        <h2>Recommended for you</h2>
        <div className="grid">{recs.map(p => <ProductCard key={p.id} p={p} />)}</div>
      </section>
    </div>
  )
}
