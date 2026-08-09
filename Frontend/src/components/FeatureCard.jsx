import { motion } from "framer-motion";

function FeatureCard({
  icon,
  title,
  description,
  color,
  delay
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 40 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.6, delay }}
      whileHover={{
        y: -8,
        scale: 1.02
      }}
      className={`feature-card ${color}`}
    >
      <div className="feature-icon">
        {icon}
      </div>

      <div>
        <h3>{title}</h3>

        <p>{description}</p>

        <button className="learn-more">
          Learn more →
        </button>
      </div>
    </motion.div>
  );
}

export default FeatureCard;