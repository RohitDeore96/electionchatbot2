import React, { useState } from 'react';
import { Search, MapPin } from 'lucide-react';
import { fetchVoterInfo } from '../services/apiClient';

export default function MapLocator() {
  const [address, setAddress] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    if(address.trim()) {
      setLoading(true);
      try {
        const data = await fetchVoterInfo(address);
        setResult(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
  };

  return (
    <section aria-labelledby="map-locator-heading" className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <h2 id="map-locator-heading" className="text-2xl font-bold text-gray-900 mb-6">Polling Place Locator</h2>
      
      <form onSubmit={handleSearch} aria-label="Polling location search" className="mb-6">
        <label htmlFor="address-input" className="sr-only">Enter your home address</label>
        <div className="relative flex items-center">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search className="h-5 w-5 text-gray-400" aria-hidden="true" />
          </div>
          <input 
            id="address-input" 
            type="text"
            value={address} 
            onChange={(e) => setAddress(e.target.value)} 
            placeholder="e.g. 123 Main St, Anytown" 
            required 
            className="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg leading-5 bg-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary sm:text-sm transition-colors"
          />
          <button 
            type="submit" 
            disabled={loading}
            className="ml-3 inline-flex items-center px-4 py-3 border border-transparent text-sm font-medium rounded-lg shadow-sm text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-colors disabled:opacity-50"
          >
            {loading ? 'Searching...' : 'Search'}
          </button>
        </div>
      </form>

      <div aria-live="polite" className="space-y-4">
        {result && (
          <div className="bg-neutral-light p-4 rounded-lg border border-gray-200">
            <div className="flex items-start justify-between">
              <div className="flex items-start">
                <MapPin className="w-5 h-5 text-primary mt-0.5 mr-2" aria-hidden="true" />
                <div>
                  <h3 className="text-md font-semibold text-gray-900">Assigned Polling Location</h3>
                  <p className="text-gray-700 mt-1">{result.address || "123 Civic Center Dr."}</p>
                </div>
              </div>
              <button 
                className="text-sm font-semibold text-primary hover:text-primary-dark focus:outline-none focus:underline px-3 py-1.5 border border-primary rounded-md hover:bg-blue-50 transition-colors"
                aria-label={`Get directions to ${result.address}`}
              >
                Get Directions
              </button>
            </div>
          </div>
        )}

        {/* Google Maps Placeholder */}
        <div 
          className="w-full h-64 bg-gray-100 rounded-lg border-2 border-dashed border-gray-300 flex items-center justify-center relative overflow-hidden"
          aria-label="Interactive map placeholder"
        >
          <div className="text-center p-4">
            <MapPin className="mx-auto h-8 w-8 text-gray-400 mb-2" />
            <p className="text-sm text-gray-500">Google Maps Canvas will render here</p>
          </div>
        </div>
      </div>
    </section>
  );
}
