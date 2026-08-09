import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import FeatureCard from "./FeatureCard";  

function Hero() {
 const navigate = useNavigate();
  return (
    <main>

      {/* =========================
          HERO SECTION
          ========================= */}
      <section className="hero-section">

        {/* Background glow */}
        <div className="glow glow-blue"></div>
        <div className="glow glow-purple"></div>

        <div className="hero-content">

          {/* =========================
              LEFT SIDE
              ========================= */}
          <div className="hero-left">

            {/* Badge */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="hero-badge"
            >
              ✨ AI That Creates. So You Can Innovate.
            </motion.div>

            {/* Heading */}
            <motion.h1
              initial={{ opacity: 0, y: 40 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
            >
              <span className="gradient-text">
                Echo
              </span>

              <br />

              <span className="gradient-text">
                AI Creator
              </span>
            </motion.h1>

            {/* Description */}
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.8, delay: 0.3 }}
              className="hero-description"
            >
              AI creates, remembers, and publishes content
              automatically so you can focus on what truly
              matters.
            </motion.p>

            {/* =========================
                BUTTONS
                ========================= */}
            <div className="hero-buttons">

              <motion.button
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
  className="hero-btn"
  onClick={() => navigate("/dashboard")}
>
  Launch Dashboard
</motion.button>

              <motion.button
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
  className="hero-btn"
>
  <span className="play-icon">▶</span>
  Watch Demo
</motion.button>

            </div>

            {/* =========================
                STATS
                ========================= */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.5 }}
              className="stats-container"
            >

              <div className="stat">
                <strong>10K+</strong>
                <span>Creators Trust Us</span>
              </div>

              <div className="stat-divider"></div>

              <div className="stat">
                <strong>1M+</strong>
                <span>Content Generated</span>
              </div>

              <div className="stat-divider"></div>

              <div className="stat">
                <strong>99.9%</strong>
                <span>Automation Rate</span>
              </div>

            </motion.div>

          </div>


          {/* =========================
              RIGHT SIDE — AI VISUAL
              ========================= */}
          <div className="hero-visual">

            {/* Orbit rings */}
            <div className="orbit orbit-one"></div>
            <div className="orbit orbit-two"></div>
            <div className="orbit orbit-three"></div>


            {/* =========================
                AI BRAIN — CENTER
                ========================= */}
            <motion.div
              animate={{
                y: [0, -15, 0],
                rotate: [0, 2, 0, -2, 0]
              }}
              transition={{
                duration: 5,
                repeat: Infinity,
                ease: "easeInOut"
              }}
              className="ai-core"
            >
              <div className="ai-core-inner">
                🧠
              </div>
            </motion.div>


            {/* =================================================
                FLOATING CARD 1 — TOP LEFT
                ================================================= */}
            <motion.div
              className="floating-card card-one"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.7, delay: 0.3 }}
            >

              <span>✦</span>

              <div>
                <strong>AI Generates</strong>
                <small>Smart Content</small>
              </div>

            </motion.div>


            {/* =================================================
                FLOATING CARD 2 — TOP RIGHT
                ================================================= */}
            <motion.div
              className="floating-card card-two"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.7, delay: 0.5 }}
            >

              <span>🧠</span>

              <div>
                <strong>AI Remembers</strong>
                <small>Every Detail</small>
              </div>

            </motion.div>


            {/* =================================================
                FLOATING CARD 3 — BOTTOM LEFT
                ================================================= */}
            <motion.div
              className="floating-card card-three"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.7, delay: 0.7 }}
            >

              <span>⚡</span>

              <div>
                <strong>AI Publishes</strong>
                <small>Automatically</small>
              </div>

            </motion.div>


            {/* =================================================
                FLOATING CARD 4 — BOTTOM RIGHT
                ================================================= */}
            <motion.div
              className="floating-card card-four"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.7, delay: 0.9 }}
            >

              <span>📈</span>

              <div>
                <strong>AI Improves</strong>
                <small>Every Time</small>
              </div>

            </motion.div>

          </div>

        </div>

      </section>


      {/* =========================
          FEATURES SECTION
          ========================= */}
      <section
        id="features"
        className="features-section"
      >

        <div className="section-heading">

          <span>POWERED BY AUTONOMY</span>

          <h2>
            Your AI.
            <span> Your Creator.</span>
          </h2>

          <p>
            One intelligent system that creates, learns,
            publishes and continuously improves.
          </p>

        </div>


        {/* Feature cards */}
        <div className="features-grid">

          <FeatureCard
            icon="✦"
            title="AI Generates"
            description="Smart content crafted automatically."
            color="blue-card"
            delay={0}
          />

          <FeatureCard
            icon="🧠"
            title="AI Remembers"
            description="Learns your style and remembers everything."
            color="purple-card"
            delay={0.1}
          />

          <FeatureCard
            icon="📅"
            title="AI Publishes"
            description="Publishes at the perfect time, every time."
            color="blue-card"
            delay={0.2}
          />

          <FeatureCard
            icon="📊"
            title="AI Improves"
            description="Continuously improves with every action."
            color="purple-card"
            delay={0.3}
          />

        </div>

      </section>

    </main>
  );
}

export default Hero;