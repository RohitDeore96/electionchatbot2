import { fetchVoterInfo, sendChatMessage } from '../src/services/apiClient';

describe('apiClient', () => {
  beforeEach(() => {
    global.fetch = jest.fn();
  });

  afterEach(() => {
    jest.resetAllMocks();
  });

  test('fetchVoterInfo calls correct endpoint', async () => {
    global.fetch.mockResolvedValueOnce({ json: async () => ({ address: "123 Test St" }) });
    const result = await fetchVoterInfo("123 Test St");
    expect(global.fetch).toHaveBeenCalledWith('http://localhost:8080/api/civic/voter-info?address=123%20Test%20St');
    expect(result).toEqual({ address: "123 Test St" });
  });

  test('sendChatMessage calls correct endpoint with payload', async () => {
    global.fetch.mockResolvedValueOnce({ json: async () => ({ response: "Test reply" }) });
    const result = await sendChatMessage("Hi");
    expect(global.fetch).toHaveBeenCalledWith('http://localhost:8080/api/ai/chat', {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: "Hi" })
    });
    expect(result).toEqual({ response: "Test reply" });
  });
});
