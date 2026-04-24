import React, { useState, useEffect } from 'react';
import { Search, MapPin } from 'lucide-react';
import { fetchVoterInfo, fetchMapKey } from '../services/apiClient';
import { GoogleMap, useJsApiLoader, Marker } from '@react-google-maps/api';

const mapContainerStyle = {
  width: '100%',
  height: '400px'
};

const center = {
  lat: 38.8977,
  lng: -77.0365
};

export default function MapLocator() {
  const [address, setAddress] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [apiKey, setApiKey] = useState(null);

  useEffect(() => {
    fetchMapKey().then(data => {
      if (data && data.key) {
        setApiKey(data.key);
      }
    }).catch(err => console.error("Failed to load map key", err));
  }, []);

  const { isLoaded } = useJsApiLoader({
    id: 'google-map-script',
    googleMapsApiKey: apiKey || "",
  });

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

        <div 
          className="w-full bg-gray-100 rounded-lg border-2 border-dashed border-gray-300 flex items-center justify-center relative overflow-hidden"
          aria-label="Interactive map"
          style={{ height: '400px' }}
        >
          {isLoaded && apiKey ? (
            <GoogleMap
              mapContainerStyle={mapContainerStyle}
              center={center}
              zoom={10}
            >
              <Marker position={center} />
            </GoogleMap>
          ) : (
            <div className="text-center p-4">
              <MapPin className="mx-auto h-8 w-8 text-gray-400 mb-2" />
              <p className="text-sm text-gray-500">Loading Google Maps...</p>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
