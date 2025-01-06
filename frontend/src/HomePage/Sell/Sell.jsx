import React from "react";

export default function Sell() {
  const handleSignUp = () => {
    // TODO: Implement sign-up logic or navigation
    console.log("Sign up button clicked");
    // You might want to use React Router to navigate to a sign-up page
    // or open a modal for sign-up
  };

  return (
    <section
      className="bg-gray-200 min-h-screen flex flex-col items-center justify-center"
      id="signup"
    >
      <h1 className="text-5xl mb-6 text-black text-center">
        <span className="text-yellow-500">Unlock </span> Your Potential
      </h1>
      <p className="text-xl mb-8 max-w-2xl text-center text-gray-700">
        Join our platform to access advanced trading tools, real-time market
        analysis, and a community of expert traders. Start maximizing your
        crypto investments today!
      </p>
      <div className="space-y-6 text-center">
        <ul className="text-left inline-block">
          <li className="flex items-center mb-3">
            <svg
              className="w-6 h-6 mr-2 text-green-500"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M5 13l4 4L19 7"
              ></path>
            </svg>
            Advanced trading algorithms
          </li>
          <li className="flex items-center mb-3">
            <svg
              className="w-6 h-6 mr-2 text-green-500"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M5 13l4 4L19 7"
              ></path>
            </svg>
            Real-time market insights
          </li>
          <li className="flex items-center mb-3">
            <svg
              className="w-6 h-6 mr-2 text-green-500"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M5 13l4 4L19 7"
              ></path>
            </svg>
            Cutting edge technologies
          </li>
        </ul>
      </div>
      <button
        onClick={handleSignUp}
        className="mt-8 px-6 py-3 bg-yellow-500 text-black font-bold rounded-lg hover:bg-yellow-600 transition duration-300"
      >
        Sign Up Now
      </button>
      <p className="mt-4 text-sm text-gray-600">
        Already have an account?{" "}
        <a href="/login" className="text-yellow-500 hover:underline">
          Log in here
        </a>
      </p>
    </section>
  );
}
