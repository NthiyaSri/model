import React, { useEffect, useState } from 'react'
import { api } from '../api'
import { Link } from 'react-router-dom'

export default function Cart(){
  const [items, setItems] = useState([])

  async function load(){
    const r = await api.getCart()
    if (r.ok) setItems(await r.json())
  }
  useEffect(()=>{ load() },[])

  const total = items.reduce((s,i)=> s + i.product.price * i.quantity, 0)
  return (
    <div className="container">
      <h1>Your Cart</h1>
      {items.map((i)=>(
        <div key={i.id} className="row" style={{justifyContent:'space-between', borderBottom:'1px solid #eee', padding:'8px 0'}}>
          <div className="flex"><img src={i.product.image_url || 'https://via.placeholder.com/64'} width="64"/><div>{i.product.title}</div></div>
          <div>x{i.quantity}</div>
          <div>${(i.product.price * i.quantity).toFixed(2)}</div>
        </div>
      ))}
      <div className="mt"><strong>Total: ${total.toFixed(2)}</strong></div>
      <div className="mt"><Link to="/checkout" className="btn">Checkout</Link></div>
    </div>
  )
}
