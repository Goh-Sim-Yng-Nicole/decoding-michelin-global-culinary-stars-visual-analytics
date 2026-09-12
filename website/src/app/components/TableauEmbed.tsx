import React, { useState, useEffect, useRef } from 'react';

declare global {
  namespace JSX {
    interface IntrinsicElements {
      'tableau-viz': any;
    }
  }
}

interface TableauEmbedProps {
  src: string;
  height: string;
  title: string;
}

export const TableauEmbed: React.FC<TableauEmbedProps> = ({ src, height, title }) => {
  const [isVisible, setIsVisible] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          observer.disconnect();
        }
      },
      { rootMargin: '200px' } // Start loading 200px before scroll
    );

    if (containerRef.current) {
      observer.observe(containerRef.current);
    }

    return () => observer.disconnect();
  }, []);

  return (
    <div 
      ref={containerRef}
      className="w-full relative shadow-inner bg-gray-50 flex flex-col items-center justify-center overflow-hidden transition-all duration-500" 
      style={{ minHeight: height }}
    >
      {isVisible ? (
        <tableau-viz
          id={`tableauViz-${title.replace(/\s+/g, '-')}`}
          src={src}
          device="desktop"
          hide-tabs={true}
          toolbar="bottom"
          style={{ width: '100%', height: height }}
          className="w-full"
        />
      ) : (
        <div className="flex flex-col items-center gap-4 text-gray-400">
          <div className="w-12 h-12 border-4 border-gray-200 border-t-[#C8102E] rounded-full animate-spin"></div>
          <span className="text-sm font-medium tracking-wide uppercase">Preparing Visualization...</span>
        </div>
      )}
    </div>
  );
};
