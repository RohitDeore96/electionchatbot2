/**
 * Fetches voter information based on the provided address.
 * @param {string} address - The voter's address.
 * @returns {Promise<Object>} The voter info response.
 */
export const fetchVoterInfo = async (address) => {
    const res = await fetch(`/api/civic/voter-info?address=${encodeURIComponent(address)}`);
    return res.json();
};

/**
 * Sends a chat message to the AI assistant.
 * @param {string} message - The message to send.
 * @returns {Promise<Object>} The AI response.
 */
export const sendChatMessage = async (message) => {
    const res = await fetch(`/api/ai/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
    });
    return res.json();
};

/**
 * Fetches the Google Maps API key from the backend.
 * @returns {Promise<Object>} The API key response.
 */
export const fetchMapKey = async () => {
    const res = await fetch(`/api/map/key`);
    return res.json();
};
