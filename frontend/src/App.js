import React, { useState } from "react";
import "./styles.css";
import { createItem } from "./api";

export default function App() {
  const [state, setState] = useState({
    city: "",
    email: "",
    brand: ""
  });

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setState((prevProps) => ({
      ...prevProps,
      [name]: value
    }));
  };

  const handleSubmit = async (event) => {
    // event.preventDefault();
    try {
      await createItem(state);
      console.log('Store created successfully!');
      // Optionally, you can reset the form or perform other actions after successful submission
    } catch (error) {
      console.error('Error creating store:', error);
      // Handle errors, show an error message, or redirect the user
    }
  };

  return (
    <div className="App">
      <form onSubmit={handleSubmit}>
        <div className="form-control">
          <label>City</label>
          <input
              type="text"
              name="city"
              value={state.city}
              onChange={handleInputChange}
          />
        </div>
        <div className="form-control">
          <label>Email</label>
          <input
              type="text"
              name="email"
              value={state.email}
              onChange={handleInputChange}
          />
        </div>
        <div className="form-control">
          <label>Brand</label>
          <input
              type="text"
              name="brand"
              value={state.brand}
              onChange={handleInputChange}
          />
        </div>
        <div className="form-control">
          <label></label>
          <button type="submit">create_store</button>
        </div>
      </form>
    </div>
  );
}
