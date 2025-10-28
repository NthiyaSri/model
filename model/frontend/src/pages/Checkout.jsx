import React, { useState } from 'react'
import { api } from '../api'

export default function Checkout(){
  const [shipping_address, setAddr] = useState('')
  const [message, setMessage] = useState('')

  async function submit(e){
    e.preventDefault()
    const r = await api.checkout({ shipping_address, payment_token: 'demo' })
    const j = await r.json()
    if (r.ok) setMessage('Order placed! #' + j.order_id)
    else setMessage(j.error || 'Failed')
  }

  return (
    <div className="container">
      <h1>Checkout</h1>
      <form className="form" onSubmit={submit}>
        <label>Shipping Address</label>
        <textarea value={shipping_address} onChange={e=>setAddr(e.target.value)} required />
        <button className="btn" type="submit">Place Order</button>
      </form>
      {message && <div className="mt">{message}</div>}
    </div>
  )
}
