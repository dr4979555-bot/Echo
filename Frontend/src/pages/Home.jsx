import Navbar from "../components/Navbar";
import Hero from "../components/Hero";

function Home() {
  return (
    <div className="min-h-screen bg-[#02030a] text-white overflow-hidden">
      <Navbar />
      <Hero />
    </div>
  );
}

export default Home;