import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { api } from '../api'

export default function ProductDetails(){
  const { id } = useParams()
  const [p, setP] = useState(null)
  const [desc, setDesc] = useState('')

  useEffect(() => {
    api.product(id).then(async r => {
      if (r.ok) {
        const j = await r.json()
        setP(j)
        if (!j.description) {
          const ai = await api.aiDescription({ title: j.title, short_desc: j.short_desc, features: ['durable', 'popular'] })
          if (ai.ok) setDesc((await ai.json()).description)
        }
      }
    })
  }, [id])

  async function addToCart() {
    const r = await api.addToCart({ product_id: Number(id), quantity: 1 })
    if (r.ok) alert('Added to cart')
    else alert('Login required')
  }

  if (!p) return <div className="container">Loading...</div>
  return (
    <div className="container">
      <div className="row">
        <img src={p.image_url || 'https://via.placeholder.com/500x380'} alt={p.title} style={{maxWidth:480, width:'100%'}}/>
        <div>
          <h1>{p.title}</h1>
          <h3>${p.price?.toFixed(2)}</h3>
          <p>{p.description || desc}</p>
          <button className="btn" onClick={addToCart}>Add to Cart</button>
        </div>
      </div>
    </div>
  )
}
