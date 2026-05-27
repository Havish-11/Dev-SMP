import { Routes, Route } from "react-router-dom";
import Headbar from "./components/Headbar";
import Home from "./pages/Home";
import ItemPage from "./pages/ItemPage";
import About from "./pages/About";
import Collections from "./pages/Collections";
import Contact from "./pages/Contact";
import { ThemeProvider } from "./context/ThemeContext";

function App() {
  return (
    <ThemeProvider>
    <div className="app">
      <Headbar />

      <main className="app-content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/collections" element={<Collections />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/item/:id" element={<ItemPage />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </main>
    </div>
    </ThemeProvider>
  );
}

export default App;
