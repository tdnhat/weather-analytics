'use client'

import React, { useState, useEffect } from 'react'
import DashboardNav from '@/components/DashboardNav'
import Sidebar from '@/components/Sidebar'

function DashboardLayoutComp({ children }: { children: React.ReactNode }) {
  const [isExpanded, setIsExpanded] = useState(true);

  // Create a debounced resize event when sidebar toggles
  useEffect(() => {
    // Dispatch a resize event after the transition completes
    const timeoutId = setTimeout(() => {
      window.dispatchEvent(new Event('resize'));
    }, 200); // Match the transition duration

    return () => clearTimeout(timeoutId);
  }, [isExpanded]);

  return (
    <div className="min-h-screen bg-gray-50 relative">
      <div 
        className="absolute inset-0 bg-cover bg-center bg-no-repeat opacity-100 pointer-events-none"
        // style={{ backgroundImage: 'url("/weather-background.jpg")' }}
        style={{ backgroundImage: 'url("/bg7.jpg")' }}

      />
      <div className="relative z-10">
        <DashboardNav onToggleSidebar={() => setIsExpanded(!isExpanded)} />
        <div className="flex h-[calc(100vh-var(--ds-header-height))] pt-[var(--ds-header-height)]">
          <Sidebar isExpanded={isExpanded} />
          <main className={`
            flex-1 overflow-auto
            transition-all duration-200 ease-in-out
          `}>
            {children}
          </main>
        </div>
      </div>
    </div>
  )
}

export default DashboardLayoutComp
