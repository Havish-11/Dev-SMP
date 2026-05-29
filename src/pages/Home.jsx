import { Link } from "react-router-dom";
import items from "../data/items";
import CartSidebar from "../components/CartSidebar";
import { CartProvider } from "../context/CartContext";

function Home() {
  return (
  <CartProvider>
   <main className="page home-page">
    <CartSidebar />
      <section className="home-hero">
        <div>
          <p className="hero-eyebrow">Curated marketplace</p>
          <h1 className="hero-title">
            Discover premium products that feel made for you.
          </h1>
          <p className="hero-copy">
            Shop everyday favorites across home, tech, fitness, and lifestyle.
            Every item is selected for quality, value, and real usefulness.
          </p>
          <div className="hero-actions">
            <Link to="/contact" className="btn btn-ghost">
              Contact Us
            </Link>
          </div>
        </div>
      </section>

      <section>
        <input type ="text" className="search-bar" placeholder="Search products by name or category...">
        </input>
        </section>      

      <nav>
        <section className="filter-section">
          <div className="filter-container">
          <h2 className = "filter-header">CATEGORY</h2>  
          <select className ="filter-category" name="categories">
            <option value="all">All categories </option>
            <option value="furniture">Furniture</option>
            <option value="apparel">Apparel</option>
            <option value="kitchen">Kitchen</option>
            <option value="electronics">Electronics</option>
            <option value="outdoors">Outdoors</option>
            </select> 
            </div>   

            <div>
            <h2 className = "filter-header">PRICE</h2>  
                <select className="filter-category" name="prices">
                  <option value="all prices">All prices</option>
                  <option value="under 20">Under ₹20</option>
                  <option value="20-40"> ₹20 - ₹40</option>
                  <option value="Over 40">Over ₹40</option>
                </select>
             </div>
        </section>
      </nav>


      <section className="item-grid">
        {items.map((item) => (
          <div key={item.id} className="item-card">
            <a href="#" className="item-card-image-link">
              <div className="item-card-image">
                <img src={item.image}/>
                <div className="item-card-label">{item.category}</div>
              </div>
            </a>

            <div style={{ padding: "1rem" }}>
              <a href="#" className="item-card-image-link">
              <h3 style={{ margin: "0 0 0.5rem 0" }}>{item.name}</h3>
              </a>
              <p style={{ margin: 0, fontSize: "0.9rem" }}>{item.description}</p>
            </div>

            <div style={{ padding: "1rem", borderTop: "1px solid var(--border)" }}>
              <b>₹{item.price}</b>
            </div>
          </div>
        ))}
      </section>


    </main>
    </CartProvider>
  );
}

export default Home;
