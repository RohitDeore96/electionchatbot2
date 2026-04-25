import React, { useState } from 'react';
import { CheckCircle2, Circle } from 'lucide-react';

/**
 * Component responsible for rendering the sequential election events.
 * @returns {React.JSX.Element} The interactive timeline interface.
 */
export default function VotingTimeline() {
  const [activeStep, setActiveStep] = useState(0);

  const steps = [
    {
      title: "Register to Vote",
      date: "Deadline: 30 days before election",
      details: "Ensure you are registered to vote at your current address. You can register online, by mail, or in-person at designated locations."
    },
    {
      title: "Early Voting",
      date: "Opens: 15 days before election",
      details: "Beat the crowds by casting your ballot early. Check your county's board of elections website for early voting locations and hours."
    },
    {
      title: "Election Day",
      date: "November 5th",
      details: "Polls are open from 7 AM to 8 PM. Bring valid identification if required in your state. If you are in line before polls close, you have the right to vote."
    }
  ];

  return (
    <section role="navigation" aria-labelledby="timeline-heading" className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <h2 id="timeline-heading" className="text-2xl font-bold text-gray-900 mb-6">Election Timeline</h2>
      <div className="space-y-4">
        {steps.map((step, index) => {
          const isActive = index === activeStep;
          return (
            <div key={index} className="relative">
              <button
                onClick={() => setActiveStep(index)}
                aria-expanded={isActive}
                aria-controls={`step-content-${index}`}
                className="w-full text-left flex items-start focus:outline-none focus:ring-2 focus:ring-primary rounded-lg p-2 transition-colors hover:bg-gray-50"
              >
                <div className="flex-shrink-0 mt-1">
                  {index <= activeStep ? (
                    <CheckCircle2 className="w-6 h-6 text-primary" aria-hidden="true" />
                  ) : (
                    <Circle className="w-6 h-6 text-gray-300" aria-hidden="true" />
                  )}
                </div>
                <div className="ml-4 flex-1">
                  <h3 className={`text-lg font-semibold ${isActive ? 'text-primary' : 'text-gray-900'}`}>
                    {step.title}
                  </h3>
                  <p className="text-sm font-medium text-gray-500">{step.date}</p>
                </div>
              </button>
              
              {isActive && (
                <div 
                  id={`step-content-${index}`}
                  className="ml-12 mt-2 text-gray-700 bg-blue-50 p-4 rounded-lg text-sm border-l-4 border-primary"
                  role="region"
                  aria-labelledby={`step-${index}`}
                >
                  {step.details}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </section>
  );
}
