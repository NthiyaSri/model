import React, { useEffect, useState } from 'react'
import { api } from '../api'

export default function AdminDashboard(){
  const [items, setItems] = useState([])
  const [form, setForm] = useState({ title:'', short_desc:'', price:'', image_url:'' })

  async function load(){ const r = await api.products(''); if (r.ok) setItems(await r.json()) }
  useEffect(()=>{ load() },[])

  async function create(e){
    e.preventDefault()
    const r = await api.createProduct({ ...form, price: Number(form.price)||0 })
    if (r.ok) { setForm({ title:'', short_desc:'', price:'', image_url:'' }); load() }
    else alert('Admin login required')
  }
  async function del(id){ const r = await api.deleteProduct(id); if (r.ok) load(); else alert('Admin login required') }

  return (
    <div className="container">
      <h1>Admin</h1>
      <form className="form" onSubmit={create}>
        <input className="input" placeholder="Title" value={form.title} onChange={e=>setForm(f=>({...f,title:e.target.value}))}/>
        <input className="input" placeholder="Short Desc" value={form.short_desc} onChange={e=>setForm(f=>({...f,short_desc:e.target.value}))}/>
        <input className="input" placeholder="Price" value={form.price} onChange={e=>setForm(f=>({...f,price:e.target.value}))}/>
        <input className="input" placeholder="Image URL" value={form.image_url} onChange={e=>setForm(f=>({...f,image_url:e.target.value}))}/>
        <button className="btn">Create</button>
      </form>
      <div className="grid mt">
        {items.map(p => (
          <div key={p.id} className="card">
            <img src={p.image_url || 'https://via.placeholder.com/400x300'} />
            <div className="p">
              <div>{p.title}</div>
              <div className="row"><button className="btn" onClick={()=>del(p.id)}>Delete</button></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
