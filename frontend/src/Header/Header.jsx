import React from "react";
import { FaBitcoin, FaSignInAlt, FaUserCircle } from "react-icons/fa";

export default function Header() {
  return (
    <header className="fixed top-2 left-0 right-0 flex justify-center items-center h-24 z-50">
      <nav className="w-10/12 bg-[#141c29d9] rounded-3xl h-full my-3 flex items-center">
        <div className="grid grid-cols-12 items-center w-full px-6">
          <FaBitcoin className="w-12 h-12 justify-self-start col-span-2 text-yellow-500" />
          <div className="col-span-8 flex gap-40 justify-center items-center space-x-8 font-extrabold text-xl">
            <span className="text-white hover:text-yellow-500 hover:scale-110 focus:text-yellow transition-all duration-400 cursor-pointer">
              Analyze
            </span>
            <span className="text-white hover:text-yellow-500 hover:scale-110 focus:text-yellow transition-all duration-400 cursor-pointer">
              Trade
            </span>
            <span className="text-white hover:text-yellow-500 hover:scale-110 focus:text-yellow transition-all duration-400 cursor-pointer">
              Learn
            </span>
          </div>
          <FaUserCircle className="w-12 h-12 col-span-2 text-white text-2xl font-bold justify-self-end" />
        </div>
      </nav>
    </header>
  );
}
