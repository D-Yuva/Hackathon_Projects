import React from "react";

const Home = () => {
  return (
    <div className="text-center">

      <section className="bg-blue-400 text-white py-20">
        <h1 className="text-5xl font-extrabold mb-4">Welcome to Chiller Evolution</h1>
        <p className="text-lg text-gray-200 mb-8">
          Global leader in advanced pump solutions and water technology.
        </p>
        <a
          href="#services"
          className="bg-white text-blue-600 py-3 px-8 rounded-lg font-bold hover:bg-gray-200 transition duration-300"
        >
          Explore Our Services
        </a>
      </section>

      <section className="py-16 px-6 relative">
        <h2 className="text-4xl font-bold text-blue-600 mb-6">About Grundfos</h2>
        <p className="text-lg text-gray-500 max-w-3xl mx-auto mb-8">
          Grundfos is a global leader in water technology, offering innovative
          and sustainable pump solutions for various industries. Our mission is
          to create a better world by providing efficient solutions that reduce
          energy and water consumption, helping to address the most critical
          water and energy challenges globally.
        </p>
        
        <div className="relative">
          <video
            className="w-full h-auto rounded-lg shadow-lg"
            autoPlay
            loop
            muted
            playsInline
          >
            <source src="https://grundfos.scene7.com/is/content/grundfos/grundfos-homepage-local-10mb-0x720-3000k" type="video/mp4" />
            Your browser does not support the video tag.
          </video>

          <div className="absolute inset-0 bg-black opacity-30 rounded-lg"></div>
          
          <div className="absolute inset-0 flex items-center justify-center">
            <h3 className="text-2xl font-bold text-white">Innovating Water Solutions</h3>
          </div>
        </div>
      </section>


      <section id="services" className="bg-gray-100 py-16 px-6">
        <h2 className="text-4xl font-bold text-blue-600 mb-10">Our Services</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white p-6 rounded-lg shadow-lg">
            <h3 className="text-2xl font-bold text-blue-600 mb-4">Water Pump Solutions</h3>
            <p className="text-gray-700">
              We provide high-efficiency water pump solutions tailored to your
              industrial, municipal, and residential needs.
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-lg">
            <h3 className="text-2xl font-bold text-blue-600 mb-4">Sustainable Energy</h3>
            <p className="text-gray-700">
              Our advanced energy-saving technologies reduce your carbon
              footprint and help conserve energy in all water-related
              operations.
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-lg">
            <h3 className="text-2xl font-bold text-blue-600 mb-4">Smart Pump Systems</h3>
            <p className="text-gray-700">
              With IoT-enabled smart pump systems, you can monitor and control
              your water usage more efficiently and securely.
            </p>
          </div>
        </div>
      </section>

      <section className="py-16 bg-blue-400 text-white">
        <h2 className="text-4xl font-bold mb-6">Ready to Experience Innovation?</h2>
        <p className="text-lg text-gray-200 mb-8">
          Join thousands of customers worldwide who trust Grundfos for reliable
          and sustainable water solutions.
        </p>
        <a
          href="#"
          className="bg-white text-blue-600 py-3 px-8 rounded-lg font-bold hover:bg-gray-200 transition duration-300"
        >
          Contact Us
        </a>
      </section>
    </div>
  );
};

export default Home;
