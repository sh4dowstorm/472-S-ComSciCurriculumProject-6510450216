import React from "react";
import { useNavigate } from "react-router-dom";
import Button from "../components/button";
import Header from "../components/header";
import "../styles/home.css";

const HomePage: React.FC = () => {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate("/creditcheck");
  };

  return (
    <div className="home-page">
      <Header />
      <div className="content">
        <h1>Home Page</h1>
        <p>This is the home page.</p>
        <Button
          text="To Credit Check"
          className="button"
          onClick={handleClick}
        />
      </div>
    </div>
  );
};

export default HomePage;
