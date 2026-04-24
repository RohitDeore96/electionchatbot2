export const fetchVoterInfo = async (address) => {
    const res = await fetch(`/api/civic/voter-info?address=${encodeURIComponent(address)}`);
    return res.json();
};

export const sendChatMessage = async (message) => {
    const res = await fetch(`/api/ai/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
    });
    return res.json();
};

export const fetchMapKey = async () => {
    const res = await fetch(`/api/map/key`);
    return res.json();
};
