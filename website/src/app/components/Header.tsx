import { useState } from 'react';
import { Link, useLocation } from 'react-router';
import { Menu, X } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';

export function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;
  const toggleMenu = () => setIsMenuOpen(!isMenuOpen);
  const closeMenu = () => setIsMenuOpen(false);

  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-8 py-4 sm:py-5">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link
            to="/"
            onClick={closeMenu}
            className="flex items-center gap-2 sm:gap-3 hover:opacity-80 transition-opacity"
          >
            <ImageWithFallback
              src="https://upload.wikimedia.org/wikipedia/commons/9/9f/Michelin_guide_logo.png"
              alt="Michelin Guide Logo"
              className="h-8 sm:h-10 md:h-12 w-auto object-contain"
            />
            <div className="border-l border-gray-300 pl-3 sm:pl-4">
              <div className="text-[10px] sm:text-xs md:text-sm font-light text-gray-500 tracking-wide">
                Singapore Analysis
              </div>
              <div className="text-sm sm:text-base md:text-lg font-semibold text-[#2B2B2B] -mt-0.5">
                En-tire-ly Overrated?
              </div>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex gap-1">
            <Link
              to="/"
              className={`px-4 lg:px-6 py-2 text-sm font-medium transition-all ${isActive('/')
                  ? 'text-[#C8102E]'
                  : 'text-gray-700 hover:text-[#C8102E]'
                }`}
            >
              Introduction
            </Link>
            <Link
              to="/dashboards"
              className={`px-4 lg:px-6 py-2 text-sm font-medium transition-all ${isActive('/dashboards')
                  ? 'text-[#C8102E]'
                  : 'text-gray-700 hover:text-[#C8102E]'
                }`}
            >
              Dashboards
            </Link>
            <Link
              to="/insights"
              className={`px-4 lg:px-6 py-2 text-sm font-medium transition-all ${isActive('/insights')
                  ? 'text-[#C8102E]'
                  : 'text-gray-700 hover:text-[#C8102E]'
                }`}
            >
              Insights
            </Link>
          </nav>

          {/* Mobile Menu Button */}
          <button
            onClick={toggleMenu}
            className="md:hidden p-2 text-gray-600 hover:text-[#C8102E] transition-colors"
            aria-label="Toggle menu"
          >
            {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </div>

      {/* Mobile Navigation Dropdown */}
      {isMenuOpen && (
        <div className="md:hidden bg-white border-b border-gray-200 animate-in slide-in-from-top duration-200">
          <nav className="flex flex-col p-4">
            <Link
              to="/"
              onClick={closeMenu}
              className={`px-4 py-3 text-base font-medium border-l-2 transition-all ${isActive('/')
                  ? 'text-[#C8102E] border-[#C8102E] bg-red-50'
                  : 'text-gray-700 border-transparent hover:bg-gray-50'
                }`}
            >
              Introduction
            </Link>
            <Link
              to="/dashboards"
              onClick={closeMenu}
              className={`px-4 py-3 text-base font-medium border-l-2 transition-all ${isActive('/dashboards')
                  ? 'text-[#C8102E] border-[#C8102E] bg-red-50'
                  : 'text-gray-700 border-transparent hover:bg-gray-50'
                }`}
            >
              Dashboards
            </Link>
            <Link
              to="/insights"
              onClick={closeMenu}
              className={`px-4 py-3 text-base font-medium border-l-2 transition-all ${isActive('/insights')
                  ? 'text-[#C8102E] border-[#C8102E] bg-red-50'
                  : 'text-gray-700 border-transparent hover:bg-gray-50'
                }`}
            >
              Insights
            </Link>
          </nav>
        </div>
      )}
    </header>
  );
}