import React from "react";
import { Link } from "react-router-dom";
import image from "../utils/image.png";

const Navbar = () => {
  return (
    <nav className="bg-blue-700 p-4 shadow-md">
      <div className="container mx-auto flex justify-between items-center">
        <div className="flex items-center text-2xl font-bold">
          <Link to="/" className="text-white flex items-center">
            <img src={image} alt="Logo" className="h-5 w-5 mr-2" />
            Grundfos
          </Link>
        </div>
        <ul className="flex space-x-6">
          <li>
            <Link to="/" className="hover:text-blue-300 font-semibold">Home</Link>
          </li>
          <li>
            <Link to="/predict" className="hover:text-blue-300 font-semibold">Predict</Link>
          </li>
          <li>
            <Link to="/upload" className="hover:text-blue-300 font-semibold">Efficiency</Link>
          </li>
          <li>
            <Link to="/assistant" className="hover:text-blue-300 font-semibold">Assistant</Link>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
