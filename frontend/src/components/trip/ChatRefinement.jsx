import React, { useState } from 'react';

const ChatRefinement = ({ onSubmit, currentDay }) => {
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([
    { role: 'assistant', content: 'How would you like to refine your itinerary? You can ask me to change activities, add recommendations, or adjust the schedule.' }
  ]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!message.trim()) return;

    // Add user message to chat
    setChatHistory([
      ...chatHistory,
      { role: 'user', content: message }
    ]);

    // Prepare request data
    const refinementRequest = {
      natural_language_request: message,
      specific_day: currentDay
    };

    // Clear input
    setMessage('');
    
    // Set loading state
    setIsLoading(true);

    try {
      // In a real application, this would be an API call
      // Instead, we'll simulate the API response with a timeout
      setTimeout(() => {
        const aiResponse = "I've updated your itinerary based on your request. I've added more outdoor activities, replaced the museum visit with a park exploration, and scheduled a traditional local dinner instead of the previous restaurant.";
        
        setChatHistory(prev => [
          ...prev,
          { role: 'assistant', content: aiResponse }
        ]);
        
        // Call the onSubmit callback with the refinement request
        onSubmit(refinementRequest);
        setIsLoading(false);
      }, 1500);
    } catch (error) {
      console.error('Error sending refinement request:', error);
      setChatHistory(prev => [
        ...prev,
        { role: 'assistant', content: 'Sorry, there was an error processing your request. Please try again.' }
      ]);
      setIsLoading(false);
    }
  };

  // Example message suggestions
  const suggestions = [
    "Add more outdoor activities to day 2",
    "Replace lunch on day 3 with a local restaurant",
    "Make day 1 more relaxed with fewer activities",
    `Focus more on art and culture on day ${currentDay}`
  ];

  const handleSuggestionClick = (suggestion) => {
    setMessage(suggestion);
  };

  return (
    <div className="flex flex-col h-full">
      {/* Chat messages */}
      <div className="flex-1 overflow-y-auto mb-4 space-y-4">
        {chatHistory.map((msg, index) => (
          <div 
            key={index}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div 
              className={`max-w-3/4 rounded-lg px-4 py-2 ${
                msg.role === 'user' 
                  ? 'bg-primary-100 text-primary-800' 
                  : 'bg-gray-100 text-gray-800'
              }`}
            >
              <p>{msg.content}</p>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 rounded-lg px-4 py-2 flex items-center space-x-1">
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
            </div>
          </div>
        )}
      </div>

      {/* Suggestions */}
      <div className="flex flex-wrap gap-2 mb-4">
        {suggestions.map((suggestion, index) => (
          <button
            key={index}
            onClick={() => handleSuggestionClick(suggestion)}
            className="text-sm bg-gray-100 hover:bg-gray-200 rounded-full px-3 py-1 text-gray-800"
          >
            {suggestion}
          </button>
        ))}
      </div>

      {/* Message input */}
      <form onSubmit={handleSendMessage} className="flex">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          className="flex-grow form-input rounded-r-none"
          placeholder="How would you like to refine your itinerary?"
          disabled={isLoading}
        />
        <button
          type="submit"
          className="btn btn-primary rounded-l-none"
          disabled={!message.trim() || isLoading}
        >
          {isLoading ? (
            <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          ) : (
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.707l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13a1 1 0 102 0V9.414l1.293 1.293a1 1 0 001.414-1.414z" clipRule="evenodd" />
            </svg>
          )}
        </button>
      </form>
    </div>
  );
};

export default ChatRefinement;
