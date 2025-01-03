'use client'

import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBars } from '@fortawesome/free-solid-svg-icons';

function DashboardNav() {
    // Add state management for sidebar
    const [isSidebarOpen, setIsSidebarOpen] = React.useState(false);

    const toggleSidebar = () => {
        setIsSidebarOpen(!isSidebarOpen);
        // Dispatch a custom event with data
        window.dispatchEvent(new CustomEvent('toggle-sidebar', {
            detail: { isOpen: !isSidebarOpen }
        }));
    };

    return (
        <nav className="fixed w-full z-10">
            <div className={`
                flex justify-between items-center px-6 h-[var(--ds-header-height)]
                bg-clip-padding backdrop-filter backdrop-blur-md bg-opacity-30 border-b border-white/30
            `}>
                {/* Menu Button */}
                <button 
                    id="menu-button" 
                    onClick={toggleSidebar}
                    aria-label="Toggle sidebar"
                >
                    <FontAwesomeIcon icon={faBars} className="text-white text-lg" />
                </button>
                
                {/* Logo */}
                <div className="mx-auto text-xl font-bold text-white">
                    Phân tích dữ liệu thời tiết - Thừa Thiên Huế
                </div>
            </div>
        </nav>
    );
}

export default DashboardNav; 