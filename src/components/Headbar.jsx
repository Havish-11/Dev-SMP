import { useTheme } from "../context/ThemeContext";

const NAV_ITEMS = [
  { label: "Shop" },
  { label: "Collections" },
  { label: "About" },
  { label: "Contact" },
];

function Headbar() {
  const { darkMode, toggleTheme } = useTheme();
  return (
    <header className="header">
      <div className="header-brand">
        <span className="brand-mark">MS</span>
        <div>
          <span className="brand-name">MiniShop</span>
          <span className="brand-tagline">
            Curated essentials, better shopping
          </span>
        </div>
      </div>


      <nav className="header-nav">
        {NAV_ITEMS.map((item) => (
          <span key={item.label} className="nav-link">
            {item.label}
          </span>
        ))}
      </nav>

  <nav className="header-actions">
   <button type="button" className="btn btn-ghost" onClick={toggleTheme}>
    {darkMode ? "Dark" : "Light"}
  </button>

  <button type="button" className="btn btn-sm btn-ghost">
    Sign In
  </button>
</nav>


    </header>
  );
}

export default Headbar;
