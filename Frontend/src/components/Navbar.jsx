import { motion } from "framer-motion";

function Navbar() {
  return (
    <nav className="fixed top-0 left-0 w-full z-50 px-6 py-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between">

        {/* Logo */}
        <motion.div
          whileHover={{ scale: 1.05 }}
          className="text-xl font-bold text-cyan-400"
        >
          Autonomous AI
        </motion.div>

        {/* Navigation */}
        <div className="nav-links">

  <a href="#home">Home</a>

  <a href="#features">Features</a>

  <a href="#how-it-works">How It Works</a>

  <a href="#use-cases">Use Cases</a>

  <a href="#pricing">Pricing</a>

  <a href="#about">About</a>

</div>

        {/* Login Button */}
        <motion.button
  whileHover={{
    scale: 1.05,
    boxShadow: "0 0 25px rgba(168, 85, 247, 0.45)",
  }}
  whileTap={{ scale: 0.95 }}
  className="login-btn"
>
  Login
</motion.button>

      </div>
    </nav>
  );
}

export default Navbar;