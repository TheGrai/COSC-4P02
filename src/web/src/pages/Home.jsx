import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Home.css";

export const Home = ({ name, handleNameChange }) => {
  const [aboutMeText, setAboutMeText] = useState("");
  const navigate = useNavigate();

  const handleTextAreaChange = (e) => {
    setAboutMeText(e.target.value);
  };

  const onNextClick = () => {
    if (name === "") {
      alert("please input a name");
      return;
    }

    navigate("/chat");
  };

  const onSwitchClick = () => {

    document.getElementById("mainApp").classList.add("AppCG");
    document.getElementById("mainApp").classList.remove("App");
    navigate("/homeCG");

  };

  return (
    <div className="Home">
        <img src = "brockuRed.png" height = "150"/>
      <h1>Brock U Chat App</h1>
      <h3>About</h3>
      <p>
        This chat app is designed for BrockU Students and others to
          ask questions about the School
      </p>
      <label className="name-input-label">
        <p>Name: </p>
        <input
          value={name}
          onChange={handleNameChange}
          className="name-input"
        />
      </label>
      <button onClick={onNextClick} className="next-btn">
        Next page
      </button>
      <button onClick={onSwitchClick} className="switchCG-btn">
        Canada Games
      </button>
    </div>
  );
};
