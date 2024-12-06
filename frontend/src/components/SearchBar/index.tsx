import React from 'react';

function SearchBar() {
    return (
        <div className="flex items-center w-full p-4">
            <div className="relative w-full">
                <span className="absolute inset-y-0 left-0 pl-3 flex items-center">
                    <i className="fas fa-search text-gray-400"></i>
                </span>
                <input 
                    type="text" 
                    className="pl-10 pr-4 py-2 rounded-full border border-gray-300 w-full text-sm placeholder-gray-400" 
                    placeholder="Search..." 
                />
            </div>
        </div>
    );
}

export default SearchBar; 